import game
import game_setup
import pprint
import gui

def main():
    board = game_setup.new_board()
    print(board)

    gui.start(board)




if __name__ == '__main__':
    main()
