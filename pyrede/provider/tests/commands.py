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
Unit tests for Pyrede.Provider management commands

"""
from datetime import datetime
from django.test import TestCase
from django.core.management import call_command
from pyrede.drp.models import Package
from pyrede.drp.models import PackageVersion
from pyrede.provider.tests.httpserver import TestServer
from pyrede.provider.utils.main import split_title


class CommandsTests(TestCase):  # pylint: disable-msg=R0904
    """
    The unitests for Package model

    """
    def setUp(self):
        """
        Init
        """
        PackageVersion.objects.all().delete()
        Package.objects.all().delete()

    def test_create(self):
        """
        Create a Package
        """
        http = TestServer()
        http.start()
        url = 'http://127.0.0.1:%d/rss' % (http.port)

        call_command('import_latest', url)

        self.assertEqual(Package.objects.all().count(), 2)
        self.assertEqual(PackageVersion.objects.all().count(), 2)

    def test_update(self):
        """
        Test when a package will be update
        """
        pack = Package.objects.create(name='python-dikbm-adapter',
                                      latest_version='0.0.1',
                                      link='http://www.foo.bar',
                                      description='lorem ipsum',
                                      last_update=datetime(2012,12,12,7,50,2))

        PackageVersion.objects.create(package=pack,
                                      version='0.0.1',
                                      link='http://www.foo.bar',
                                      description='lorem ipsum',
                                      pubdate=datetime.today())

        http = TestServer()
        http.start()
        url = 'http://127.0.0.1:%d/rss' % (http.port)

        call_command('import_latest', url)

        self.assertEqual(Package.objects.all().count(), 2)
        self.assertEqual(PackageVersion.objects.all().count(), 3)

    def test_split_title_simple(self):
        """
        Split title
        """
        result = split_title("foo 1.0.0")
        self.assertEqual(result, ["foo", "1.0.0"])

    def test_split_title_double(self):
        """
        Split title
        """
        result = split_title("foo bar 1.0.0")
        self.assertEqual(result, ["foo bar", "1.0.0"])

    def test_split_title_triple(self):
        """
        Split title
        """
        result = split_title("foo bar lorem 1.0.0")
        self.assertEqual(result, ["foo bar lorem", "1.0.0"])
