from textwrap import dedent

from content import Human


class ScientistOne(Human):
    """This is the first scientist that the player meets in
    the laboratory building.
    """

    def back_story(self):
        return dedent("""\
        \nHere is a lot of text.\n
        Just testing how this would work.\n\n
        Needs updating.
        """)
