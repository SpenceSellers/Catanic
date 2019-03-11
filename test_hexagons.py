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
    def test_normalize_wraps_vertice_number(self):
        result = VertexCoord(HexCoord(0, 0), 6).normalize()
        assert result.vertex == 0

    def test_normalize_
