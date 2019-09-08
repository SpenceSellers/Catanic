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
    current_game_thread = None
    game_control_queue = queue.Queue()
    while True:
        (command, config) = command_queue.get()
        if command == 'start':
            if current_game_thread:
                logging.warning('Waiting for current game to finish before starting another')
                current_game_thread.join()

            current_game_thread = threading.Thread(target=lambda: game_thread(game_queue, game_control_queue), daemon=True)
            current_game_thread.start()

        elif command in ['play', 'pause', 'step']:
            game_control_queue.put((command, config))


def game_thread(game_queue, game_control_queue):
    board = game_setup.new_board_started()

    agents = {
        0: RandomAgent(),
        1: RandomAgent(),
        2: InformedRandomAgent(),
        3: InformedRandomAgent(),
    }

    the_game = game.Game(board, agents)
    game_queue.put(the_game)

    ms_per_turn = 10
    paused = True
    for i in itertools.count():
        is_stepping = False
        while True:
            try:
                # If we're paused, there's no sense in looping constantly.
                # We'll wait for our next command if we're paused, otherwise
                # it'd be better to be running the game
                should_wait = paused
                (cmd, params) = game_control_queue.get(block=should_wait)

                if cmd == 'pause':
                    paused = True
                elif cmd == 'play':
                    paused = False
                elif cmd == 'step':
                    is_stepping = True
            except queue.Empty:
                print('Empty')
                pass

            if not paused:
                break

            if paused and is_stepping:
                # We're being given special permission to run a single step, but the game is still "paused"
                break

        ongoing = the_game.tick(agents)
        game_queue.put(the_game)

        if not ongoing:
            # Someone won!
            return

        # Slow down the execution for a better viewing experience
        # There's no sense in waiting if we're paused anyway
        if not paused:
            # TODO don't sleep every time, aggregate sleeps into blocks
            time.sleep(ms_per_turn/1000)


def main():
    logging.basicConfig(level=logging.WARNING)
    game_queue = queue.Queue()
    command_queue = queue.Queue()

    thread = threading.Thread(target=lambda: game_manager_thread(game_queue, command_queue), daemon=True)
    thread.start()

    gui.start(game_queue, command_queue)


if __name__ == '__main__':
    main()
