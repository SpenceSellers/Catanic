import queue
import threading
import time

import game
import game_setup
import pprint
import gui
import hexagons

def main():

    q = queue.Queue()

    thread = threading.Thread(target=lambda: gui.start(q))
    thread.start()

    while True:
        board = game_setup.new_board_started()

        q.put(board)

        time.sleep(30)
    # gui.start(board)




if __name__ == '__main__':
    main()
