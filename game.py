import random
from typing import Dict

import agents
import board
import player
from agents import Agent
from hexagons import HexCoord
from resources import Resource


class Game:
    def __init__(self, board: board.Board, num_players: int = 4):
        self.board = board
        self.players = {}
        self.num_players = num_players

        self.next_to_play = 0

        for i in range(num_players):
            self.players[i] = player.Player(i)

    def give_player_resource(self, player_id: int, resource: Resource, quantity: int = 1):
        self.players[player_id].hand.add_resource(resource, quantity)

    def dispense_resource(self, coord: HexCoord):
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
        print('Rolled', roll)
        for tile in self.board.tiles.values():
            if tile.number == roll:
                self.dispense_resource(tile.coords)

    def do_move(self, player_id: int, move: agents.Move) -> agents.MoveResult:
        try:
            if type(move) == agents.BuildSettlementMove:
                self.board.add_settlement(board.Settlement(player_id, move.vertex))
        except board.IllegalMoveError:
            return agents.FailedMoveResult()

        return agents.SuccessfulMoveResult()

    def tick(self, ags: Dict[int, Agent]):
        roll = random.randint(1, 7) + random.randint(1, 7)
        self.rolled(roll)

        moves = ags[self.next_to_play].do_moves(self)
        try:
            while True:
                move = next(moves)
                print('Running move', move)
                result = self.do_move(self.next_to_play, move)
                moves.send(result)
        except StopIteration:
            pass

        self.next_to_play = (self.next_to_play + 1) % self.num_players





