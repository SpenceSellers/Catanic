import math
from dataclasses import dataclass
from typing import Tuple, List, Iterable


@dataclass(eq=True, frozen=True)
class HexCoord:
    q: int
    r: int

    def shared_edge(self, other: 'HexCoord'):
        pass

    def adjacent(self) -> Iterable['HexCoord']:
        for i in range(6):
            yield self.through_side(i)

    def vertices(self) -> Iterable['VerticeCoord']:
        for i in range(6):
            yield VerticeCoord(self, i).normalize()

    def add(self, other: 'HexCoord'):
        return HexCoord(self.q + other.q, self.r + other.r)

    def through_side(self, side: int) -> 'HexCoord':
        return self.add(HEX_SIDE_OFFSETS[side])

    def edge(self, side: int) -> 'EdgeCoord':
        return EdgeCoord(self, side).normalize()


HEX_SIDE_OFFSETS = {
    0: HexCoord(1, 0),
    1: HexCoord(0, 1),
    2: HexCoord(-1, 1),
    3: HexCoord(-1, 0),
    4: HexCoord(0, -1),
    5: HexCoord(1, -1)
}


@dataclass(eq=True, frozen=True)
class VerticeCoord:
    tile: HexCoord
    vertice: int

    def pos(self, center: Tuple[float, float], radius: float) -> Tuple[float, float]:
        return pixel_corner(center, radius, self.vertice)

    def normalize(self) -> 'VerticeCoord':
        # When addressing vertices, a hex only "owns" corner 0 and 1, making each vertice unique.
        vertice = self.vertice % 6
        if vertice == 2:
            return VerticeCoord(self.tile.through_side(2), 0)
        elif vertice == 3:
            return VerticeCoord(self.tile.through_side(3), 1)
        elif vertice == 4:
            return VerticeCoord(self.tile.through_side(3), 0)
        elif vertice == 5:
            return VerticeCoord(self.tile.through_side(4), 1)
        else:
            return VerticeCoord(self.tile, vertice)

    def edges(self) -> List['EdgeCoord']:
        us = self.normalize()
        if us.vertice == 0:
            return [self.tile.edge(0), self.tile.edge(5), self.tile.through_side(0).edge(4)]
        elif us.vertice == 1:
            return [self.tile.edge(0), self.tile.edge(1), self.tile.through_side(0).edge(2)]


@dataclass(eq=True, frozen=True)
class EdgeCoord:
    tile: HexCoord
    edge: int

    def vertices(self) -> List[VerticeCoord]:
        return [
            VerticeCoord(self.tile, self.edge).normalize(),
            VerticeCoord(self.tile, self.edge + 1).normalize()
        ]

    def normalize(self) -> 'EdgeCoord':
        # When addressing edges, the hexagon only "owns" edges 0, 1, and 2.
        edge = self.edge % 6
        if edge == 3:
            return EdgeCoord(self.tile.through_side(3, 0))
        if edge == 4:
            return EdgeCoord(self.tile.through_side(4), 1)
        if edge == 5:
            return EdgeCoord(self.tile.through_side(5), 2)
        else:
            return EdgeCoord(self.tile, edge)


def hex_distance(coord_a: HexCoord, coord_b: HexCoord) -> int:
    a_q = coord_a[0]
    a_r = coord_a[1]
    b_q = coord_b[0]
    b_r = coord_b[1]
    return int((abs(a_q - b_q) + abs(a_q + a_r - b_q - b_r) + abs(a_r - b_r)) / 2)


def pixel_corners(center: Tuple[float, float], radius: float):
    for i in range(6):
        yield pixel_corner(center, radius, i)


def pixel_corner(center: Tuple[float, float], radius: float, corner: int):
    angle_deg = 60 * corner - 30
    angle_rad = (math.pi / 180) * angle_deg
    return center[0] + radius * math.cos(angle_rad), center[1] + radius * math.sin(angle_rad)
