import threading

import game
import game_setup
import pprint
import gui
import hexagons

def main():
    board = game_setup.new_board()

    vtc = hexagons.VerticeCoord((0, 0), 0)
    board.settlements[vtc] = game.Settlement(1, vtc)

    ec = hexagons.EdgeCoord((0,0), 0)
    board.roads[ec] = game.Road(1, ec)

    threading.Thread(lambda: gui.start(board))

    # gui.start(board)




if __name__ == '__main__':
    main()
