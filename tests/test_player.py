import pytest
from catan.player import *


class TestPlayerHand:
    def test_adding_single_resource_types(self):
        hand = Hand()
        hand.add_resource(Resource.SHEEP, 1)
        hand.add_resource(Resource.WOOD, 5)
        hand.add_resource(Resource.SHEEP, 2)

        assert hand.resources[Resource.SHEEP] == 3
        assert hand.resources[Resource.STONE] == 0
        assert hand.resources[Resource.WOOD] == 5

    def test_adding_resource_defaults_to_quantity_of_one(self):
        hand = Hand()

    def test_removing_resources(self):
        hand = Hand()
        hand.add_resource(Resource.STONE, 5)
        hand.take_resources({Resource.STONE: 2})
        assert hand.resources[Resource.STONE] == 3

    def test_removing_too_many_resources(self):
        hand = Hand()
        with pytest.raises(NotEnoughResourcesError):
            hand.add_resource(Resource.SHEEP, 5)
            hand.take_resources({Resource.SHEEP: 10})

        # It shouldn't have affected the values
        assert hand.resources[Resource.SHEEP] == 5, "Since it failed, the values should not have been affected"

    def test_has_resources(self):
        hand = Hand()
        hand.add_resources({
            Resource.SHEEP: 5,
            Resource.MUD: 5
        })

        assert hand.has_resources({Resource.MUD: 5})
        assert hand.has_resources({Resource.MUD: 2, Resource.SHEEP: 2})
        assert not hand.has_resources({Resource.MUD: 2, Resource.SHEEP: 20})
