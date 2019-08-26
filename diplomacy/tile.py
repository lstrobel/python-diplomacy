#  python-diplomacy is a tool for exploring the game diplomacy in python.
#  Copyright (C) 2019 Lukas Strobel
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

from diplomacy.unit import Unit


class Tile:
    """A board tile, with information about its owner and the unit on it"""

    def __init__(self, id_: int, aliases: dict, equivalencies: list, adjacencies: list, is_supply_center=False,
                 is_ocean=False, is_coast=False, owner: str = None, unit: Unit = None):
        self.id = id_
        self.aliases = aliases
        self.equivalencies = equivalencies
        self.adjacencies = adjacencies
        self.is_supply_center = is_supply_center
        self.is_ocean = is_ocean
        self.is_coast = is_coast
        self.owner = owner
        self.unit = unit

    def serialize(self):
        """Serialize this Tile as a dict for JSON"""
        equivalencies = []
        for equivalence in self.equivalencies:
            equivalencies.append(equivalence.id)
        adjacencies = []
        for adjacency in self.adjacencies:
            adjacencies.append(adjacency.id)
        unit = self.unit.serialize() if self.unit is not None else None
        return {'id': self.id,
                'aliases': self.aliases,
                'equivalencies': equivalencies,
                'adjacencies': adjacencies,
                'is_supply_center': self.is_supply_center,
                'is_ocean': self.is_ocean,
                'is_coast': self.is_coast,
                'owner': self.owner,
                'unit': unit}

    @classmethod
    def create_from_dict(cls, dict_):
        unit = Unit.create_from_dict(dict_['unit']) if dict_['unit'] is not None else None
        return cls(dict_['id'], dict_['aliases'], dict_['equivalencies'], dict_['adjacencies'],
                   dict_['is_supply_center'], dict_['is_ocean'], dict_['is_coast'], dict_['owner'], unit)
