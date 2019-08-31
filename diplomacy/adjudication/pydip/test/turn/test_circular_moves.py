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

from diplomacy.adjudication.pydip.player.unit import Unit, UnitTypes
from diplomacy.adjudication.pydip.test.command_helper import CommandHelper, CommandType
from diplomacy.adjudication.pydip.test.player_helper import PlayerHelper
from diplomacy.adjudication.pydip.test.turn_helper import TurnHelper


def test_three_country_rotation():
    helper = TurnHelper([
        PlayerHelper('Germany', [
            CommandHelper(CommandType.MOVE, UnitTypes.TROOP, 'Galicia', 'Bohemia'),
        ]),
        PlayerHelper('Austria', [
            CommandHelper(CommandType.MOVE, UnitTypes.TROOP, 'Bohemia', 'Vienna'),
        ]),
        PlayerHelper('Turkey', [
            CommandHelper(CommandType.MOVE, UnitTypes.TROOP, 'Vienna', 'Galicia'),
        ]),
    ])

    result = helper.resolve()
    assert result == {
        'Germany': {
            Unit(UnitTypes.TROOP, 'Bohemia'): None,
        },
        'Austria': {
            Unit(UnitTypes.TROOP, 'Vienna'): None,
        },
        'Turkey': {
            Unit(UnitTypes.TROOP, 'Galicia'): None,
        },
    }


def test_three_country_rotation_with_one_move_supported():
    helper = TurnHelper([
        PlayerHelper('Germany', [
            CommandHelper(CommandType.MOVE, UnitTypes.TROOP, 'Galicia', 'Bohemia'),
            CommandHelper(CommandType.SUPPORT, UnitTypes.TROOP, 'Silesia', 'Galicia', 'Bohemia'),
        ]),
        PlayerHelper('Austria', [
            CommandHelper(CommandType.MOVE, UnitTypes.TROOP, 'Bohemia', 'Vienna'),
        ]),
        PlayerHelper('Turkey', [
            CommandHelper(CommandType.MOVE, UnitTypes.TROOP, 'Vienna', 'Galicia'),
        ]),
    ])

    result = helper.resolve()
    assert result == {
        'Germany': {
            Unit(UnitTypes.TROOP, 'Bohemia'): None,
            Unit(UnitTypes.TROOP, 'Silesia'): None,
        },
        'Austria': {
            Unit(UnitTypes.TROOP, 'Vienna'): None,
        },
        'Turkey': {
            Unit(UnitTypes.TROOP, 'Galicia'): None,
        },
    }


def test_three_country_rotation_with_one_support_each():
    helper = TurnHelper([
        PlayerHelper('Germany', [
            CommandHelper(CommandType.MOVE, UnitTypes.TROOP, 'Galicia', 'Bohemia'),
            CommandHelper(CommandType.SUPPORT, UnitTypes.TROOP, 'Silesia', 'Galicia', 'Bohemia'),
        ]),
        PlayerHelper('Austria', [
            CommandHelper(CommandType.MOVE, UnitTypes.TROOP, 'Bohemia', 'Vienna'),
            CommandHelper(CommandType.SUPPORT, UnitTypes.TROOP, 'Tyrolia', 'Bohemia', 'Vienna'),
        ]),
        PlayerHelper('Turkey', [
            CommandHelper(CommandType.MOVE, UnitTypes.TROOP, 'Vienna', 'Galicia'),
            CommandHelper(CommandType.SUPPORT, UnitTypes.TROOP, 'Budapest', 'Vienna', 'Galicia'),
        ]),
    ])

    result = helper.resolve()
    assert result == {
        'Germany': {
            Unit(UnitTypes.TROOP, 'Bohemia'): None,
            Unit(UnitTypes.TROOP, 'Silesia'): None,
        },
        'Austria': {
            Unit(UnitTypes.TROOP, 'Vienna'): None,
            Unit(UnitTypes.TROOP, 'Tyrolia'): None,
        },
        'Turkey': {
            Unit(UnitTypes.TROOP, 'Galicia'): None,
            Unit(UnitTypes.TROOP, 'Budapest'): None,
        },
    }


def test_three_country_rotation_with_external_disruption():
    helper = TurnHelper([
        PlayerHelper('Germany', [
            CommandHelper(CommandType.MOVE, UnitTypes.TROOP, 'Galicia', 'Bohemia'),
        ]),
        PlayerHelper('Austria', [
            CommandHelper(CommandType.MOVE, UnitTypes.TROOP, 'Bohemia', 'Vienna'),
        ]),
        PlayerHelper('Turkey', [
            CommandHelper(CommandType.MOVE, UnitTypes.TROOP, 'Vienna', 'Galicia'),
        ]),
        PlayerHelper('Russia', [
            CommandHelper(CommandType.MOVE, UnitTypes.TROOP, 'Ukraine', 'Galicia'),
        ]),
    ])

    result = helper.resolve()
    assert result == {
        'Germany': {
            Unit(UnitTypes.TROOP, 'Galicia'): None,
        },
        'Austria': {
            Unit(UnitTypes.TROOP, 'Bohemia'): None,
        },
        'Turkey': {
            Unit(UnitTypes.TROOP, 'Vienna'): None,
        },
        'Russia': {
            Unit(UnitTypes.TROOP, 'Ukraine'): None,
        },
    }


def test_three_country_rotation_with_external_dislodge():
    helper = TurnHelper([
        PlayerHelper('Germany', [
            CommandHelper(CommandType.MOVE, UnitTypes.TROOP, 'Galicia', 'Bohemia'),
        ]),
        PlayerHelper('Austria', [
            CommandHelper(CommandType.MOVE, UnitTypes.TROOP, 'Bohemia', 'Vienna'),
        ]),
        PlayerHelper('Turkey', [
            CommandHelper(CommandType.MOVE, UnitTypes.TROOP, 'Vienna', 'Galicia'),
        ]),
        PlayerHelper('Russia', [
            CommandHelper(CommandType.MOVE, UnitTypes.TROOP, 'Ukraine', 'Galicia'),
            CommandHelper(CommandType.SUPPORT, UnitTypes.TROOP, 'Warsaw', 'Ukraine', 'Galicia'),
        ]),
    ])

    result = helper.resolve()
    assert result == {
        'Germany': {
            Unit(UnitTypes.TROOP, 'Galicia'): {
                'Silesia',
                'Budapest',
                'Rumania',
            },
        },
        'Austria': {
            Unit(UnitTypes.TROOP, 'Bohemia'): None,
        },
        'Turkey': {
            Unit(UnitTypes.TROOP, 'Vienna'): None,
        },
        'Russia': {
            Unit(UnitTypes.TROOP, 'Galicia'): None,
            Unit(UnitTypes.TROOP, 'Warsaw'): None,
        },
    }


def test_three_country_rotation_with_external_disruption_overcome_by_support():
    helper = TurnHelper([
        PlayerHelper('Germany', [
            CommandHelper(CommandType.MOVE, UnitTypes.TROOP, 'Galicia', 'Bohemia'),
        ]),
        PlayerHelper('Austria', [
            CommandHelper(CommandType.MOVE, UnitTypes.TROOP, 'Bohemia', 'Vienna'),
        ]),
        PlayerHelper('Turkey', [
            CommandHelper(CommandType.MOVE, UnitTypes.TROOP, 'Vienna', 'Galicia'),
            CommandHelper(CommandType.SUPPORT, UnitTypes.TROOP, 'Budapest', 'Vienna', 'Galicia'),
        ]),
        PlayerHelper('Russia', [
            CommandHelper(CommandType.MOVE, UnitTypes.TROOP, 'Ukraine', 'Galicia'),
        ]),
    ])

    result = helper.resolve()
    assert result == {
        'Germany': {
            Unit(UnitTypes.TROOP, 'Bohemia'): None,
        },
        'Austria': {
            Unit(UnitTypes.TROOP, 'Vienna'): None,
        },
        'Turkey': {
            Unit(UnitTypes.TROOP, 'Galicia'): None,
            Unit(UnitTypes.TROOP, 'Budapest'): None,
        },
        'Russia': {
            Unit(UnitTypes.TROOP, 'Ukraine'): None,
        },
    }
