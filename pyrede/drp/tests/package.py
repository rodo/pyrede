# -*- coding: utf-8 -*-
#
# Copyright (c) 2012 Rodolphe Quiédeville <rodolphe@quiedeville.org>
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
Unit tests for Package

"""
from datetime import datetime
from django.test import TestCase
from pyrede.drp.models import Package


class PackageTests(TestCase):  # pylint: disable-msg=R0904
    """
    The unitests for Package model

    """
    def setUp(self):
        """
        Init
        """
        Package.objects.all().delete()

    def test_create(self):
        """
        Create a Package
        """
        pack = Package.objects.create(name='foobar',
                                      latest_version='1.0.0',
                                      link='http://www.foo.bar',
                                      description='lorem ipsum',
                                      last_update=datetime.now())

        self.assertGreater(pack.id, 0)

    def test_absolute_url(self):
        """
        The absolute url
        """
        pack = Package.objects.create(name='foobar',
                                      latest_version='1.0.0',
                                      link='http://www.foo.bar',
                                      description='lorem ipsum',
                                      last_update=datetime.now())

        url = "/pypi/foobar/"

        self.assertEqual(pack.get_absolute_url(), url)

    def test_string(self):
        """
        The absolute url
        """
        pack = Package.objects.create(name='foobar',
                                      latest_version='1.0.1',
                                      link='http://www.foo.bar',
                                      description='lorem ipsum',
                                      last_update=datetime.now())

        self.assertEqual('{}'.format(pack), "foobar 1.0.1")
