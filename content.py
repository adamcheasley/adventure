from exc import GameOver
from tools import array_to_id


class World(object):

    def __init__(self, adventure_map, sprites=None):
        player = Player([0, 0, 0], self)
        self.player = player
        self.adventure_map = adventure_map
        self.sprites = sprites
        self.parse_map(self.adventure_map)
        self.date = 'present'

    def parse_map(self, adventure_map):
        self.world = {}
        for timezone, map_details in adventure_map.items():
            for location_id, room in map_details.items():
                room_items = room.get('room_items', [])
                room_ob = Room(room['title'],
                               room['description'],
                               room.get('short_description', ''),
                               room.get('blocked', False),
                               room.get('blocked_reason', ''),
                               room.get('unblocked', ''),
                               room.get('blocked_description', ''),
                               )
                for room_item in room_items:
                    if room_item['title'] == 'time machine':
                        time_machine = TimeMachine(
                            room_item['title'],
                            room_item.get('description', ''),
                            room_item.get('use_location', ''))
                        room_ob.items[room_item['title']] = time_machine
                    elif room_item['title'].startswith('human'):
                        room_ob.sprites.append(
                            self.sprites.get(room_item['title']))
                    else:
                        item = Item(
                            room_item['title'],
                            room_item.get('description', ''),
                            room_item.get('use_location', ''),
                            room_item.get('hidden', False),
                            room_item.get('when_eaten', ''),
                        )
                        item.death_if_eaten = room_item.get(
                            'death_if_eaten', False)
                        room_ob.items[room_item['title']] = item
                self.world[location_id] = room_ob

    def current_room(self):
        return self.world.get(self.player.current_location())

    def toggle_date(self):
        if self.date == 'present':
            self.date = 'past'
        else:
            self.date = 'present'


class Human(object):

    def __init__(self, location=None):
        self.current_coordinates = location
        self.told_back_story = False

    def current_location(self):
        """Gives the current coords in form 'x-y-z'
        """
        return array_to_id(self.current_coordinates)

    def back_story(self):
        """If this user has a story to tell, they do it here.
        """


class Player(Human):

    def __init__(self, location, world):
        self.world = world
        self.current_coordinates = location
        self.visited = set()
        self.items = {}

    def _add_to_items(self, title, room):
        self.items[title] = room.items[title]
        del room.items[title]

    def take(self, user_input, room):
        """
        a player is only allowed to hold up to 5 items
        """
        if getattr(self, 'items', False) and len(self.items) == 5:
            return 'Your backpack can only hold up to 5 items'

        if not user_input and len(room.items) > 0:
            # assume the user wants to pick up the first item in the room
            item_title = [x for x in room.items][0]
            self._add_to_items(item_title, room)
            return 'Took %s\n' % item_title

        # otherwise they have asked to pick up a specific item so
        # check item is in room
        if not room.items:
            raise TypeError
        item_title = ' '.join(user_input).lower()
        self._add_to_items(item_title, room)
        return 'Taken\n'

    def drop(self, user_input, room):
        if not user_input:
            return 'Drop what?\n'
        if not self.items:
            return 'You are not carrying anything.\n'
        item_title = ' '.join(user_input)
        if item_title not in self.items:
            return 'You are not carrying a %s' % item_title

        room.items[item_title] = self.items[item_title]
        del self.items[item_title]
        return 'Dropped\n'

    def inventory(self, user_input, room):
        if getattr(self, 'items', []):
            s = 'You are carrying:\n'
            for item in self.items.values():
                s += 'A %s\n' % item.title
            return s
        else:
            return 'You are not carrying anything.\n'

    def look(self, user_input, room):
        """If user types just 'look', describe the room,
        If not, look at what they are carrying for a match,
        or look at the objects in the room.
        """
        if not user_input:
            return room.describe_location()

        joined_input = ' '.join(user_input).lower()
        try:
            return self.items[joined_input].description
        except KeyError:
            pass

        try:
            return room.items[joined_input].description
        except KeyError:
            return 'I cannot see that'

    def use(self, user_input, room):
        # first see if we have that item
        if not user_input:
            return "Use what?\n"
        if not getattr(self, 'items', False):
            return "You have nothing to use.\n"

        requested_item = ' '.join(user_input)
        try:
            found_item = self.items[requested_item]
        except KeyError:
            return "You don't have a %s" % requested_item
        else:
            del self.items[requested_item]

        # check to see if that item can be used here
        use_location = found_item.use_location
        if found_item.title == 'time machine':
            self.world.toggle_date()
            print("There is a blinding light. You feel strange.")
        elif use_location is None or array_to_id(
                use_location) != self.current_location():
            return "Nothing happens.\n"

        # perform the action
        room.blocked = False
        return room.unblocked

    def eat(self, user_input, room):
        """Attempt to eat the item. This item can either be in the inventory
        or in the room.
        This doesn't usually end well.
        """
        requested_item = ' '.join(user_input)
        try:
            found_item = self.items[requested_item]
        except KeyError:
            found_item = None

        if found_item is None:
            try:
                found_item = room.items[requested_item]
            except KeyError:
                return "I cannot see a {}".format(requested_item)

        if found_item.death_if_eaten:
            print(found_item.when_eaten)
            raise GameOver()
        return found_item.when_eaten or "I can't eat that"


class Actor(Human):
    """These are the actors with which the player will interact
    during the game. These actors can give information to the player
    or simply give them an object.
    """


class Item(object):

    def __init__(self, title, description, use_location, hidden, when_eaten):
        self.title = title
        self.description = description
        self.use_location = use_location
        self.hidden = hidden
        self.when_eaten = when_eaten

    def __repr__(self):
        return "<Item: {}>".format(self.title)

    def further_description(self):
        """
        used when a users 'looks' at this item
        """


class TimeMachine(Item):

    def __init__(self, title, description, use_location):
        self.title = title
        self.description = description
        self.use_location = use_location

    def set_time(self):
        pass

    def travel(self):
        pass

    def output(self):
        """
        shows the user the current date/time set on the dial
        """


class Watch(Item):
    """
    the watch lets the user check what time/date it is
    """

    def __init__(self, title, description, use_location):
        self.title = title
        self.description = description
        self.use_location = use_location

    def output(self):
        """
        shows the current date/time
        """


class Room(object):

    def __init__(self, title, description, short_description,
                 blocked, blocked_reason, unblocked,
                 blocked_description):
        self.title = title
        self.long_description = description
        self.short_description = short_description
        self.blocked = blocked
        self.blocked_reason = blocked_reason
        self.unblocked = unblocked
        self.blocked_description = blocked_description
        self.items = {}
        self.sprites = []

    def describe_location(self):
        """
        returns the current room and any items
        """
        main_description = '%s\n%s' % (self.title,
                                       self.long_description)
        # if the room is blocked, we add the blocked_description
        if self.blocked:
            main_description = '%s \n%s' % (
                main_description,
                self.blocked_description)

        if self.items:
            all_items = ''
            for item in self.items.values():
                if not item.hidden:
                    all_items += '\nThere is a %s here.' % item.title
            main_description = '{} {}'.format(
                main_description, all_items)

        if self.sprites:
            for sprite in self.sprites:
                main_description += sprite.back_story()

        return main_description
