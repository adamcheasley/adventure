#!/usr/bin/python

import sys

import yaml
import transaction
import ZODB
from ZODB import FileStorage
from content import World
from exc import GameOver
from sprites import sprites_to_init
from tools import parse_user_input

# setup database
storage = FileStorage.FileStorage('data.fs')
db = ZODB.DB(storage)
connection = db.open()
root = connection.root
try:
    player = root.player
except AttributeError:
    player = None

if player is None:
    # initial scene setting
    print("\n\n\n\nWelcome player.\n"
          "Two days ago, you awoke in hospital to find"
          " the world you knew had changed dramatically.\n"
          "The small village where you once lived is now almost silent.\n"
          "There are no cars on the roads, "
          "no planes in the sky\n"
          "and no people on the streets.\n"
          "The electricity in what's left of the village is intermittent.\n"
          "For the last two days you have "
          "been travelling towards the city, looking for answers.\n")

# initialise sprites
sprites = {x.sprite_id: x() for x in sprites_to_init}

# initialise the map and game state
map_file = open('new_map.yaml', 'r')
main_map = yaml.load(map_file.read())
world = World(main_map, sprites=sprites, player=player)
room = world.current_room()
if player is None:
    player = world.player
    # store the new player in zodb
    root.player = player

print(room.describe_location())
print('\n')
room_described = True
exit_text = 'Goodbye\n'

# main execution loop
while True:
    if not room_described:
        if room.death_if_entered:
            exit_text = "{}\n\n".format(room.long_description)
            break
        elif player.current_location() in player.visited:
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
exit_input = input('\nWould you like to save your game?\n')
if exit_input.strip().lower() in {'y', 'yes'}:
    transaction.commit()

sys.exit(1)
