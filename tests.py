import unittest
from content import World


class TestWorld(unittest.TestCase):

    def test_parse_map(self):
        """parse map expects a python data structure
        """
        world_data = {'present':
                      {'0-0-0': {'description': 'You are at the end of a long '
                                 'driveway.\n'
                                 'In the  distance is a large '
                                 'building. \n'
                                 'To either side is grass and then a '
                                 'high concrete wall.\n'
                                 'The drive leads north.',
                       'title': 'Gate'},
                       '0-1-0': {'description':
                                 'You are half way up the driveway. '
                                 'At the end of the drive is a tall,\n'
                                 'modern office building.\n'
                                 'The drive continues north.',
                                 'room_items':
                                 {'description': 'A laser cut key. It '
                                  'looks very new.',
                                  'title': 'key',
                                  'use_location': [0, 2, 0]},
                                 'title': 'Driveway'}}}
        world = World(world_data)
        self.assertTrue(isinstance(world.adventure_map, dict))
        self.assertTrue('present' in world.adventure_map)
        self.assertEqual(len(world.adventure_map['present']), 2)


if __name__ == '__main__':
    unittest.main()
