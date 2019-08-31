from diplomacy.adjudication.pydip.map import Map, SupplyCenterMap, OwnershipMap


def _create_starting_pydip_map(tiles):
    territory_descriptors = []
    visited = set()
    adjacencies = []
    supply_centers = set()
    home_territories = {}
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

        # Add to home territories
        if tile.owner is not None and tile.is_supply_center:
            if tile.owner not in home_territories:
                home_territories[tile.owner] = set()
            home_territories[tile.owner].add(str(tile.id))

    generate_map = Map(territory_descriptors, adjacencies)
    generate_supply_center_map = SupplyCenterMap(generate_map, supply_centers)

    return OwnershipMap(generate_supply_center_map, home_territories, home_territories)
