from utils import create_location_id


class Player(object):

    def __init__(self, location):
        self.current_location = location

    def take(self, item, room):
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
        print 'Taken\n'

    def drop(self, item, room):
        if not getattr(self, 'items', False):
            raise KeyError
        if not self.items:
            raise KeyError
        item_titles = [x.title for x in self.items]
        if item not in item_titles:
            raise TypeError

        new_items = []
        for player_item in self.items:
            if player_item.title != item:
                new_items.append(player_item)
            else:
                item_for_room = player_item
        self.items = new_items
        room.items.append(item_for_room)
        print 'Dropped\n'

    def inventory(self):
        if getattr(self, 'items', None) is not None:
            print 'You are carrying:\n'
            for item in self.items:
                print item.title
        else:
            print 'You are not carrying anything.\n'

    def look(self, user_input, world):
        input_list = user_input.split()
        if len(input_list) == 1:
            print world.describe_location(self.current_location)
            return
        # otherwise we need to look in our inventory and describe
        # the item
        if not getattr(self, 'items', False):
            print 'You are not carrying anything.\n'
        for item in self.items:
            if item.title == input_list[1].strip():
                print item.description
                return
        return 'You do not have one of those\n'

    def use(self, user_input, room):
        # first see if we have that item
        try:
            requested_item = user_input.split()[1]
        except IndexError:
            return "Use what?\n"

        found_item = None
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
