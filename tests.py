import pytest
import yaml

from content import Item, Player, Room, TimeMachine, World
from sprites import sprites_to_init
from exc import GameOver
from tools import parse_user_input


class FakeScreen(object):
    """Minimal stand-in for a curses window that records output."""

    def __init__(self):
        self.buf = ""

    def addstr(self, text):
        self.buf += text


def world_with_item():
    """A one-room world (at the player's start position) holding a key."""
    world_data = {
        "present": {
            "0_5_0": {
                "title": "Room",
                "description": "A plain room.",
                "room_items": [{"title": "key", "description": "a small key"}],
            }
        }
    }
    return World(world_data)


def make_room(**overrides):
    """Build a Room with sensible defaults for tests."""
    kwargs = dict(
        title="test room",
        description="this is just a test",
        short_description="just a test",
        blocked=False,
        blocked_reason="",
        unblocked="",
        blocked_description="",
        death_if_entered=False,
        loop=None,
    )
    kwargs.update(overrides)
    return Room(**kwargs)


def make_item(**overrides):
    kwargs = dict(
        title="thing",
        description="just a test",
        use_location=None,
        hidden=False,
        when_eaten="",
    )
    kwargs.update(overrides)
    return Item(**kwargs)


def test_parse_map():
    """parse map expects a python data structure
    """
    world_data = {
        "present": {
            "0-0-0": {
                "description": "You are at the end of a long "
                "driveway.\n"
                "In the  distance is a large "
                "building. \n"
                "To either side is grass and then a "
                "high concrete wall.\n"
                "The drive leads north.",
                "title": "Gate",
            },
            "0-1-0": {
                "description": "You are half way up the driveway. "
                "At the end of the drive is a tall,\n"
                "modern office building.\n"
                "The drive continues north.",
                "room_items": [
                    {
                        "description": "A laser cut key. It " "looks very new.",
                        "title": "key",
                        "use_location": [0, 2, 0],
                    }
                ],
                "title": "Driveway",
            },
        }
    }
    world = World(world_data)
    assert isinstance(world.adventure_map, dict)
    assert "present" in world.adventure_map
    assert len(world.adventure_map["present"]) == 2


def test_room():
    # First entry shows the title followed by the full description.
    room = make_room()
    expected = "{}\n{}".format(room.title, room.long_description)
    assert room.describe_location() == expected

    item = make_item(title="test object", use_location=[0, 0, 0])
    room.items[item.title] = item
    assert "There is a test object here" in room.describe_location()


def test_take_specific_item_not_present():
    """Asking for an item that isn't here returns a friendly message."""
    player = Player([0, 0, 0], None)
    room = make_room()
    room.items["rock"] = make_item(title="rock")

    result = player.take(["key"], room)
    assert "cannot see a key" in result
    assert player.items == {}
    assert "rock" in room.items


def test_take_respects_inventory_limit():
    player = Player([0, 0, 0], None)
    player.items = {str(i): make_item(title=str(i)) for i in range(Player.MAX_ITEMS)}
    room = make_room()
    room.items["key"] = make_item(title="key")

    result = player.take(["key"], room)
    assert "can only hold" in result
    assert "key" in room.items


def test_use_wrong_location_keeps_item():
    """Using an item where it doesn't apply must not consume it."""
    player = Player([0, 0, 0], None)
    player.items["key"] = make_item(title="key", use_location=[9, 9, 9])
    room = make_room(blocked=True, unblocked="The door swings open.")

    result = player.use(["key"], room)
    assert result == "Nothing happens.\n"
    assert "key" in player.items
    assert room.blocked is True


def test_use_right_location_unblocks_and_consumes():
    player = Player([0, 0, 0], None)
    player.items["key"] = make_item(title="key", use_location=[0, 0, 0])
    room = make_room(blocked=True, unblocked="The door swings open.")

    result = player.use(["key"], room)
    assert result == "The door swings open."
    assert "key" not in player.items
    assert room.blocked is False


def test_eat_consumes_item():
    player = Player([0, 0, 0], None)
    room = make_room()
    room.items["apple"] = make_item(title="apple", when_eaten="Delicious.")

    result = player.eat(["apple"], room)
    assert result == "Delicious."
    assert "apple" not in room.items
    # eating it again should no longer find it
    assert "cannot see" in player.eat(["apple"], room)


def test_eat_poison_raises_game_over():
    player = Player([0, 0, 0], None)
    room = make_room()
    poison = make_item(title="rock", when_eaten="You feel unwell and die.")
    poison.death_if_eaten = True
    room.items["rock"] = poison

    with pytest.raises(GameOver):
        player.eat(["rock"], room)


def test_room_end_state():
    assert make_room().end_state() is None
    assert make_room(death_if_entered=True).end_state() == "dead"
    assert make_room(win_if_entered=True).end_state() == "won"


def test_map_parses_win_room():
    """win_if_entered round-trips from the map into the Room."""
    rooms = {
        "present": {
            "0_0_0": {"title": "Start", "description": "x"},
            "0_1_0": {
                "title": "Finish",
                "description": "you made it",
                "win_if_entered": True,
            },
        }
    }
    world = World(rooms)
    assert world.world["present"]["0_0_0"].end_state() is None
    assert world.world["present"]["0_1_0"].end_state() == "won"


def test_real_map_loads():
    """Smoke test: the shipped map.yaml builds a World without errors.

    Guards against schema/code drift (e.g. a new Room field or a bad
    sprite_id reference in the map).
    """
    sprites = {x.sprite_id: x() for x in sprites_to_init}
    with open("map.yaml") as map_file:
        adventure_map = yaml.safe_load(map_file)
    world = World(adventure_map, sprites=sprites)
    # the player starts in a room that actually exists
    assert world.current_room() is not None
    # all three times are populated and share the lab coordinate, so the time
    # machine always has somewhere to land
    for timezone in ("present", "past", "future"):
        assert world.world[timezone], "%s has no rooms" % timezone
        assert "0_0_-1" in world.world[timezone]
    # the game is winnable: the future has a winning room
    win_rooms = [r for r in world.world["future"].values() if r.end_state() == "won"]
    assert win_rooms, "no winning room in the future"


def make_time_world():
    """A world with the same coordinate in every time."""
    rooms = {
        "present": {"0_0_0": {"title": "Now", "description": "the present"}},
        "past": {"0_0_0": {"title": "Then", "description": "the past"}},
        "future": {"0_0_0": {"title": "Later", "description": "the future"}},
    }
    return World(rooms)


def test_time_machine_cycles_timezones():
    world = make_time_world()
    world.player.current_coordinates = [0, 0, 0]
    world.player.items["time machine"] = TimeMachine("time machine", "a device", "")

    assert world.date == "present"
    world.player.use(["time", "machine"], world.current_room())
    assert world.date == "past"
    world.player.use(["time", "machine"], world.current_room())
    assert world.date == "future"
    world.player.use(["time", "machine"], world.current_room())
    assert world.date == "present"


def test_time_machine_no_counterpart_stays_put():
    """Using the machine where no other time has a room does nothing."""
    rooms = {
        "present": {
            "0_0_0": {"title": "Now", "description": "here"},
            "1_0_0": {"title": "Edge", "description": "only in the present"},
        },
        "past": {"0_0_0": {"title": "Then", "description": "there"}},
    }
    world = World(rooms)
    world.player.current_coordinates = [1, 0, 0]  # exists only in the present
    world.player.items["time machine"] = TimeMachine("time machine", "a device", "")

    result = world.player.use(["time", "machine"], world.current_room())
    assert world.date == "present"
    assert "Nothing happens" in result


def test_visited_key_distinguishes_timezones():
    world = make_time_world()
    player = world.player
    player.current_coordinates = [0, 0, 0]
    assert player.visited_key() == "present:0_0_0"
    world.date = "future"
    assert player.visited_key() == "future:0_0_0"


def test_blocked_room_blocks_then_unblocks():
    """A blocked room can't be left into new territory until an item is used."""
    rooms = {
        "present": {
            "0_5_0": {  # the player starts here (START_POS)
                "title": "Gate",
                "description": "A locked gate.",
                "blocked": True,
                "blocked_reason": "The gate is locked.\n",
                "unblocked": "The gate opens.\n",
                "room_items": [
                    {"title": "key", "description": "a key", "use_location": [0, 5, 0]}
                ],
            },
            "0_6_0": {"title": "Beyond", "description": "past the gate"},
        }
    }
    world = World(rooms)
    player = world.player

    # blocked: moving north into the unvisited room is refused
    screen = FakeScreen()
    parse_user_input("north", player, world, screen)
    assert "locked" in screen.buf.lower()
    assert player.current_location() == "0_5_0"

    # take and use the key, then the way opens
    parse_user_input("take key", player, world, FakeScreen())
    parse_user_input("use key", player, world, FakeScreen())
    parse_user_input("north", player, world, FakeScreen())
    assert player.current_location() == "0_6_0"


def test_dispatch_take_synonym():
    """'get' and 'grab' are synonyms for 'take'."""
    world = world_with_item()
    player = world.player
    parse_user_input("get key", player, world, FakeScreen())
    assert "key" in player.items
    assert "key" not in world.current_room().items


def test_dispatch_examine_synonym():
    """'examine' dispatches to look and describes the item."""
    world = world_with_item()
    screen = FakeScreen()
    parse_user_input("examine key", world.player, world, screen)
    assert "small key" in screen.buf


def test_dispatch_unknown_verb():
    world = world_with_item()
    screen = FakeScreen()
    parse_user_input("frobnicate the key", world.player, world, screen)
    assert "I do not understand." in screen.buf


def test_dispatch_rejects_internal_method():
    """Typing an internal method name must not invoke it."""
    world = world_with_item()
    player = world.player
    screen = FakeScreen()
    parse_user_input("_add_to_items key", player, world, screen)
    assert "I do not understand." in screen.buf
    # the item was not secretly moved into the inventory
    assert player.items == {}
    assert "key" in world.current_room().items


def test_dispatch_bare_on_does_not_crash():
    world = world_with_item()
    screen = FakeScreen()
    parse_user_input("turn on", world.player, world, screen)
    assert screen.buf  # produced some message rather than raising


def test_dispatch_game_over_propagates():
    """A fatal action raised inside a handler still ends the game."""
    world = world_with_item()
    room = world.current_room()
    poison = make_item(title="rock", when_eaten="You die.")
    poison.death_if_eaten = True
    room.items["rock"] = poison
    with pytest.raises(GameOver):
        parse_user_input("eat rock", world.player, world, FakeScreen())
