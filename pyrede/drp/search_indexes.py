# -*- coding: utf-8 -*-
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
"""
Fulltext indexing with haystack
"""
from haystack import site
from haystack.indexes import SearchIndex
from haystack.fields import CharField
from pyrede.drp.models import Package


class PackageIndex(SearchIndex):
    """
    Fulltext indexing for PyPI packages
    """
    text = CharField(document=True, use_template=True)
    name = CharField(model_attr='name')

    def get_model(self):
        return Package

site.register(Package, PackageIndex)
