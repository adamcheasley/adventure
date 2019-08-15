from textwrap import dedent

from content import Item


class BaseSprite(object):
    def __init__(self, *args):
        pass

    def back_story(self):
        return self.description


class ScientistOne(BaseSprite):
    """
    A scientist.

    This is the first scientist that the player meets in
    the laboratory building.
    """

    sprite_id = "human_1"
    title = "man"
    description = "A man, who is clearly not well..."

    def back_story(self):
        return dedent(
            """\
        \n"Who are you? How did you get in here?\n
It doesn't matter. It was us, we did it. It was a virus. We couldn't stop it, it had
mutated too much. Our medicine could not fight it yet. You have to find the machine.
Find the machine, go back and stop this from every happening!"\n
The man coughs a few more times, then closes his eyes.
        """
        )


class ComputerOne(BaseSprite, Item):

    sprite_id = "computer_1"
    title = "computer"
    description = "A standard beige computer. The power is off."
    use_location = None
    hidden = False
    when_eaten = (
        "You gnaw at the computer, but it" " is too difficult to eat the whole thing."
    )

    def on(self):
        return (
            "The screen flickers a bit. Then"
            " goes dark. I think it's not going to work."
        )


sprites_to_init = (ScientistOne, ComputerOne)
