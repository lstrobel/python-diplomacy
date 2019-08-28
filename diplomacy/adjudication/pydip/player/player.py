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

from diplomacy.adjudication.pydip.map.territory import CoastTerritory
from diplomacy.adjudication.pydip.player.helpers import unit_type_can_enter
from diplomacy.adjudication.pydip.player.unit import Unit


class Player:
    """ String -- name identifier for player """
    name = None

    """ Map -- reference to game board """
    game_map = None

    """ Unit[] -- units owned by this player """
    units = None

    """ String{} -- names of starting territories for player """
    starting_territories = None

    """
     * name: String -- identifier for player
     * map:  Map    -- reference to game board
     * starting_configuration: Defines how player should begin configuration. List of structs of form:
        { 'territory_name': String, 'unit_type': UnitType? (None indicates no unit) }
        - Duplicate territory definitions are not allowed!
        - Coasts should be provided as starting territories for fleets, but the parent will be labeled as the actual
          starting territory.
    """

    def __init__(self, name, game_map, starting_configuration=None):
        if starting_configuration is None:
            starting_configuration = []
        self.name = name
        self.game_map = game_map
        self.starting_territories = set()
        self.units = []

        for config in starting_configuration:
            name = config['territory_name']
            unit_type = config['unit_type']
            assert name in self.game_map.name_map.keys()

            territory = self.game_map.name_map[name]
            starting_territory = territory.parent if isinstance(territory, CoastTerritory) else territory
            assert starting_territory.name in self.game_map.name_map.keys()
            assert starting_territory.name not in self.starting_territories
            self.starting_territories.add(starting_territory.name)

            if unit_type is None:
                continue
            assert unit_type_can_enter(unit_type, territory)

            self.units.append(Unit(unit_type, name))

        assert len(self.starting_territories) == len(starting_configuration)

    def __repr__(self):
        return self.name

    def __str__(self):
        return '{}: {}\n  Units: {}'.format(self.name, self.starting_territories, self.units)

    def find_unit(self, territory):
        return next(unit for unit in self.units if unit.position == territory)
