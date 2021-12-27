from events import GameEvent


__all__ = (
    'is_self_inflicted',
    'is_not_self_inflicted',
)


def is_self_inflicted(game_event: GameEvent) -> bool:
    """Check if a game event is self-inflicted."""
    return (not game_event['attacker']) or game_event['attacker'] == game_event['userid']


def is_not_self_inflicted(game_event: GameEvent) -> bool:
    """Check if a game event is not self-inflicted."""
    return not is_self_inflicted(game_event)
