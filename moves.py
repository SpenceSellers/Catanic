from dataclasses import dataclass

from hexagons import VertexCoord
import game
import board

@dataclass
class MoveContext:
    game: 'game.Game'
    player_id: int

class Move:
    def execute(self):
        pass

@dataclass
class BuildSettlementMove(Move):
    vertex: VertexCoord

    def execute(self, ctx: MoveContext):
        settlement = board.Settlement(ctx.player_id, self.vertex)
        ctx.game.board.add_settlement(settlement)


class MoveResult:
    pass


class SuccessfulMoveResult(MoveResult):
    pass


class FailedMoveResult(MoveResult):
    pass
