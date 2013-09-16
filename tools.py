from textwrap import dedent
from content import Room


class Utils(object):

    def adventure_help(self):
        return dedent("""\
        Welcome to adventure, written by Adam Forsythe-Cheasley.
        """)

    def parse_user_input(self, user_input, player):
        room_described = True
        # remove the verb 'go' as we only care about the direction
        if user_input.startswith('go'):
            user_input = user_input[3:]

        if user_input == 'help':
            print self.adventure_help()
        elif user_input == 'look':
            return False
        elif user_input in ['east', 'e']:
            player.current_location[0] += 1
            room_described = False
        elif user_input in ['west', 'w']:
            player.current_location[0] -= 1
            room_described = False
        else:
            print 'I do not understand.\n'

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
