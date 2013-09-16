#!/usr/bin/python

import sys
from tools import World
from tools import Utils


print "Welcome player.\n"

# load the map
world_info = open('world.py', 'r')
# initialise the map
world = World(world_info)
utils = Utils()

while True:
    user_input = raw_input('>:')
    if user_input == 'exit':
        print 'Goodbye\n'
        sys.exit(1)
    else:
        utils.parse_user_input(user_input)
