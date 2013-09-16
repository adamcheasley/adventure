from textwrap import dedent


class Utils(object):

    def adventure_help(self):
        return dedent("""\
        Welcome to adventure, written by Adam Forsythe-Cheasley.
        """)


class World(object):

    def __init__(self, adventure_map):
        self.adventure_map = adventure_map

    def parse_map(self):
        pass
