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
Unit tests for all urls

"""
from django.test import TestCase
from django.test import Client
from pyrede.drp.models import Package


class UrlsTests(TestCase):  # pylint: disable-msg=R0904
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
        pack = Package.objects.create(name='aeHohee1',
                                      latest_version='1.0.0',
                                      link='http://www.foo.bar',
                                      description='lorem ipsum')

        client = Client()
        response = client.get('/packages/')

        self.assertContains(response, pack.name, status_code=200)

