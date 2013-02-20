#!/usr/bin/python
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
Consolidate statistics and print on stdout
"""
from django.core.management.base import BaseCommand
from django.db.models import Count
from django.core.cache import cache
from pyrede.drp.models import Package


class Command(BaseCommand):
    help = 'Consolidate statistics'

    def handle(self, *args, **options):
        """
        Handle the command
        """
        foos = Package.objects.annotate(num_pack=Count('pypstats')).filter(num_pack__gt=0).order_by('-num_pack')

        for pack in foos:
            self.stdout.write("{} {}\n".format(pack.name, pack.num_pack))
            cache.set("stats_nb_{}".format(pack.name), pack.num_pack)
