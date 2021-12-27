from typing import Dict, List

from paths import CUSTOM_DATA_PATH

from .conditions import is_self_inflicted, is_not_self_inflicted
from .models import EventFireCondition, GameEventConversion
from .parser import JsonGameEventConversionParser


__all__ = (
    'DEFAULT_EVENT_FIRE_CONDITIONS',
    'DEFAULT_GAME_EVENT_CONVERSIONS',
)


DEFAULT_EVENT_FIRE_CONDITIONS: Dict[str, EventFireCondition] = {
    'self_inflicted': is_self_inflicted,
    'not_self_inflicted': is_not_self_inflicted,
}

_parser = JsonGameEventConversionParser(DEFAULT_EVENT_FIRE_CONDITIONS)
_path = CUSTOM_DATA_PATH / 'easyevents' / 'game_event_conversions.json'

DEFAULT_GAME_EVENT_CONVERSIONS: List[GameEventConversion] = _parser(_path)
