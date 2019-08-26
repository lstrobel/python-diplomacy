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


class Unit:
    """A unit that is placed in a diplomacy map"""

    def __init__(self, owner: str, type_: str):
        self.owner = owner
        self.type = type_

    def serialize(self):
        """Serialize this Unit as a dict for JSON"""
        return self.__dict__

    @classmethod
    def create_from_dict(cls, dict_):
        return cls(dict_['owner'], dict_['type'])
