# Adventure

A text adventure game featuring time travel.

This project is not really in a playable state. I am still working on
the framework, so the actual story needs a lot of work.


## Installation

This game was written for python 3.

Get yourself a virtualenv:
```
python3 -m venv .
. bin/activate
```

Then install the requirements:  
`pip install -r requirements.txt `

To play, simply run `python adventure.py`


## Map Layout

The map (`map.yaml`) is split into three time dimensions: `past`, `present`
and `future`. Each is a set of rooms keyed by an `"x_y_z"` coordinate string.

```yaml
present:
  "0_0_0":
    title: Foyer
    description: A bare concrete foyer.
    room_items:
      - title: key
        description: A laser-cut key.
        use_location: [0, 1, 0]
```

Movement maps to the axes as: `north`/`in` → +y, `south` → -y, `east` → +x,
`west` → -x, `up` → +z, `down` → -z. A move only succeeds if a room exists at
the target coordinate (`loop` directions aside, below).

The time machine cycles the player through the times **in place**:
`present → past → future → present`. Using it only works if a room exists at
the player's current coordinate in the destination time, so the same
coordinate should be defined across the times you want to travel between.

### Room fields

| Field               | Type   | Meaning                                                        |
|---------------------|--------|----------------------------------------------------------------|
| `title`             | str    | Short name, shown on entry and on re-entry.                    |
| `description`       | str    | Long description, shown on first entry and on `look`.          |
| `short_description` | str    | Parsed but not yet used in output.                             |
| `blocked`           | bool   | If true, the player cannot move from here into an unvisited room until it is unblocked (see `use`). |
| `blocked_reason`    | str    | Printed when the player tries to leave a blocked room.         |
| `blocked_description`| str   | Appended to the description while the room is blocked.         |
| `unblocked`         | str    | Printed when the room is unblocked.                            |
| `death_if_entered`  | bool   | Entering the room ends the game in death.                      |
| `win_if_entered`    | bool   | Entering the room wins the game.                               |
| `loop`              | str    | Comma-separated directions (e.g. `"n, e, w"`) that loop back to this room instead of failing — used to build mazes. |
| `room_items`        | list   | Items and sprites in the room (below).                         |

### room_items

A `room_items` entry is one of three kinds:

* **Item** — `title`, `description`, optional `use_location: [x, y, z]`
  (where `use`-ing it does something), `hidden: bool` (if true it is not
  listed automatically — describe it in the room text instead), `when_eaten`
  (text shown when eaten; if set and not fatal, the item is consumed), and
  `death_if_eaten: bool` (eating it ends the game).
* **Sprite** — `sprite_id` referencing a sprite class in `sprites.py`
  (e.g. `human_1`, `computer_1`). Sprites can have a `back_story` (shown on
  `look`) or be switched `on`.
* **Time machine** — an item with `title: time machine`. Take it, then `use`
  it to travel.
