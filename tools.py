from textwrap import dedent
from content import Room
from content import Item


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
        room = world.current_room(player.current_location)
        # remove the verb 'go' as we only care about the direction
        if user_input.startswith('go'):
            user_input = user_input[3:]

        if user_input == 'help':
            print self.adventure_help()
        elif user_input == 'look':
            return False
        elif user_input == 'inventory':
            player.inventory()
            return room_described
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
        elif user_input.startswith('take'):
            try:
                player.take(user_input.split()[1], room)
            except TypeError:
                print 'You cannot take that.\n'
        elif user_input.startswith('drop'):
            try:
                player.drop(user_input.split()[1], room)
            except KeyError:
                print 'You do not have anything to drop!\n'
            except TypeError:
                print 'You do not have a %s.\n' % user_input.split()[1]
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
            items = ob['items']
            location_id = self.create_location_id(room['location'])
            room_ob = Room(room['title'], room['description'])
            room_ob.items = []
            for item in items:
                room_ob.items.append(Item(item['title']))
            self.world[location_id] = room_ob

    def current_room(self, current_location):
        return self.world.get(self.create_location_id(current_location))

    def describe_location(self, current_location):
        """
        returns the current room and any items
        """
        location = self.current_room(current_location)
        if location is not None:
            main_description = '%s\n%s' % (location.title,
                                           location.long_description)
            if location.items:
                all_items = ''
                for item in location.items:
                    all_items += '\nThere is a %s here.' % item.title
                return '%s %s' % (main_description,
                                  all_items)
            else:
                return main_description
        else:
            return 'You are lost.\n'
