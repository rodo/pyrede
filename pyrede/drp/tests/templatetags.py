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
Unit tests for template tags
"""
from datetime import datetime
from django.test import TestCase
from django.core.cache import cache
from pyrede.drp.models import Distribution
from pyrede.drp.templatetags.distrostats import distro_nb_package


class TemplateTagsTests(TestCase):  # pylint: disable-msg=R0904
    """
    Test templatetags
    """
    def setUp(self):
        """
        Init
        """
        cache.clear()
        Distribution.objects.all().delete()

    def test_dnp(self):
        """
        Do the first lookup
        """
        dist_a = Distribution.objects.create(name='Foo',
                                             version_name='Bar',
                                             version_number='1.2')

        result = distro_nb_package(dist_a.id)

        self.assertEqual(result, "0")

    def test_dnp_snd(self):
        """
        Do the first lookup
        """
        dist_a = Distribution.objects.create(name='Foo',
                                             version_name='Bar',
                                             version_number='1.2')

        key = "stats_nb_dispack_distro_{}".format(dist_a.id)
        cache.set(key, 42)
        # do 2 calls to fill the cache
        result = distro_nb_package(dist_a.id)
        result = distro_nb_package(dist_a.id)

        self.assertEqual(result, "42")
