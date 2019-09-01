from dataclasses import dataclass
from typing import Any
from abc import ABC, abstractmethod
import random

from catan.board import IllegalMoveError
from catan.player import Player, NotEnoughResourcesError
from catan.resources import Resource
from hexagons.hexagons import VertexCoord, EdgeCoord
from catan import game, board


@dataclass
class MoveContext:
    game: 'game.Game'
    player_id: int

    def player(self) -> Player:
        return self.game.players[self.player_id]


@dataclass
class MoveResult:
    successful: bool
    results: Any


class Move(ABC):
    """During their turn, Player agents interact with the state of the game through Move objects.

    A Move instance is responsible for:
    - Verifying that the move is legal
    - Interacting with the game state to effect the desired change
    - Reporting the result of that move, if any
    """

    def execute(self, ctx: MoveContext) -> MoveResult:
        validation = self.validate(ctx)
        if not validation.successful:
            return validation

        return self.perform(ctx)

    def validate(self, ctx: MoveContext) -> MoveResult:
        return MoveContext(True, None)

    @abstractmethod
    def perform(self, ctx: MoveContext):
        pass


class BuildSettlementMove(Move):
    cost = {
        Resource.WOOD: 1,
        Resource.WHEAT: 1,
        Resource.MUD: 1,
        Resource.SHEEP: 1
    }

    def __init__(self, vertex: VertexCoord):
        self.vertex = vertex

    def validate(self, ctx: MoveContext) -> MoveResult:
        if not ctx.player().hand.has_resources(self.cost):
            return MoveResult(False, "Not enough resources")

        settlement = board.Settlement(ctx.player_id, self.vertex)
        if not ctx.game.board.can_build_settlement(settlement):
            return MoveResult(False, "Cannot build settlement")

        return MoveResult(True, None)

    def perform(self, ctx: MoveContext) -> MoveResult:

        ctx.player().hand.take_resources(self.cost)
        settlement = board.Settlement(ctx.player_id, self.vertex)
        ctx.game.board.add_settlement(settlement)

        return MoveResult(True, None)


class BuildRoadMove(Move):
    cost = {
        Resource.WOOD: 1,
        Resource.MUD: 1,
    }

    def __init__(self, edge: EdgeCoord):
        self.edge = edge

    def validate(self, ctx: MoveContext) -> MoveResult:
        if not ctx.player().hand.has_resources(self.cost):
            return MoveResult(False, "Not enough resources")

        road = board.Road(ctx.player_id, self.edge)
        if not ctx.game.board.can_build_road(road):
            return MoveResult(False, "Cannot build road here")

        return MoveResult(True, None)

    def perform(self, ctx: MoveContext) -> MoveResult:
        ctx.player().hand.take_resources(self.cost)
        road = board.Road(ctx.player_id, self.edge)
        ctx.game.board.add_road(road)

        return MoveResult(True, None)


class ProposeTradeMove(Move):
    def __init__(self, offering, wants):
        self.offering = offering
        self.wants = wants

    def validate(self, ctx: MoveContext):
        if not ctx.player().hand.has_resources(self.offering):
            return MoveResult(False, "Does not have offered resources")
        return MoveResult(True, None)

    def perform(self, ctx: MoveContext) -> MoveResult:
        agent_items = list(ctx.game.agents.items())
        # Propose in a random order
        random.shuffle(agent_items)
        for player_id, agent in ctx.game.agents.items():
            player = ctx.game.players[player_id]
            if agent.would_accept_trade(ctx.game, self.offering, self.wants) and player.hand.has_resources(self.wants):
                player.hand.take_resources(self.wants)
                ctx.player().hand.add_resources(self.wants)
                player.hand.add_resources(self.offering)
                ctx.player().hand.take_resources(self.offering)
                return MoveResult(True, None)

        return MoveResult(False, "Nobody wanted to trade")

    def __str__(self):
        return f"Trade {self.wants} for {self.offering}"

        

