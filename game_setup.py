from game import *
import random
import hexagons


def random_tile_type() -> TileType:

    return random.choice(list(TileType))


def random_tile(coords) -> Tile:
    return Tile(coords, random_tile_type(), random.randint(1, 12))


def new_board():
    board = Board()
    # tile_places = [(x, y) for x in range(-3, 4) for y in range(-3, 4)]
    # tile_places = [
    #     (0, 0),
    #     (0, 1),
    #     (1, 0),
    #     # (1, 1),
    #     (0, -1),
    #     (-1, 0),
    #     # (-1, -1),
    #     (1, -1),
    #     (-1, 1)
    # ]

    tile_places = [(x, y) for x in range(-5, 6) for y in range(-5, 6) if hexagons.hex_distance((0,0), (x, y)) < 5]
    for place in tile_places:
        board.tiles[place] = random_tile(place)

    return board
