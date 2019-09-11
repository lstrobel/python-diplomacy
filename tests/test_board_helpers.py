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

from diplomacy import Board, Order, Unit

with open("/media/Storage/Projects/python-diplomacy/data/premade_boards/vanilla.json") as f:
    vanilla_board = Board(json.load(f))

with open("/media/Storage/Projects/python-diplomacy/data/premade_boards/vanilla.json") as f:
    test_board = Board(json.load(f))
    orders = [Order("Russia", "Warsaw", "move", "Galicia")]
    test_board.orders.extend(orders)
    test_board.resolve_orders()
    test_board.tiles[115].unit = Unit("France", "army")
    test_board.tiles[89].unit = Unit("France", "army")
    test_board.tiles[31].unit = Unit("France", "army")
    test_board.tiles[86].unit = Unit("France", "army")
    orders = [Order("Austria", "Vienna", "move", "Galicia"),
              Order("Austria", "Budapest", "support", "Galicia", "Vienna")]
    test_board.orders.extend(orders)
    test_board.resolve_orders()
    test_board.orders.append(Order("Russia", "Galicia", "retreat", "Ukraine"))
    test_board.resolve_orders()


@pytest.mark.parametrize('tile, player, distance', [(vanilla_board.tiles[29], "Germany", 0),
                                                    (vanilla_board.tiles[29], "Italy", 3),
                                                    (vanilla_board.tiles[79], "Germany", 1),
                                                    (vanilla_board.tiles[79], "England", 4),
                                                    (vanilla_board.tiles[30], "Germany", 0),
                                                    (vanilla_board.tiles[79], "Germany", 1),
                                                    (vanilla_board.tiles[68], "Italy", 0),
                                                    (vanilla_board.tiles[68], "Turkey", 3),
                                                    (vanilla_board.tiles[13], "Turkey", 6),
                                                    (vanilla_board.tiles[13], "Russia", 3),
                                                    (test_board.tiles[86], "France", 5)])
def test__distance_to_home_center(tile, player, distance):
    assert vanilla_board._distance_to_home_center(tile, player) == distance


@pytest.mark.parametrize('board, player, tile_id', [(test_board, "France", 86),
                                                    (test_board, "Germany", 57),
                                                    (test_board, "England", 46),
                                                    (vanilla_board, "England", 46),
                                                    (test_board, "Italy", 69),
                                                    (vanilla_board, "Italy", 69)])
def test__find_unit_to_disband(board, player, tile_id):
    assert board._find_unit_to_disband(player).id == tile_id
