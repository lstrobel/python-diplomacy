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
import random

from diplomacy.tile import Tile
from diplomacy.visualization.map import *


class Board:

    def __init__(self, map_dict: dict, interpreter='vanilla'):

        if interpreter != 'vanilla':
            raise ModuleNotFoundError('No module found named {}'.format(interpreter))

        self.tiles = {}
        self.interpreter = interpreter
        self.players = set()

        # Fill in initial tiles
        for tile in map_dict['tiles']:
            self.tiles[tile['id']] = Tile.create_from_dict(tile)
            if tile['owner'] is not None:
                self.players.add(tile['owner'])

        self.__verify_tiles()
        print(
            "Successfully verified map dict with {} entries and {} players.".format(len(self.tiles), len(self.players)))

    def __verify_tiles(self):
        """Assert that the tiles are in a valid game state - DOESNT HAVE FULL COVERAGE!"""
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
                assert tile.unit.owner in self.players, 'Unit found with unregistered player in tile {}'.format(tile.id)
                if tile.is_coast or tile.is_ocean:
                    assert tile.unit.type == 'fleet', \
                        'Non-fleet found on coast or ocean, id: {}'.format(tile.id)
                else:
                    assert tile.unit.type == 'army', \
                        'Non-army found on land, id: {}'.format(tile.id)

    def write_image(self, output_dir):  # TODO: Finish this so that you can decide the output file
        """Write the board as an image to the specified location"""
        if self.interpreter == 'vanilla':
            for tile in self.tiles.values():
                if tile.owner is not None:
                    context(self.__get_vis_country_class(tile.owner))
                    shortname = tile.aliases['short_name']
                    if len(shortname) <= 3 and (not tile.is_ocean):  # Prevent setting tiles that can't change color
                        set_(shortname)
                if tile.unit is not None:
                    context(self.__get_vis_country_class(tile.unit.owner))
                    if tile.unit.type == 'army':
                        army_hold(tile.aliases['short_name'])
                    elif tile.unit.type == 'fleet':
                        fleet_hold(tile.aliases['short_name'])
            done()

    @staticmethod
    def __get_vis_country_class(name):
        """Return the map-object corresponding to the vanilla country passed"""
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

    def scramble_board(self):
        """Completely shuffle the owners and units on each tile.
            Maintains the number and type of units on the board.
            Does not maintain the number of supply centers. (yet)
            The board must have nonzero players"""
        if len(self.players):
            army_list = []
            fleet_list = []
            for tile in self.tiles.values():
                tile.owner = random.choice(tuple(self.players))
                if tile.unit is not None:
                    if tile.unit.type == 'army':
                        army_list.append(tile.unit)
                    else:
                        fleet_list.append(tile.unit)
                    tile.unit = None
            tiles = list(self.tiles.values())
            while len(army_list) or len(fleet_list):
                tile = random.choice(tiles)
                if tile.unit is None:
                    if (tile.is_ocean or tile.is_coast) and len(fleet_list):
                        tile.unit = fleet_list.pop()
                    elif not (tile.is_ocean or tile.is_coast) and len(army_list):
                        tile.unit = army_list.pop()
        else:
            raise NotImplementedError("Can't shuffle a board with no players")

# TODO: Reimport pydip because you accidentally deleted the tests
# TODO: Add tests
# TODO: Add game information to the json/dict
