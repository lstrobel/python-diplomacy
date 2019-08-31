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

from diplomacy.adjudication.pydip.map.predefined import vanilla_dip
from diplomacy.adjudication.pydip.player.command.retreat_command import RetreatDisbandCommand, RetreatMoveCommand
from diplomacy.adjudication.pydip.player.player import Player
from diplomacy.adjudication.pydip.test.command_helper import RetreatCommandType
from diplomacy.adjudication.pydip.turn.retreat import resolve_retreats


class RetreatHelper:
    def __init__(self, retreat_map, player_helpers, game_map=vanilla_dip.generate_map()):
        self.game_map = game_map
        self.retreat_map = retreat_map
        self.players = {
            player_helper.name: Player(player_helper.name, game_map, player_helper.get_starting_configuration())
            for player_helper in player_helpers
        }
        self.commands = self._build_commands(player_helpers)

    def resolve(self):
        return resolve_retreats(self.retreat_map, self.commands)

    def _build_commands(self, player_helpers):
        commands = []
        for player_helper in player_helpers:
            player = self.players[player_helper.name]
            for command_helper in player_helper.command_helpers:
                commands.append(self._build_command(player, command_helper))
        return commands

    def _build_command(self, player, command):
        unit = self._find_unit(command.unit)
        if command.command_type == RetreatCommandType.MOVE:
            return RetreatMoveCommand(self.retreat_map, player, unit, command.destination)
        if command.command_type == RetreatCommandType.DISBAND:
            return RetreatDisbandCommand(self.retreat_map, player, unit)
        raise ValueError("Invalid command type: {}".format(command.command_type))

    def _find_unit(self, territory):
        for player in self.players.values():
            for unit in player.units:
                if unit.position == territory:
                    return unit
        raise ValueError("Unable to find unit with position {}".format(territory))
