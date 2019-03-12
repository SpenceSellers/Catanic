from resources import Resource


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
            Resource.WOOD: 0
        }

    def add_resource(self, resource: Resource, quantity: int = 1):
        self.resources[resource] += quantity
