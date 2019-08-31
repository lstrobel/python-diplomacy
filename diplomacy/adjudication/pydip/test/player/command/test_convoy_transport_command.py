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

import pytest

from diplomacy.adjudication.pydip.map.predefined.vanilla_dip import generate_map
from diplomacy.adjudication.pydip.player.command.command import ConvoyTransportCommand
from diplomacy.adjudication.pydip.player.player import Player
from diplomacy.adjudication.pydip.player.unit import UnitTypes


def test_convoy_transport_fails_for_troop_transporting():
    game_map = generate_map()
    starting_configuration = [
        {'territory_name': 'Apulia', 'unit_type': UnitTypes.TROOP},
        {'territory_name': 'Rome', 'unit_type': UnitTypes.TROOP},
    ]
    player = Player("Italy", game_map, starting_configuration)

    with pytest.raises(AssertionError):
        ConvoyTransportCommand(player, player.units[0], player.units[1], 'Marseilles')


def test_convoy_transport_fails_for_fleet_moving():
    game_map = generate_map()
    starting_configuration = [
        {'territory_name': 'Spain South Coast', 'unit_type': UnitTypes.FLEET},
        {'territory_name': 'Western Mediterranean Sea', 'unit_type': UnitTypes.FLEET},
    ]
    player = Player("France", game_map, starting_configuration)

    with pytest.raises(AssertionError):
        ConvoyTransportCommand(player, player.units[0], player.units[1], 'Tunis')


def test_convoy_transport_fails_for_landlocked_origin():
    game_map = generate_map()
    starting_configuration = [
        {'territory_name': 'Tyrrhenian Sea', 'unit_type': UnitTypes.FLEET},
        {'territory_name': 'Bohemia', 'unit_type': UnitTypes.TROOP},
    ]
    player = Player("Germany", game_map, starting_configuration)

    with pytest.raises(AssertionError):
        ConvoyTransportCommand(player, player.units[0], player.units[1], 'Rome')


def test_convoy_transport_fails_for_landlocked_destination():
    game_map = generate_map()
    starting_configuration = [
        {'territory_name': 'Tyrrhenian Sea', 'unit_type': UnitTypes.FLEET},
        {'territory_name': 'Naples', 'unit_type': UnitTypes.TROOP},
    ]
    player = Player("Italy", game_map, starting_configuration)

    with pytest.raises(AssertionError):
        ConvoyTransportCommand(player, player.units[0], player.units[1], 'Warsaw')


def test_convoy_transport_success():
    game_map = generate_map()
    starting_configuration = [
        {'territory_name': 'Tyrrhenian Sea', 'unit_type': UnitTypes.FLEET},
        {'territory_name': 'Constantinople', 'unit_type': UnitTypes.TROOP},
    ]
    player = Player("Turkey", game_map, starting_configuration)

    command = ConvoyTransportCommand(player, player.units[0], player.units[1], 'Tunis')

    assert command.unit.position == 'Tyrrhenian Sea'
    assert command.transported_unit.position == 'Constantinople'
    assert command.destination == 'Tunis'
