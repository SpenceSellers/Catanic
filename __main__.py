import queue
import threading
import time
import logging

from catan import game
import game_setup
from gui import gui
from agents.agents import RandomAgent


def main():
    logging.basicConfig(level=logging.DEBUG)
    q = queue.Queue()

    thread = threading.Thread(target=lambda: gui.start(q))
    thread.start()

    board = game_setup.new_board_started()
    q.put(board)

    agents = {
        0: RandomAgent(),
        1: RandomAgent(),
        2: RandomAgent(),
        3: RandomAgent()
    }

    the_game = game.Game(board)
    while True:
        time.sleep(0.05)
        the_game.tick(agents)
        q.put(the_game.board)


if __name__ == '__main__':
    main()
