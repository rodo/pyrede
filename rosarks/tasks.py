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
from celery.task import task
from rosarks.utils.deltas import Deltas
from rosarks.models import AtomicValue
from rosarks.models import ConsolidateValue


@task
def delta_bymonth(ref):
    """
    Consolidate the delta by month
    """


    queryset = AtomicValue.objects.filter(ref=ref)

    delt = Deltas()
    datas = []

    for obj in queryset:
        datas.append([obj.create, obj.value])

    result = delt.delta_bymonth(datas)

    key = result.keys()[0]

    keyc = "{}_delta_month_{}".format(ref, key)
    ConsolidateValue.objects.filter(ref=keyc).delete()
    cons = ConsolidateValue.objects.create(ref=keyc,
                                           value=result[key])

    return key, result[key]
