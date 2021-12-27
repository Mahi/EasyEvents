# EasyEvents
EasyEvents is a custom package for [Source.Python][sp],
designed to make it easier for plugin developers to interact with events.

## Usage

EasyEvents provides an `EasyEvents` class to manage both game events and custom events in an easy and uniform manner.
It simplifies Source.Python's event management by replacing all the `userid`s with instances of Player entity
or its subclass. In other words, your event listeners will receive your player objects as arguments.

```py
from easyevents import EasyEvents

player_dict = PlayerDictionary(MyPlayer)
events = EasyEvents(player_dict)

@events.on('player_kill')
def on_player_kill(player, victim, **eargs):  # You can pick any arguments from the event args ("eargs")
    assert type(player) == MyPlayer
    print(victim.my_custom_attribute)  # No userids, no index conversions
```

You can easily create and fire custom events, or even fire pre-created events:

```py
events.create_event('my_custom_event')

events['my_custom_event'].fire(player=my_player, some_argument='some value')
events['player_jump'].fire(player=my_player)
```

You can also listen to multiple events at once:

```py
@events.on('player_jump', 'my_custom_event')
def on_multiple_events(player, **eargs):
    print(f'Player {player.name} did something!')
```

Or better yet, use the `named` keyword argument to receive the event's name as an argument:

```py
@events.on('player_jump', 'my_custom_event', named=True)
def on_multiple_events(event_name, player, **eargs):
    print(f'Player {player.name} did {event_name}!')
```

## Installation

To install EasyEvents onto your game server:

1. Make sure you have [Source.Python][sp] installed.
2. Download it from [the releases page][rel].
3. Extract the `addons` folder into your game directory (e.g. `csgo`).
4. Restart your game server.

[sp]: http://forums.sourcepython.com/
[rel]: https://github.com/Mahi/EasyEvents/releases
