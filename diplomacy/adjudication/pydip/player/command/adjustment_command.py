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

from diplomacy.adjudication.pydip.player.helpers import unit_type_can_enter


class AdjustmentCommand:
    def __init__(self, player, unit):
        self.player = player
        self.unit = unit


class AdjustmentDisbandCommand(AdjustmentCommand):
    def __init__(self, player, unit):
        super().__init__(player, unit)
        assert unit in player.units

    def __repr__(self):
        return '{}: {} {} Disband'.format(
            self.player.name,
            self.unit.unit_type,
            self.unit.position,
        )

    def __eq__(self, other):
        return (super(AdjustmentDisbandCommand, self).__eq__(other) and
                isinstance(other, AdjustmentDisbandCommand))

    def __ne__(self, other):
        return not self.__eq__(other)


class AdjustmentCreateCommand(AdjustmentCommand):
    """
    Unlike a traditional command, this one uses the unit to represent the new unit to be created.
    So this command takes an OwnershipMap, representing current board state, to determine if the
    provided unit would be allowed to be created for this player.
    """

    def __init__(self, ownership_map, player, unit):
        super().__init__(player, unit)

        unit_territory = ownership_map.supply_map.game_map.name_map[unit.position]
        assert ownership_map.territory_is_owned(player.name, unit.position)
        assert ownership_map.territory_is_home(player.name, unit.position)
        assert unit_type_can_enter(unit.unit_type, unit_territory)

        for existing_unit in player.units:
            existing_unit_territory = ownership_map.supply_map.game_map.name_map[existing_unit.position]
            assert not unit_territory.same_territory(existing_unit_territory)

    def __eq__(self, other):
        return (super(AdjustmentCreateCommand, self).__eq__(other) and
                isinstance(other, AdjustmentCreateCommand))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return '{}: {} {} Create'.format(
            self.player.name,
            self.unit.unit_type,
            self.unit.position,
        )
