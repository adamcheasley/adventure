class Player(object):

    def __init__(self, location):
        self.current_location = location

    def take(self, item, room):
        # check item is in room
        if not room.items:
            raise TypeError
        if item != room.items[0].title:
            raise TypeError

        if getattr(self, 'items', None) is None:
            self.items = []
        self.items.append(item)
        print 'Taken\n'

    def drop(self):
        pass

    def inventory(self):
        if getattr(self, 'items', None) is not None:
            print 'You are carrying:\n'
            for item in self.items:
                print item
        else:
            print 'You are not carrying anything.\n'


class Item(object):

    def __init__(self, title):
        self.title = title

    def description(self):
        pass

    def further_description(self):
        """
        used when a users 'looks' at this item
        """

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
