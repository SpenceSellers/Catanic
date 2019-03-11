import math
from tkinter import *
import game
import multiprocessing

import hexagons

TILE_COLORS = {
    game.TileType.DESERT: '#a5a27d',
    game.TileType.MUD: '#9e6c1c',
    game.TileType.STONE: '#7589a8',
    game.TileType.WHEAT: '#8f9131',
    game.TileType.WOOD: '#273f0c'
}

PLAYER_COLORS = {
    0: 'red',
    1: 'blue',
    2: 'green',
    3: 'brown',
    4: 'orange',
    5: 'white'
}

class App(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.canvas = Canvas(self, width=900, height=800)
        self.canvas.configure(background='white')
        self.canvas.pack()

        self.btn = Button(self, text='U sux')
        self.btn.pack(side='left')

        self.tile_offset = (400, 400)
        self.tile_radius = 50
        self.show_coordinates = False

    def draw_hex_raw(self, center, radius, color='red'):
        xys = []
        for corner in hexagons.pixel_corners(center, radius):
            xys.append(corner[0])
            xys.append(corner[1])

        self.canvas.create_polygon(*xys, outline='gray', fill=color, width=4)

    def hex_pixel_coords(self, coords):
        x = self.tile_radius * (math.sqrt(3) * coords[0] + math.sqrt(3)/2 * coords[1]) + self.tile_offset[0]
        y = self.tile_radius * (3.0 / 2 * coords[1]) + self.tile_offset[1]
        return x, y

    def vertice_pixel_coords(self, vertice: hexagons.VerticeCoord):
        return vertice.pos(self.hex_pixel_coords(vertice.tile), self.tile_radius)

    def draw_hex(self, pos, color=None):
        self.draw_hex_raw(pos, self.tile_radius, color=color)

    def draw_tile(self, tile: game.Tile):
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

        if self.show_coordinates:
            self.canvas.create_text(center_pos[0], center_pos[1] + 25, text=str(tile.coords))

    def draw_board(self, board: game.Board):
        for tile in board.tiles.values():
            self.draw_tile(tile)

        for settlement in board.settlements.values():
            self.draw_settlement(settlement)

        for road in board.roads.values():
            self.draw_road(road)

    def draw_settlement(self, settlement: game.Settlement):
        coords = self.vertice_pixel_coords(settlement.coords)

        rectangle_size = 10
        self.canvas.create_rectangle(
            coords[0] - rectangle_size,
            coords[1] - rectangle_size,
            coords[0] + rectangle_size,
            coords[1] + rectangle_size,
            fill=PLAYER_COLORS[settlement.owner]
        )

    def draw_road(self, road: game.Road):
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




def start(board: game.Board):
    root = Tk()
    # root.geometry('1000x500')
    app = App(master=root)
    app.draw_board(board)
    app.mainloop()
