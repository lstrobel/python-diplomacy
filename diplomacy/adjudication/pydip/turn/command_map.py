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

from collections import defaultdict

from diplomacy.adjudication.pydip.player.command.command import ConvoyMoveCommand, ConvoyTransportCommand, MoveCommand, \
    SupportCommand


class CommandMap:
    """ territory -> MoveCommand[], representing commands with destination at key territory """
    _attacker_map = None
    """ territory -> ConvoyMoveCommand[], representing commands with destination at key territory """
    _convoy_attacker_map = None
    """ (source, dest) -> ConvoyTransportCommand[], representing transport commands from source to dest territories """
    _transport_map = None
    """ (source, dest) -> SupportCommand[], representing supports of units attacking from source to dest territories """
    _support_map = None
    """ territory -> Command, representing command for unit originating at key territory """
    _home_map = None

    _game_map = None

    """ Builds CommandMap from provided Command[] """

    def __init__(self, game_map, commands):
        self._game_map = game_map
        self._attacker_map = defaultdict(list)
        self._convoy_attacker_map = defaultdict(list)
        self._transport_map = defaultdict(list)
        self._support_map = defaultdict(list)
        self._home_map = dict()

        for command in commands:
            home_name = self._game_map.relevant_name_for_territory(command.unit.position)
            self._home_map[home_name] = command
            if isinstance(command, MoveCommand):
                destination_name = self._game_map.relevant_name_for_territory(command.destination)
                self._attacker_map[destination_name].append(command)
            elif isinstance(command, ConvoyMoveCommand):
                destination_name = self._game_map.relevant_name_for_territory(command.destination)
                self._convoy_attacker_map[destination_name].append(command)
            elif isinstance(command, ConvoyTransportCommand):
                source = self._game_map.relevant_name_for_territory(command.transported_unit.position)
                dest = self._game_map.relevant_name_for_territory(command.destination)
                self._transport_map[(source, dest)].append(command)
            elif isinstance(command, SupportCommand):
                source = self._game_map.relevant_name_for_territory(command.supported_unit.position)
                dest = self._game_map.relevant_name_for_territory(command.destination)
                self._support_map[(source, dest)].append(command)

    def get_attackers(self, territory_name):
        territory_name = self._game_map.relevant_name_for_territory(territory_name)
        return self._attacker_map[territory_name]

    def get_convoy_attackers(self, territory_name):
        territory_name = self._game_map.relevant_name_for_territory(territory_name)
        return self._convoy_attacker_map[territory_name]

    def get_convoy_transports(self, source_name, destination_name):
        source_name = self._game_map.relevant_name_for_territory(source_name)
        destination_name = self._game_map.relevant_name_for_territory(destination_name)
        return self._transport_map[(source_name, destination_name)]

    def get_supports(self, source_name, destination_name):
        source_name = self._game_map.relevant_name_for_territory(source_name)
        destination_name = self._game_map.relevant_name_for_territory(destination_name)
        return self._support_map[(source_name, destination_name)]

    def get_home_command(self, territory_name):
        territory_name = self._game_map.relevant_name_for_territory(territory_name)
        return self._home_map.get(territory_name, None)
