class Player(object):

    def __init__(self, location):
        self.current_location = location

    def take(self, item):
        if getattr(self, 'items', None) is None:
            self.items = []
        self.items.append(item)

    def drop(self):
        pass

    def inventory(self):
        pass


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

    def items(self):
        return self.items
