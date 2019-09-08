import queue
import threading
import logging
import itertools
import time

from catan import game
import game_setup
from gui import gui
from agents.agents import RandomAgent, InformedRandomAgent


def game_manager_thread(game_queue, command_queue):
    while True:
        (command, config) = command_queue.get()
        if command == 'start':
            thread = threading.Thread(target=lambda: game_thread(game_queue), daemon=True)
            thread.start()
            thread.join()


def game_thread(game_queue):
    board = game_setup.new_board_started()

    agents = {
        0: RandomAgent(),
        1: RandomAgent(),
        2: InformedRandomAgent(),
        3: RandomAgent(),
    }

    the_game = game.Game(board, agents)
    game_queue.put(the_game)
    for i in itertools.count():
        ongoing = the_game.tick(agents)
        game_queue.put(the_game)
        if i % 10 == 0:
            time.sleep(0.1)

        if not ongoing:
            game_queue.put(the_game)
            return


def main():
    logging.basicConfig(level=logging.DEBUG)
    game_queue = queue.Queue()
    command_queue = queue.Queue()

    thread = threading.Thread(target=lambda: game_manager_thread(game_queue, command_queue), daemon=True)
    thread.start()

    gui.start(game_queue, command_queue)


if __name__ == '__main__':
    main()
