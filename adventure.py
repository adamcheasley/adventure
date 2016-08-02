#!/usr/bin/python

import sys

import yaml
from content import World
from exc import GameOver
from sprites import sprites_to_init
from tools import parse_user_input

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
sprites = {x.sprite_id: x() for x in sprites_to_init}

# initialise the map
map_file = open('world_map.yaml', 'r')
main_map = yaml.load(map_file.read())
world = World(main_map, sprites=sprites)
room = world.current_room()
player = world.player
print(room.describe_location())
print('\n')
room_described = True
game_over = False
exit_text = 'Goodbye\n'

# main execution loop
while not game_over:
    if not room_described:
        if player.current_location() in player.visited:
            print('%s\n' % room.title)
        else:
            print(room.describe_location())
            print('\n')

    try:
        user_input = input('>:')
    except:
        break

    if user_input in ['exit', 'quit', 'q']:
        break
    else:
        try:
            room_described = parse_user_input(user_input, player, world)
        except GameOver:
            exit_text = "You are dead."
            break

    room = world.current_room()

print(exit_text)
sys.exit(1)
