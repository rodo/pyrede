# -*- coding: utf-8 -*-  pylint: disable-msg=R0801
#
# Copyright (c) 2013 Rodolphe Quiédeville <rodolphe@quiedeville.org>
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from django.core.cache import cache


def stats():
    """
    Return stats of database

    Cached value are set by munin management command
    """
    pack = cache.get("stats_nb_pack")
    packversion = cache.get("stats_nb_packversion")
    dispack = cache.get("stats_nb_dispack")

    return {'stats_nb_pack': pack,
            'dispack': dispack}
