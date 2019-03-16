import random
from abc import abstractmethod, ABC
from typing import Generator
from catan.moves import *

from catan import game


class Agent(ABC):
    @abstractmethod
    def play_turn(self, game: 'game.Game') -> Generator[Move, MoveResult, None]:
        pass


class RandomAgent(Agent):
    def play_turn(self, game: 'game.Game') -> Generator[Move, MoveResult, None]:
        rand_tile = random.choice(list(game.board.tiles.keys()))
        rand_vertex = random.choice(list(rand_tile.vertices()))
        result = yield BuildSettlementMove(rand_vertex)
