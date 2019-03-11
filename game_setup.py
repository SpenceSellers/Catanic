from game import *
import random
import hexagons



def random_tile_type() -> TileType:
    return random.choice(list(TileType))


def random_tile(coords) -> Tile:
    return Tile(coords, random_tile_type(), random.randint(1, 12))


def random_vertice(coords) -> hexagons.VerticeCoord:
    tile = random.choice(coords)
    return hexagons.VerticeCoord(tile, random.randint(0, 6)).normalize()


def new_board():
    board = Board()

    tile_places = [(x, y) for x in range(-5, 6) for y in range(-5, 6) if hexagons.hex_distance((0,0), (x, y)) < 5]
    for place in tile_places:
        board.tiles[place] = random_tile(place)

    return board

def new_board_started():
    board = new_board()
    tiles = list(board.tiles.keys())
    for player in range(2):
        board.add_settlement(Settlement(player, random_vertice(tiles)))

    return board
