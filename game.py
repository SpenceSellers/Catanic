from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, Tuple


class TileType(Enum):
    STONE = 'stone'
    MUD = 'mud'
    WOOD = 'wood'
    WHEAT = 'wheat'
    DESERT = 'desert'


@dataclass
class Tile:
    coords: Tuple[int, int]
    type: TileType
    number: int


class Resource(Enum):
    STONE = auto()
    MUD = auto()
    WHEAT = auto()
    WOOD = auto()


class Board:
    tiles: Dict[Tuple[int, int], Tile]

    def __init__(self):
        self.tiles = {}

    def __str__(self):
        return f'{self.tiles}'



