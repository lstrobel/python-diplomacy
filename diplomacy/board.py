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

    def __init__(self, map_dict: dict, interpreter='vanilla'):

        self.tiles = {}
        self.interpreter = interpreter
        if interpreter != 'vanilla':
            raise ModuleNotFoundError('No module found named {}'.format(interpreter))

        # Fill in initial tiles
        for tile in map_dict['tiles']:
            self.tiles[tile['id']] = Tile.from_dict(tile)

        self.__verify_tiles()
        print("Successfully verified map dict with", len(self.tiles), "entries.")

    def __verify_tiles(self):
        for tile in self.tiles.values():
            # Assert equivalent tiles have the same owner and supply center status
            if len(tile.equivalencies):
                for equiv_id in tile.equivalencies:
                    assert self.tiles[equiv_id].owner == tile.owner, 'Mismatching owners for equivalent tiles'
                    assert self.tiles[equiv_id].is_supply_center == tile.is_supply_center, \
                        'Mismatching supply center status for equivalent tiles'
                    if tile.unit is not None:
                        assert self.tiles[equiv_id] is None, 'Two units on equivalent tiles'
                        if (tile.is_coast) or ((not tile.is_coast) and (not len(tile.equivalencies))):  # Coast or ocean
                            assert tile.unit.type == 'fleet', 'Non-fleet found on coast or ocean'
                        else:  # Non-coast, non-ocean:
                            assert tile.unit.type == 'army', 'Non-army found on land'

    def write_image(self, output_file):
        if self.interpreter == 'vanilla':
            pass

# TODO: Reimport pydip because you accidentally deleted the tests
# TODO: Add tests
# TODO: Add interpreter differentiation
# TODO: Add game information to the json/dict
# TODO: Add game printing
