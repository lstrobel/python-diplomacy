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

import pytest

from diplomacy.adjudication.pydip.map.territory import CoastTerritory, LandTerritory, SeaTerritory


def test_coast_needs_land_parent():
    bad_parent = SeaTerritory('Black Sea')
    good_parent = LandTerritory('Sevastopol', ['Sevastopol Coast'])

    with pytest.raises(AssertionError):
        CoastTerritory('Test Fail Coast 1', bad_parent)

    with pytest.raises(AssertionError):
        CoastTerritory('Test Fail Coast 2', good_parent.coasts[0])

    """ expect this to create a coast without AssertionError """
    CoastTerritory('Test Success Coast', good_parent)
