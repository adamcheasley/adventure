from textwrap import dedent

DIRECTIONS = {
    'north',
    'n',
    'east',
    'e',
    'south',
    's',
    'west',
    'w',
    'up',
    'down',
    'in',
}


def array_to_id(array):
    return '_'.join(str(x) for x in array)


def adventure_help():
    return dedent(u"""\
    Welcome to Adventure, written by Adam Forsythe-Cheasley.

    Here is some useful information:

    - Directions are: north, south, up, etc.

    - These can be shortened to n, s, u

    - Try other commands, e.g. in, use, look etc.

    - Be very mindful of the time or date in any location.
      This will help you
      a great deal as the game progresses.

    - Your backpack will only hold 5 items. You can drop items at any time.
    """)


def parse_user_input(user_input, player, world, stdscr):
    user_input = user_input.strip()
    if not user_input:
        return True

    room_described = True
    # create a copy of the current coordinates to store new
    # coordinates into
    new_location = list(player.current_coordinates)
    room = world.current_room()

    # remove the verb 'go' as we only care about the direction
    if user_input.startswith('go'):
        user_input = user_input[3:]
    elif user_input.startswith('pick up'):
        user_input = user_input.replace('pick up', 'take')
    elif user_input.startswith('pick'):
        user_input = user_input.replace('pick', 'take')
    elif user_input.startswith('walk'):
        user_input = user_input[3:]
    elif user_input.startswith(
            'turn on') or user_input.startswith('switch on'):
        user_input = ' '.join(user_input.split()[1:])

    # http://www.quickforge.co.uk/catalog/view/theme/default/image/3D-XYZ-Graph.gif
    # negative on x/y are flipped
    if user_input == 'help':
        stdscr.addstr(adventure_help())
    elif user_input in {'north', 'n', 'in'}:
        new_location[0] += 1
    elif user_input in ['south', 's']:
        new_location[0] -= 1
    elif user_input in ['east', 'e']:
        new_location[1] += 1
    elif user_input in ['west', 'w']:
        new_location[1] -= 1
    elif user_input == 'up':
        new_location[2] += 1
    elif user_input == 'down':
        new_location[2] -= 1
    else:
        # otherwise assume this is a verb that the user can deal with
        input_list = user_input.split()
        try:
            stdscr.addstr(getattr(player, input_list[0])(input_list[1:], room))
        except AttributeError:
            stdscr.addstr('I do not understand.\n')
        except TypeError:
            stdscr.addstr("I cannot do that.\n")
        except KeyError:
            stdscr.addstr("I cannot see that.\n")
        return room_described

    if user_input in DIRECTIONS:
        room_described = False
        new_location_id = array_to_id(new_location)
        # check we can move that direction
        if room.blocked and new_location_id not in player.visited:
            stdscr.addstr(room.blocked_reason)
            return True
        if world.valid_move(new_location_id):
            player.visited.add(player.current_location())
            player.current_coordinates = new_location
        else:
            stdscr.addstr('You cannot go that way.\n')
            room_described = True

    return room_described
