#!/usr/bin/python

import sys
from tools import World
from tools import Utils
from world import world as world_info
from content import Player


print "Welcome player.\n"

# initialise the map
world = World(world_info)
utils = Utils()
player = Player((0, 0, 0))

while True:
    user_input = raw_input('>:')
    if user_input == 'exit':
        print 'Goodbye\n'
        sys.exit(1)
    else:
        utils.parse_user_input(user_input, player)
