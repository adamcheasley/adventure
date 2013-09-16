class Player(object):

    def __init__(self, location):
        self.location = location

    def take(self):
        pass

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

    def __init__(self, title):
        self.title = title

    def long_description(self):
        pass

    def short_description(self):
        pass

    def location(self):
        pass

    def items(self):
        pass
