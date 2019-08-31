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


def test_same_position_and_type_are_equal():
    unit_a = Unit(UnitTypes.FLEET, 'Adriatic Sea')
    unit_b = Unit(UnitTypes.FLEET, 'Adriatic Sea')

    assert unit_a == unit_b
    assert not unit_a != unit_b


def test_different_position_same_type_are_not_equal():
    unit_a = Unit(UnitTypes.TROOP, 'Trieste')
    unit_b = Unit(UnitTypes.TROOP, 'Constantinople')

    assert not unit_a == unit_b
    assert unit_a != unit_b


def test_same_position_different_type_are_not_equal():
    unit_a = Unit(UnitTypes.FLEET, 'Constantinople')
    unit_b = Unit(UnitTypes.TROOP, 'Constantinople')

    assert not unit_a == unit_b
    assert unit_a != unit_b


def test_different_position_and_type_are_not_equal():
    unit_a = Unit(UnitTypes.FLEET, 'Finland Coast')
    unit_b = Unit(UnitTypes.TROOP, 'Constantinople')

    assert not unit_a == unit_b
    assert unit_a != unit_b
