#!/usr/bin/python

import sys
from tools import World
from tools import Utils
from world import world as world_info
from content import Player
from utils import create_location_id


print "Welcome player."
print "Two days ago, you awoke to find the world you knew had changed dramatically."
print "The busy city where you once lived is now almost silent."
print "There are no cars on the roads, no planes in the sky\nand the electricity is intermittent."
print "For the last two days you have been wandering aimlessly, looking for answers."
print

# initialise the map
world = World(world_info)
utils = Utils()
player = Player([0, 0, 0])
player.visited = set([])
room = world.current_room(player.current_location)
print '%s\n' % room.describe_location()
room_described = True

while True:
    if not room_described:
        if create_location_id(player.current_location) in player.visited:
            print '%s\n' % room.title
        else:
            print '%s\n' % room.describe_location()

    user_input = raw_input('>:')
    if user_input == 'exit':
        print 'Goodbye\n'
        sys.exit(1)
    else:
        room_described = utils.parse_user_input(user_input, player, world)

    room = world.current_room(player.current_location)
