import math
from dataclasses import dataclass
from typing import Tuple, List, Iterable


@dataclass(eq=True, frozen=True)
class HexCoord:
    """Represents a the coordinates for a Hexagon in an infinitely tiling hexagon-space.

    "q" and "r" are close equivalents to "x" and "y", but unlike on the familiar cartesian plane,
    they are not perfectly orthogonal. Interpreted graphically, The "q" and "r" axes are
    60 degrees apart, instead of 90.

    This incredible guide from Red Blob Games was an invaluable reference for this.
    https://www.redblobgames.com/grids/hexagons/

    Negative q and r values are permitted.
    """
    q: int
    r: int

    def shared_edge(self, other: 'HexCoord'):
        pass

    def adjacent(self) -> Iterable['HexCoord']:
        """Provides the six hexagons that touch this hexagon"""
        for i in range(6):
            yield self.through_side(i)

    def vertices(self) -> Iterable['VertexCoord']:
        """Provides the six corners of this hexagon"""
        for i in range(6):
            yield VertexCoord(self, i).normalize()

    def add(self, other: 'HexCoord'):
        """Shifts these coordinates by the coordinates of another hexagon"""
        return HexCoord(self.q + other.q, self.r + other.r)

    def through_side(self, side: int) -> 'HexCoord':
        """Provides the hexagon on the "other side" of a given edge"""
        return self.add(HEX_SIDE_OFFSETS[side])

    def edge(self, side: int) -> 'EdgeCoord':
        """Provides the coordinates of a particular edge on this hexagon (shared with one other hexagon)"""
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
class VertexCoord:
    """Represents the coordinates of a single 'corner' of a hexagon in hexagon-space.

    Every vertex is shared by three hexagons. The VertexCoord can be normalized to
    decide which hexagon it "belongs" to for the purposes of identification."""
    tile: HexCoord
    vertex: int

    def pos(self, center: Tuple[float, float], radius: float) -> Tuple[float, float]:
        return pixel_corner(center, radius, self.vertex)

    def normalize(self) -> 'VertexCoord':
        """Converts a possibly non-normalized VerrtexCoord to a singular, comparable, normalized form.

        When addressing vertices, a hex only "owns" corner 0 and 1.
        This is because a hexagon has six vertices, but each vertex is shared by three hexagons. 6 / 3 = 2 unique
        vertices per hexagon.
        """

        vertex = self.vertex % 6
        if vertex == 2:
            return VertexCoord(self.tile.through_side(2), 0)
        elif vertex == 3:
            return VertexCoord(self.tile.through_side(3), 1)
        elif vertex == 4:
            return VertexCoord(self.tile.through_side(3), 0)
        elif vertex == 5:
            return VertexCoord(self.tile.through_side(4), 1)
        else:
            return VertexCoord(self.tile, vertex)

    def edges(self) -> List['EdgeCoord']:
        """Provides the three edges that lead away from this corner"""
        us = self.normalize()
        if us.vertex == 0:
            return [
                us.tile.edge(0),
                us.tile.edge(5),
                us.tile.through_side(0).edge(4)
            ]
        elif us.vertex == 1:
            return [
                us.tile.edge(0),
                us.tile.edge(1),
                us.tile.through_side(0).edge(2)
            ]


@dataclass(eq=True, frozen=True)
class EdgeCoord:
    """Represents the coordinates of a single 'edge' of a hexagon in hexagon-space.

    Each edge belongs to two hexagons. An EdgeCoord can be normalized to decide which of the two hexagons
    it "belongs" to for the purposes of identification.
    """
    tile: HexCoord
    edge: int

    def vertices(self) -> List[VertexCoord]:
        """Provides the two vertices that are on either end of this edge."""
        return [
            VertexCoord(self.tile, self.edge).normalize(),
            VertexCoord(self.tile, self.edge + 1).normalize()
        ]

    def swap_side(self) -> 'EdgeCoord':
        """Provides a (likely denormalized) alternative view of the edge which "belongs" to the hexagon on the other
        side of the edge."""

        opposite_side = (self.edge + 3) % 6
        return EdgeCoord(self.tile.through_side(self.edge), opposite_side)

    def normalize(self) -> 'EdgeCoord':
        """Converts a possibly non-normalized EdgeCoord into a singular, comparable normalized form.

        When addressing edges, the hexagon only "owns" edges 0, 1, and 2. This is because a hexagon has six edges and
        every edge is shared by two hexagons. 6 / 2 = 3 unique edges per hexagon"""
        edge = self.edge % 6
        owned_edges = [0, 1, 2]
        if edge in owned_edges:
            return EdgeCoord(self.tile, edge)
        else:
            return EdgeCoord(self.tile, edge).swap_side()

    def between_hexes(self) -> List[HexCoord]:
        return [self.tile, self.swap_side().tile]



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
