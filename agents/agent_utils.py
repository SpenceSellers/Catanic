from typing import Set

from catan.board import Board, Settlement, Road
from hexagons.hexagons import VertexCoord, EdgeCoord


def all_vertices(board: Board) -> Set[VertexCoord]:
    def all_vertices_with_dups():
        for tile in board.tiles.keys():
            yield from tile.vertices()

    return set(all_vertices_with_dups())


def all_edges(board: Board) -> Set[EdgeCoord]:
    def all_edges_with_dups():
        for tile in board.tiles.keys():
            yield from tile.edges()

    return set(all_edges_with_dups())


def vertices_where_settlement_can_be_built(board: Board, player_id: int) -> Set[VertexCoord]:
    return set(vertex for vertex in all_vertices(board) if board.can_build_settlement(Settlement(player_id, vertex)))


def edges_where_road_can_be_built(board: Board, player_id: int) -> Set[EdgeCoord]:
    return set(edge for edge in all_edges(board) if board.can_build_road(Road(player_id, edge)))

