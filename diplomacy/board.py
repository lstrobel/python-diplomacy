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
from diplomacy.adjudication.pydip.test import TurnHelper, PlayerHelper
from diplomacy.adjudication.pydip_connector import create_pydip_map, convert_order_to_pydip_commandhelper, \
    unit_type_to_str
from diplomacy.order import Order
from diplomacy.tile import Tile
from diplomacy.unit import Unit
from diplomacy.visualization.map import *


class Board:

    def __init__(self, map_dict: dict, interpreter='vanilla'):

        if interpreter != 'vanilla':
            raise ModuleNotFoundError('No interpreter found named {}'.format(interpreter))

        # Passed properties
        self.interpreter = interpreter
        self.players = {player_name for player_name in map_dict['players']}
        self.year = map_dict['year']
        self.season = map_dict['season']
        self.phase = map_dict['phase']

        # Fill in initial tiles
        self.tiles = {tile['id']: Tile.create_from_dict(tile) for tile in map_dict['tiles']}
        self.alias_map = {None: None}
        # Add equivalencies and adjacencies - and add to alias_map
        for tile in map_dict['tiles']:
            for equiv_id in tile['equivalencies']:
                self.tiles[tile['id']].equivalencies.append(self.tiles[equiv_id])
            for adjacent_id in tile['adjacencies']:
                self.tiles[tile['id']].adjacencies.append(self.tiles[adjacent_id])
            for alias in tile['aliases'].values():
                self.alias_map[alias] = tile['id']
            self.alias_map[str(tile['id'])] = tile['id']

        self._validate_tiles()
        print(
            "Successfully verified map dict with {} entries and {} players.".format(len(self.tiles), len(self.players)))
        self.previous_orders = []
        self.orders = []

    @property
    def sc_counts(self):
        """Return a dict mapping player strings to the number of SCs they control"""
        sc_dict = {}
        for player in self.players:
            sc_dict[player] = 0
        for tile in self.tiles.values():
            if tile.owner is not None and not tile.is_coast and tile.is_supply_center:
                sc_dict[tile.owner] += 1
        return sc_dict

    @property
    def num_supply_centers(self):
        """Return the number of supply center tiles on the board"""
        return sum(tile.is_supply_center and not tile.is_coast for tile in self.tiles.values())

    @property
    def num_ocean_tiles(self):
        """Return the number of ocean tiles on the board"""
        return sum(tile.is_ocean for tile in self.tiles.values())

    @property
    def num_land_tiles(self):
        """Return the number of land (non-ocean) tiles on the board"""
        return len(self.tiles) - self.num_ocean_tiles

    def _validate_tiles(self):
        """Assert that the tiles are in a valid game state - DOESNT HAVE FULL COVERAGE!"""
        for tile in self.tiles.values():
            # Assert equivalent tiles have the same owner and supply center status
            if len(tile.equivalencies):
                assert not tile.is_ocean, 'Ocean tile found with equivalencies: id {}'.format(tile.id)
                for equiv_tile in tile.equivalencies:
                    assert equiv_tile.owner == tile.owner, \
                        'Mismatching owners for equivalent tiles: ids {} and {}'.format(tile.id, equiv_tile.id)
                    assert equiv_tile.is_supply_center == tile.is_supply_center, \
                        'Mismatching SC status for equivalent tiles: ids {} and {}'.format(tile.id, equiv_tile.id)
                    if tile.unit is not None:
                        assert equiv_tile.unit is None, \
                            'Two units on equivalent tiles: ids {} and {}'.format(tile.id, equiv_tile.id)
            # Assert the units on this tile are valid
            if tile.unit is not None:
                assert tile.unit.owner is not None, 'Unit with no owner in tile: id {}'.format(tile.id)
                assert tile.unit.owner in self.players, 'Unit found with unregistered player in tile: id {}'.format(
                    tile.id)
                if tile.is_coast or tile.is_ocean:
                    assert tile.unit.type == 'fleet', \
                        'Non-fleet found on coast or ocean: id {}'.format(tile.id)
                else:
                    assert tile.unit.type == 'army', \
                        'Non-army found on land: id {}'.format(tile.id)
            # Assert that the owner of this tile is valid
            if tile.owner is not None:
                assert tile.owner in self.players, 'Tile without valid owner found: id {}'.format(tile.id)
            # Assert each tile has at least one adjacency
            assert len(tile.adjacencies), 'Tile without adjacencies: id {}'.format(tile.id)
            # Assert that home centers are for a valid player
            if tile.home_center_for is not None:
                assert tile.home_center_for in self.players, 'Home center has invalid player string: id {}'.format(
                    tile.id)
            for adj_tile in tile.adjacencies:
                # Assert adjacencies are bidirectional
                assert tile in adj_tile.adjacencies, 'Unidirectional adjacency found: ids {} and {}'.format(tile.id,
                                                                                                            adj_tile.id)

    def scramble(self):
        """Completely shuffle the owners and units on each tile.
            Then adds a adequate number of units to the board (placing them anywhere).
            The board must have nonzero players"""
        raise NotImplementedError("scramble has yet to be implemented after pydip addition")
        # if len(self.players):
        #     for tile in self.tiles.values():
        #         tile.owner = random.choice(tuple(self.players))
        #         tile.unit = None
        #     tiles = list(self.tiles.values())
        #     for country, count in self.sc_counts.items():
        #         for _ in range(count):
        #             tile = random.choice(tiles)
        #             if tile.unit_include_equivs is None:
        #                 if tile.is_ocean or tile.is_coast:
        #                     tile.unit = Unit(country, 'fleet')
        #                 elif not (tile.is_ocean or tile.is_coast):
        #                     tile.unit = Unit(country, 'army')
        #     self._validate_tiles()
        # else:
        #     raise NotImplementedError("Can't shuffle a board with no players")

    def write_image(self, output_dir):
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
            done(output_dir)

    def serialize(self):
        """Serialize this Board into a dict that can be used to construct another Board"""
        out_dict = {'year': self.year, 'season': self.season, 'phase': self.phase, 'players': list(self.players)}
        tile_dict = [tile.serialize() for tile in self.tiles.values()]
        out_dict['tiles'] = tile_dict
        return out_dict

    def resolve_orders(self):
        """Parse all orders and resolve the board accordingly. If no orders exist for a unit, it adds a hold order"""
        pydip_map = create_pydip_map(self.tiles)
        if self.phase == 'diplomacy':
            player_order_map = {player: [] for player in self.players}
            tiles_with_orders = set()
            for order in self.orders:  # Collect and convert orders
                player_order_map[order.player].append(
                    convert_order_to_pydip_commandhelper(self.tiles, self.alias_map, order))
                tiles_with_orders.add(self.alias_map[order.source_tile])

            for tile in self.tiles.values():  # Add hold orders for every unit without an order
                if (tile.unit is not None) and (tile.id not in tiles_with_orders):
                    player_order_map[tile.unit.owner].append(
                        convert_order_to_pydip_commandhelper(self.tiles, self.alias_map,
                                                             Order(tile.unit.owner, str(tile.id))))

            player_helpers = [PlayerHelper(player, orders) for player, orders in player_order_map.items()]
            helper = TurnHelper(player_helpers, game_map=pydip_map.supply_map.game_map)
            results = helper.resolve()
            # Update units
            for tile in self.tiles.values():
                tile.unit = None

            for player, result_dict in results.items():
                for result_unit in result_dict:
                    self.tiles[int(result_unit.position)].unit = Unit(player, unit_type_to_str(result_unit.unit_type))

            # TODO: Increment phase
        elif self.phase == 'retreats':
            pass
        elif self.phase == 'unit-placement':
            pass

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

# TODO: Remove 'short_name' dependency from write_image() and update self.aliases construction accordingly
# TODO: Add move visualization to write_image()
