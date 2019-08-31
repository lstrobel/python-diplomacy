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

import os

dirname = os.path.dirname(os.path.abspath(__file__))
IMAGE_NAMES = os.path.join(dirname, '../../data/visualization/mapNames.png')
IMAGE_MAP = os.path.join(dirname, '../../data/visualization/in.png')
IMAGE_ARMY = os.path.join(dirname, '../../data/visualization/army.png')
IMAGE_FLEET = os.path.join(dirname, '../../data/visualization/fleet.png')
IMAGE_MASK = os.path.join(dirname, '../../data/visualization/mask.png')
IMAGE_OUTLINE = os.path.join(dirname, '../../data/visualization/outline.png')
IMAGE_DIS = os.path.join(dirname, '../../data/visualization/dis.png')
INDEX_COLOR = 0
INDEX_TYPEMASK = 1
INDEX_COORD = 2

COLOR_OCEAN = (197, 223, 234)
COLOR_NEUTRAL = (226, 198, 158)
COLOR_ENGLAND = (239, 196, 228)
COLOR_GERMANY = (160, 138, 117)
COLOR_AUSTRIA = (196, 143, 133)
COLOR_RUSSIA = (168, 126, 159)
COLOR_TURKEY = (234, 234, 175)
COLOR_FRANCE = (121, 175, 198)
COLOR_ITALY = (164, 196, 153)
LAND = 0x1 << 1
SEA = 0x1 << 2
SPECIAL = 0x1 << 3


def is_land(loc):
    return DIP[loc][0][INDEX_TYPEMASK] & LAND


def is_coast_or_sea(loc):
    return DIP[loc][0][INDEX_TYPEMASK] & SEA


def is_special(loc):
    return DIP[loc][0][INDEX_TYPEMASK] & SPECIAL


def find_borders(loc):
    return DIP[loc][1]


DIP = {
    'spa_nc': (((250, 0, 0), SEA | SPECIAL, (138, 651)), ('por', 'mao', 'gas')),
    'spa_sc': (((250, 0, 0), SEA | SPECIAL, (188, 836)), ('por', 'wes', 'lyo', 'mar')),
    'bul_nc': (((90, 0, 0), SEA | SPECIAL, (788, 746)), ('rum', 'bla', 'con')),
    'bul_sc': (((90, 0, 0), SEA | SPECIAL, (740, 818)), ('con', 'gre', 'aeg')),
    'stp_nc': (((0, 200, 0), SEA | SPECIAL, (922, 88)), ('bar', 'nor')),
    'stp_sc': (((0, 200, 0), SEA | SPECIAL, (754, 324)), ('fin', 'bot', 'lvn')),
    'spa': (((250, 0, 0), LAND | SPECIAL, (190, 754)), ('por', 'gas', 'mar')),
    'por': (((0, 0, 50), LAND | SEA, (82, 746)), ('spa', 'mao')),
    'naf': (((0, 0, 60), LAND | SEA, (192, 931)), ('tun', 'wes', 'mao')),
    'tun': (((0, 0, 70), LAND | SEA, (412, 936)), ('naf', 'wes', 'tyr', 'ion')),
    'gre': (((0, 0, 130), LAND | SEA, (679, 873)), ('ion', 'aeg', 'ser', 'bul', 'alb')),
    'bul': (((90, 0, 0), LAND | SPECIAL, (729, 762)), ('gre', 'con', 'ser', 'rum')),
    'alb': (((80, 0, 0), LAND | SEA, (635, 812)), ('gre', 'ion', 'adr', 'ser', 'tri')),
    'ser': (((70, 0, 0), LAND, (650, 773)), ('alb', 'gre', 'bul', 'rum', 'bud', 'tri')),
    'rum': (((100, 0, 0), LAND | SEA, (766, 706)), ('bul', 'bla', 'sev', 'bud', 'ukr', 'gal')),
    'con': (((110, 0, 0), LAND | SEA, (802, 832)), ('bla', 'bul', 'smy', 'ank', 'aeg')),
    'smy': (((0, 0, 110), LAND | SEA, (833, 891)), ('con', 'ank', 'aeg', 'eas', 'syr', 'arm')),
    'ank': (((0, 0, 100), LAND | SEA, (952, 817)), ('con', 'smy', 'arm', 'bla')),
    'arm': (((0, 0, 90), LAND | SEA, (1122, 828)), ('syr', 'bla', 'ank', 'smy', 'sev')),
    'syr': (((0, 0, 80), LAND | SEA, (1133, 943)), ('arm', 'smy', 'eas')),
    'sev': (((0, 180, 0), LAND | SEA, (897, 586)), ('bla', 'arm', 'rum', 'ukr', 'mos')),
    'ruh': (((0, 60, 0), LAND, (439, 548)), ('bel', 'mun', 'kie', 'hol', 'bur', 'pic')),
    'ven': (((120, 0, 0), LAND | SEA, (487, 707)), ('tri', 'trl', 'pie', 'tus', 'apu', 'adr')),
    'tus': (((160, 0, 0), LAND | SEA, (470, 748)), ('pie', 'ven', 'apu', 'rom', 'tyr', 'lyo')),
    'rom': (((150, 0, 0), LAND | SEA, (510, 802)), ('tus', 'nap', 'apu', 'ven', 'tyr')),
    'nap': (((140, 0, 0), LAND | SEA, (552, 846)), ('tyr', 'ion', 'apu', 'rom')),
    'apu': (((130, 0, 0), LAND | SEA, (578, 821)), ('ion', 'adr', 'nap', 'rom', 'ven')),
    'ukr': (((0, 170, 0), LAND, (765, 565)), ('sev', 'mos', 'war', 'gal', 'rum')),
    'lvn': (((0, 160, 0), LAND | SEA, (709, 432)), ('stp', 'mos', 'war', 'pru', 'bot', 'bal')),
    'mos': (((0, 190, 0), LAND, (884, 426)), ('stp', 'lvn', 'war', 'ukr', 'sev')),
    'stp': (((0, 200, 0), LAND | SEA, (966, 202)), ('mos', 'lvn', 'fin', 'nor', 'bar')),
    'fin': (((0, 150, 0), LAND | SEA, (695, 226)), ('stp', 'nor', 'swe', 'bot')),
    'swe': (((0, 140, 0), LAND | SEA, (577, 257)), ('nor', 'fin', 'bal', 'bot', 'ska', 'den')),
    'nor': (((0, 130, 0), LAND | SEA, (510, 266)), ('swe', 'stp', 'fin', 'bar', 'nwg', 'nth', 'ska')),
    'den': (((0, 120, 0), LAND | SEA, (495, 409)), ('swe', 'bal', 'ska', 'nth', 'hel', 'kie')),
    'war': (((0, 210, 0), LAND, (654, 541)), ('lvn', 'pru', 'mos', 'ukr', 'gal', 'sil')),
    'sil': (((0, 80, 0), LAND, (579, 537)), ('ber', 'pru', 'war', 'gal', 'boh', 'mun')),
    'mun': (((0, 70, 0), LAND, (478, 587)), ('ruh', 'kie', 'ber', 'sil', 'boh', 'trl', 'bur')),
    'trl': (((50, 0, 0), LAND, (530, 634)), ('mun', 'boh', 'vie', 'tri', 'ven', 'pie')),
    'tri': (((60, 0, 0), LAND | SEA, (571, 707)), ('trl', 'vie', 'bud', 'ser', 'alb', 'adr', 'ven')),
    'pie': (((170, 0, 0), LAND | SEA, (428, 687)), ('trl', 'ven', 'tus', 'lyo', 'mar')),
    'mar': (((180, 0, 0), LAND | SEA, (363, 692)), ('gas', 'bur', 'pie', 'lyo', 'spa', 'spa_sc')),
    'bur': (((200, 0, 0), LAND, (388, 625)), ('par', 'pic', 'bel', 'ruh', 'mun', 'mar', 'gas')),
    'gas': (((190, 0, 0), LAND | SEA, (297, 667)), ('bre', 'par', 'bur', 'mar', 'spa', 'spa_nc', 'mao')),
    'par': (((210, 0, 0), LAND, (334, 606)), ('pic', 'bur', 'gas', 'bre')),
    'bre': (((220, 0, 0), LAND | SEA, (281, 574)), ('eng', 'pic', 'par', 'gas', 'mao')),
    'pic': (((230, 0, 0), LAND | SEA, (350, 553)), ('eng', 'bel', 'ruh', 'bur', 'par', 'bre')),
    'bud': (((0, 230, 0), LAND, (660, 664)), ('gal', 'rum', 'ser', 'tri', 'vie')),
    'vie': (((0, 240, 0), LAND, (588, 630)), ('boh', 'gal', 'bud', 'tri', 'trl')),
    'boh': (((0, 250, 0), LAND, (553, 581)), ('sil', 'gal', 'vie', 'tri', 'trl', 'mun')),
    'gal': (((0, 220, 0), LAND, (680, 593)), ('war', 'ukr', 'rum', 'bud', 'vie', 'boh', 'sil')),
    'pru': (((0, 90, 0), LAND | SEA, (602, 485)), ('bal', 'lvn', 'war', 'sil', 'ber')),
    'ber': (((0, 100, 0), LAND | SEA, (541, 472)), ('bal', 'pru', 'sil', 'mun', 'kie')),
    'kie': (((0, 110, 0), LAND | SEA, (477, 497)), ('hel', 'den', 'ber', 'mun', 'ruh', 'hol')),
    'hol': (((0, 50, 0), LAND | SEA, (422, 489)), ('nth', 'hel', 'kie', 'ruh', 'bel')),
    'bel': (((240, 0, 0), LAND | SEA, (392, 525)), ('nth', 'hol', 'ruh', 'bur', 'pic', 'eng')),
    'edi': (((0, 0, 180), LAND | SEA, (328, 335)), ('nwg', 'nth', 'yor', 'lvp', 'cly')),
    'yor': (((0, 0, 160), LAND | SEA, (340, 427)), ('edi', 'nth', 'lon', 'wal', 'lvp')),
    'lvp': (((0, 0, 170), LAND | SEA, (312, 400)), ('cly', 'edi', 'yor', 'lon', 'wal', 'iri', 'nao')),
    'lon': (((0, 0, 140), LAND | SEA, (352, 481)), ('yor', 'nth', 'eng', 'wal')),
    'wal': (((0, 0, 150), LAND | SEA, (289, 463)), ('lvp', 'yor', 'lon', 'eng', 'iri')),
    'cly': (((0, 0, 190), LAND | SEA, (297, 331)), ('nao', 'nwg', 'edi', 'lvp')),
    # begin oceans
    'iri': (((0, 0, 170), SEA, (200, 477)), ('lvp', 'wal', 'eng', 'mao', 'nao')),
    'eng': ((COLOR_OCEAN, SEA, (282, 526)), ('wal', 'lon', 'nth', 'bel', 'pic', 'bre', 'mao', 'iri')),
    'bla': ((COLOR_OCEAN, SEA, (917, 733)), ('sev', 'arm', 'ank', 'con', 'bul_nc', 'rum')),
    'nao': ((COLOR_OCEAN, SEA, (104, 217)), ('nwg', 'cly', 'iri', 'mao')),
    'eas': ((COLOR_OCEAN, SEA, (848, 961)), ('aeg', 'smy', 'syr', 'ion')),
    'aeg': ((COLOR_OCEAN, SEA, (749, 903)), ('bul_sc', 'con', 'smy', 'eas', 'ion', 'gre')),
    'ion': ((COLOR_OCEAN, SEA, (589, 942)), ('adr', 'alb', 'gre', 'aeg', 'eas', 'tun', 'tyr', 'nap')),
    'tyr': ((COLOR_OCEAN, SEA, (465, 836)), ('lyo', 'tus', 'rom', 'nap', 'ion', 'tun', 'wes')),
    'adr': ((COLOR_OCEAN, SEA, (553, 763)), ('tri', 'alb', 'ion', 'apu', 'ven')),
    'lyo': ((COLOR_OCEAN, SEA, (360, 765)), ('mar', 'pie', 'tus', 'tyr', 'wes', 'spa_sc')),
    'wes': ((COLOR_OCEAN, SEA, (302, 843)), ('spa_sc', 'lyo', 'tyr', 'ion', 'tun', 'naf')),
    'mao': ((COLOR_OCEAN, SEA, (78, 577)), ('nao', 'iri', 'eng', 'bre', 'gas', 'spa_nc', 'por', 'wes', 'naf')),
    'nth': (
        (COLOR_OCEAN, SEA, (403, 383)), ('nwg', 'nor', 'ska', 'den', 'hel', 'hol', 'bel', 'eng', 'lon', 'yor', 'edi')),
    'nwg': ((COLOR_OCEAN, SEA, (427, 105)), ('bar', 'nor', 'nth', 'edi', 'cly')),
    'ska': ((COLOR_OCEAN, SEA, (501, 361)), ('nor', 'swe', 'den', 'nth')),
    'hel': ((COLOR_OCEAN, SEA, (447, 442)), ('nth', 'den', 'kie', 'hol')),
    'bal': ((COLOR_OCEAN, SEA, (610, 428)), ('swe', 'bot', 'lvn', 'pru', 'ber', 'kie', 'den')),
    'bot': ((COLOR_OCEAN, SEA, (647, 321)), ('swe', 'fin', 'stp', 'lvn', 'bal')),
    'bar': ((COLOR_OCEAN, SEA, (838, 36)), ('nwg', 'stp', 'nor')),
}

UNALIGNED = ['spa', 'por', 'naf', 'tun', 'hol', 'bel', 'nor', 'swe', 'den', 'rum', 'bul', 'ser', 'alb', 'gre']
DEFAULT_ENGLAND = ['cly', 'yor', 'lon', 'wal', 'lvp', 'edi']
DEFAULT_FRANCE = ['bre', 'par', 'bur', 'pic', 'gas', 'mar']
DEFAULT_GERMANY = ['kie', 'ber', 'pru', 'sil', 'mun', 'ruh']
DEFAULT_AUSTRIA = ['boh', 'vie', 'tri', 'bud', 'gal', 'trl']
DEFAULT_ITALY = ['pie', 'ven', 'tus', 'rom', 'nap', 'apu']
DEFAULT_TURKEY = ['con', 'ank', 'smy', 'syr', 'arm']
DEFAULT_RUSSIA = ['fin', 'stp', 'mos', 'sev', 'ukr', 'war', 'lvn']
SUPPLY_CENTERS = ['stp', 'mos', 'sev', 'war', 'con', 'ank', 'smy', 'ven', 'rom', 'nap', 'vie', 'tri', 'bud', 'kie',
                  'ber', 'mun', 'bre', 'par', 'mar', 'lon', 'lvp', 'edi', 'spa', 'por', 'tun', 'hol', 'bel', 'nor',
                  'swe', 'den', 'rum', 'bul', 'ser', 'gre']
