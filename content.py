import persistent

from exc import GameOver
from tools import array_to_id

START_POS = [0, 5, 0]  # [x, y, z]


class World(object):
    def __init__(self, adventure_map, sprites=None, player=None):
        """Init world."""
        if player is None:
            player = Player(START_POS, self)
        self.player = player
        self.adventure_map = adventure_map
        self.sprites = sprites
        self.parse_map(self.adventure_map)
        self.date = "present"

    def parse_map(self, adventure_map):
        self.world = {"past": {}, "present": {}, "future": {}}
        for timezone, map_details in adventure_map.items():
            for location_id, room in map_details.items():
                room_items = room.get("room_items", [])
                room_ob = Room(
                    room["title"],
                    room["description"],
                    room.get("short_description", ""),
                    room.get("blocked", False),
                    room.get("blocked_reason", ""),
                    room.get("unblocked", ""),
                    room.get("blocked_description", ""),
                    room.get("death_if_entered", False),
                    room.get("loop", None),
                )
                for room_item in room_items:
                    if room_item["title"] == "time machine":
                        time_machine = TimeMachine(
                            room_item["title"],
                            room_item.get("description", ""),
                            room_item.get("use_location", ""),
                        )
                        room_ob.items[room_item["title"]] = time_machine
                    elif room_item.get("sprite_id", None) is not None:
                        sprite = self.sprites[room_item["sprite_id"]]
                        room_ob.items[sprite.title] = sprite
                    else:
                        item = Item(
                            room_item["title"],
                            room_item.get("description", ""),
                            room_item.get("use_location", ""),
                            room_item.get("hidden", False),
                            room_item.get("when_eaten", ""),
                        )
                        item.death_if_eaten = room_item.get("death_if_eaten", False)
                        room_ob.items[room_item["title"]] = item
                self.world[timezone][location_id] = room_ob

    def current_room(self):
        return self.world[self.date].get(self.player.current_location())

    def valid_move(self, new_location_id):
        return new_location_id in self.world[self.date]

    def toggle_date(self):
        if self.date == "present":
            self.date = "past"
        else:
            self.date = "present"


class Human(persistent.Persistent):
    def __init__(self, location=None):
        self.current_coordinates = location
        self.told_back_story = False

    def current_location(self):
        """Gives the current coords in form 'x-y-z'"""
        return array_to_id(self.current_coordinates)

    def back_story(self):
        """If this user has a story to tell, they do it here."""


class Player(Human):
    # the player's backpack can only hold this many items
    MAX_ITEMS = 5

    def __init__(self, location, world):
        self.world = world
        self.current_coordinates = location
        self.visited = set()
        self.items = {}

    def _add_to_items(self, title, room):
        self.items[title] = room.items[title]
        del room.items[title]

    def take(self, user_input, room):
        """Player is only allowed to hold up to MAX_ITEMS items."""
        if getattr(self, "items", False) and len(self.items) == self.MAX_ITEMS:
            return "Your backpack can only hold up to %d items\n" % self.MAX_ITEMS

        if not room.items:
            return "There is nothing here to take.\n"

        if not user_input:
            # assume the user wants to pick up the first item in the room
            item_title = next(iter(room.items))
            self._add_to_items(item_title, room)
            return "Took %s\n" % item_title

        # otherwise they have asked to pick up a specific item, so
        # check that the item is actually in the room
        item_title = " ".join(user_input).lower()
        if item_title not in room.items:
            return "I cannot see a %s here.\n" % item_title
        self._add_to_items(item_title, room)
        return "Taken\n"

    def drop(self, user_input, room):
        if not user_input:
            return "Drop what?\n"
        if not self.items:
            return "You are not carrying anything.\n"
        item_title = " ".join(user_input)
        if item_title not in self.items:
            return "You are not carrying a %s" % item_title

        room.items[item_title] = self.items[item_title]
        del self.items[item_title]
        return "Dropped\n"

    def inventory(self, user_input, room):
        if getattr(self, "items", []):
            s = "You are carrying:\n"
            for item in self.items.values():
                s += "A %s\n" % item.title
            return s
        else:
            return "You are not carrying anything.\n"

    def look(self, user_input, room):
        """Look around or at something.

        If user types just 'look', describe the room,
        If not, look at what they are carrying for a match,
        or look at the objects in the room.
        """
        if not user_input:
            return f"{room.describe_location()}\n"

        joined_input = " ".join(user_input).lower()
        try:
            return self.items[joined_input].description
        except KeyError:
            pass

        try:
            item = room.items[joined_input]
        except KeyError:
            return "I cannot see that"
        else:
            try:
                return item.back_story()
            except AttributeError:
                return item.description

    def use(self, user_input, room):
        # first see if we have that item
        if not user_input:
            return "Use what?\n"
        if not getattr(self, "items", False):
            return "You have nothing to use.\n"

        requested_item = " ".join(user_input)
        try:
            found_item = self.items[requested_item]
        except KeyError:
            return "You don't have a %s" % requested_item

        # the time machine is reusable and works anywhere; it is not consumed
        if found_item.title == "time machine":
            self.world.toggle_date()
            return "There is a blinding light. You feel strange.\n"

        # otherwise the item only does something at its use_location. If it
        # can't be used here, leave it in the inventory rather than wasting it.
        use_location = found_item.use_location
        if use_location is None or array_to_id(use_location) != self.current_location():
            return "Nothing happens.\n"

        # the item is consumed and the action is performed
        del self.items[requested_item]
        room.blocked = False
        return room.unblocked

    def eat(self, user_input, room):
        """
        Attempt to eat the item.

        This item can either be in the inventory or in the room.
        This doesn't usually end well.
        """
        requested_item = " ".join(user_input)
        if requested_item in self.items:
            container = self.items
        elif requested_item in room.items:
            container = room.items
        else:
            return "I cannot see a {}".format(requested_item)

        found_item = container[requested_item]
        if getattr(found_item, "death_if_eaten", False):
            raise GameOver(found_item.when_eaten)

        when_eaten = getattr(found_item, "when_eaten", "")
        if not when_eaten:
            return "I can't eat that"

        # the item is actually eaten, so remove it from wherever it was
        del container[requested_item]
        return when_eaten

    def on(self, user_input, room):
        if not user_input:
            return "Turn on what?\n"
        try:
            return room.items[user_input[0]].on()
        except AttributeError:
            return "I can't seem to turn it on."


class Item(object):
    def __init__(self, title, description, use_location, hidden, when_eaten):
        self.title = title
        self.description = description
        self.use_location = use_location
        self.hidden = hidden
        self.when_eaten = when_eaten
        # may be overridden by the map loader for poisonous items
        self.death_if_eaten = False

    def __repr__(self):
        return "<Item: {}>".format(self.title)


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
        """Show the current date/time."""


class Room(object):
    def __init__(
        self,
        title,
        description,
        short_description,
        blocked,
        blocked_reason,
        unblocked,
        blocked_description,
        death_if_entered,
        loop,
    ):
        self.title = title
        self.long_description = description
        self.short_description = short_description
        self.blocked = blocked
        # this is a message to the player when room is unblocked
        self.blocked_reason = blocked_reason
        self.unblocked = unblocked
        self.blocked_description = blocked_description
        self.items = {}
        self.sprites = []
        self.death_if_entered = death_if_entered
        self.loop = loop

    def describe_location(self):
        """Describe the current room and any items.

        Shown on first entry (and on "look"): the room title followed by the
        full description. On re-entry the main loop shows just the title.
        """
        main_description = "{}\n{}".format(self.title, self.long_description)
        # if the room is blocked, we add the blocked_description
        if self.blocked:
            main_description = "%s \n%s" % (main_description, self.blocked_description)

        if self.items:
            all_items = ""
            for item in self.items.values():
                try:
                    hidden = item.hidden
                except AttributeError:
                    pass
                else:
                    if not hidden:
                        all_items += "\nThere is a %s here." % item.title
            main_description = "{} {}".format(main_description, all_items)

        return main_description
