import math
import queue
from tkinter import *
import threading
import logging

from catan import board, game

from hexagons import hexagons

TILE_COLORS = {
    board.TileType.DESERT: '#a5a27d',
    board.TileType.MUD: '#9e6c1c',
    board.TileType.STONE: '#7589a8',
    board.TileType.WHEAT: '#8f9131',
    board.TileType.WOOD: '#273f0c',
    board.TileType.SHEEP: '#7fea67'
}

PLAYER_COLORS = {
    0: 'red',
    1: 'blue',
    2: 'green',
    3: 'orange',
    4: 'brown',
    5: 'white'
}


class App(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.board = BoardFrame(self)
        self.board.pack(side='bottom')

        self.turn_counter = Label(self)
        self.turn_counter.pack()

    def draw_game(self, game: game.Game):
        self.board.draw_board(game.board)
        self.turn_counter.configure(text=str(game.turn_number))

    def clear(self):
        self.board.clear()


class BoardFrame(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.canvas = Canvas(self, width=900, height=800)
        self.canvas.configure(background='white')
        self.canvas.pack()

        self.btn = Button(self, text='More Info', command=self.toggle_debug)
        self.btn.pack(side='left')

        self.tile_offset = (400, 400)
        self.tile_radius = 50
        self.debug = False

    def toggle_debug(self):
        self.debug = not self.debug

    def draw_hex_raw(self, center, radius, color='red'):
        xys = []
        for corner in hexagons.pixel_corners(center, radius):
            xys.append(corner[0])
            xys.append(corner[1])

        self.canvas.create_polygon(*xys, outline='gray', fill=color, width=4)

    def hex_pixel_coords(self, coords: hexagons.HexCoord):
        x = self.tile_radius * (math.sqrt(3) * coords.q + math.sqrt(3)/2 * coords.r) + self.tile_offset[0]
        y = self.tile_radius * (3.0 / 2 * coords.r) + self.tile_offset[1]
        return x, y

    def vertice_pixel_coords(self, vertice: hexagons.VertexCoord):
        return vertice.pos(self.hex_pixel_coords(vertice.tile), self.tile_radius)

    def draw_hex(self, pos, color=None):
        self.draw_hex_raw(pos, self.tile_radius, color=color)

    def draw_tile(self, tile: board.Tile):
        color = TILE_COLORS[tile.type]

        center_pos = self.hex_pixel_coords(tile.coords)

        self.draw_hex(
            center_pos,
            color=color)

        num_circle_radius = 15

        self.canvas.create_oval(
            center_pos[0] - num_circle_radius,
            center_pos[1] - num_circle_radius,
            center_pos[0] + num_circle_radius,
            center_pos[1] + num_circle_radius,
            fill='white',
            outline='gray'
        )

        self.canvas.create_text(center_pos[0], center_pos[1], text=str(tile.number))

        if self.debug:
            self.canvas.create_text(center_pos[0], center_pos[1] + 25, text=f'{tile.coords.q}, {tile.coords.r}')

    def draw_board(self, board: board.Board):
        for tile in board.tiles.values():
            self.draw_tile(tile)

        for settlement in board.settlements.values():
            self.draw_settlement(settlement)

        for road in board.roads.values():
            self.draw_road(road)

    def draw_settlement(self, settlement: board.Settlement):
        coords = self.vertice_pixel_coords(settlement.coords)

        if settlement.is_city:
            rectangle_size = 15
            self.canvas.create_rectangle(
                coords[0] - rectangle_size,
                coords[1] - rectangle_size,
                coords[0] + rectangle_size,
                coords[1] + rectangle_size,
                fill=PLAYER_COLORS[settlement.owner]
            )
        else:
            rectangle_size = 10
            self.canvas.create_rectangle(
                coords[0] - rectangle_size,
                coords[1] - rectangle_size,
                coords[0] + rectangle_size,
                coords[1] + rectangle_size,
                fill=PLAYER_COLORS[settlement.owner]
            )

    def draw_road(self, road: board.Road):
        [v1, v2] = road.coords.vertices()
        c1 = self.vertice_pixel_coords(v1)
        c2 = self.vertice_pixel_coords(v2)

        self.canvas.create_line(
            c1[0],
            c1[1],
            c2[0],
            c2[1],
            fill=PLAYER_COLORS[road.owner],
            width=5
        )

    def clear(self):
        self.canvas.delete(ALL)


def queue_thread_func(q: queue.Queue, app: Frame):
    logging.info('Starting GUI queue thread')
    while True:
        logging.debug('Showing board state')
        game = q.get(True)
        print(game)
        app.clear()

        app.draw_game(game)


def start(q: queue.Queue):
    root = Tk()
    # root.geometry('1000x500')
    app = App(master=root)
    queue_thread = threading.Thread(target=lambda: queue_thread_func(q, app), daemon=True)
    queue_thread.start()
    app.mainloop()
