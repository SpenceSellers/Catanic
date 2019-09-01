from typing import Dict

from catan.resources import Resource


class Player:
    def __init__(self, id: int):
        self.id = id
        self.hand = Hand()


class Hand:
    def __init__(self):
        self.resources = {
            Resource.WHEAT: 0,
            Resource.STONE: 0,
            Resource.MUD: 0,
            Resource.WOOD: 0,
            Resource.SHEEP: 0
        }

    def add_resource(self, resource: Resource, quantity: int = 1):
        self.resources[resource] += quantity

    def add_resources(self, resources: Dict[Resource, int]):
        for resource, quantity in resources.items():
            self.add_resource(resource, quantity)

    def take_resources(self, demanded_resources: Dict[Resource, int]) -> None:
        if self.has_resources(demanded_resources):
            for resource, quantity in demanded_resources.items():
                self.resources[resource] -= quantity
        else:
            raise NotEnoughResourcesError()

    def has_resources(self, resources: Dict[Resource, int]) -> bool:
        for resource, quantity in resources.items():
            if self.resources[resource] < quantity:
                return False
        return True


class NotEnoughResourcesError(Exception):
    def __init__(self):
        super().__init__("Not enough resources")

