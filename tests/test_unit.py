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

import pytest

from diplomacy import Unit

test_data = [(Unit('Germany', 'army'), {'owner': 'Germany', 'type': 'army'}),
             (Unit('France', 'fleet'), {'owner': 'France', 'type': 'fleet'}),
             (Unit('Austria', 'army'), {'owner': 'Austria', 'type': 'army'})]


@pytest.mark.parametrize('unit, out_dict', test_data)
def test_serialize(unit, out_dict):
    """Test that units serialize correctly"""
    assert unit.serialize() == out_dict


@pytest.mark.parametrize('unit, dict_', test_data)
def test_create_from_dict(unit, dict_):
    """Test that units deserialize correctly"""
    assert Unit.create_from_dict(dict_).__dict__ == unit.__dict__
