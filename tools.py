from textwrap import dedent

from exc import GameOver

DIRECTIONS = {
    "north",
    "n",
    "east",
    "e",
    "south",
    "s",
    "west",
    "w",
    "up",
    "u",
    "down",
    "d",
    "in",
}

# Verbs the player may type, mapped to the Player method that handles them.
# Dispatch is restricted to this whitelist so a player cannot invoke arbitrary
# attributes/methods on the player object (e.g. "_add_to_items", "visited").
VERB_SYNONYMS = {
    "take": "take",
    "get": "take",
    "grab": "take",
    "drop": "drop",
    "leave": "drop",
    "inventory": "inventory",
    "inv": "inventory",
    "i": "inventory",
    "look": "look",
    "examine": "look",
    "inspect": "look",
    "x": "look",
    "use": "use",
    "eat": "eat",
    "on": "on",
}


def array_to_id(array):
    return "_".join(str(x) for x in array)


def adventure_help():
    return dedent(
        """\
    Welcome to Adventure, written by Adam Forsythe-Cheasley.

    Here is some useful information:

    - Directions are: north, south, up, etc.

    - These can be shortened to n, s, u

    - Try other commands, e.g. in, use, look etc.

    - Be very mindful of the time or date in any location.
      This will help you
      a great deal as the game progresses.

    - Your backpack will only hold 5 items. You can drop items at any time.
    """
    )


def parse_user_input(user_input, player, world, stdscr):
    user_input = user_input.strip()
    if not user_input:
        return True

    room_described = True
    # create a copy of the current coordinates to store new
    # coordinates into
    new_location = list(player.current_coordinates)
    room = world.current_room()
    words = user_input.split()

    # normalise multi-word verb phrases down to a single leading verb
    if words[0].strip().lower() in {"go", "move", "walk"}:
        # drop the movement verb; we only care about the direction
        user_input = " ".join(words[1:])
    elif user_input.startswith("pick up "):
        user_input = user_input.replace("pick up ", "take ", 1)
    elif user_input.startswith("pick "):
        user_input = user_input.replace("pick ", "take ", 1)
    elif user_input.startswith("turn on ") or user_input.startswith("switch on "):
        # drop the leading "turn"/"switch", leaving "on <thing>"
        user_input = " ".join(user_input.split()[1:])

    # http://www.quickforge.co.uk/catalog/view/theme/default/image/3D-XYZ-Graph.gif
    # x, y, z
    if user_input == "help":
        stdscr.addstr(adventure_help())
    elif user_input in {"north", "n", "in"}:  # +y
        direction = "n"
        new_location[1] += 1
    elif user_input in {"south", "s"}:
        direction = "s"
        new_location[1] -= 1
    elif user_input in {"east", "e"}:  # +x
        direction = "e"
        new_location[0] += 1
    elif user_input in {"west", "w"}:
        direction = "w"
        new_location[0] -= 1
    elif user_input in {"up", "u"}:
        new_location[2] += 1
    elif user_input in {"d", "down"}:
        new_location[2] -= 1
    else:
        # otherwise treat the first word as a verb and dispatch it, but only
        # if it's a known command — never call an arbitrary player attribute
        input_list = user_input.split()
        method_name = VERB_SYNONYMS.get(input_list[0])
        if method_name is None:
            stdscr.addstr("I do not understand.\n")
            return room_described

        handler = getattr(player, method_name)
        try:
            stdscr.addstr(handler(input_list[1:], room))
        except (TypeError, IndexError):
            stdscr.addstr("I cannot do that.\n")
        except KeyError:
            stdscr.addstr("I cannot see that.\n")
        except GameOver as ex:
            stdscr.addstr(f"{str(ex)}\n")
            raise GameOver
        return room_described

    if user_input in DIRECTIONS:
        room_described = False
        new_location_id = array_to_id(new_location)
        # check we can move that direction
        if room.blocked and player.visited_key(new_location_id) not in player.visited:
            stdscr.addstr(room.blocked_reason)
            return True
        if world.valid_move(new_location_id):
            player.visited.add(player.visited_key())
            player.current_coordinates = new_location
        elif room.loop and direction in room.loop.split(", "):
            return False
        else:
            stdscr.addstr("You cannot go that way.\n")
            room_described = True

    return room_described
