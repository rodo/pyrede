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
import sys
import unittest
import urllib2
from datetime import datetime
from datetime import timedelta
from datetime import date


class Deltas():
    """Main parts"""
    def delta_byweek(self, datas):
        """Consolidate datas by week

        datas : Array(2)
          - datetime
          - value
        """
        code = "delta_week"
        timecode = '%Y%U'
        return self.delta_period(datas, code, timecode)

    def delta_bymonth(self, datas):
        """Consolidate datas by month

        datas : Array(2)
          - datetime
          - value
        """
        code = "delta_month"
        timecode = '%Y%m'
        return self.delta_period(datas, code, timecode)

    def delta_byyear(self, datas):
        """Consolidate datas by year

        datas : Array(2)
          - datetime
          - value
        """
        code = "delta_year"
        timecode = '%Y'
        return self.delta_period(datas, code, timecode)

    def delta_period(self, datas, code, timecode):
        """Consolidate datas by period

        datas : Array(2)
          - datetime
          - value
        code : string
        timecode : string

        Return : dict
        """
        datas.sort()
        old = datas[0]
        result = {}
        delta = 0
        for data in datas:
            if (date.strftime(data[0], timecode) == date.strftime(old[0], timecode)):
                delta = delta + (data[1] - old[1])
                key = '{}_{}'.format(code, date.strftime(data[0], timecode))
                result[key] = delta
            else:
                delta = delta + (data[1] - old[1])
                key = '{}_{}'.format(code, date.strftime(old[0], timecode))
                result[key] = delta
                delta = 0
            old=data
        return result
