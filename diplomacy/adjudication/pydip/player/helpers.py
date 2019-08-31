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

from diplomacy.adjudication.pydip.map.territory import CoastTerritory, LandTerritory, SeaTerritory
from diplomacy.adjudication.pydip.player.unit import UnitTypes


def unit_can_enter(game_map, unit, territory):
    if territory.name not in game_map.adjacency[unit.position]:
        return False
    else:
        return unit_type_can_enter(unit.unit_type, territory)


def unit_type_can_enter(unit_type, territory):
    if unit_type == UnitTypes.TROOP:
        return isinstance(territory, LandTerritory)
    elif unit_type == UnitTypes.FLEET:
        return isinstance(territory, SeaTerritory) or isinstance(territory, CoastTerritory)
    else:
        raise ValueError("Invalid UnitType: {}".format(unit_type))


def unit_can_support(game_map, unit, territory):
    """
    Being able to enter a coast or a land territory allows you to support,
    so we'll check each possible option
    """
    territories_to_check = [territory]
    if isinstance(territory, LandTerritory):
        territories_to_check.extend(territory.coasts)
    elif isinstance(territory, CoastTerritory):
        territories_to_check.append(territory.parent)
        territories_to_check.extend(territory.parent.coasts)

    return any(unit_can_enter(game_map, unit, to_check) for to_check in territories_to_check)


def territory_is_convoy_compatible(territory):
    return isinstance(territory, LandTerritory) and len(territory.coasts) > 0
