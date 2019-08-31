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

from diplomacy.adjudication.pydip.map.map import OwnershipMap
from diplomacy.adjudication.pydip.map.predefined import vanilla_dip
from diplomacy.adjudication.pydip.player.command.adjustment_command import AdjustmentCreateCommand, \
    AdjustmentDisbandCommand
from diplomacy.adjudication.pydip.player.player import Player
from diplomacy.adjudication.pydip.player.unit import Unit
from diplomacy.adjudication.pydip.test.command_helper import AdjustmentCommandType
from diplomacy.adjudication.pydip.turn.adjustment import calculate_adjustments, resolve_adjustment, \
    resolve_adjustment__validated


class AdjustmentHelper:
    def __init__(
            self,
            player_helpers,
            player_units=vanilla_dip.generate_starting_player_units(),
            owned_territories=vanilla_dip.generate_home_territories(),
            home_territories=vanilla_dip.generate_home_territories(),
            supply_map=vanilla_dip.generate_supply_center_map(),
    ):
        self.ownership_map = OwnershipMap(supply_map, owned_territories, home_territories)
        self.player_units = player_units
        self.ownership_map, self.adjustment_counts = calculate_adjustments(self.ownership_map, self.player_units)

        self.players = {
            player_helper.name: Player(
                player_helper.name,
                self.ownership_map.supply_map.game_map,
                _get_starting_configuration(player_units[player_helper.name]))
            for player_helper in player_helpers
        }
        self.commands = self._build_commands(player_helpers)

    def resolve(self):
        return resolve_adjustment(self.ownership_map, self.adjustment_counts, self.player_units, self.commands)

    def resolve__validated(self):
        return resolve_adjustment__validated(
            self.ownership_map,
            self.adjustment_counts,
            self.player_units,
            self.commands,
        )

    def _build_commands(self, player_helpers):
        commands = []
        for player_helper in player_helpers:
            player = self.players[player_helper.name]
            for command_helper in player_helper.command_helpers:
                commands.append(self._build_command(player, command_helper))
        return commands

    def _build_command(self, player, command):
        unit = Unit(command.unit_type, command.territory)
        if command.type == AdjustmentCommandType.CREATE:
            return AdjustmentCreateCommand(self.ownership_map, player, unit)
        if command.type == AdjustmentCommandType.DISBAND:
            return AdjustmentDisbandCommand(player, unit)
        raise ValueError("Invalid command type: {}".format(command.type))


def _get_starting_configuration(units):
    return [
        {'territory_name': unit.position, 'unit_type': unit.unit_type}
        for unit in units
    ]
