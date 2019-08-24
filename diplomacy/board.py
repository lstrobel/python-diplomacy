#  python-diplomacy is a tool for exploring the game diplomacy in python.
#  Copyright (C) 2019 Lukas Strobel
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

from diplomacy.tile import Tile


class Board():

    def __init__(self, map_dict: dict):

        self.tiles = {}

        # Fill in initial tiles
        for tile in map_dict['tiles']:
            self.tiles[tile['id']] = Tile.from_dict(tile)

        self.__verify_tiles()

    def __verify_tiles(self):
        for tile in self.tiles.values():
            # Assert equivalent tiles have the same owner and supply center status
            if len(tile.equivalencies) > 0:
                for equiv_id in tile.equivalencies:
                    assert self.tiles[equiv_id].owner == tile.owner, 'Mismatching owners for equivalent tiles'
                    assert self.tiles[equiv_id].is_supply_center == tile.is_supply_center, \
                        'Mismatching supply center status for equivalent tiles'

# TODO: Add units in vanilla_1914.json
# TODO: Reimport pydip because you accidentally deleted the tests
# TODO: Add tests