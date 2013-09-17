from textwrap import dedent
from content import Room


DIRECTIONS = ['north', 'n', 'east', 'e', 'south', 's', 'west', 'w', 'up',
              'down']


class Utils(object):

    def adventure_help(self):
        return dedent("""\
        Welcome to adventure, written by Adam Forsythe-Cheasley.
        """)

    def parse_user_input(self, user_input, player, world):
        room_described = True
        new_location = list(player.current_location)
        # remove the verb 'go' as we only care about the direction
        if user_input.startswith('go'):
            user_input = user_input[3:]

        if user_input == 'help':
            print self.adventure_help()
        elif user_input == 'look':
            return False
        elif user_input in ['east', 'e']:
            new_location[0] += 1
            room_described = False
        elif user_input in ['west', 'w']:
            new_location[0] -= 1
            room_described = False
        elif user_input in ['north', 'n']:
            new_location[1] += 1
            room_described = False
        elif user_input in ['south', 's']:
            new_location[1] -= 1
            room_described = False
        else:
            print 'I do not understand.\n'

        if user_input in DIRECTIONS:
            # check we can move that direction
            location_id = world.create_location_id(new_location)
            if location_id in world.world.keys():
                player.current_location = new_location
            else:
                print 'You cannot go that way.\n'
                room_described = True

        return room_described


class World(object):

    def __init__(self, adventure_map):
        self.adventure_map = adventure_map
        self.parse_map(self.adventure_map)

    def create_location_id(self, location):
        return '-'.join(str(x) for x in location)

    def parse_map(self, adventure_map):
        self.world = {}
        for ob in adventure_map:
            room = ob['room']
            location_id = self.create_location_id(room['location'])
            self.world[location_id] = Room(room['title'],
                                           room['description'],
                                           )

    def location(self, current_location):
        """
        returns the current room
        """
        location = self.world.get(self.create_location_id(current_location))
        if location is not None:
            return location.long_description
        else:
            return 'You are lost.\n'
