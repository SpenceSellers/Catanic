from typing import Set

from catan.board import Board, Settlement
from hexagons.hexagons import VertexCoord


def all_vertices(board: Board) -> Set[VertexCoord]:
    def all_vertices_with_dups():
        for tile in board.tiles.keys():
            yield from tile.vertices()

    return set(all_vertices_with_dups())


def vertices_where_settlement_can_be_built(board: Board, player_id: int) -> Set[VertexCoord]:
    return set(vertex for vertex in all_vertices(board) if board.can_build_settlement(Settlement(player_id, vertex)))

