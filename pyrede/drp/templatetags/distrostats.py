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
from django import template
from django.core.cache import cache
register = template.Library()


@register.simple_tag
def distro_nb_package(distro_id):
    """
    Return nb of package in a distribution
    """

    key = "stats_nb_dispack_distro_{}".format(distro_id)
    if cache.get(key):
        value = cache.get(key)
    else:
        value = "0"
    return '{}'.format(value)
