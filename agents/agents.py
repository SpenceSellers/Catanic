import random
from abc import abstractmethod, ABC
from typing import Generator
from catan.moves import *

from catan import game
from hexagons.hexagons import HexCoord, EdgeCoord
from agents import agent_utils


class Agent(ABC):
    player_id: int
    game: 'game.Game'

    @abstractmethod
    def play_turn(self) -> Generator[Move, MoveResult, None]:
        pass

    @abstractmethod
    def would_accept_trade(self, offering, wants):
        pass

    def join_game(self, game, player_id):
        self.game = game
        self.player_id = player_id

    @property
    def player(self):
        return self.game.players[self.player_id]


class RandomAgent(Agent):
    def play_turn(self) -> Generator[Move, MoveResult, None]:
        rand_tile = random.choice(list(self.game.board.tiles.keys()))
        rand_vertex = random.choice(list(rand_tile.vertices()))
        result = yield BuildSettlementMove(rand_vertex)

        rand_vertex = random.choice(list(rand_tile.vertices()))
        result = yield UpgradeSettlementMove(rand_vertex)

        rand_tile: HexCoord = random.choice(list(self.game.board.tiles.keys()))
        rand_edge: EdgeCoord = random.choice(list(rand_tile.edges()))
        result = yield BuildRoadMove(rand_edge)

        rand_resource_want = random.choice(list(Resource))
        rand_resource_offering = random.choice(list(Resource))

        result = yield ProposeTradeMove({rand_resource_offering: 1}, {rand_resource_want: 1})

        rand_resource_want = random.choice(list(Resource))
        rand_resource_offering = random.choice(list(Resource))
        result = yield ExchangeMove({rand_resource_offering: 4}, rand_resource_want)

    def would_accept_trade(self, offering, wants):
        return random.choice([True, False])


class InformedRandomAgent(Agent):
    def play_turn(self) -> Generator[Move, MoveResult, None]:
        if self.player.hand.has_resources(BuildSettlementMove.cost):
            buildable_settlements = agent_utils.vertices_where_settlement_can_be_built(self.game.board, self.player_id)
            if len(buildable_settlements):
                yield BuildSettlementMove(
                    random.choice(list(buildable_settlements))
                )

        if self.player.hand.has_resources(UpgradeSettlementMove.cost):
            upgradable_settlements = [
                settlement.coords for settlement in self.game.board.settlements.values()
                if settlement.owner == self.player_id
                   and not settlement.is_city
            ]

            if len(upgradable_settlements):
                yield UpgradeSettlementMove(random.choice(upgradable_settlements))

        rand_tile: HexCoord = random.choice(list(self.game.board.tiles.keys()))
        rand_edge: EdgeCoord = random.choice(list(rand_tile.edges()))
        yield BuildRoadMove(rand_edge)

        rand_resource_want = random.choice(list(Resource))
        rand_resource_offering = random.choice(list(Resource))

        yield ProposeTradeMove({rand_resource_offering: 1}, {rand_resource_want: 1})

        rand_resource_want = random.choice(list(Resource))
        rand_resource_offering = random.choice(list(Resource))
        yield ExchangeMove({rand_resource_offering: 4}, rand_resource_want)

    def would_accept_trade(self, offering, wants):
        return random.choice([True, False])
