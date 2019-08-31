#  python-diplomacy is a tool for exploring the game diplomacy in python.
#  Copyright (C) 2017 Aric Parkinson
#  Copyright (C) 2019 Lukas Strobel
#
#  The following code is a derivative work of the code from Aric Parkinson's pydip,
#  which is licensed MIT. This derivative is licensed under the terms
#  of the GNU Affero General Public License, version 3.
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

from diplomacy.adjudication.pydip.map.territory import CoastTerritory, LandTerritory, SeaTerritory


class Map:
    """ String -> Territory """
    name_map = None

    """ String -> String{} (Adjacency List) """
    adjacency = None

    """
    territory_descriptors: list of structs defining new territories. Of the form:
        {
            'name': String,
            'coasts': [ { 'name': String } ] (Optional)
        }

        If 'coasts' is provided, the territory is Land, with Coasts as children. Otherwise it is Sea.

    adjacencies: list of tuples of names representing adjacent territories. Must be legal:
        * Sea adjacent only to Sea or Coast
        * Coast adjacent only to Sea or Coast
        * Land adjacent only to Land
        * All names must be provided in territory_descriptors
        * No duplicate adjacencies!
    """

    def __init__(self, territory_descriptors, adjacencies):
        self.name_map = dict()
        self.adjacency = dict()

        self._setup_name_map(territory_descriptors)
        self._setup_adjacencies(adjacencies)

    def __str__(self):
        territories = []
        for name, territory in self.name_map.items():
            territories.append(('{}: {}'.format(territory, self.adjacency[name])))
        return '\n'.join(territories)

    def relevant_name_for_territory(self, territory_name):
        territory = self.name_map[territory_name]
        if isinstance(territory, CoastTerritory):
            territory_name = territory.parent.name
        return territory_name

    def _setup_name_map(self, territory_descriptors):
        for descriptor in territory_descriptors:
            assert 'name' in descriptor
            name = descriptor['name']
            if 'coasts' in descriptor:
                land = LandTerritory(name, descriptor['coasts'])
                self._add_territory(land)
                for coast in land.coasts:
                    self._add_territory(coast)
            else:
                self._add_territory(SeaTerritory(name))

    def _add_territory(self, territory):
        self.name_map[territory.name] = territory
        self.adjacency[territory.name] = set()

    def _setup_adjacencies(self, adjacencies):
        for name_a, name_b in adjacencies:
            assert name_a in self.name_map
            assert name_b in self.name_map

            territory_a = self.name_map[name_a]
            territory_b = self.name_map[name_b]

            assert ~(isinstance(territory_a, LandTerritory) ^ isinstance(territory_b, LandTerritory))
            assert name_b not in self.adjacency[name_a]
            assert name_a not in self.adjacency[name_b]

            self.adjacency[name_a].add(name_b)
            self.adjacency[name_b].add(name_a)


class SupplyCenterMap:
    """ Map """
    game_map = None

    """ String{}, subset of map.name_map.keys() """
    supply_centers = None

    def __init__(self, game_map, supply_centers):
        assert supply_centers < game_map.name_map.keys()

        self.supply_centers = set(supply_centers)
        self.game_map = game_map

    def __str__(self):
        return 'Adjacencies:\n------------\n{}\n\nSCs:\n----\n{}'.format(self.game_map, self.supply_centers)


class OwnershipMap:
    """ SupplyCenterMap """
    supply_map = None

    """ String -> String{}, mapping Player names to which territories they control """
    owned_territories = None

    """ String -> String{}, mapping Player names to which territories are their home territories """
    home_territories = None

    def __init__(self, supply_map, owned_territories, home_territories):
        players = owned_territories.keys()
        assert all(owned_territories[player] - supply_map.supply_centers == set() for player in players)
        assert all(home_territories[player] - supply_map.supply_centers == set() for player in players)

        self.supply_map = supply_map
        self.owned_territories = owned_territories
        self.home_territories = home_territories

    def __str__(self):
        lines = ['{}\n'.format(self.supply_map), 'Supply centers\n--------------']
        for player, territories in self.owned_territories.items():
            lines.append('{}:\n  Owned: {}\n  Home: {}'.format(player, territories, self.home_territories[player]))
        return '\n'.join(lines)

    def territory_is_owned(self, player, territory_name):
        relevant_name = self.supply_map.game_map.relevant_name_for_territory(territory_name)
        return relevant_name in self.owned_territories[player]

    def territory_is_home(self, player, territory_name):
        relevant_name = self.supply_map.game_map.relevant_name_for_territory(territory_name)
        return relevant_name in self.home_territories[player]
