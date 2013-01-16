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
from pyrede.provider.utils import create_update_pack
from pyrede.provider.utils import split_title

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
        datas = feedparser.parse(url)
        for item in datas['items']:
            try:
                name, version = split_title(item['title'])
                count = create_update_pack(item, name, version)
            except:
                logger.error("cant split %s" % item['title'])

        return count
