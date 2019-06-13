#!/usr/bin/python
import curses
import os
import sys

import transaction
import yaml
import ZODB
from content import World
from exc import GameOver
from sprites import sprites_to_init
from tools import parse_user_input
from ZODB import FileStorage


def init_db():
    """Setup database."""
    os.makedirs('data', exist_ok=True)
    storage = FileStorage.FileStorage('data/data.fs')
    db = ZODB.DB(storage)
    connection = db.open()
    root = connection.root
    return root


def init_world(root, player):
    """Setup the world object and sprites"""
    # initialise sprites
    sprites = {x.sprite_id: x() for x in sprites_to_init}

    # initialise the map and game state
    map_file = open('new_map.yaml', 'r')
    main_map = yaml.safe_load(map_file.read())
    world = World(main_map, sprites=sprites, player=player)
    return world


def main(stdscr):
    """Main game function."""
    root = init_db()
    try:
        player = root.player
    except AttributeError:
        player = None

    world = init_world(root, player)
    room = world.current_room()
    if player is None:
        player = world.player
        # store the new player in zodb
        root.player = player

    curses.echo()
    # Clear screen
    stdscr.clear()
    stdscr.addstr(f'{room.describe_location()}\n')
    stdscr.refresh()
    room_described = True
    exit_text = 'Goodbye\n'
    #
    # # main execution loop
    # while True:
    #     if not room_described:
    #         if room.death_if_entered:
    #             exit_text = "{}\n\n".format(room.long_description)
    #             break
    #         elif player.current_location() in player.visited:
    #             print('%s\n' % room.title)
    #         else:
    #             print(room.describe_location())
    #             print('\n')
    #
    #     try:
    #         user_input = input('>:')
    #     except:
    #         break
    #
    #     if user_input in ['exit', 'quit', 'q']:
    #         break
    #     else:
    #         try:
    #             room_described = parse_user_input(user_input, player, world)
    #         except GameOver:
    #             exit_text = "You are dead."
    #             break
    #
    #     room = world.current_room()
    #
    # print(exit_text)
    # exit_input = input('\nWould you like to save your game? [y/n]\n')
    # if exit_input.strip().lower() in {'y', 'yes'}:
    #     transaction.commit()
    #
    # sys.exit(1)


curses.wrapper(main)
