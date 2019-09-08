import queue
import threading
import logging
import itertools
import time

from catan import game
import game_setup
from game_events import GameUpdateEvent
from gui import gui
from agents.agents import RandomAgent, InformedRandomAgent


class GameManager:
    def __init__(self, game_queue: queue.Queue, command_queue: queue.Queue):
        self.game_queue = game_queue
        self.command_queue = command_queue
        self.current_game_thread = None
        self.game_control_queue = queue.Queue()

    def run_loop(self):
        while True:
            (command, config) = self.command_queue.get()
            if command == 'start':
                self.end()
                self.start()

            elif command == 'end':
                self.end()

            elif command in ['play', 'pause', 'step']:
                self.game_control_queue.put((command, config))

    def start(self):
        print('Starting game')
        self.current_game_thread = threading.Thread(target=lambda: game_thread(self.game_queue, self.game_control_queue), daemon=True)
        self.current_game_thread.start()

    def end(self):
        if self.current_game_thread:
            logging.warning('Ending current game')
            self.game_control_queue.put(('end', None))
            self.current_game_thread.join()
            self.current_game_thread = None


def game_thread(game_queue, game_control_queue):
    board = game_setup.new_board_started()

    agents = {
        0: RandomAgent(),
        1: RandomAgent(),
        2: InformedRandomAgent(),
        3: InformedRandomAgent(),
    }

    the_game = game.Game(board, agents)

    # Send the initial board state
    game_queue.put(GameUpdateEvent(the_game))

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
                elif cmd == 'end':
                    return
            except queue.Empty:
                pass

            if not paused:
                break

            if paused and is_stepping:
                # We're being given special permission to run a single step, but the game is still "paused"
                break

        ongoing = the_game.tick(agents)
        game_queue.put(GameUpdateEvent(the_game))

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

    thread = threading.Thread(target=lambda: GameManager(game_queue, command_queue).run_loop(), daemon=True)
    thread.start()

    gui.start(game_queue, command_queue)


if __name__ == '__main__':
    main()
