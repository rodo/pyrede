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
from django.test import TestCase
from pyrede.drp.models import Package
from pyrede.drp.models import DisPack
from pyrede.drp.models import Distribution
from datetime import datetime


class DisPackTests(TestCase):  # pylint: disable-msg=R0904
    """
    The unitests for Package model

    """
    def setUp(self):
        """
        Init
        """
        Package.objects.all().delete()
        DisPack.objects.all().delete()

    def test_create(self):
        """
        Create a Package
        """
        dist = Distribution.objects.create(name='foodeb',
                                           version_name='sid',
                                           version_number='0')

        pack = Package.objects.create(name='foobar',
                                      latest_version='1.0.0',
                                      link='http://www.foo.bar',
                                      description='lorem ipsum',
                                      last_update=datetime.now())

        dispack = DisPack.objects.create(name='python-foo',
                                         version='1.1.2c',
                                         distribution=dist,
                                         package=pack,
                                         package_version='1.1.0')

        self.assertGreater(dispack.id, 0)

    def test_sender_create(self):
        """
        Create a Package
        """
        dist = Distribution.objects.create(name='foodeb',
                                           version_name='sid',
                                           version_number='0')

        pack = Package.objects.create(name='foobar',
                                      latest_version='1.0.0',
                                      link='http://www.foo.bar',
                                      description='lorem ipsum',
                                      last_update=datetime.now())

        DisPack.objects.create(name='python-foo',
                               version='1.1.2c',
                               distribution=dist,
                               package=pack,
                               package_version='1.1.0')

        result = Package.objects.get(pk=pack.id).nbdispack

        self.assertEqual(result, 1)

    def test_sender_delete(self):
        """
        a dispack is deleted
        """
        dist = Distribution.objects.create(name='foodeb',
                                           version_name='sid',
                                           version_number='0')

        pack = Package.objects.create(name='foobar',
                                      latest_version='1.0.0',
                                      link='http://www.foo.bar',
                                      description='lorem ipsum',
                                      nbdispack=1,
                                      last_update=datetime.now())

        dispack = DisPack.objects.create(name='python-foo',
                                         version='1.1.2c',
                                         distribution=dist,
                                         package=pack,
                                         package_version='1.1.0')

        # delete the dipack
        dispack.delete()

        result = Package.objects.get(pk=pack.id).nbdispack

        self.assertEqual(result, 0)

    def test_sender_update(self):
        """
        a dispack is updated
        """
        dist = Distribution.objects.create(name='foodeb',
                                           version_name='sid',
                                           version_number='0')

        pack = Package.objects.create(name='foobar',
                                      latest_version='1.0.0',
                                      link='http://www.foo.bar',
                                      description='lorem ipsum',
                                      nbdispack=1,
                                      last_update=datetime.now())

        dispack = DisPack.objects.create(name='python-foo',
                                         version='1.1.2c',
                                         distribution=dist,
                                         package=pack,
                                         package_version='1.1.0')

        dispack.name = 'foo-foo'
        dispack.save()

        result = Package.objects.get(pk=pack.id).nbdispack

        self.assertEqual(result, 1)

    def test_sender_url(self):
        """
        The url method
        """
        dist = Distribution.objects.create(name='foodeb',
                                           version_name='sid',
                                           version_number='0',
                                           query_link="qry_{}_{}")

        pack = Package.objects.create(name='foobar',
                                      latest_version='1.0.0',
                                      link='http://www.foo.bar',
                                      description='lorem ipsum',
                                      nbdispack=1,
                                      last_update=datetime.now())

        dispack = DisPack.objects.create(name='python-foo',
                                         source_name='foo',
                                         version='1.1.2c',
                                         distribution=dist,
                                         package=pack,
                                         package_version='1.1.0')

        url = "qry_foo_python-foo"

        self.assertEqual(dispack.url(), url)
