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
Output stats for munin on stdout and set values in cache
"""
import logging
from django.core.management.base import BaseCommand
from django.core.cache import cache
from django.db.models import Count
from pyrede.drp.models import Package
from pyrede.drp.models import PackageVersion
from pyrede.drp.models import DisPack
from pyrede.drp.models import Distribution
from pyrede.drp.models import PackSubscr
from datetime import datetime
from datetime import timedelta


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    args = '<ircnick>'
    help = 'Import recursively all ogg file in a directory'

    def handle(self, *args, **options):
        """
        Handle the munin command
        """
        pack = Package.objects.all().count()
        dispack = DisPack.objects.all().count()
        packversion = PackageVersion.objects.all().count()
        packsub = PackSubscr.objects.all().count()

        lastmonth = datetime.now() - timedelta(days=30)
        freshm = PackageVersion.objects.filter(pubdate__gte=lastmonth).count()

        delta = datetime.now() - timedelta(days=1)
        freshday = PackageVersion.objects.filter(pubdate__gte=delta).count()

        self.stdout.write("%s.value %s\n" % ('package', pack))
        self.stdout.write("%s.value %s\n" % ('packageversion', packversion))
        self.stdout.write("%s.value %s\n" % ('dispack', dispack))
        self.stdout.write("%s.value %s\n" % ('packsub', packsub))
        self.stdout.write("%s.value %s\n" % ('version_last_month', freshm))
        self.stdout.write("%s.value %s\n" % ('version_last_day', freshday))

        cache.set("stats_nb_pack", pack)
        cache.set("stats_nb_packversion", packversion)
        cache.set("stats_nb_dispack", dispack)
        cache.set("stats_nb_packsub", packsub)

        for dat in Distribution.objects.annotate(np=Count('dispack')):
            cache.set("stats_nb_dispack_distro_{}".format(dat.id), dat.np)
