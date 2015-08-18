#!/usr/bin/python

import sys
import yaml
from tools import Utils
from content import World


# initial scene setting
print("Welcome player.")
print("Two days ago, you awoke to find"
      " the world you knew had changed dramatically.")
print("The busy city where you once lived is now almost silent.")
print("There are no cars on the roads, "
      "no planes in the sky\nand no people on the streets.")
print("The electricity in what's left of the city is intermittent.")
print("For the last two days you have "
      "been wandering aimlessly, looking for answers.\n")

# initialise the map
map_file = open('world_map.yaml', 'r')
main_map = yaml.load(map_file.read())
world = World(main_map)
utils = Utils()
room = world.current_room()
player = world.player
print('%s\n' % room.describe_location())
room_described = True

# main execution loop
while True:
    if not room_described:
        if player.current_location in player.visited:
            print('%s\n' % room.title)
        else:
            print('%s\n' % room.describe_location())

    user_input = input('>:')
    if user_input in ['exit', 'quit', 'q']:
        print('Goodbye\n')
        sys.exit(1)
    else:
        room_described = utils.parse_user_input(user_input, player, world)

    room = world.current_room()
