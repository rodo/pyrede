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
from django.core.cache import cache
from pyrede.utils.reqparser import requ_parser
from pyrede.drp.utils import stats


class UtilsTests(TestCase):  # pylint: disable-msg=R0904
    """
    The unitests for Package model

    """

    def test_equal(self):
        """
        Parse with requirements ==
        """
        result = requ_parser("foo==1\n")
        attend = [['foo', '==', '1']]
        self.assertEqual(result, attend)

    def test_sup(self):
        """
        Parse with requirements >=
        """
        result = requ_parser("foo>=1.0\n")
        attend = [['foo', '>=', '1.0']]
        self.assertEqual(result, attend)

    def test_inf(self):
        """
        Parse with requirements =<
        """
        result = requ_parser("foo=<1.0\n")
        attend = [['foo', '=<', '1.0']]
        self.assertEqual(result, attend)

    def test_2lines(self):
        """
        Test with 2 lines
        """
        result = requ_parser("foo>=1.0\nDjango>=1.3.4")
        attend = [['foo', '>=', '1.0'],
                  ['Django', '>=', '1.3.4']]
        self.assertEqual(result, attend)

    def test_overlimit(self):
        """
        Test with 2 lines
        """
        result = requ_parser("foo>=1.0\nDjango>=1.3\ndateutil\argparse\n", 2)
        attend = [['foo', '>=', '1.0'],
                  ['Django', '>=', '1.3.4']]
        self.assertEqual(result, attend)

    def test_whitespace(self):
        """
        Whitespaces on line
        """
        result = requ_parser("foo bar\nDjango>=1.3.4\n")
        attend = [['foo'],
                  ['Django', '>=', '1.3.4']]
        self.assertEqual(result, attend)

    def test_nover(self):
        """
        Test with no version number
        """
        result = requ_parser("foo\nDjango>=1.3.4")
        attend = [['foo'],
                  ['Django', '>=', '1.3.4']]
        self.assertEqual(result, attend)

    def test_stats(self):
        """
        stats return a dict
        """
        cache.set("stats_nb_pack", 1)
        cache.set("stats_nb_packversion", 2)
        cache.set("stats_nb_dispack", 3)

        result = stats()

        attend = {'stats_nb_pack': 1,
                  'stats_nb_packbersion': 2,
                  'dispack': 3}

        self.assertEqual(result, attend)
