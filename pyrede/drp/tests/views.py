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
Unit tests for views in drp app
"""
from datetime import datetime
from django.test import TestCase
from django.http import HttpRequest
from pyrede.drp.models import Distribution
from pyrede.drp.models import DisPack
from pyrede.drp.models import Lookup
from pyrede.drp.models import Package
from pyrede.drp import views


class ViewsTests(TestCase):  # pylint: disable-msg=R0904
    """
    Test views independantly to urls
    """
    def setUp(self):
        """
        Init
        """
        Package.objects.all().delete()
        DisPack.objects.all().delete()
        Distribution.objects.all().delete()

    def test_lookup(self):
        """
        Do a lookup with existing datas
        """
        dist_a = Distribution.objects.create(name='Foo',
                                             version_name='Bar',
                                             version_number='1.2')

        dist_b = Distribution.objects.create(name='Foo',
                                             version_name='Lorem',
                                             version_number='1.1')

        Lookup.objects.create(distribution=dist_a,
                              content='aeHohee1\n')

        pack = Package.objects.create(name='aeHohee1',
                                      latest_version='1.0.0',
                                      link='http://www.foo.bar',
                                      description='lorem ipsum',
                                      last_update=datetime.now())

        DisPack.objects.create(name='aeHohee1',
                               version='1.0.0',
                               distribution=dist_a,
                               link='http://www.foo.bar',
                               package=pack,
                               package_version='1.0.0')

        DisPack.objects.create(name='aeHohee1',
                               version='1.0.0',
                               distribution=dist_b,
                               link='http://www.foo.bar',
                               package=pack,
                               package_version='1.0.0')

        result = views.lookup(pack)

        self.assertTrue(type(result) is dict)
        self.assertEqual(result['result'], 1)
        self.assertEqual(result['found'], 2)

    def test_lookup_alt(self):
        """
        More complicated lookup

        The distri_b is an unofficial distri of distri_a
        """
        dist_a = Distribution.objects.create(name='Foo',
                                             version_name='Bar',
                                             version_number='1.2')

        dist_b = Distribution.objects.create(name='Foo',
                                             version_name='Lorem',
                                             version_number='1.1',
                                             official=dist_a)

        Lookup.objects.create(distribution=dist_a,
                              content='aeHohee1\n')

        pack = Package.objects.create(name='aeHohee1',
                                      latest_version='1.0.0',
                                      link='http://www.foo.bar',
                                      description='lorem ipsum',
                                      last_update=datetime.now())

        DisPack.objects.create(name='aeHohee1',
                               version='1.0.0',
                               distribution=dist_a,
                               link='http://www.foo.bar',
                               package=pack,
                               package_version='1.0.0')

        DisPack.objects.create(name='aeHohee1',
                               version='1.0.0',
                               distribution=dist_b,
                               link='http://www.foo.bar',
                               package=pack,
                               package_version='1.0.0')

        result = views.lookup(pack)

        self.assertTrue(type(result) is dict)
        self.assertEqual(result['result'], 1)
        self.assertEqual(result['found'], 2)

    def test_analyze(self):
        """
        Call with POST datas, all good datas

        Assert : return a 302 to /analyze/id/ id of the created analyze
        """
        dist = Distribution.objects.create(name='Foo',
                                           version_name='Lorem',
                                           version_number='1.1')

        # prepare datas
        requ = HttpRequest()
        requ.method = 'POST'
        requ.META = {'HTTP_REFERER': 'FOO_SERVER_NAME'}
        requ.POST = {'content': 'fooname',
                     'distribution': str(dist.id)}

        #  action
        result = views.analyze(requ)
        #  asserts
        self.assertEqual(result.status_code, 302)  # pylint: disable-msg=E1103

    def test_analyze_fail(self):
        """
        Call with wrong datas

        The distribution id 1042 does not exists
        """
        # prepare datas
        requ = HttpRequest()
        requ.method = 'POST'
        requ.META = {'HTTP_REFERER': 'FOO_SERVER_NAME'}
        requ.POST = {'content': 'fooname',
                     'distribution': '1042'}

        #  action
        result = views.analyze(requ)
        #  asserts
        self.assertEqual(result.status_code, 200)  # pylint: disable-msg=E1103

    def test_analyze_fail(self):
        """
        Call with wrong datas

        The distribution id 1042 does not exists
        """
        # prepare datas
        requ = HttpRequest()
        requ.method = 'POST'
        requ.META = {'HTTP_REFERER': 'FOO_SERVER_NAME'}
        requ.POST = {'content': 'fooname',
                     'distribution': '1042'}

        #  action
        result = views.analyze(requ)
        #  asserts
        self.assertEqual(result.status_code, 200)  # pylint: disable-msg=E1103
