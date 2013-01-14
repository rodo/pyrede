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
import requests
import json
from datetime import datetime
from django.core.management.base import BaseCommand
from pyrede.provider.management.commands.utils import create_update_pack
from pyrede.provider.management.commands.utils import split_title

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    args = '<ircnick>'
    help = 'Import recursively all ogg file in a directory'

    def handle(self, *args, **options):
        nbp = 40
        if len(args) == 0:
            return 'Missing url'

        logger.debug('parse %s' % args[0])

        nbp = self.parse(args[0])

    def parse(self, package):

        url = "http://pypi.python.org/pypi"

        params= {':action': 'json',
                 'name': package}

        headers = {'content-type': 'application/json'}

        item = {}

        req = requests.get(url, params=params, headers=headers)
        datas = json.loads(req.content)
        version = datas['info']['version']
        item['description'] = datas['info']['description']
        item['link'] = datas['info']['package_url']
        logger.debug("import %s" % package)
        create_update_pack(item, package, version)

