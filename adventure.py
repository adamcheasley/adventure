import curses
import os
import sys

import transaction
import yaml
import ZODB
from ZODB import FileStorage

from content import World
from exc import GameOver
from sprites import sprites_to_init
from tools import parse_user_input

MAP_FILE_NAME = "map.yaml"


def init_db():
    """Initialise database."""
    os.makedirs("data", exist_ok=True)
    storage = FileStorage.FileStorage("data/data.fs")
    db = ZODB.DB(storage)
    connection = db.open()
    root = connection.root
    return root


def init_world(root, player):
    """Initialise the world object and sprites."""
    # initialise sprites
    sprites = {x.sprite_id: x() for x in sprites_to_init}

    # initialise the map and game state
    map_file = open(MAP_FILE_NAME, "r")
    main_map = yaml.safe_load(map_file.read())
    world = World(main_map, sprites=sprites, player=player)
    return world


def save_game(stdscr, exit_text, dead):
    """Deal with saving the game."""
    stdscr.addstr("{}\n".format(exit_text))
    if not dead:
        stdscr.addstr("Would you like to save your game? [y/n]\n")
        exit_input = stdscr.getstr().decode("utf8")
        if exit_input.strip().lower() in {"y", "yes"}:
            transaction.commit()
    else:
        stdscr.addstr("Game over.\n")
        stdscr.addstr("Press any key to quit.\n")
        stdscr.getch()


def init_screen(stdscr, room):
    """Initialise screen."""
    curses.echo()
    stdscr.clear()
    stdscr.addstr(f"{room.describe_location()}\n")
    stdscr.refresh()
    stdscr.scrollok(True)
    stdscr.idlok(True)


def main(stdscr):
    """Execute main game function."""
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

    init_screen(stdscr, room)
    room_described = True
    exit_text = "Goodbye\n"
    dead = False

    # main execution loop
    while True:
        if not room_described:
            if room.death_if_entered:
                exit_text = "{}\n\n".format(room.long_description)
                dead = True
                break
            elif player.current_location() in player.visited:
                stdscr.addstr("{}\n".format(room.title))
            else:
                stdscr.addstr(f"{room.describe_location()}\n")
            stdscr.refresh()

        stdscr.addstr("> ")
        user_input = stdscr.getstr().decode("utf8")

        if user_input.strip().lower() in {"exit", "quit", "q"}:
            break

        try:
            room_described = parse_user_input(user_input, player, world, stdscr)
        except GameOver:
            exit_text = "You are dead."
            dead = True
            break

        room = world.current_room()
        stdscr.refresh()

    save_game(stdscr, exit_text, dead)
    sys.exit(1)


curses.wrapper(main)
