import math
from dataclasses import dataclass
from typing import Tuple, List

@dataclass(eq=True, frozen=True)
class HexCoord:
    q: int
    r: int


@dataclass(eq=True, frozen=True)
class VerticeCoord:
    tile: HexCoord
    vertice: int

    def pos(self, center: Tuple[float, float], radius: float) -> Tuple[float, float]:
        return pixel_corner(center, radius, self.vertice)

    def normalize(self) -> 'VerticeCoord':
        # TODO
        return VerticeCoord(self.tile, self.vertice % 6)

    def edges(self) -> List['EdgeCoord']:
        pass

    def touching_tiles(self) -> List[HexCoord]:
        pass



@dataclass(eq=True, frozen=True)
class EdgeCoord:
    tile: HexCoord
    edge: int

    def vertices(self) -> List[VerticeCoord]:
        return [
            VerticeCoord(self.tile, self.edge),
            VerticeCoord(self.tile, self.edge + 1)
        ]


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
