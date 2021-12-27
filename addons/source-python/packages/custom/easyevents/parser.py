import json
from typing import Callable, Dict, Generic, List, TypeVar

from pathlib import Path

from .models import EventFire, EventFireCondition, GameEventConversion, PlayerConversion


__all__ = (
    'RawData',
    'FileLoader',
    'DataParser',
    'GameEventConversionParser',
    'JsonGameEventConversionParser',
)


RawData = TypeVar('RawData')
FileLoader = Callable[[Path], RawData]
DataParser = Callable[[RawData], List[GameEventConversion]]


class GameEventConversionParser(Generic[RawData]):
    """Parse game event conversions from other type of data."""

    def __init__(self, event_fire_conditions: Dict[str, EventFireCondition]=None):
        if event_fire_conditions is None:
            self.event_fire_conditions = {}
        else:
            self.event_fire_conditions = event_fire_conditions

    def __call__(self, path: Path) -> List[GameEventConversion]:
        """Load and parse a file."""
        return self.parse_data(self.load_file(path))

    def load_file(self, path: Path) -> RawData:
        """Load a file from file path."""
        return NotImplemented

    def parse_data(self, data: RawData) -> List[GameEventConversion]:
        """Parse game event conversions from data."""
        return NotImplemented


class JsonGameEventConversionParser(GameEventConversionParser[dict]):
    """Parse game event conversions from JSON."""

    def load_file(self, path: Path) -> dict:
        with open(path) as file:
            return json.load(file)

    def parse_data(self, data: dict) -> List[GameEventConversion]:
        result = []
        for row in data:
            conversion = GameEventConversion(row['game_event'])

            for pc in row['player_conversions']:
                conversion.player_conversions.append(PlayerConversion(pc['userid'], pc['player']))

            for ef in row['event_fires']:
                condition_key = ef.get('condition')
                if condition_key is not None:
                    condition = self.event_fire_conditions[condition_key]
                else:
                    condition = None
                conversion.event_fires.append(EventFire(ef['event'], ef['player'], condition))

            result.append(conversion)
        return result
