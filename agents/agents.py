import random
from abc import abstractmethod, ABC
from typing import Generator
from catan.moves import *

from catan import game
from hexagons.hexagons import HexCoord, EdgeCoord


class Agent(ABC):
    @abstractmethod
    def play_turn(self, game: 'game.Game') -> Generator[Move, MoveResult, None]:
        pass

    @abstractmethod
    def would_accept_trade(self, game: 'game.Game', offering, wants):
        pass


class RandomAgent(Agent):
    def play_turn(self, game: 'game.Game') -> Generator[Move, MoveResult, None]:
        rand_tile = random.choice(list(game.board.tiles.keys()))
        rand_vertex = random.choice(list(rand_tile.vertices()))
        result = yield BuildSettlementMove(rand_vertex)

        rand_vertex = random.choice(list(rand_tile.vertices()))
        result = yield UpgradeSettlementMove(rand_vertex)

        rand_tile: HexCoord = random.choice(list(game.board.tiles.keys()))
        rand_edge: EdgeCoord = random.choice(list(rand_tile.edges()))
        result = yield BuildRoadMove(rand_edge)

        rand_resource_want = random.choice(list(Resource))
        rand_resource_offering = random.choice(list(Resource))

        result = yield ProposeTradeMove({rand_resource_offering: 1}, {rand_resource_want: 1})

        rand_resource_want = random.choice(list(Resource))
        rand_resource_offering = random.choice(list(Resource))
        result = yield ExchangeMove({rand_resource_offering: 4}, rand_resource_want)

    def would_accept_trade(self, game: 'game.Game', offering, wants):
        return random.choice([True, False])

