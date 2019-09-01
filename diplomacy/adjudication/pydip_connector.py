from diplomacy.adjudication.pydip.map import Map, OwnershipMap, SupplyCenterMap
from diplomacy.adjudication.pydip.player import Unit, UnitTypes


def create_starting_pydip_map(tiles):
    """Create an ownership map for pydip to use"""
    territory_descriptors = []
    visited = set()
    adjacencies = []
    supply_centers = set()
    home_territories = {}
    owned_territories = {}
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
            if tile.owner not in owned_territories:
                owned_territories[tile.owner] = set()
            owned_territories[tile.owner].add(str(tile.id))

        # Add to home territories
        if tile.is_supply_center and tile.home_center_for is not None:
            if tile.home_center_for not in home_territories:
                home_territories[tile.home_center_for] = set()
            home_territories[tile.home_center_for].add(str(tile.id))

    generate_map = Map(territory_descriptors, adjacencies)
    generate_supply_center_map = SupplyCenterMap(generate_map, supply_centers)

    return OwnershipMap(generate_supply_center_map, owned_territories, home_territories)


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
