#  python-diplomacy is a tool for exploring the game diplomacy in python.
#  Copyright (C) 2017 Aric Parkinson
#  Copyright (C) 2019 Lukas Strobel
#
#  The following code is a derivative work of the code from Aric Parkinson's pydip,
#  which is licensed MIT. This derivative is licensed under the terms
#  of the GNU Affero General Public License, verison 3.
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

from diplomacy.adjudication.pydip.map.map import Map
from diplomacy.adjudication.pydip.map.territory import LandTerritory, SeaTerritory


def test_empty_map():
    territory_descriptors = []
    adjacencies = []

    game_map = Map(territory_descriptors, adjacencies)
    expected_name_map = dict()
    expected_adjacency = dict()

    assert game_map.name_map == expected_name_map
    assert game_map.adjacency == expected_adjacency


def test_singleton_map():
    territory_descriptors = [{'name': 'Pacific Ocean'}]
    adjacencies = []

    game_map = Map(territory_descriptors, adjacencies)
    expected_name_map = {'Pacific Ocean': SeaTerritory('Pacific Ocean')}
    expected_adjacency = {'Pacific Ocean': set()}

    assert game_map.name_map == expected_name_map
    assert game_map.adjacency == expected_adjacency


def test_two_connected_land_territories():
    territory_descriptors = [
        {'name': 'United States', 'coasts': []},
        {'name': 'Mexico', 'coasts': []},
    ]
    adjacencies = [('United States', 'Mexico')]

    game_map = Map(territory_descriptors, adjacencies)
    expected_name_map = {
        'United States': LandTerritory('United States', []),
        'Mexico': LandTerritory('Mexico', []),
    }
    expected_adjacency = {
        'United States': {'Mexico'},
        'Mexico': {'United States'},
    }

    assert game_map.name_map == expected_name_map
    assert game_map.adjacency == expected_adjacency


def test_land_territories_with_lake():
    territory_descriptors = [
        {'name': 'Salt Lake City', 'coasts': ['Salt Lake City Coast']},
        {'name': 'Ogden', 'coasts': ['Ogden Coast']},
        {'name': 'Great Salt Lake'},
    ]
    adjacencies = [
        ('Salt Lake City', 'Ogden'),
        ('Salt Lake City Coast', 'Great Salt Lake'),
        ('Salt Lake City Coast', 'Ogden Coast'),
        ('Ogden Coast', 'Great Salt Lake'),
    ]

    game_map = Map(territory_descriptors, adjacencies)
    slc_territory = LandTerritory('Salt Lake City', ['Salt Lake City Coast'])
    ogden_territory = LandTerritory('Ogden', ['Ogden Coast'])
    expected_name_map = {
        'Salt Lake City': slc_territory,
        'Salt Lake City Coast': slc_territory.coasts[0],
        'Ogden': ogden_territory,
        'Ogden Coast': ogden_territory.coasts[0],
        'Great Salt Lake': SeaTerritory('Great Salt Lake')
    }
    expected_adjacency = {
        'Salt Lake City': {'Ogden'},
        'Salt Lake City Coast': {'Ogden Coast', 'Great Salt Lake'},
        'Ogden': {'Salt Lake City'},
        'Ogden Coast': {'Salt Lake City Coast', 'Great Salt Lake'},
        'Great Salt Lake': {'Salt Lake City Coast', 'Ogden Coast'}
    }

    assert game_map.name_map == expected_name_map
    assert game_map.adjacency == expected_adjacency
