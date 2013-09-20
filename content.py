from utils import create_location_id


class Player(object):

    def __init__(self, location):
        self.current_location = location

    def take(self, user_input, room):
        if not user_input and len(room.items) > 0:
            # assume the user wants to pick up the first item in the room
            if not getattr(self, 'items', False):
                self.items = []
            item = room.items.pop()
            self.items.append(item)
            return 'Took %s\n' % item.title

        # otherwise they have asked to pick up a specific item
        item = user_input[-1]
        # check item is in room
        if not room.items:
            raise TypeError
        item_to_add = [x for x in room.items if x.title == item]
        if not item_to_add:
            raise TypeError

        if getattr(self, 'items', None) is None:
            self.items = []
        self.items.append(item_to_add[0])
        room.items.pop()
        return 'Taken\n'

    def drop(self, item, room):
        try:
            item = item[0]
        except IndexError:
            return 'Drop what?\n'
        if not getattr(self, 'items', False):
            return 'You are not carrying anything.\n'
        if not self.items:
            return 'You are not carrying anything.\n'
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
        if getattr(self, 'items', None) is not None:
            s = 'You are carrying:\n'
            for item in self.items:
                s += 'A %s\n' % item.title
            return s
        else:
            return 'You are not carrying anything.\n'

    def look(self, user_input, room):
        if not user_input:
            return room.describe_location()
        # otherwise we need to look in our inventory and describe
        # the item
        if not getattr(self, 'items', False):
            return 'You are not carrying anything.\n'
        for item in self.items:
            if item.title == user_input[1].strip():
                return item.description
        return 'You do not have one of those\n'

    def use(self, user_input, room):
        # first see if we have that item
        if not user_input:
            return "Use what?\n"
        if not getattr(self, 'items', False):
            return "You have nothing to use.\n"

        found_item = None
        requested_item = user_input[0]
        for item in self.items:
            if item.title == requested_item:
                found_item = item
        if found_item is None:
            return "You don't have a %s" % requested_item

        # check to see if that item can be used here
        if create_location_id(item.use_location) != create_location_id(self.current_location):
            return "Nothing happens.\n"

        # perform the action
        room.blocked = False
        return room.unblocked


class Item(object):

    def __init__(self, title, description, use_location):
        self.title = title
        self.description = description
        self.use_location = use_location

    def further_description(self):
        """
        used when a users 'looks' at this item
        """
        pass


class Room(object):

    def __init__(self, title, description, blocked, blocked_reason, unblocked):
        self.title = title
        self.long_description = description[0]
        self.short_description = description[1]
        self.blocked = blocked
        self.blocked_reason = blocked_reason
        self.unblocked = unblocked

    def describe_location(self):
        """
        returns the current room and any items
        """
        main_description = '%s\n%s' % (self.title,
                                       self.long_description)
        if self.items:
            all_items = ''
            for item in self.items:
                all_items += '\nThere is a %s here.' % item.title
            return '%s %s' % (main_description,
                              all_items)
        else:
            return main_description
