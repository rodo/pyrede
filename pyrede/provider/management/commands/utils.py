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
from datetime import datetime
from pyrede.drp.models import Package
from pyrede.drp.models import PackageVersion

logger = logging.getLogger(__name__)


def split_title(title):
    """
    Split the title
    """
    parts = title.split(' ')

    data = [" ".join(parts[:-1]), parts[-1]]

    return data


def create_update_pack(item, name, version):
    """
    Create or update package
    """
    exs = Package.objects.filter(name=name,
                                 latest_version=version)
    count = 0
    if len(exs) == 0:

        packs = Package.objects.filter(name=name)

        if len(packs) == 0:
            count += 1
            create_pack(item, name, version)
        else:
            count += 1
            update_pack(item, packs[0], version)

    return count


def create_pack(item, name, version):
    logger.debug('add %s %s' % (name, version))

    pack = Package.objects.create(name=name,
                                  latest_version=version,
                                  link=item['link'],
                                  description=item['description'][:2000])

    PackageVersion.objects.create(package=pack,
                                  version=version,
                                  link=item['link'],
                                  description=item['description'][:2000],
                                  pubdate=datetime.today())


def update_pack(item, pack, version):
    logger.debug('update %s from %s to %s' % (pack.name,
                                              pack.latest_version,
                                              version))

    pack.latest_version = version
    pack.save()

    PackageVersion.objects.create(package=pack,
                                  version=version,
                                  link=item['link'],
                                  description=item['description'],
                                  pubdate=datetime.today())