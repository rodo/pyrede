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
Update the most used packages
"""
import logging
from time import sleep
from django.core.management.base import BaseCommand
from pyrede.provider.utils.main import import_package
from pyrede.drp.models import Package
from rosarks.retrieve import fetch_byid_dm

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Update all package'

    def handle(self, *args, **options):
        """
        Handle the command
        """
        packs = Package.objects.filter()
        
        for pack in packs:
            logger.debug('parse %s' % pack.name)
            nbp = import_package(pack.name, True)
            sleep(1) # be smart
        
        packs = Package.objects.all()
        for pack in packs:
            val = fetch_byid_dm('package', pack.id, 'downloads')
            pack.pypi_downloadstm = val[1]
            pack.save()
