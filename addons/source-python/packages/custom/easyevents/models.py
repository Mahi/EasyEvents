from dataclasses import dataclass, field
from typing import Callable, List, Optional

from events import GameEvent


__all__ = (
    'EventFireCondition',
    'PlayerConversion',
    'EventFire',
    'GameEventConversion',
)


EventFireCondition = Callable[[GameEvent], bool]


@dataclass
class PlayerConversion:
    """Information for converting a game event userid to a player earg."""
    userid_key: str
    player_key: str


@dataclass
class EventFire:
    """Information for firing an easy event from a game event."""
    event_name: str
    player_key: str
    condition: Optional[EventFireCondition] = None


@dataclass
class GameEventConversion:
    """Information for converting a game event to an easy event."""
    game_event: str
    player_conversions: List[PlayerConversion] = field(default_factory=list)
    event_fires: List[EventFire] = field(default_factory=list)
