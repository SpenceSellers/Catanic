from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional

from hexagons import hexagons as hex
from catan.resources import Resource


class TileType(Enum):
    STONE = 'stone'
    MUD = 'mud'
    WOOD = 'wood'
    WHEAT = 'wheat'
    DESERT = 'desert'

    def resource(self) -> Optional[Resource]:
        if self == TileType.MUD:
            return Resource.MUD
        elif self == TileType.STONE:
            return Resource.STONE
        elif self == TileType.WHEAT:
            return Resource.WHEAT
        elif self == TileType.WOOD:
            return Resource.WOOD
        return None


@dataclass
class Tile:
    coords: hex.HexCoord
    type: TileType
    number: int


@dataclass
class Settlement:
    owner: int
    coords: hex.VertexCoord
    is_city: bool = False


@dataclass
class Road:
    owner: int
    coords: hex.EdgeCoord


class Board:
    tiles: Dict[hex.HexCoord, Tile]
    settlements: Dict[hex.VertexCoord, Settlement]
    roads: Dict[hex.EdgeCoord, Road]

    def __init__(self):
        self.tiles = {}
        self.settlements = {}
        self.roads = {}

    def is_land(self, coord: hex.HexCoord) -> bool:
        return coord in self.tiles

    def add_settlement(self, settlement: Settlement) -> None:
        if not self.can_build_settlement(settlement):
            raise IllegalMoveError('Cannot build a settlement here')

        self.settlements[settlement.coords] = settlement

    def can_build_settlement(self, settlement: Settlement):
        if settlement.coords in self.settlements:
            return False

        # Cannot place a settlement on the end of an enemy road
        if any(edge in self.roads and self.roads[edge].owner != settlement.owner for edge in settlement.coords.edges()):
            return False

        # Cannot place a settlement one space away from another settlement
        nearby_vertices = (
            vertex
            for edge in settlement.coords.edges()
            for vertex in edge.vertices()
            if vertex != settlement.coords
        )
        if any(vertex in self.settlements for vertex in nearby_vertices):
            return False

        return True

    def add_road(self, road: Road):
        if not self.can_build_road(road):
            raise IllegalMoveError('Cannot build a road here')

        self.roads[road.coords] = road

    def can_build_road(self, road: Road):
        if road.coords in self.roads:
            return False

        # Cannot build a road that doesn't have land on at least one side
        adjacent_hexes = road.coords.between_hexes()
        if not any(self.is_land(hex) for hex in adjacent_hexes):
            return False

        # Cannot build a road that touches an enemy settlement
        vertices = road.coords.vertices()
        if any(vertex in self.settlements and self.settlements[vertex].owner != road.owner for vertex in vertices):
            return False

        return True

    def __str__(self):
        return f'{self.tiles}'


class IllegalMoveError(Exception):
    pass



