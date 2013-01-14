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
import last package
"""
import logging
import feedparser
from django.core.management.base import BaseCommand
from pyrede.drp.models import Package
from pyrede.drp.models import PackageVersion
from pyrede.drp.models import DisPack

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    args = '<ircnick>'
    help = 'Import recursively all ogg file in a directory'

    def handle(self, *args, **options):

        pack = Package.objects.all().count()
        dispack = DisPack.objects.all().count()
        packversion = Package.objects.all().count()
        print "%s.value %s" % ('package', pack)
        print "%s.value %s" % ('packageversion', packversion)
        print "%s.value %s" % ('dispack', dispack)
