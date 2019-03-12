from game import *
import random
import hexagons



def random_tile_type() -> TileType:
    return random.choice(list(TileType))


def random_tile(coords) -> Tile:
    return Tile(coords, random_tile_type(), random.randint(1, 12))


def random_vertice(coords) -> hexagons.VertexCoord:
    tile = random.choice(coords)
    return hexagons.VertexCoord(tile, random.randint(0, 6)).normalize()


def new_board():
    board = Board()

    tile_places = [hexagons.HexCoord(x, y) for x in range(-4, 5) for y in range(-5, 5) if hexagons.hex_distance((0, 0), (x, y)) < 4]
    for place in tile_places:
        board.tiles[place] = random_tile(place)

    return board


def new_board_started():
    board = new_board()
    tiles = list(board.tiles.keys())
    for player in range(4):
        settlement = Settlement(player, random_vertice(tiles))
        board.add_settlement(settlement)

        vertex = settlement.coords
        for _ in range(7):
            try:
                edge = random.choice(vertex.edges())
                road = Road(player, edge)
                board.add_road(road)
            except IllegalMoveError:
                continue
            vertex = random.choice(edge.vertices())

    return board
