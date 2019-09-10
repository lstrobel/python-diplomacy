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
import json

import pytest

from diplomacy import Board

with open("/media/Storage/Projects/python-diplomacy/data/premade_boards/vanilla.json") as f:
    vanilla_board = Board(json.load(f))


@pytest.mark.parametrize('tile, player, distance', [(vanilla_board.tiles[29], "Germany", 0),
                                                    (vanilla_board.tiles[29], "Italy", 3),
                                                    (vanilla_board.tiles[79], "Germany", 1),
                                                    (vanilla_board.tiles[79], "England", 4),
                                                    (vanilla_board.tiles[30], "Germany", 0),
                                                    (vanilla_board.tiles[79], "Germany", 1),
                                                    (vanilla_board.tiles[68], "Italy", 0),
                                                    (vanilla_board.tiles[68], "Turkey", 3),
                                                    (vanilla_board.tiles[13], "Turkey", 6),
                                                    (vanilla_board.tiles[13], "Russia", 3)])
def test__distance_to_home_center(tile, player, distance):
    assert vanilla_board._distance_to_home_center(tile, player) == distance
