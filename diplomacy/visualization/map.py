#  python-diplomacy is a tool for exploring the game diplomacy in python.
#  Copyright (C) 2019 davidoskky
#  Copyright (C) 2019 Lukas Strobel
#
#  The following code is a derivative work of the code from davidoskky's diplomacy-tactical-map,
#  which is licensed AGPLv3. This code therefore is also licensed under the terms
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

import math

from PIL import Image, ImageDraw

from diplomacy.visualization.data import *


class Context:
    nation = None


std_width = 3
std_length = 20


def context(n):
    Context.nation = n


def line(draw, c, width=1, fill='#ffffff'):
    for i in range(1, width + 1):
        dx, dy = 0, i - width / 2
        draw.line((c[0] + dx, c[1] + dy, c[2] + dx, c[3] + dy), width=1, fill=fill)
    for i in range(1, width + 1):
        dx, dy = i - width / 2, 0
        draw.line((c[0] + dx, c[1] + dy, c[2] + dx, c[3] + dy), width=1, fill=fill)


def arrow(img, oldcoord, coord, color, noarrow=False, extrawidth=0):
    w = std_width + extrawidth
    draw = ImageDraw.Draw(img)
    x = coord[0] - oldcoord[0]
    y = coord[1] - oldcoord[1]
    length = math.sqrt(x ** 2 + y ** 2)
    ux = x / length
    uy = y / length
    x = ux * -std_length
    y = uy * -std_length
    coord = (coord[0] - ux * 3, coord[1] - uy * 3)
    x1 = math.cos(.5) * x - math.sin(.5) * y
    y1 = math.sin(.5) * x + math.cos(.5) * y
    x2 = math.cos(-.5) * x - math.sin(-.5) * y
    y2 = math.sin(-.5) * x + math.cos(-.5) * y
    line(draw, oldcoord + coord, width=w, fill=color)
    if not noarrow:
        line(draw, coord + (x1 + coord[0], y1 + coord[1]), width=w, fill=color)
        line(draw, coord + (x2 + coord[0], y2 + coord[1]), width=w, fill=color)


def t_arrow(img, oldcoord, coord, color):
    draw = ImageDraw.Draw(img)
    line(draw, oldcoord + coord, width=std_width, fill=color)
    x = coord[0] - oldcoord[0]
    y = coord[1] - oldcoord[1]
    mx, my = midpoint(coord, (midpoint(coord, oldcoord)))
    length = math.sqrt(x ** 2 + y ** 2)
    ux = x / length
    uy = y / length
    x = ux * -std_length / 2
    y = uy * -std_length / 2
    x1 = math.cos(1.57) * x - math.sin(1.57) * y
    y1 = math.sin(1.57) * x + math.cos(1.57) * y
    x2 = math.cos(-1.57) * x - math.sin(-1.57) * y
    y2 = math.sin(-1.57) * x + math.cos(-1.57) * y
    orig = (x + mx, y + my)
    line(draw, orig + (x1 + orig[0], y1 + orig[1]), width=std_width, fill=color)
    line(draw, orig + (x2 + orig[0], y2 + orig[1]), width=std_width, fill=color)


def draw_x(img, oldcoord, coord, color):
    draw = ImageDraw.Draw(img)
    x = coord[0] - oldcoord[0]
    y = coord[1] - oldcoord[1]
    mx, my = midpoint(coord, oldcoord)
    length = math.sqrt(x ** 2 + y ** 2)
    ux = x / length
    uy = y / length
    x = ux * -std_length / 2
    y = uy * -std_length / 2
    x1 = math.cos(.785) * x - math.sin(.785) * y
    y1 = math.sin(.785) * x + math.cos(.785) * y
    x2 = math.cos(-.785) * x - math.sin(-.785) * y
    y2 = math.sin(-.785) * x + math.cos(-.785) * y
    orig = (x + mx, y + my)
    line(draw, orig + (x1 + orig[0], y1 + orig[1]), width=2 + std_width, fill=color)
    line(draw, orig + (x2 + orig[0], y2 + orig[1]), width=2 + std_width, fill=color)
    line(draw, orig + (-x1 + orig[0], -y1 + orig[1]), width=2 + std_width, fill=color)
    line(draw, orig + (-x2 + orig[0], -y2 + orig[1]), width=2 + std_width, fill=color)


def write_substitution_image(file, out, table):
    img = Image.open(file).convert('RGBA')
    img_army = Image.open(IMAGE_ARMY).convert('RGBA')
    img_fleet = Image.open(IMAGE_FLEET).convert('RGBA')
    mask = Image.open(IMAGE_MASK).convert('RGBA')
    outline = Image.open(IMAGE_OUTLINE).convert('RGBA')
    buf = []

    def without_alpha(c):
        return c[0], c[1], c[2]

    i = 0
    for color in img.getdata():
        noalpha = without_alpha(color)
        i += 1
        if i % 2 ** 17 == 0:
            print('%i pixels filled' % i)
        if noalpha in table:
            buf.append(table[noalpha])
        else:
            buf.append(color)
    img.putdata(buf)
    if move_signs[0]:
        print('drawing movements...')
        for line in yellow:
            oldcoord = line[0]
            coord = line[1]
            arrow(img, oldcoord, coord, '#fcd116')
        for line in blue:
            oldcoord = line[0]
            coord = line[1]
            arrow(img, oldcoord, coord, '#22aadd', noarrow=True)
        for line in lines:
            oldcoord = line[0]
            coord = line[1]
            s = support.get(line[2], 0)
            arrow(img, oldcoord, coord, '#aa0000', extrawidth=s)
        for line in green:
            oldcoord = line[0]
            coord = line[1]
            t_arrow(img, oldcoord, coord, '#00dd00')
        for line in purple:
            oldcoord = line[0]
            coord = line[1]
            arrow(img, oldcoord, coord, '#ff00ff')
        for x in failed:
            draw_x(img, x[0], x[1], '#aa0000')
        for dis in ldislodge:
            x = Image.open(IMAGE_DIS).convert('RGBA')
            coord = DIP[dis][0][INDEX_COORD]
            coord = (coord[0] + 10, coord[1])
            img.paste(x, coord, x)
        for dis in ldestroy:
            x = Image.open(IMAGE_DIS).convert('RGBA')
            coord = DIP[dis][INDEX_COORD]
            coord = (coord[0], coord[1])
            img.paste(x, coord, x)
    print('drawing units...')
    for army in armies:
        if (army[0] in ldestroy or army[0] in ldislodge) and destroy_data[army[0]] == army[1]:
            continue
        coord = DIP[army[0]][0][INDEX_COORD]
        land_owner = get(army[0])
        army_owner = army[1]
        unit_img = img_army
        if land_owner != army_owner:
            img.paste(outline, (coord[0], coord[1] - 15), outline)
            img.paste(army[2], (coord[0] + 1, coord[1] - 14), mask)
        img.paste(unit_img, coord, unit_img)
    for fleet in fleets:
        if (fleet[0] in ldestroy or fleet[0] in ldislodge) and destroy_data[fleet[0]] == fleet[1]:
            continue
        coord = DIP[fleet[0]][0][INDEX_COORD]
        land_owner = get(fleet[0])
        fleet_owner = fleet[1]
        unit_img = img_fleet
        if land_owner != fleet_owner:
            img.paste(outline, (coord[0], coord[1] - 15), outline)
            img.paste(fleet[2], (coord[0] + 1, coord[1] - 14), mask)
        img.paste(unit_img, coord, unit_img)
    if move_signs[0]:
        for loc in create_army:
            star = Image.open('data/star.png').convert('RGBA')
            coord = DIP[loc][INDEX_COORD]
            img.paste(star, (coord[0] + 15, coord[1] - 13), star)
        for loc in create_fleet:
            star = Image.open('data/star.png').convert('RGBA')
            coord = DIP[loc][INDEX_COORD]
            img.paste(star, (coord[0] + 15, coord[1] - 8), star)
    text = Image.open(IMAGE_NAMES).convert('RGBA')
    img.paste(text, text)
    img.save(out, 'PNG')


ENGLAND = ('ENG', COLOR_ENGLAND)
RUSSIA = ('RUS', COLOR_RUSSIA)
FRANCE = ('FRA', COLOR_FRANCE)
ITALY = ('ITA', COLOR_ITALY)
TURKEY = ('TUR', COLOR_TURKEY)
GERMANY = ('GER', COLOR_GERMANY)
AUSTRIA = ('AUS', COLOR_AUSTRIA)
N_COLOR = 1
N_NAME = 0

init = {}
move_signs = [True]
armies = []
create_army = []
create_fleet = []
fleets = []
failed = []
blue = []
lines = []
purple = []
yellow = []
green = []
land = {}
occupied = set()
ldislodge = []
ldestroy = []
destroy_data = {}
support = {}


def disable_symbols():
    move_signs[0] = False


def check_army_can_go(loc):
    if not is_land(loc):
        print("An army cannot be on the ocean '%s'." % loc)
        raise SystemExit


def check_fleet_can_go(loc):
    if not is_coast_or_sea(loc):
        print("A fleet cannot be on '%s', which is landlocked." % loc)
        raise SystemExit


def check_army_can_support(loc):
    if not is_land(loc) and not is_special(loc):
        print("An army cannot support the ocean '%s'." % loc)
        raise SystemExit


def check_fleet_can_support(loc):
    if not is_coast_or_sea(loc) and not is_special(loc):
        print("A fleet cannot support '%s', which is landlocked." % loc)
        raise SystemExit


def lcheck(f):
    def g(*args):
        for loc in args:
            if isinstance(loc, str) and loc not in DIP:
                print("'%s' is an invalid location." % loc)
                if len(loc) > 0:
                    print('Suggestions:')
                    for k in DIP:
                        if k[0] == loc[0]:
                            print(' ' + k)
                raise SystemExit
        return f(*args)

    return g


def enhance(loc):
    if loc in support:
        support[loc] += 1
    else:
        support[loc] = 1


duplicates = []


def occupy(loc):
    loc = loc[:3]
    if loc in occupied:
        duplicates.append(loc)
    else:
        occupied.add(loc)


def assert_one_unit_per_loc():
    x = False
    for loc in duplicates:
        if loc not in ldislodge:
            print("You have already placed a unit at '%s'" % loc)
            x = True
    if x:
        raise SystemExit


def midpoint(a, b):
    return (a[0] + b[0]) / 2, (a[1] + b[1]) / 2


def unit_coords(t):
    a = DIP[t][0][INDEX_COORD]
    return a[0] + 13, a[1] + 8


def set_color(t, color):
    if not is_land(t):
        print("Cannot set color of the ocean '%s'" % t)
        raise SystemExit
    x = DIP[t]
    init[x[0][INDEX_COLOR]] = color


def get(t):
    return land[t] if t in land else None


@lcheck
def set_(t):
    land[t] = Context.nation[0]
    set_color(t, Context.nation[N_COLOR])


@lcheck
def army_hold(t):
    check_army_can_go(t)
    tmp = []
    tmp.append(t)
    tmp.append(Context.nation[0])
    tmp.append(Context.nation[1])
    # armies.append((t, Context.nation))
    armies.append(tmp)
    occupy(t)


@lcheck
def army_create(t):
    check_army_can_go(t)
    create_army.append(t)
    # armies.append((t, Context.nation))
    army_hold(t)


@lcheck
def fleet_create(t):
    check_fleet_can_go(t)
    create_fleet.append(t)
    fleet_hold(t)


@lcheck
def dislodge(t):
    ldislodge.append(t)
    destroy_data[t] = Context.nation


@lcheck
def destroy(t):
    ldestroy.append(t)
    destroy_data[t] = Context.nation[0]


@lcheck
def fleet_support_move(t, other, t2):
    check_fleet_can_go(t)
    check_fleet_can_support(t2)
    enhance(t2)
    other = unit_coords(other)
    dest = unit_coords(t2)
    dest = midpoint(dest, midpoint(other, dest))
    orig = unit_coords(t)
    yellow.append((orig, dest))
    fleet_hold(t)


@lcheck
def fleet_convoy(t, other, t2):
    check_fleet_can_go(t)
    check_fleet_can_support(other)
    check_fleet_can_support(t2)
    other = unit_coords(other)
    dest = unit_coords(t2)
    mp = midpoint(other, dest)
    dest = midpoint(mp, midpoint(dest, midpoint(other, dest)))
    orig = unit_coords(t)
    blue.append((orig, dest))
    fleet_hold(t)


@lcheck
def army_support_move(t, other, t2):
    check_army_can_go(t)
    check_army_can_support(t2)
    enhance(t2)
    other = unit_coords(other)
    dest = unit_coords(t2)
    dest = midpoint(dest, midpoint(other, dest))
    orig = unit_coords(t)
    yellow.append((orig, dest))
    army_hold(t)


@lcheck
def fleet_retreat(t, t2):
    check_fleet_can_go(t)
    check_fleet_can_go(t2)
    dest = unit_coords(t2)
    orig = unit_coords(t)
    purple.append((orig, dest))
    fleet_hold(t2)


@lcheck
def army_retreat(t, t2):
    check_army_can_go(t)
    check_army_can_go(t2)
    dest = unit_coords(t2)
    orig = unit_coords(t)
    purple.append((orig, dest))
    army_hold(t2)


@lcheck
def fleet_support_hold(t, t2):
    check_fleet_can_go(t)
    check_fleet_can_support(t2)
    dest = unit_coords(t2)
    orig = unit_coords(t)
    green.append((orig, dest))
    fleet_hold(t)


@lcheck
def army_support_hold(t, t2):
    check_army_can_go(t)
    check_army_can_support(t2)
    dest = unit_coords(t2)
    orig = unit_coords(t)
    green.append((orig, dest))
    army_hold(t)


@lcheck
def army_move(t, t2):
    check_army_can_go(t)
    check_army_can_go(t2)
    dest = unit_coords(t2)
    orig = unit_coords(t)
    lines.append((orig, dest, t2))
    army_hold(t2)


@lcheck
def fleet_move(t, t2):
    check_fleet_can_go(t)
    check_fleet_can_go(t2)
    dest = unit_coords(t2)
    orig = unit_coords(t)
    lines.append((orig, dest, t2))
    fleet_hold(t2)


@lcheck
def fleet_move_failed(t, t2):
    check_fleet_can_go(t)
    check_fleet_can_go(t2)
    dest = unit_coords(t2)
    orig = unit_coords(t)
    lines.append((orig, dest, t2))
    failed.append((orig, dest, t2))
    fleet_hold(t)


@lcheck
def army_move_failed(t, t2):
    check_army_can_go(t)
    check_army_can_go(t2)
    dest = unit_coords(t2)
    orig = unit_coords(t)
    lines.append((orig, dest, t2))
    failed.append((orig, dest, t2))
    army_hold(t)


@lcheck
def fleet_hold(t):
    check_fleet_can_go(t)
    tmp = [t, Context.nation[0], Context.nation[1]]
    # fleets.append((t, Context.nation))
    fleets.append(tmp)
    occupy(t)


for t in UNALIGNED:
    set_color(t, COLOR_NEUTRAL)
for t in DEFAULT_ENGLAND:
    set_color(t, COLOR_NEUTRAL)
for t in DEFAULT_GERMANY:
    set_color(t, COLOR_NEUTRAL)
for t in DEFAULT_FRANCE:
    set_color(t, COLOR_NEUTRAL)
for t in DEFAULT_ITALY:
    set_color(t, COLOR_NEUTRAL)
for t in DEFAULT_AUSTRIA:
    set_color(t, COLOR_NEUTRAL)
for t in DEFAULT_TURKEY:
    set_color(t, COLOR_NEUTRAL)
for t in DEFAULT_RUSSIA:
    set_color(t, COLOR_NEUTRAL)


def done(dir):
    assert_one_unit_per_loc()
    write_substitution_image(IMAGE_MAP, dir, init)
