from dataclasses import dataclass

from hexagons import VertexCoord


class Move:
    pass

@dataclass
class BuildSettlementMove(Move):
    vertex: VertexCoord


class MoveResult:
    pass


class SuccessfulMoveResult(MoveResult):
    pass


class FailedMoveResult(MoveResult):
    pass
