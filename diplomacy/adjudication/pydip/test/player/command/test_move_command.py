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
from diplomacy.adjudication.pydip.player.command.command import HoldCommand, MoveCommand
from diplomacy.adjudication.pydip.player.player import Player
from diplomacy.adjudication.pydip.player.unit import UnitTypes


def test_move_not_adjacent():
    game_map = generate_map()
    starting_configuration = [
        {'territory_name': 'Trieste', 'unit_type': UnitTypes.TROOP},
    ]
    player = Player("Austria", game_map, starting_configuration)

    with pytest.raises(AssertionError):
        MoveCommand(player, player.units[0], 'Sevastopol')


def test_move_wrong_type():
    game_map = generate_map()
    starting_configuration = [
        {'territory_name': 'St. Petersburg North Coast', 'unit_type': UnitTypes.FLEET},
    ]
    player = Player("Russia", game_map, starting_configuration)

    with pytest.raises(AssertionError):
        MoveCommand(player, player.units[0], 'Moscow')


def test_move_land_to_land():
    game_map = generate_map()
    starting_configuration = [
        {'territory_name': 'Paris', 'unit_type': UnitTypes.TROOP},
    ]
    player = Player("France", game_map, starting_configuration)

    command = MoveCommand(player, player.units[0], 'Brest')

    assert command.unit.position == 'Paris'
    assert command.destination == 'Brest'


def test_move_sea_to_sea():
    game_map = generate_map()
    starting_configuration = [
        {'territory_name': 'North Sea', 'unit_type': UnitTypes.FLEET},
    ]
    player = Player("England", game_map, starting_configuration)

    command = MoveCommand(player, player.units[0], 'Norwegian Sea')

    assert command.unit.position == 'North Sea'
    assert command.destination == 'Norwegian Sea'


def test_move_sea_to_coast():
    game_map = generate_map()
    starting_configuration = [
        {'territory_name': 'Adriatic Sea', 'unit_type': UnitTypes.FLEET},
    ]
    player = Player("Italy", game_map, starting_configuration)

    command = MoveCommand(player, player.units[0], 'Trieste Coast')

    assert command.unit.position == 'Adriatic Sea'
    assert command.destination == 'Trieste Coast'


def test_move_coast_to_coast():
    game_map = generate_map()
    starting_configuration = [
        {'territory_name': 'Spain North Coast', 'unit_type': UnitTypes.FLEET},
    ]
    player = Player("France", game_map, starting_configuration)

    command = MoveCommand(player, player.units[0], 'Portugal Coast')

    assert command.unit.position == 'Spain North Coast'
    assert command.destination == 'Portugal Coast'


def test_hold():
    game_map = generate_map()
    starting_configuration = [
        {'territory_name': 'Trieste', 'unit_type': UnitTypes.TROOP},
    ]
    player = Player("Austria", game_map, starting_configuration)

    command = HoldCommand(player, player.units[0])

    assert command.unit.position == 'Trieste'
    assert command.destination == 'Trieste'
