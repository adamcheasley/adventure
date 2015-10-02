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
                room_item = room.get('room_items', [])
                room_ob = Room(room['title'],
                               room['description'],
                               room.get('short_description', ''),
                               room.get('blocked', False),
                               room.get('blocked_reason', ''),
                               room.get('unblocked', ''),
                               room.get('blocked_description', ''),
                               )
                room_ob.items = []
                room_ob.sprites = []
                if room_item:
                    if room_item['title'] == 'time machine':
                        room_ob.items.append(
                            TimeMachine(room_item['title'],
                                        room_item.get('description', ''),
                                        room_item.get('use_location', ''))
                        )
                    elif room_item['title'].startswith('human'):
                        room_ob.sprites.append(
                            self.sprites.get(room_item['title']))
                    else:
                        room_ob.items.append(
                            Item(room_item['title'],
                                 room_item.get('description', ''),
                                 room_item.get('use_location', ''))
                        )
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
        self.items = []

    def take(self, user_input, room):
        """
        a player is only allowed to hold up to 5 items
        """
        if getattr(self, 'items', False) and len(self.items) == 5:
            return 'Your backpack can only hold up to 5 items'

        if not user_input and len(room.items) > 0:
            # assume the user wants to pick up the first item in the room
            item = room.items.pop()
            self.items.append(item)
            return 'Took %s\n' % item.title

        # otherwise they have asked to pick up a specific item so
        # check item is in room
        if not room.items:
            raise TypeError
        item_to_add = [x for x in room.items
                       if x.title.lower() == ' '.join(user_input).lower()]
        if not item_to_add:
            raise TypeError

        if getattr(self, 'items', None) is None:
            self.items = []
        self.items.append(item_to_add[0])
        room.items.pop()
        return 'Taken\n'

    def drop(self, item, room):
        if not item:
            return 'Drop what?\n'
        if not getattr(self, 'items', False):
            return 'You are not carrying anything.\n'
        if not self.items:
            return 'You are not carrying anything.\n'
        item = ' '.join(item)
        item_titles = [x.title for x in self.items]
        if item not in item_titles:
            return 'You are not carrying a %s' % item

        new_items = []
        for player_item in self.items:
            if player_item.title != item:
                new_items.append(player_item)
            else:
                item_for_room = player_item
        self.items = new_items
        room.items.append(item_for_room)
        return 'Dropped\n'

    def inventory(self, user_input, room):
        if getattr(self, 'items', []):
            s = 'You are carrying:\n'
            for item in self.items:
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
        for item in self.items:
            if item.title == joined_input:
                return item.description

        for item in room.items:
            if item.title == joined_input:
                return item.description

        return 'I cannot see a {}\n'.format(joined_input)

    def use(self, user_input, room):
        # first see if we have that item
        if not user_input:
            return "Use what?\n"
        if not getattr(self, 'items', False):
            return "You have nothing to use.\n"

        found_item = None
        requested_item = ' '.join(user_input)
        for index, item in enumerate(self.items):
            if item.title == requested_item:
                found_item = item
                del self.items[index]
        if found_item is None:
            return "You don't have a %s" % requested_item

        # check to see if that item can be used here
        use_location = item.use_location
        if item.title == 'time machine':
            self.world.toggle_date()
            print("There is a blinding light. You feel strange.")
        elif use_location is None or array_to_id(
                use_location) != self.current_location():
            return "Nothing happens.\n"

        # perform the action
        room.blocked = False
        return room.unblocked


class Actor(Human):
    """These are the actors with which the player will interact
    during the game. These actors can give information to the player
    or simply give them an object.
    """


class Item(object):

    def __init__(self, title, description, use_location):
        self.title = title
        self.description = description
        self.use_location = use_location

    def further_description(self):
        """
        used when a users 'looks' at this item
        """


class TimeMachine(Item):

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

    def describe_location(self):
        """
        returns the current room and any items
        """
        main_description = '%s\n%s' % (self.title,
                                       self.long_description)
        # if the room is blocked, we add the blocked_description
        if self.blocked:
            main_description = '%s %s' % (main_description,
                                          self.blocked_description)

        if self.items:
            all_items = ''
            for item in self.items:
                all_items += '\nThere is a %s here.' % item.title
            print('{} {}'.format(
                main_description, all_items))
        else:
            print(main_description)

        if self.sprites:
            for sprite in self.sprites:
                sprite.back_story()
