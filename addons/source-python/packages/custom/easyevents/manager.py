import collections
from typing import Dict, Iterable, List, Tuple, Union

from core import AutoUnload
from events import GameEvent, event_manager
from players.dictionary import PlayerDictionary

from .defaults import DEFAULT_GAME_EVENT_CONVERSIONS
from .event import Event, EventListener, NamedEventListener
from .models import GameEventConversion


__all__ = (
    'EventManager',
)


class EventManager(AutoUnload):
    """Manage game events and custom events in a uniform manner."""

    def __init__(self,
        player_dict: PlayerDictionary,
        game_event_conversions: List[GameEventConversion]=DEFAULT_GAME_EVENT_CONVERSIONS,
    ):
        """Initialize the event manager for a player dict."""
        self.player_dict = player_dict
        self._events = {}
        self._game_event_conversions: Dict[str, List[GameEventConversion]] = collections.defaultdict(list)
        for conversion in game_event_conversions:
            self.add_game_event_conversion(conversion)

    def add_game_event_conversion(self, conversion: GameEventConversion):
        """Add a game event conversion to the manager."""

        ge = conversion.game_event
        self._game_event_conversions[ge].append(conversion)
        if ge not in event_manager or self._on_game_event not in event_manager[ge]:
            event_manager.register_for_event(ge, self._on_game_event)

        for event_fire in conversion.event_fires:
            self.create_event(event_fire.event_name)

    def _unload_instance(self):
        """Automatically unload the GameEvent listeners."""
        for event_name in self._game_event_conversions.keys():
            event_manager.unregister_for_event(event_name, self._on_game_event)

    def __getitem__(self, key: str) -> Event:
        return self._events[key]

    def __contains__(self, key: str) -> bool:
        return key in self._events

    def __iter__(self) -> Iterable[str]:
        return iter(self._events.keys())

    def create_event(self, event_name: str) -> Event:
        """Create a new event into the manager."""
        event = Event(event_name)
        self._events[event_name] = event
        return event

    def on(self, *event_names: Tuple[str], named: bool=False) -> Union[EventListener, NamedEventListener]:
        """Decorator to add a listener to multiple events at once.

        Supports `named` argument to determine whether the listener
        should receive the event's name as a positional argument.
        """
        def decorator(listener):
            for event_name in event_names:
                if named:
                    self[event_name].named_listeners.append(listener)
                else:
                    self[event_name].listeners.append(listener)
            return listener
        return decorator

    def _on_game_event(self, game_event: GameEvent):
        """Invoke easy events for a game event."""
        event_args = game_event.variables.as_dict()
        for conversion in self._game_event_conversions[game_event.name]:

            for player_conversion in conversion.player_conversions:
                try:
                    userid = event_args.pop(player_conversion.userid_key)
                    event_args[player_conversion.player_key] = self.player_dict.from_userid(userid)
                except (KeyError, ValueError):
                    event_args[player_conversion.player_key] = None
    
            for event_fire in conversion.event_fires:
                if event_fire.condition is None or event_fire.condition(game_event):
                    player = event_args[event_fire.player_key]
                    if player is not None:
                        self[event_fire.event_name].fire(event_args, player=player)
