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
from diplomacy.visualization.map import *


class Board:

    def __init__(self, map_dict: dict, interpreter='vanilla'):

        self.tiles = {}
        self.interpreter = interpreter
        if interpreter != 'vanilla':
            raise ModuleNotFoundError('No module found named {}'.format(interpreter))

        # Fill in initial tiles
        for tile in map_dict['tiles']:
            self.tiles[tile['id']] = Tile.create_from_dict(tile)

        self.__verify_tiles()
        print("Successfully verified map dict with", len(self.tiles), "entries.")

    def __verify_tiles(self):
        for tile in self.tiles.values():
            # Assert equivalent tiles have the same owner and supply center status
            if len(tile.equivalencies):
                for equiv_id in tile.equivalencies:
                    assert self.tiles[equiv_id].owner == tile.owner, \
                        'Mismatching owners for equivalent tiles, ids: {} and {}'.format(tile.id,
                                                                                         self.tiles[equiv_id].id)
                    assert self.tiles[equiv_id].is_supply_center == tile.is_supply_center, \
                        'Mismatching SC status for equivalent tiles, ids: {} and {}'.format(tile.id,
                                                                                            self.tiles[equiv_id].id)
                    if tile.unit is not None:
                        assert self.tiles[equiv_id].unit is None, \
                            'Two units on equivalent tiles, ids: {} and {}'.format(tile.id, self.tiles[equiv_id].id)
            if tile.unit is not None:
                assert tile.unit.owner is not None, 'Unit with no owner in tile: {}'.format(tile.id)
                if tile.is_coast:  # Coast or ocean
                    assert tile.unit.type == 'fleet', \
                        'Non-fleet found on coast, id: {}'.format(tile.id)

    def write_image(self, output_file):
        if self.interpreter == 'vanilla':
            for tile in self.tiles.values():
                if tile.owner is not None:
                    context(self.__get_vis_country_class(tile.owner))
                    shortname = tile.aliases['short_name']
                    if len(shortname) <= 3: # Prevent the north-coasts and south-coasts from erring
                        set(shortname)
                if tile.unit is not None:
                    context(self.__get_vis_country_class(tile.unit.owner))
                    if tile.unit.type == 'army':
                        army_hold(tile.aliases['short_name'])
                    elif tile.unit.type == 'fleet':
                        fleet_hold(tile.aliases['short_name'])
            done()

    def __get_vis_country_class(self, name):
        if name == 'England':
            return ENGLAND
        elif name == 'Italy':
            return ITALY
        elif name == 'France':
            return FRANCE
        elif name == 'Germany':
            return GERMANY
        elif name == 'Russia':
            return RUSSIA
        elif name == 'Austria':
            return AUSTRIA
        elif name == 'Turkey':
            return TURKEY
        else:
            raise AttributeError('Unknown country')

# TODO: Reimport pydip because you accidentally deleted the tests
# TODO: Add tests
# TODO: Add game information to the json/dict
