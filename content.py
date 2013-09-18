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


class Item(object):

    def __init__(self, title, description):
        self.title = title
        self.description = description

    def further_description(self):
        """
        used when a users 'looks' at this item
        """
        pass

    def use_location(self):
        """
        the location where this object should be used
        """
        pass


class Room(object):

    def __init__(self, title, description):
        self.title = title
        self.long_description = description[0]
        self.short_description = description[1]
