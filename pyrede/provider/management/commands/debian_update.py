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
from datetime import datetime
from django.core.management.base import BaseCommand
from pyrede.provider.utils.debian import lookup_latest_version
from pyrede.drp.models import DisPack
from pyrede.drp.models import Distribution

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    args = '<ircnick>'
    help = 'Import recursively all ogg file in a directory'

    def handle(self, *args, **options):
        """
        Handle the command
        """
        stable = lookup_latest_version(args[0], "stable")
        testing = lookup_latest_version(args[0], "testing")

        if testing:
            update(args[0], 'Wheezy', testing)

        if stable:
            update(args[0], 'Squeeze', stable)

    def update(package, dist, version):
        """
        Update the package in database
        """

        data = Distribution.objects.filter(version_name=dist)

        if len(data) == 1:
            dispack = DisPack.objects.filter(name=package,
                                             distribution=data[0])

            dispack.version = version
            dispack.save()