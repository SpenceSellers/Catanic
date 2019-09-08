from attr import dataclass

from catan.moves import Move


@dataclass
class GameUpdateEvent:
    game: 'game.Game'


@dataclass
class RollEvent:
    player_id: int
    roll: int


@dataclass
class PlayedMoveEvent:
    player_id: int
    move: Move
