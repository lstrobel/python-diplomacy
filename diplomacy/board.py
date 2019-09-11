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
from collections import deque

from diplomacy.adjudication.pydip.test import PlayerHelper, TurnHelper
from diplomacy.adjudication.pydip.test.adjustment_helper import AdjustmentHelper
from diplomacy.adjudication.pydip.test.command_helper import AdjustmentCommandType
from diplomacy.adjudication.pydip.test.retreat_helper import RetreatHelper
from diplomacy.adjudication.pydip_connector import convert_order_to_pydip_commandhelper, create_pydip_map, \
    get_player_units, unit_type_to_str
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
        self.previous_orders = None
        self._previous_results = None
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

    @property
    def unit_deltas(self):
        """Return a dict mapping players to the delta between the number of SCs
        they control and how many units they have"""
        counts = self.sc_counts
        deltas = {}
        for tile in self.tiles.values():
            if tile.unit is not None:
                if tile.unit.owner not in deltas:
                    deltas[tile.unit.owner] = counts[tile.unit.owner]
                deltas[tile.unit.owner] -= 1
        return deltas

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
        player_order_map, tiles_with_orders = self._get_pydip_orders()

        # Arrange default orders
        if self.phase == 'diplomacy':
            self._add_default_hold_orders(player_order_map, tiles_with_orders)
        elif self.phase == 'retreats':
            self._add_default_disband_orders(player_order_map, tiles_with_orders)
        elif self.phase == 'unit-placement':
            self._add_default_unit_placement_orders(player_order_map)

        # Setup PlayerHelpers
        player_helpers = [PlayerHelper(player, orders) for player, orders in player_order_map.items()]

        # Build the right turn helper
        if self.phase == 'diplomacy':
            helper = TurnHelper(player_helpers, game_map=pydip_map.supply_map.game_map)
        elif self.phase == 'retreats':
            helper = RetreatHelper(self._previous_results, player_helpers, game_map=pydip_map.supply_map.game_map)
        elif self.phase == 'unit-placement':
            helper = AdjustmentHelper(player_helpers, player_units=get_player_units(self.tiles),
                                      owned_territories=pydip_map.owned_territories,
                                      home_territories=pydip_map.home_territories, supply_map=pydip_map.supply_map)

        # Resolve move
        if self.phase == 'unit-placement':
            results = helper.resolve__validated()
        else:
            results = helper.resolve()
        self._update_units(results)

        # Increment phase
        if self.phase == 'diplomacy' and (not all(
                all(retreat_options == None for retreat_options in country.values()) for country in
                results.values())):  # There are retreats to be made
            self.phase = 'retreats'
        else:
            self._increment_diplomacy()

        # Set properties for the future
        self.previous_orders = self.orders
        self._previous_results = results
        self.orders = []

        # TODO: Somehow notify/inform clients of what needs to be retreated/disbanded/built

    def _add_default_unit_placement_orders(self, player_order_map):
        """Disband excess units for players if they didnt give disband orders"""
        deltas = self.unit_deltas
        disbanded_tiles = set()
        for player, delta in deltas.items():
            # Compensate for existing disband orders
            delta += len([x for x in player_order_map[player] if x.command_type == AdjustmentCommandType.DISBAND])
            while delta < 0:
                disband_tile = self._find_unit_to_disband(player, disbanded_tiles)
                disbanded_tiles.add(disband_tile)
                player_order_map[player].append(convert_order_to_pydip_commandhelper(self.tiles, self.alias_map,
                                                                                     Order(player, str(disband_tile.id),
                                                                                           'disband'),
                                                                                     phase='unit-placement'))
                delta += 1

    def _add_default_disband_orders(self, player_order_map, tiles_with_orders):
        """Disband units that need to retreat but don't have an order"""
        for player, move_dict in self._previous_results.items():
            for unit, move_set in move_dict.items():
                if (move_set is not None) and (int(unit.position) not in tiles_with_orders):
                    player_order_map[player].append(
                        convert_order_to_pydip_commandhelper(self.tiles, self.alias_map,
                                                             Order(player, unit.position, 'disband'),
                                                             retreat_map=self._previous_results))

    def _add_default_hold_orders(self, player_order_map, tiles_with_orders):
        """Add hold orders for every unit without an order"""
        for tile in self.tiles.values():
            if (tile.unit is not None) and (tile.id not in tiles_with_orders):
                player_order_map[tile.unit.owner].append(
                    convert_order_to_pydip_commandhelper(self.tiles, self.alias_map,
                                                         Order(tile.unit.owner, str(tile.id))))

    def _find_unit_to_disband(self, player, excluded=None):
        """Searches for a unit to disband if not disband orders were given, but one is needed.
         Prioritizes units furthest away from a home center, then fleets over armies,
         then in tile alphabetical order if there is still a tie. Returns the tile that this unit is on"""
        if excluded is None:
            excluded = []
        distances = {}
        for tile in self.tiles.values():
            if tile.unit is not None and tile.unit.owner == player and tile not in excluded:
                distances[tile] = self._distance_to_home_center(tile, player)
        max_distance = max(distances.values())
        furthest_tiles = [tile for tile, distance in distances.items() if distance == max_distance]
        if len(furthest_tiles) > 1:
            fleets = [tile for tile in furthest_tiles if tile.unit.type == 'fleet']
            if len(fleets) > 1:
                fleets.sort(
                    key=lambda x: x.aliases["long_name"])  # TODO: Remove alias dependency when refactoring later
            return fleets[0]
        else:
            return furthest_tiles[0]

    def _distance_to_home_center(self, tile, player):
        """Finds the distance between the given tile and a home center for the given player"""
        # Currently implemented using BFS
        queue = deque()
        visited = {tile: 0}
        queue.append(tile)
        while len(queue):
            next_tile = queue.popleft()
            if next_tile.home_center_for == player:
                return visited[next_tile]
            for equivalent_tile in next_tile.equivalencies:
                if equivalent_tile not in visited:
                    visited[equivalent_tile] = visited[next_tile]
                    queue.append(equivalent_tile)
            for adjacent_tile in next_tile.adjacencies:
                if adjacent_tile not in visited:
                    visited[adjacent_tile] = visited[next_tile] + 1
                    queue.append(adjacent_tile)

    def _increment_diplomacy(self):
        # TODO: Once everything is ready, see if you can make this able to be called safely (not private)
        """Increment to the next diplomacy phase, or to unit-placement if necessary"""
        if self.season == 'fall':
            # Determine if a unit-placement phase is necessary
            self._update_ownerships()

            if not all(delta == 0 for delta in self.unit_deltas.values()):  # No unit-placement necessary
                print(self.unit_deltas)
                self.phase = 'unit-placement'
            else:
                self._increment_season()
                self.phase = 'diplomacy'
        else:  # We are in spring, so just continue to the next diplomacy phase
            self._increment_season()
            self.phase = 'diplomacy'

    def _update_units(self, results):
        """Using the passed results, change the units on the board to match their new positions"""
        # TODO: Respect retreating units as underneath
        # Clear all units
        for tile in self.tiles.values():
            tile.unit = None
        # Write new unit positions
        for player, result_set in results.items():
            for result_unit in result_set:
                self.tiles[int(result_unit.position)].unit = Unit(player, unit_type_to_str(result_unit.unit_type))

    def _get_pydip_orders(self):
        """Convert all orders in self.orders to pydip orders and return them"""
        player_order_map = {player: [] for player in self.players}
        tiles_with_orders = set()
        for order in self.orders:  # Collect and convert orders
            player_order_map[order.player].append(
                convert_order_to_pydip_commandhelper(self.tiles, self.alias_map, order))
            tiles_with_orders.add(self.alias_map[order.source_tile])
        return player_order_map, tiles_with_orders

    def _increment_season(self):
        """Increment the game season and year without regard to phase"""
        if self.season == 'spring':
            self.season = 'fall'
        else:
            self.year = str(int(self.year) + 1)
            self.season = 'spring'

    def _update_ownerships(self):
        """Update the ownership of tiles to whichever unit is on them at the moment"""
        for tile in self.tiles.values():
            if tile.unit is not None:
                tile.owner = tile.unit.owner

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
