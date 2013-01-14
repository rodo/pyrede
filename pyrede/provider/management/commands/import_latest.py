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
from pyrede.drp.models import Package
from pyrede.drp.models import PackageVersion

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    args = '<ircnick>'
    help = 'Import recursively all ogg file in a directory'

    def handle(self, *args, **options):
        nbp = 40
        url = 'http://pypi.python.org/pypi?%3Aaction=rss'
        if len(args):
            url = args[0]

        logger.debug('parse %s' % url)

        while nbp == 40:
            nbp = self.parse(url)
            logger.debug('found %s package' % nbp)

    def parse(self, url):
        count = 0
        d = feedparser.parse(url)
        for item in d['items']:
            name, version = item['title'].split(' ')
            exs = Package.objects.filter(name=name,
                                         latest_version=version)

            if len(exs) == 0:

                packs = Package.objects.filter(name=name)

                if len(packs) == 0:
                    count +=1
                    self.create_pack(item, name, version)

                else:
                    count +=1
                    self.update_pack(item, packs[0], version)

        return count

    def create_pack(self, item, name, version):
        logger.debug('add %s %s' % (name, version))

        pack = Package.objects.create(name=name,
                                      latest_version=version,
                                      link=item['link'],
                                      description=item['description'])

        PackageVersion.objects.create(package=pack,
                                      version=version,
                                      link=item['link'],
                                      description=item['description'],
                                      pubdate=datetime.strptime(item['published'], '%d %b %Y %H:%M:%S %Z'))

    def update_pack(self, item, pack, version):
        logger.debug('update %s from %s to %s' % (pack.name,
                                                  pack.latest_version,
                                                  version))

        pack.latest_version = version
        pack.save()

        PackageVersion.objects.create(package=pack,
                                      version=version,
                                      link=item['link'],
                                      description=item['description'],
                                      pubdate=datetime.strptime(item['published'], '%d %b %Y %H:%M:%S %Z'))
