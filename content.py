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

    def __init__(self, title, description, location):
        self.title = title
        self.long_description = description[0]
        self.short_description = description[1]
        self.location = location

    def items(self):
        pass
