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
Tasks for rosarks
"""
from rosarks import tasks as rosatasks
from rosarks.models import ConsolidateValue
from datetime import datetime
from datetime import timedelta
from datetime import date


def fetch_byid_dm(name, ref, value):
    """
    Consolidate the delta by month
    """
    # package_428_downloads_delta_month_201302

    timecode = '%Y%m'

    key = '{}_{}_{}_delta_month_{}'.format(name,
                                           ref,
                                           value,
                                           date.strftime(date.today(), timecode))

    vals = ConsolidateValue.objects.filter(ref=key)

    if len(vals) == 0:
        return (key, 0)
    else:
        return (key, vals)
