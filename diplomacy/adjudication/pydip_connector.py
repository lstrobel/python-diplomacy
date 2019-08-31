from diplomacy.adjudication.pydip.map import Map


def _create_pydip_map(tiles):
    territory_descriptors = []
    visited = set()
    adjacencies = []
    for tile in tiles.values():
        if not tile.is_coast:
            descriptor_dict = {'name': str(tile.id)}
            if not tile.is_ocean:
                descriptor_dict['coasts'] = [equiv_tile.id for equiv_tile in tile.equivalencies]
            territory_descriptors.append(descriptor_dict)
        for adjacent_tile in tile.adjacencies:
            if adjacent_tile not in visited:
                adjacencies.append((tile.id, adjacent_tile.id))
        visited.add(tile)
    return Map(territory_descriptors, adjacencies)
