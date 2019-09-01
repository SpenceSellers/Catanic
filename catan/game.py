import logging
import random
from typing import Dict

from catan import board, player, moves
from agents import agents
from agents.agents import Agent
from hexagons.hexagons import HexCoord
from catan.resources import Resource


class Game:
    def __init__(self, board: board.Board, agents: Dict[int, Agent], num_players: int = 4):
        self.board = board
        self.agents = agents
        self.players = {}
        self.num_players = num_players
        self.turn_number = 0

        self.next_to_play = 0

        for i in range(num_players):
            self.players[i] = player.Player(i)

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

    def rolled(self, roll: int):
        logging.info(f'Number was rolled: {roll}')
        if roll == 7:
            self.roll_seven()
        else:
            for tile in self.board.tiles.values():
                if tile.number == roll:
                    self.dispense_resource(tile.coords)

    def roll_seven(self):
        # TODO
        pass

    def do_move(self, player_id: int, move: moves.Move) -> moves.MoveResult:
        """Executes a player's Move"""
        move_context = moves.MoveContext(self, player_id)
        return move.execute(move_context)

    def tick(self, player_agents: Dict[int, Agent]):
        """Performs one turn of the game"""
        roll = random.randint(1, 7) + random.randint(1, 7)
        self.rolled(roll)

        move_generator = player_agents[self.next_to_play].play_turn(self)
        logging.info(f"PLAYER {self.next_to_play} BEGIN TURN NUMBER {self.turn_number}")
        logging.info(f"Player has {self.players[self.next_to_play].hand.resources}")

        # Advance to the first yield point
        move = next(move_generator)
        try:
            while True:
                logging.info(f'Player {self.next_to_play} is playing move {move}')
                result_of_move = self.do_move(self.next_to_play, move)

                if not result_of_move.successful:
                    logging.info(f"Player {self.next_to_play}'s move failed because {result_of_move.results}")
                else:
                    logging.info(f"The move was successful")

                move = move_generator.send(result_of_move)
        except StopIteration:
            pass

        logging.info(f"PLAYER {self.next_to_play} END TURN")

        # Advance to next player's turn
        self.next_to_play = (self.next_to_play + 1) % self.num_players
        self.turn_number += 1





