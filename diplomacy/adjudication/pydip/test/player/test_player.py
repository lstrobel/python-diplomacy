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

import pytest

from diplomacy.adjudication.pydip.map.predefined.vanilla_dip import generate_map
from diplomacy.adjudication.pydip.player.player import Player
from diplomacy.adjudication.pydip.player.unit import Unit, UnitTypes


def test_player_with_no_starting_position():
    game_map = generate_map()
    starting_configuration = []
    player = Player("test player", game_map, starting_configuration)

    assert player.starting_territories == set()
    assert player.units == []


def test_player_with_one_starting_position_without_unit():
    game_map = generate_map()
    starting_configuration = [
        {'territory_name': 'Sevastopol', 'unit_type': None}
    ]
    player = Player("test player", game_map, starting_configuration)

    assert player.starting_territories == {'Sevastopol'}
    assert player.units == []


def test_player_with_one_starting_position_with_unit():
    game_map = generate_map()
    starting_configuration = [
        {'territory_name': 'Sevastopol', 'unit_type': UnitTypes.TROOP}
    ]
    player = Player("test player", game_map, starting_configuration)

    assert player.starting_territories == {'Sevastopol'}
    assert player.units == [Unit(UnitTypes.TROOP, 'Sevastopol')]


def test_player_invalid_for_troop_on_sea():
    game_map = generate_map()
    starting_configuration = [
        {'territory_name': 'Norwegian Sea', 'unit_type': UnitTypes.TROOP}
    ]
    with pytest.raises(AssertionError):
        Player("test player", game_map, starting_configuration)


def test_player_invalid_for_troop_on_coast():
    game_map = generate_map()
    starting_configuration = [
        {'territory_name': 'Liverpool Coast', 'unit_type': UnitTypes.TROOP}
    ]
    with pytest.raises(AssertionError):
        Player("test player", game_map, starting_configuration)


def test_player_invalid_for_fleet_on_land():
    game_map = generate_map()
    starting_configuration = [
        {'territory_name': 'Trieste', 'unit_type': UnitTypes.FLEET}
    ]
    with pytest.raises(AssertionError):
        Player("test player", game_map, starting_configuration)


def test_player_invalid_for_invalid_starting_territory():
    game_map = generate_map()
    starting_configuration = [
        {'territory_name': 'Fake Territory', 'unit_type': None}
    ]
    with pytest.raises(AssertionError):
        Player("test player", game_map, starting_configuration)


def test_player_with_coastal_starting_position_labeled_as_parent():
    game_map = generate_map()
    starting_configuration = [
        {'territory_name': 'Sevastopol Coast', 'unit_type': UnitTypes.FLEET}
    ]
    player = Player("test player", game_map, starting_configuration)

    assert player.starting_territories == {'Sevastopol'}
    assert player.units == [Unit(UnitTypes.FLEET, 'Sevastopol Coast')]


def test_player_multiple_starting_territories():
    game_map = generate_map()
    starting_configuration = [
        {'territory_name': 'St. Petersburg North Coast', 'unit_type': UnitTypes.FLEET},
        {'territory_name': 'Warsaw', 'unit_type': UnitTypes.TROOP},
        {'territory_name': 'Moscow', 'unit_type': UnitTypes.TROOP},
        {'territory_name': 'Sevastopol Coast', 'unit_type': UnitTypes.FLEET},
    ]

    player = Player("test player", game_map, starting_configuration)
    assert player.starting_territories == {'St. Petersburg', 'Warsaw', 'Moscow', 'Sevastopol'}
    assert player.units == [
        Unit(UnitTypes.FLEET, 'St. Petersburg North Coast'),
        Unit(UnitTypes.TROOP, 'Warsaw'),
        Unit(UnitTypes.TROOP, 'Moscow'),
        Unit(UnitTypes.FLEET, 'Sevastopol Coast'),
    ]
