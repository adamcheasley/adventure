class Player(object):

    def take(self):
        pass

    def drop(self):
        pass

    def inventory(self):
        pass

    def location(self):
        pass


class Item(object):

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

    def long_description(self):
        pass

    def short_description(self):
        pass

    def location(self):
        pass

    def items(self):
        pass
