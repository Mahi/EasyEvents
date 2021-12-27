from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List


__all__ = (
    'EventArgs',
    'EventListener',
    'NamedEventListener',
    'Event',
)


EventArgs = Dict[str, Any]
EventListener = Callable[[EventArgs], None]
NamedEventListener = Callable[[str, EventArgs], None]


@dataclass
class Event:
    """Event class for managing and notifying listeners.

    Separates listeners that take the event's name as an argument
    from the listeners that only wish to receive the event arguments
    themselves.

    Forwards all event arguments ("eargs") as keyword arguments,
    allowing the listener to unpack any arguments they need:

    >>> my_event = Event('my_event')
    >>> def on_event(event_name, player, **eargs):
    ...     print(event_name, player.name)
    ...
    >>> my_event.named_listeners.append(on_event)
    >>> my_event.fire(player=my_player)
    my_event Mahi
    """

    name: str
    listeners: List[EventListener] = field(default_factory=list)
    named_listeners: List[NamedEventListener] = field(default_factory=list)

    def fire(self, event_args={}, **kwargs):
        """Fire an event.

        Merges `event_args` with any provided keyword arguments
        and notifies all listeners with the merged arguments.
        """
        kwargs.update(event_args)
        for listener in self.listeners:
            listener(**kwargs)
        for listener in self.named_listeners:
            listener(self.name, **kwargs)
