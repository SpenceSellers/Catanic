from hexagons import *
import pytest


class TestHexCoord:
    @pytest.mark.parametrize('coord, side, expected', [
        (HexCoord(0, 0), 0, HexCoord(1, 0)),
        (HexCoord(0, 0), 4, HexCoord(0, -1)),
        (HexCoord(1, 0), 3, HexCoord(0, 0)),
    ])
    def test_through_side(self, coord, side, expected):
        assert coord.through_side(side) == expected


class TestVerticeCoord:
    def test_normalize_wraps_vertex_number(self):
        result = VertexCoord(HexCoord(0, 0), 6).normalize()
        assert result.vertex == 0


class TestEdgeCoord:
    def test_normalize_swaps_to_correct_side(self):
        denorm = EdgeCoord(HexCoord(0, 0), 4)
        assert denorm.normalize() == EdgeCoord(HexCoord(0, -1), 1)

    @pytest.mark.parametrize('side', [0, 1])
    def test_normalize_keeps_normalized_sides(self, side):
        edge = EdgeCoord(HexCoord(100, 100), side)
        assert edge.normalize() == edge

    def test_normalize_wraps_edges(self):
        edge = EdgeCoord(HexCoord(100, 100), 13)
        assert edge.normalize().edge == 1

