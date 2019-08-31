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

from diplomacy.adjudication.pydip.player.command.retreat_command import RetreatCommand, RetreatMoveCommand
from diplomacy.adjudication.pydip.player.unit import Unit


def resolve_retreats(retreat_map, commands):
    """
    Returns resulting board state by considering interactions of provided list
    of retreat commands.

    retreat_map is intended to be the output from turn.resolve.resolve_turn.
    That is, a mapping of players to mappings of units to either None (in the
    case that a retreat is not expected for that unit), or a set of territory
    names (which hold the valid retreat targets).

    Returns a mapping of players to lists of units, representing which units
    in which locations those players will have after resolving retreats. Will
    be equivalent to the entries in retreat_map, minus any disbanded units --
    and, of course, without any retreat requirements.
    """
    assert all(isinstance(command, RetreatCommand) for command in commands)
    retreaters = {(command.player.name, command.unit) for command in commands}
    valid_retreaters = set()
    for player in retreat_map.keys():
        valid_retreaters |= {
            (player, unit)
            for unit in retreat_map[player].keys()
            if retreat_map[player][unit] is not None
        }
    assert retreaters == valid_retreaters

    result_map = {player: set() for player in retreat_map}
    for player in retreat_map:
        for unit in retreat_map[player]:
            if retreat_map[player][unit] is None:
                result_map[player].add(unit)

    commands = list(filter(lambda c: isinstance(c, RetreatMoveCommand), commands))
    for command in commands:
        other_commands = list(filter(lambda c: c != command, commands))
        if all(command.destination != other_command.destination for other_command in other_commands):
            result_map[command.player.name].add(Unit(command.unit.unit_type, command.destination))

    return result_map
