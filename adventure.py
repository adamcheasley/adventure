#!/usr/bin/python

import sys
import yaml
from tools import Utils
from content import World
from sprites import ScientistOne


# initial scene setting
print(u"\n\n\n\nWelcome player.")
print(u"Two days ago, you awoke to find"
      u" the world you knew had changed dramatically.")
print(u"The busy city where you once lived is now almost silent.")
print(u"There are no cars on the roads, "
      u"no planes in the sky\nand no people on the streets.")
print(u"The electricity in what's left of the city is intermittent.")
print(u"For the last two days you have "
      u"been wandering aimlessly, looking for answers.\n")

# initialise sprites
sprites = {
    'human_1': ScientistOne(),
}

# initialise the map
map_file = open('world_map.yaml', 'r')
main_map = yaml.load(map_file.read())
world = World(main_map, sprites=sprites)
utils = Utils()
room = world.current_room()
player = world.player
room.describe_location()
print('\n')
room_described = True

# main execution loop
while True:
    if not room_described:
        if player.current_location() in player.visited:
            print('%s\n' % room.title)
        else:
            room.describe_location()
            print('\n')

    try:
        user_input = input('>:')
    except:
        print('Goodbye\n')
        sys.exit(1)

    if user_input in ['exit', 'quit', 'q']:
        print('Goodbye\n')
        sys.exit(1)
    else:
        room_described = utils.parse_user_input(user_input, player, world)

    room = world.current_room()
