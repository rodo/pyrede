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
from django.conf import settings
from django.core.management.base import BaseCommand
from pyrede.provider.utils.debian import lookup_latest_version
from pyrede.drp.models import DisPack
from pyrede.drp.models import Package
from pyrede.drp.models import Distribution
from pyrede.provider.tasks import sendmail_admin

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Lookup for updates in debian, send mail new version'

    def handle(self, *args, **options):
        """
        Handle the command
        """
        dispacks = DisPack.objects.all()

        for pack in dispacks:
            self.update_pack(pack)


    def update_pack(self, pack):
        stable = lookup_latest_version(pack.name, "stable")
        testing = lookup_latest_version(pack.name, "testing")

        if testing:
            print "{} testing {}".format(pack.name, testing)
            self.update(pack, 'Wheezy', testing)

        if stable:
            print "{} stable {}".format(pack.name, stable)
            self.update(pack, 'Squeeze', stable)

    def update(self, package, dist, version):
        """
        Update the package in database

        TODO Finish name detection
        """
        data = Distribution.objects.filter(version_name=dist)

        if len(data) == 1:
            if package.distribution.id == data[0].id:
                if version != package.version:
                    subject = "{} update  {}".format(package.name, version)
                    body = "http:/pyrede.quiedeville.org/pypi/{}/".format(package.name)
                    sendmail_admin.delay(subject, body)
                else:
                    print "{} is up to date  {}".format(package.name, version)
            else:
                subject = "{} exists in {}".format(package.name, data[0])
                body = "http:/pyrede.quiedeville.org/pypi/{}/".format(package.name)
                sendmail_admin.delay(subject, body)
