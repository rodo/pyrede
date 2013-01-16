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
Unit tests for drp management commands

"""
from StringIO import StringIO
from django.core.management import call_command
from django.test import TestCase
from pyrede.drp.models import Package


class CommandTests(TestCase):  # pylint: disable-msg=R0904
    """
    The profile view

    """
    def setUp(self):
        """
        Init
        """
        Package.objects.all().delete()

    def test_munin(self):
        """
        cleansongs manage command
        """
        Package.objects.create(name='aeHohee1',
                               latest_version='1.0.0',
                               link='http://www.foo.bar',
                               description='lorem ipsum')

        attend = '\n'.join(['package.value 1',
                            'packageversion.value 0',
                            'dispack.value 0'])
        attend += '\n'

        content = StringIO()
        call_command('munin', stdout=content)
        content.seek(0)

        self.assertEqual(content.read(), attend)
