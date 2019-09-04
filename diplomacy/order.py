class Order:

    def __init__(self, player, source_tile, type="hold", destination_tile=None, target_tile=None):
        """

        :param source_tile: The tile with the unit to order
        :param destination_tile: The tile that the unit will go to -
                                    or, in the case of supports, the tile that the other unit will go to
        :param target_tile: The tile that has the unit to be supported (if this is a support order)
        :param type: The type of move
        """
        self.player = player
        self.source_tile = source_tile
        self.destination_tile = destination_tile
        self.target_tile = target_tile
        self.type = type
