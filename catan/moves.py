from dataclasses import dataclass
from typing import Any

from catan.board import IllegalMoveError
from catan.player import Player, NotEnoughResourcesError
from catan.resources import Resource
from hexagons.hexagons import VertexCoord
from catan import game, board


@dataclass
class MoveContext:
    game: 'game.Game'
    player_id: int

    def player(self) -> Player:
        return self.game.players[self.player_id]


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
        cost = {
            Resource.WOOD: 1,
            Resource.WHEAT: 1,
            Resource.MUD: 1,
            Resource.SHEEP: 1
        }

        try:
            ctx.player().hand.take_resources(cost)
            settlement = board.Settlement(ctx.player_id, self.vertex)
            ctx.game.board.add_settlement(settlement)

        except NotEnoughResourcesError as e:
            return MoveResult(False, e)
        except IllegalMoveError as e:
            return MoveResult(False, e)

        return MoveResult(True, None)



@dataclass
class MoveResult:
    successful: bool
    results: Any

