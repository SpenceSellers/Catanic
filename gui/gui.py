import math
import queue
from tkinter import *
import threading
import logging

from catan import board, game, player
from catan.player import ResourceSet, Resource

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

        self.control_panel = ControlPanel(self.command_queue, self)
        self.control_panel.grid(column=0, row=1)

        self.turn_counter = Label(self)
        self.turn_counter.grid(column=1, row=0)

        self.game_info = GameInfo(self)
        self.game_info.grid(column=2, row=1)

        self.update()

    def draw_game(self, game: game.Game):
        self.board.draw_board(game.board)
        self.game_info.update_game(game)
        self.turn_counter.configure(text=str(game.turn_number))

    def clear(self):
        self.board.clear()

    def update(self):
        game_to_draw = None
        try:
            # We've likely missed multiple queue updates
            while True:
                # We might be getting a lot of games to draw during this update, let's only draw it once.
                game_to_draw = self.game_queue.get_nowait()

        except queue.Empty:
            pass

        if game_to_draw:
            self.clear()
            self.draw_game(game_to_draw)

        self.after(100, self.update)


class ControlPanel(Frame):
    def __init__(self, command_queue: queue.Queue, master=None):
        super().__init__(master)
        self.master = master
        self.command_queue = command_queue

        self.btn = Button(self, text='Start', command=self.start)
        self.btn.pack(side='left')

    def start(self):
        self.command_queue.put(('start', None))


class GameInfo(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.player_widgets = []

    def update_game(self, game: game.Game):
        num_players = len(game.players)
        if len(self.player_widgets) != num_players:
            for i in range(num_players):
                player = PlayerInfo(self)
                player.pack()
                self.player_widgets.append(player)

        for i in range(num_players):
            game_player = game.players[i]
            widget = self.player_widgets[i]
            widget.update_player(game, game_player)


class PlayerInfo(Frame):
    def __init__(self, master=None):
        super().__init__(
            master,
            bd=2,
            relief=SUNKEN,
            pady=5
        )
        self.master = master

        self.name = Label(self, text='Player')
        self.name.pack()

        self.victory_points = Label(self)
        self.victory_points.pack()

        self.resources = ResourcesDisplay(self)
        self.resources.pack()

    def update_player(self, game: game.Game, player: player.Player):
        self.name.configure(text=f'Player {player.id}', fg=PLAYER_COLORS[player.id])

        vps = game.get_victory_points(player.id)
        self.victory_points.config(text=f'VPs: {vps}')

        self.resources.show(player.hand.resources)


class ResourcesDisplay(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.sheep_label = Label(self, text='Sheep')
        self.sheep_label.grid(column=0, row=0)

        self.stone_label = Label(self, text='Stone')
        self.stone_label.grid(column=0, row=1)

        self.wheat_label = Label(self, text='Wheat')
        self.wheat_label.grid(column=0, row=2)

        self.mud_label = Label(self, text='Mud')
        self.mud_label.grid(column=0, row=3)

        self.wood_label = Label(self, text='Wood')
        self.wood_label.grid(column=0, row=4)

        self.sheep = Label(self)
        self.sheep.grid(column=1, row=0)

        self.stone = Label(self)
        self.stone.grid(column=1, row=1)

        self.wheat = Label(self)
        self.wheat.grid(column=1, row=2)

        self.mud = Label(self)
        self.mud.grid(column=1, row=3)

        self.wood = Label(self)
        self.wood.grid(column=1, row=4)

    def show(self, resources: ResourceSet):
        self.sheep.config(text=str(resources.get(Resource.SHEEP, 0)))
        self.wheat.config(text=str(resources.get(Resource.WHEAT, 0)))
        self.stone.config(text=str(resources.get(Resource.STONE, 0)))
        self.mud.config(text=str(resources.get(Resource.MUD, 0)))
        self.wood.config(text=str(resources.get(Resource.WOOD, 0)))


class BoardFrame(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

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
