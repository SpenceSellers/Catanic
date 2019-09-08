import logging
import queue
import random
from typing import Dict, Any

from catan import board, player, moves
from agents import agents
from agents.agents import Agent
from game_events import RollEvent, PlayedMoveEvent
from hexagons.hexagons import HexCoord
from catan.resources import Resource

WINNING_VICTORY_POINTS = 10


class Game:
    def __init__(self, board: board.Board, agents: Dict[int, Agent], game_event_callback = None):
        self.board = board
        self.agents = agents
        self.game_event_callback = game_event_callback
        self.players = {}
        self.num_players = len(agents)
        self.turn_number = 0

        self.next_to_play = 0

        for i in range(self.num_players):
            self.players[i] = player.Player(i)

        for (id, agent) in agents.items():
            agent.join_game(self, id)

    def event(self, event: Any):
        if self.game_event_callback:
            self.game_event_callback(event)

    def give_player_resource(self, player_id: int, resource: Resource, quantity: int = 1):
        self.players[player_id].hand.add_resource(resource, quantity)

    def dispense_resource(self, coord: HexCoord):
        """Causes a given tile to give its resources to those with settlements on the tile."""

        tile = self.board.tiles[coord]
        resource = tile.type.resource()
        if not resource:
            # This tile has no resource to give
            return

        for vertex in tile.coords.vertices():
            if vertex in self.board.settlements:
                settlement = self.board.settlements[vertex]
                self.give_player_resource(settlement.owner, resource, 2 if settlement.is_city else 1)

    def rolled(self, player_id: int, roll: int):
        logging.info(f'Number was rolled: {roll}')
        self.event(RollEvent(player_id, roll))

        if roll == 7:
            self.roll_seven()
        else:
            for tile in self.board.tiles.values():
                if tile.number == roll:
                    self.dispense_resource(tile.coords)

    def roll_seven(self):
        # TODO
        pass

    def get_victory_points(self, player_id: int) -> int:
        count = 0
        for settlement in self.board.settlements.values():
            if settlement.owner == player_id:
                count += 2 if settlement.is_city else 1

        return count

    def do_move(self, player_id: int, move: moves.Move) -> moves.MoveResult:
        """Executes a player's Move"""
        move_context = moves.MoveContext(self, player_id)
        return move.execute(move_context)

    def tick(self, player_agents: Dict[int, Agent]) -> bool:
        """Performs one turn of the game"""
        roll = random.randint(1, 7) + random.randint(1, 7)
        self.rolled(self.next_to_play, roll)

        move_generator = player_agents[self.next_to_play].play_turn()
        logging.info(f"PLAYER {self.next_to_play} BEGIN TURN NUMBER {self.turn_number}")

        # Advance to the first yield point
        move = next(move_generator)
        try:
            while True:
                logging.info(f'Player {self.next_to_play} is playing move {move}')
                result_of_move = self.do_move(self.next_to_play, move)

                if not result_of_move.successful:
                    logging.info(f"Player {self.next_to_play}'s move failed because {result_of_move.results}")
                else:
                    self.event(PlayedMoveEvent(self.next_to_play, move))
                    logging.info(f"The move was successful")

                move = move_generator.send(result_of_move)
        except StopIteration:
            pass

        victory_points = self.get_victory_points(self.next_to_play)
        logging.info(f"PLAYER {self.next_to_play} END TURN with {victory_points} points")
        if victory_points >= WINNING_VICTORY_POINTS:
            logging.info(f'PLAYER {self.next_to_play} WON (agent {self.agents[self.next_to_play]})')
            return False

        # Advance to next player's turn
        self.next_to_play = (self.next_to_play + 1) % self.num_players
        self.turn_number += 1

        return True
