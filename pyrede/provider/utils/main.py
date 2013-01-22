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
import requests
import json
import logging
from celery.task import task
from django.conf import settings
from django.template.loader import render_to_string
from django.core.cache import cache
from django.core.mail import send_mail
from datetime import datetime
from pyrede.drp.models import Package
from pyrede.drp.models import PackageVersion
from pyrede.drp.models import PackSubscr


logger = logging.getLogger(__name__)


def import_package(package, force=False):
    """
    Import a package from pypi
    """
    key = 'pypi_import_flag_{}'.format(package)
    if force:
        cache.delete(key)
    if cache.get(key) != None:
        logger.warning('package : [%s] was import less than 2 hours' % package)
    else:
        cache.set(key, 7200)
        logger.debug('try to import : %s' % package)
        url = "http://pypi.python.org/pypi"

        params= {':action': 'json', 'name': package}
        headers = {'content-type': 'application/json'}

        item = {}

        req = requests.get(url, params=params, headers=headers)
        if (req.ok):
            logger.debug("found : %s" % url)
            datas = json.loads(req.content)
            version = datas['info']['version']
            item['description'] = datas['info']['description']
            item['link'] = datas['info']['package_url']
            create_update_pack(item, package, version)
        else:
            logger.warning("not found : %s" % url)


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

        mail_subscribers(name)

    return count


def create_pack(item, name, version):
    logger.debug('create %s %s' % (name, version))

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
    """
    Update a package in database

    item : Array of string
    pack : Object Package
    version : string
    """
    logger.debug('package %s : update from %s to %s' % (pack.name,
                                                        pack.latest_version,
                                                        version))

    pack.latest_version = version
    pack.save()

    PackageVersion.objects.create(package=pack,
                                  version=version,
                                  link=item['link'],
                                  description=item['description'],
                                  pubdate=datetime.today())


def mail_subscribers(pack_name):
    """
    Send email to subscribers

    pack_name : string
    """
    packs = Package.objects.filter(name=pack_name)
    if len(packs) > 0:
        subscrs = PackSubscr.objects.filter(package=packs[0])
        logger.debug('package %s : found %d subscriber' % (pack_name,
                                                           len(subscrs)))
        for sub in subscrs:
            sendmail_subscriber.delay(pack_name, sub)


@task
def sendmail_subscriber(pack_name, subscr):
    """
    Send email to subscribers

    pack_name : string
    subscr : Object PackSubscr
    """
    logger.debug('package %s : sendmail to %s' % (pack_name,
                                                  subscr.email))
    parms = {'package': pack_name,
             'email': subscr.email,
             'uuid': subscr.uuid}
    body = render_to_string('emails/subscribers/update_body.txt', parms)
    subject = render_to_string('emails/subscribers/update_subject.txt', parms)

    send_mail(subject,
              body,
              settings.EMAIL_FROM,
              [subscr.email],
              fail_silently=True)
