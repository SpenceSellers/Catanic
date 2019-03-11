from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, Tuple

import hexagons as hex


class TileType(Enum):
    STONE = 'stone'
    MUD = 'mud'
    WOOD = 'wood'
    WHEAT = 'wheat'
    DESERT = 'desert'


@dataclass
class Tile:
    coords: hex.HexCoord
    type: TileType
    number: int


class Resource(Enum):
    STONE = auto()
    MUD = auto()
    WHEAT = auto()
    WOOD = auto()


@dataclass
class Settlement:
    owner: int
    coords: hex.VerticeCoord
    is_city: bool = False


@dataclass
class Road:
    owner: int
    coords: hex.EdgeCoord


class Board:
    tiles: Dict[hex.HexCoord, Tile]
    settlements: Dict[hex.VerticeCoord, Settlement]
    roads: Dict[hex.EdgeCoord, Road]

    def __init__(self):
        self.tiles = {}
        self.settlements = {}
        self.roads = {}

    def add_settlement(self, settlement: Settlement):
        self.settlements[settlement.coords] = settlement

    def add_road(self, road: Road):
        self.roads[road.coords] = road

    def __str__(self):
        return f'{self.tiles}'



