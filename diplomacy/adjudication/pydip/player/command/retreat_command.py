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

from diplomacy.adjudication.pydip.player.command.command import Command


class RetreatCommand(Command):
    """
    retreat_map is intended to be the output from turn.resolve.resolve_turn.
    That is, a mapping of players to mappings of units to either None (in the
    case that a retreat is not expected for that unit), or a set of territory
    names (which hold the valid retreat targets).

    Commands issued that disagree with the provided retreat_map will fail.
    """

    def __init__(self, retreat_map, player, unit):
        super().__init__(player, unit)
        assert unit in retreat_map[player.name]
        assert retreat_map[player.name][unit] is not None


class RetreatDisbandCommand(RetreatCommand):
    def __init__(self, retreat_map, player, unit):
        super().__init__(retreat_map, player, unit)

    def __repr__(self):
        return '{}: {} {} Disband'.format(
            self.player.name,
            self.unit.unit_type,
            self.unit.position,
        )

    def __eq__(self, other):
        return (super(RetreatDisbandCommand, self).__eq__(other) and
                isinstance(other, RetreatDisbandCommand))

    def __ne__(self, other):
        return not self.__eq__(other)


class RetreatMoveCommand(RetreatCommand):
    """
    String -- Name of territory being retreated to.
      * Must be included in retreat_map as one of the territories the unit
        is permitted to retreat to
    """
    destination = None

    def __init__(self, retreat_map, player, unit, destination):
        super().__init__(retreat_map, player, unit)
        game_map = self.player.game_map
        assert destination in game_map.name_map
        assert destination in retreat_map[player.name][unit]
        self.destination = destination

    def __eq__(self, other):
        return (super(RetreatMoveCommand, self).__eq__(other) and
                isinstance(other, RetreatMoveCommand) and
                self.destination == other.destination)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return '{}: {} {} -> {} (Retreat)'.format(
            self.player.name,
            self.unit.unit_type,
            self.unit.position,
            self.destination,
        )
