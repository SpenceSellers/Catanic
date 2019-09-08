import queue
from tkinter import *

import game_events
from catan import game, player
from catan.player import ResourceSet, Resource
from gui.board import BoardFrame
from gui.colors import PLAYER_COLORS
from gui.event_message_builder import EventMessageBuilder


class App(Frame):
    def __init__(self, game_queue: queue.Queue, command_queue: queue.Queue, master=None):
        super().__init__(master)
        self.master = master
        self.game_queue = game_queue
        self.command_queue = command_queue
        self.pack(fill=BOTH, expand=True)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=3)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        self.board = BoardFrame(self)
        self.board.grid(column=1, row=1, sticky=W+E+N+S)

        self.control_panel = ControlPanel(self.command_queue, self)
        self.control_panel.grid(column=0, row=1, sticky=W+E+N+S)

        self.turn_counter = Label(self)
        self.turn_counter.grid(column=1, row=0)

        self.game_info = GameInfo(self)
        self.game_info.grid(column=2, row=1, sticky=W+E+N+S)

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
                event = self.game_queue.get_nowait()
                if isinstance(event, game_events.GameUpdateEvent):
                    game_to_draw = event.game

                self.game_info.show_event(event)

        except queue.Empty:
            pass

        if game_to_draw:
            self.clear()
            self.draw_game(game_to_draw)

        self.after(50, self.update)


class ControlPanel(Frame):
    def __init__(self, command_queue: queue.Queue, master=None):
        super().__init__(master)
        self.master = master
        self.command_queue = command_queue

        self.start = Button(self, text='Start', command=self.start)
        self.start.pack(fill=X)

        self.play = Button(self, text='Play', command=self.play)
        self.play.pack(fill=X)

        self.pause = Button(self, text='Pause', command=self.pause)
        self.pause.pack(fill=X)

        self.step = Button(self, text='Step', command=self.step)
        self.step.pack(fill=X)

    def start(self):
        self.command_queue.put(('start', None))

    def play(self):
        self.command_queue.put(('play', None))

    def pause(self):
        self.command_queue.put(('pause', None))

    def step(self):
        self.command_queue.put(('step', None))


class GameInfo(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.player_widgets = []

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.players_frame = Frame(self)
        self.players_frame.grid(column=1, row=0, sticky=W+E+N+S)

        self.messages = Text(self, state=DISABLED)
        self.messages.grid(column=0, row=0, sticky=W+E+N+S)

        for player_id, color in PLAYER_COLORS.items():
            self.messages.tag_configure('player_' + str(player_id), foreground=color)

    def update_game(self, game: game.Game):
        num_players = len(game.players)
        if len(self.player_widgets) != num_players:
            for i in range(num_players):
                player = PlayerInfo(self.players_frame)
                player.pack(fill=X)
                self.player_widgets.append(player)

        for i in range(num_players):
            game_player = game.players[i]
            widget = self.player_widgets[i]
            widget.update_player(game, game_player)

    def build_message(self) -> EventMessageBuilder:
        return EventMessageBuilder(self.messages)

    def show_event(self, event):
        if isinstance(event, game_events.RollEvent):
            self.build_message().player(event.player_id).text(f' rolled {event.roll}').insert()
        elif isinstance(event, game_events.PlayedMoveEvent):
            self.build_message().player(event.player_id).text(f' {event.move}').insert()


class PlayerInfo(Frame):
    def __init__(self, master=None):
        super().__init__(
            master,
            bd=2,
            relief=SUNKEN,
            pady=5,
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


def start(game_queue: queue.Queue, command_queue: queue.Queue):
    root = Tk()
    root.geometry('1800x1000')
    app = App(game_queue, command_queue, master=root)
    app.mainloop()
