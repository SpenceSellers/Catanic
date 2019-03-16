from dataclasses import dataclass
from typing import Any

from hexagons.hexagons import VertexCoord
from catan import game, board


@dataclass
class MoveContext:
    game: 'game.Game'
    player_id: int


class Move:
    """During their turn, Player agents interact with the state of the game through Move objects.

    A Move instance is responsible for:
    - Verifying that the move is legal
    - Interacting with the game state to effect the desired change
    - Reporting the result of that move, if any
    """

    def execute(self, ctx: MoveContext):
        pass


@dataclass
class BuildSettlementMove(Move):
    vertex: VertexCoord

    def execute(self, ctx: MoveContext):
        settlement = board.Settlement(ctx.player_id, self.vertex)
        try:
            ctx.game.board.add_settlement(settlement)
            return MoveResult(True, None)
        except board.IllegalMoveError as e:
            return MoveResult(False, e)


@dataclass
class MoveResult:
    successful: bool
    results: Any

