import queue
import threading
import logging
import itertools
import time

from catan import game
import game_setup
from gui import gui
from agents.agents import RandomAgent, InformedRandomAgent


def gui_thread(q: queue.Queue):
    gui.start(q)


def main():
    logging.basicConfig(level=logging.DEBUG)
    q = queue.Queue()

    thread = threading.Thread(target=lambda: gui_thread(q), daemon=True)
    thread.start()

    board = game_setup.new_board_started()

    agents = {
        0: RandomAgent(),
        1: RandomAgent(),
        2: InformedRandomAgent(),
        3: RandomAgent()
    }

    the_game = game.Game(board, agents)
    q.put(the_game)
    for i in itertools.count():
        ongoing = the_game.tick(agents)
        if i % 200 == 0:
            q.put(the_game)
            time.sleep(0.1)

        if not ongoing:
            time.sleep(10000)


if __name__ == '__main__':
    main()
