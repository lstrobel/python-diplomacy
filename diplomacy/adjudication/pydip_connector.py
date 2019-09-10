import copy

from diplomacy.adjudication.pydip.map import Map, OwnershipMap, SupplyCenterMap
from diplomacy.adjudication.pydip.player import Unit, UnitTypes
from diplomacy.adjudication.pydip.test.command_helper import *


def create_pydip_map(tiles):
    """Create an ownership map for pydip to use"""
    territory_descriptors = []
    visited = set()
    adjacencies = []
    supply_centers = set()
    home_territories = {}
    owned_sc_territories = {}
    for tile in tiles.values():
        # Add to territory_descriptors
        if not tile.is_coast:
            descriptor_dict = {'name': str(tile.id)}
            if not tile.is_ocean:
                descriptor_dict['coasts'] = [str(equiv_tile.id) for equiv_tile in tile.equivalencies]
            territory_descriptors.append(descriptor_dict)

        # Add to adjacencies
        for adjacent_tile in tile.adjacencies:
            if adjacent_tile not in visited:
                adjacencies.append((str(tile.id), str(adjacent_tile.id)))
        visited.add(tile)

        # Add to supply_centers
        if tile.is_supply_center:
            supply_centers.add(str(tile.id))

        # Add to owned territories
        if tile.owner is not None and tile.is_supply_center:
            if tile.owner not in owned_sc_territories:
                owned_sc_territories[tile.owner] = set()
            owned_sc_territories[tile.owner].add(str(tile.id))

        # Add to home territories
        if tile.is_supply_center and tile.home_center_for is not None:
            if tile.home_center_for not in home_territories:
                home_territories[tile.home_center_for] = set()
            home_territories[tile.home_center_for].add(str(tile.id))

    generate_map = Map(territory_descriptors, adjacencies)
    generate_supply_center_map = SupplyCenterMap(generate_map, supply_centers)

    return OwnershipMap(generate_supply_center_map, owned_sc_territories, home_territories)


def get_starting_configs(tiles):
    """Return a map of players to a set of pydip units they control"""
    configs = {}
    for tile in tiles.values():
        if tile.unit is not None:
            if tile.unit.owner not in configs:
                configs[tile.unit.owner] = set()

            if tile.unit.type == 'army':
                configs[tile.unit.owner].add(Unit(UnitTypes.TROOP, str(tile.id)))
            else:
                configs[tile.unit.owner].add(Unit(UnitTypes.FLEET, str(tile.id)))
    return configs


def convert_order_to_pydip_commandhelper(tiles, aliases, order_, phase='retreats', retreat_map=None):
    # Convert string tile names to ids for internal pydip representations
    order = copy.deepcopy(order_)
    order.source_tile = str(aliases[order_.source_tile])
    order.destination_tile = str(aliases[order_.destination_tile])
    order.target_tile = str(aliases[order_.target_tile])

    # Find unit type on passed tile
    unit_type_str = tiles[int(order.source_tile)].unit.type
    unit_type = str_to_unit_type(unit_type_str)

    # Convert to CommandHelper
    if order.type == 'hold':
        return CommandHelper(CommandType.HOLD, unit_type, order.source_tile)
    elif order.type == 'move':
        return CommandHelper(CommandType.MOVE, unit_type, order.source_tile, order.destination_tile)
    elif order.type == 'support':
        return CommandHelper(CommandType.SUPPORT, unit_type, order.source_tile, order.target_tile,
                             order.destination_tile)
    elif order.type == 'convoy move':
        return CommandHelper(CommandType.CONVOY_MOVE, unit_type, order.source_tile, order.destination_tile)
    elif order.type == 'convoy transport':
        return CommandHelper(CommandType.CONVOY_TRANSPORT, unit_type, order.source_tile, order.target_tile,
                             order.destination_tile)
    elif order.type == 'retreat':
        return RetreatCommandHelper(RetreatCommandType.MOVE, retreat_map, unit_type, order.source_tile,
                                    order.destination_tile)
    elif order.type == 'disband':
        if phase == 'retreats':
            return RetreatCommandHelper(RetreatCommandType.DISBAND, retreat_map, unit_type, order.source_tile)
        elif phase == 'unit-placement':
            raise NotImplementedError
    elif order.type == 'build':
        raise NotImplementedError


def str_to_unit_type(unit_type_str):
    if unit_type_str == 'army':
        return UnitTypes.TROOP
    elif unit_type_str == 'fleet':
        return UnitTypes.FLEET


def unit_type_to_str(unit_type):
    if unit_type == UnitTypes.TROOP:
        return 'army'
    elif unit_type == UnitTypes.FLEET:
        return 'fleet'
