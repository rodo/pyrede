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
import requests
import json
from time import sleep
from django.core.management.base import BaseCommand
from pyrede.drp.models import Package

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    args = '<ircnick>'
    help = 'Import recursively all ogg file in a directory'

    def handle(self, *args, **options):
        """
        Handle the command
        """
        packs = Package.objects.all().order_by('summary')
        for pack in packs:
            key = 'pypi_import_flag_{}'.format(pack.name)

            url = "http://pypi.python.org/pypi"

            params = {':action': 'json', 'name': pack.name}
            headers = {'content-type': 'application/json',
                       'User-agent': 'Pyrede http://pyrede.quiedeville.org/about/'}

            item = {}

            sleep(2) # be smart
            req = requests.get(url, params=params, headers=headers)

            if (req.ok):
                print "found : %s" % pack.name
                datas = json.loads(req.content)

                try:
                    pack.summary = datas['info']['summary']
                    pack.save()
                except:
                    print "Error on save %s" % pack.name
            else:
                print "not found : %s" % url
