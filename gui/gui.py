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
    def __init__(self, game_queue: queue.Queue, command_queue: queue.Queue, master=None):
        super().__init__(master)
        self.master = master
        self.game_queue = game_queue
        self.command_queue = command_queue;
        self.pack(fill=BOTH, expand=True)

        self.columnconfigure(1, weight=1)
        self.columnconfigure(0, pad=10)
        self.rowconfigure(0, pad=10)
        self.rowconfigure(1, weight=1)

        self.board = BoardFrame(self)
        self.board.grid(column=1, row=1)

        self.control_panel = ControlPanel(self)
        self.control_panel.grid(column=0, row=1)

        self.turn_counter = Label(self)
        self.turn_counter.grid(column=1, row=0)

        self.update()

    def draw_game(self, game: game.Game):
        self.board.draw_board(game.board)
        self.turn_counter.configure(text=str(game.turn_number))

    def clear(self):
        self.board.clear()

    def update(self):
        game_to_draw = None
        try:
            while True:
                game_to_draw = self.game_queue.get_nowait()

        except queue.Empty:
            pass

        if game_to_draw:
            self.clear()
            self.draw_game(game_to_draw)
            print('Drew game')

        self.after(100, self.update)


class ControlPanel(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        # self.pack()

        self.btn = Button(self, text='Start', command=self.start)
        self.btn.pack(side='left')

    def start(self):
        print('Starting')


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

    def vertex_pixel_coords(self, vertex: hexagons.VertexCoord):
        return vertex.pos(self.hex_pixel_coords(vertex.tile), self.tile_radius)

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
        coords = self.vertex_pixel_coords(settlement.coords)

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
        c1 = self.vertex_pixel_coords(v1)
        c2 = self.vertex_pixel_coords(v2)

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


def start(game_queue: queue.Queue, command_queue: queue.Queue):
    root = Tk()
    root.geometry('1800x1000')
    app = App(game_queue, command_queue, master=root)
    app.mainloop()
