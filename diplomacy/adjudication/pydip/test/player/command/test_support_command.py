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
from diplomacy.adjudication.pydip.player.command.command import SupportCommand
from diplomacy.adjudication.pydip.player.player import Player
from diplomacy.adjudication.pydip.player.unit import UnitTypes


def test_support_destination_not_adjacent():
    game_map = generate_map()
    starting_configuration = [
        {'territory_name': 'Trieste', 'unit_type': UnitTypes.TROOP},
        {'territory_name': 'Budapest', 'unit_type': UnitTypes.TROOP},
    ]
    player = Player("Austria", game_map, starting_configuration)

    with pytest.raises(AssertionError):
        SupportCommand(player, player.units[0], player.units[1], 'Galicia')


def test_support_landlocked_destination_with_fleet():
    game_map = generate_map()
    starting_configuration = [
        {'territory_name': 'Rumania Coast', 'unit_type': UnitTypes.FLEET},
        {'territory_name': 'Serbia', 'unit_type': UnitTypes.TROOP},
    ]
    player = Player("Turkey", game_map, starting_configuration)

    with pytest.raises(AssertionError):
        SupportCommand(player, player.units[0], player.units[1], 'Budapest')


def test_support_supported_unit_not_adjacent():
    game_map = generate_map()
    starting_configuration = [
        {'territory_name': 'Paris', 'unit_type': UnitTypes.TROOP},
        {'territory_name': 'Ruhr', 'unit_type': UnitTypes.TROOP},
    ]
    player = Player("France", game_map, starting_configuration)

    command = SupportCommand(player, player.units[0], player.units[1], 'Burgundy')

    assert command.unit.position == 'Paris'
    assert command.supported_unit.position == 'Ruhr'
    assert command.destination == 'Burgundy'


def test_support_supported_unit_adjacent():
    game_map = generate_map()
    starting_configuration = [
        {'territory_name': 'Tuscany', 'unit_type': UnitTypes.TROOP},
        {'territory_name': 'Rome', 'unit_type': UnitTypes.TROOP},
    ]
    player = Player("Italy", game_map, starting_configuration)

    command = SupportCommand(player, player.units[0], player.units[1], 'Venice')

    assert command.unit.position == 'Tuscany'
    assert command.supported_unit.position == 'Rome'
    assert command.destination == 'Venice'


def test_support_troop_to_parent_of_coast_with_fleet():
    game_map = generate_map()
    starting_configuration = [
        {'territory_name': 'Gulf of Lyon', 'unit_type': UnitTypes.FLEET},
        {'territory_name': 'Tuscany', 'unit_type': UnitTypes.TROOP},
    ]
    player = Player("France", game_map, starting_configuration)

    command = SupportCommand(player, player.units[0], player.units[1], 'Piedmont')

    assert command.unit.position == 'Gulf of Lyon'
    assert command.supported_unit.position == 'Tuscany'
    assert command.destination == 'Piedmont'


def test_support_fleet_to_coast_with_troop():
    game_map = generate_map()
    starting_configuration = [
        {'territory_name': 'Finland', 'unit_type': UnitTypes.TROOP},
        {'territory_name': 'Baltic Sea', 'unit_type': UnitTypes.FLEET},
    ]
    player = Player("France", game_map, starting_configuration)

    command = SupportCommand(player, player.units[0], player.units[1], 'Sweden Coast')

    assert command.unit.position == 'Finland'
    assert command.supported_unit.position == 'Baltic Sea'
    assert command.destination == 'Sweden Coast'


def test_support_troop_on_coast_to_another_coast():
    game_map = generate_map()
    starting_configuration = [
        {'territory_name': 'Norway', 'unit_type': UnitTypes.TROOP},
        {'territory_name': 'Norwegian Sea', 'unit_type': UnitTypes.FLEET},
    ]
    player = Player("Russia", game_map, starting_configuration)

    command = SupportCommand(player, player.units[1], player.units[0], 'Edinburgh')

    assert command.unit.position == 'Norwegian Sea'
    assert command.supported_unit.position == 'Norway'
    assert command.destination == 'Edinburgh'
