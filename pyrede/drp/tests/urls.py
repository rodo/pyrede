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
Unit tests for all urls

"""
from django.test import TestCase
from django.test import Client
from pyrede.drp.models import Distribution
from pyrede.drp.models import Lookup
from pyrede.drp.models import Package


class UrlsTests(TestCase):  # pylint: disable-msg=R0904
    """
    Test all available urls

    """
    def setUp(self):
        """
        Init
        """
        Package.objects.all().delete()

    def test_main(self):
        """
        The list of pypis packages
        """
        client = Client()
        response = client.get('/')

        self.assertContains(response, 'form', status_code=200)

    def test_pypilist(self):
        """
        The list of pypis packages
        """
        pack = Package.objects.create(name='aeHohee1',
                                      latest_version='1.0.0',
                                      link='http://www.foo.bar',
                                      description='lorem ipsum')

        client = Client()
        response = client.get('/pypis/')

        self.assertContains(response, pack.name, status_code=200)

    def test_json(self):
        """
        json lookup
        """
        pack = Package.objects.create(name='aeHohee1',
                                      latest_version='1.0.0',
                                      link='http://www.foo.bar',
                                      description='lorem ipsum')

        client = Client()
        response = client.get('/json/pypi/%s/' % pack.name)

        self.assertTrue(type(eval(response.content)) is dict)

    def test_json_doesnoteists(self):
        """
        json lookup on non existent package
        """
        client = Client()
        response = client.get('/json/pypi/this_package_doesnotexists/')

        self.assertTrue(type(eval(response.content)) is dict)
        self.assertEqual(response.content, '{"result": 0}')

    def test_about(self):
        """
        Teh about page
        """
        client = Client()
        response = client.get('/about/')

        self.assertContains(response, 'body', status_code=200)

    def test_analyze(self):
        """
        GET on an existing analyze
        """
        dist = Distribution.objects.create(name='Foo',
                                           version_name='Bar',
                                           version_number='1.2')

        lookup = Lookup.objects.create(distribution=dist,
                                       content='aeHohee1\n')

        pack = Package.objects.create(name='aeHohee1',
                                      latest_version='1.0.0',
                                      link='http://www.foo.bar',
                                      description='lorem ipsum')

        client = Client()
        response = client.get('/analyze/%s/' % lookup.id)

        self.assertContains(response, 'aeHohee1', status_code=200)

    def test_analyze_emptyget(self):
        """
        GET on an existing analyze with no lookup id
        """

        client = Client()
        response = client.get('/analyze/')

        self.assertEqual(response.status_code, 302)
