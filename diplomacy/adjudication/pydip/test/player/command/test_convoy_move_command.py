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
from diplomacy.adjudication.pydip.player.command.command import ConvoyMoveCommand
from diplomacy.adjudication.pydip.player.player import Player
from diplomacy.adjudication.pydip.player.unit import UnitTypes


def test_convoy_move_fails_for_fleet():
    game_map = generate_map()
    starting_configuration = [
        {'territory_name': 'St. Petersburg North Coast', 'unit_type': UnitTypes.FLEET},
    ]
    player = Player("Russia", game_map, starting_configuration)

    with pytest.raises(AssertionError):
        ConvoyMoveCommand(player, player.units[0], 'Sweden Coast')


def test_convoy_move_fails_for_landlocked_destination():
    game_map = generate_map()
    starting_configuration = [
        {'territory_name': 'Wales', 'unit_type': UnitTypes.TROOP},
    ]
    player = Player("England", game_map, starting_configuration)

    with pytest.raises(AssertionError):
        ConvoyMoveCommand(player, player.units[0], 'Paris')


def test_convoy_move_fails_for_landlocked_origin():
    game_map = generate_map()
    starting_configuration = [
        {'territory_name': 'Silesia', 'unit_type': UnitTypes.TROOP},
    ]
    player = Player("England", game_map, starting_configuration)

    with pytest.raises(AssertionError):
        ConvoyMoveCommand(player, player.units[0], 'London')


def test_convoy_move_success():
    game_map = generate_map()
    starting_configuration = [
        {'territory_name': 'Constantinople', 'unit_type': UnitTypes.TROOP},
    ]
    player = Player("France", game_map, starting_configuration)

    command = ConvoyMoveCommand(player, player.units[0], 'Tunis')

    assert command.unit.position == 'Constantinople'
    assert command.destination == 'Tunis'
