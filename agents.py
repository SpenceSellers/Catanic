import random
from abc import abstractmethod, ABC
from typing import Generator
from moves import *

import game


class Agent(ABC):
    @abstractmethod
    def do_moves(self, game: 'game.Game') -> Generator[Move, MoveResult, None]:
        pass


class RandomAgent(Agent):
    def do_moves(self, game: 'game.Game') -> Generator[Move, MoveResult, None]:
        rand_tile = random.choice(list(game.board.tiles.keys()))
        rand_vertex = random.choice(list(rand_tile.vertices()))
        r1 = yield BuildSettlementMove(rand_vertex)
        result = yield
