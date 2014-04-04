from textwrap import dedent
from content import Room
from content import Item
from utils import create_location_id


DIRECTIONS = ['north', 'n', 'east', 'e', 'south', 's', 'west', 'w', 'up',
              'down', 'in']


class Utils(object):

    def adventure_help(self):
        return dedent("""\
        Welcome to Adventure, written by Adam Forsythe-Cheasley.

        Here is some useful information:

        - Directions are: north, south, up, etc.

        - These can be shortened to n, s, u

        - Try other commands, e.g. in, use, look etc.

        - Be very mindful of the time or date in any location. This will help you
          a great deal as the game progresses.

        - Your backpack will only hold 5 items. You can drop items at any time.
        """)

    def parse_user_input(self, user_input, player, world):
        room_described = True
        new_location = list(player.current_location)
        room = world.current_room(player.current_location)
        # remove the verb 'go' as we only care about the direction
        if user_input.startswith('go'):
            user_input = user_input[3:]
        if user_input.startswith('pick'):
            user_input = user_input.replace('pick', 'take')

        if user_input == 'help':
            print self.adventure_help()
        elif user_input in ['east', 'e']:
            new_location[0] += 1
            room_described = False
        elif user_input in ['west', 'w']:
            new_location[0] -= 1
            room_described = False
        elif user_input in ['north', 'n', 'in']:
            new_location[1] += 1
            room_described = False
        elif user_input in ['south', 's']:
            new_location[1] -= 1
            room_described = False
        elif user_input == 'up':
            new_location[2] += 1
            room_described = False
        elif user_input == 'down':
            new_location[2] -= 1
            room_described = False
        else:
            # otherwise assume this is a verb that the user can deal with
            input_list = user_input.split()
            try:
                print getattr(player, input_list[0])(input_list[1:], room)
            except AttributeError:
                print 'I do not understand.\n'
            return room_described

        if user_input in DIRECTIONS:
            new_location_id = create_location_id(new_location)
            # check we can move that direction
            if room.blocked and new_location_id not in player.visited:
                print room.blocked_reason
                return True
            if new_location_id in world.world.keys():
                player.visited.add(create_location_id(player.current_location))
                player.current_location = new_location
            else:
                print 'You cannot go that way.\n'
                room_described = True

        return room_described


class World(object):

    def __init__(self, adventure_map):
        self.adventure_map = adventure_map
        self.parse_map(self.adventure_map)

    def parse_map(self, adventure_map):
        self.world = {}
        for ob in adventure_map:
            room = ob['room']
            items = ob.get('items', [])
            location_id = create_location_id(room['location'])
            room_ob = Room(room['title'],
                           room['description'],
                           room.get('blocked', False),
                           room.get('blocked_reason', ''),
                           room.get('unblocked', ''),
                           room.get('blocked_description', ''),
                           )
            room_ob.items = []
            for item in items:
                room_ob.items.append(Item(item['title'],
                                          item.get('description', ''),
                                          item.get('use_location', '')))
            self.world[location_id] = room_ob

    def current_room(self, current_location):
        return self.world.get(create_location_id(current_location))
