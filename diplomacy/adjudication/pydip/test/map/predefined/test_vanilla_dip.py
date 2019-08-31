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

from diplomacy.adjudication.pydip.map.predefined.vanilla_dip import generate_map, generate_supply_center_map


def test_territory_adjacency_counts():
    game_map = generate_map()

    expected_counts = {
        'North Atlantic Ocean': 5,
        'Mid-Atlantic Ocean': 10,
        'Irish Sea': 5,
        'English Channel': 8,
        'Brest': 3,
        'Brest Coast': 4,
        'Gascony': 5,
        'Gascony Coast': 3,
        'Spain': 3,
        'Spain North Coast': 3,
        'Spain South Coast': 5,
        'Portugal': 1,
        'Portugal Coast': 3,
        'Western Mediterranean Sea': 6,
        'North Africa': 1,
        'North Africa Coast': 3,
        'Tunis': 1,
        'Tunis Coast': 4,
        'Ionian Sea': 9,
        'Tyrrhenian Sea': 7,
        'Gulf of Lyon': 6,
        'Marseilles': 4,
        'Marseilles Coast': 3,
        'Burgundy': 7,
        'Paris': 4,
        'Picardy': 4,
        'Picardy Coast': 3,
        'Wales': 3,
        'Wales Coast': 4,
        'London': 2,
        'London Coast': 4,
        'Yorkshire': 4,
        'Yorkshire Coast': 3,
        'Liverpool': 4,
        'Liverpool Coast': 4,
        'Clyde': 2,
        'Clyde Coast': 4,
        'Edinburgh': 3,
        'Edinburgh Coast': 4,
        'Norwegian Sea': 6,
        'North Sea': 11,
        'Skagerrak': 4,
        'Helgoland Bight': 4,
        'Denmark': 2,
        'Denmark Coast': 6,
        'Holland': 3,
        'Holland Coast': 4,
        'Belgium': 4,
        'Belgium Coast': 4,
        'Ruhr': 5,
        'Munich': 7,
        'Piedmont': 4,
        'Piedmont Coast': 3,
        'Tuscany': 3,
        'Tuscany Coast': 4,
        'Naples': 2,
        'Naples Coast': 4,
        'Rome': 4,
        'Rome Coast': 3,
        'Apulia': 3,
        'Apulia Coast': 4,
        'Venice': 6,
        'Venice Coast': 3,
        'Tyrolia': 6,
        'Kiel': 5,
        'Kiel Coast': 5,
        'Berlin': 4,
        'Berlin Coast': 3,
        'Prussia': 4,
        'Prussia Coast': 3,
        'Silesia': 6,
        'Bohemia': 5,
        'Vienna': 5,
        'Trieste': 6,
        'Trieste Coast': 3,
        'Albania': 3,
        'Albania Coast': 4,
        'Greece': 3,
        'Greece Coast': 4,
        'Serbia': 6,
        'Budapest': 5,
        'Galicia': 7,
        'Warsaw': 6,
        'Livonia': 4,
        'Livonia Coast': 4,
        'Moscow': 5,
        'St. Petersburg': 4,
        'St. Petersburg North Coast': 2,
        'St. Petersburg South Coast': 3,
        'Ukraine': 5,
        'Sevastopol': 4,
        'Sevastopol Coast': 3,
        'Rumania': 6,
        'Rumania Coast': 3,
        'Bulgaria': 4,
        'Bulgaria North Coast': 3,
        'Bulgaria South Coast': 3,
        'Constantinople': 3,
        'Constantinople Coast': 6,
        'Ankara': 3,
        'Ankara Coast': 3,
        'Smyrna': 4,
        'Smyrna Coast': 4,
        'Syria': 2,
        'Syria Coast': 2,
        'Armenia': 4,
        'Armenia Coast': 3,
        'Adriatic Sea': 5,
        'Aegean Sea': 6,
        'Eastern Mediterranean Sea': 4,
        'Black Sea': 6,
        'Gulf of Bothnia': 5,
        'Baltic Sea': 7,
        'Barents Sea': 3,
        'Finland': 3,
        'Finland Coast': 3,
        'Sweden': 3,
        'Sweden Coast': 6,
        'Norway': 3,
        'Norway Coast': 6,
    }

    assert expected_counts.keys() == game_map.name_map.keys()
    for name, count in expected_counts.items():
        assert len(game_map.adjacency[name]) == count


def test_supply_center_counts():
    game_map = generate_supply_center_map()
    assert len(game_map.supply_centers) == 34
