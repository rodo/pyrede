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
from rosarks.inserts import insert_atomic


logger = logging.getLogger(__name__)

def get_req(package):
    """
    Request info by json

    package : string, package name
    """
    url = "http://pypi.python.org/pypi"

    params = {':action': 'json', 'name': package}
    headers = {'content-type': 'application/json',
               'User-agent': 'Pyrede bot, contact http://pyrede.quiedeville.org/about/'}

    return requests.get(url, params=params, headers=headers)
    


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
        item = {}

        req = get_req(package)
        if (req.ok):
            logger.debug("found : %s" % package)
            datas = json.loads(req.content)
            version = datas['info']['version']
            item['description'] = datas['info']['description']
            item['link'] = datas['info']['package_url']
            create_update_pack(item, package, version, datas)
        else:
            logger.warning("not found : %s" % url)


def split_title(title):
    """
    Split the title
    """
    parts = title.split(' ')

    data = [" ".join(parts[:-1]), parts[-1]]

    return data


def create_update_pack(item, name, version, datas=None):
    """
    Create or update pypi package
    """
    logger.debug("create_update_pack {} {}".format(name, version))
    count = 0
    if name and version:
        exs = Package.objects.filter(name=name,
                                     latest_version=version)

        if len(exs) == 0:
            packs = Package.objects.filter(name=name)
            last_version = packs[0].latest_version

            if len(packs) == 0:
                count += 1
                create_pack(item, name, version, datas)
            else:
                count += 1
                update_pack(item, packs[0], version, datas)
                mail_subscribers(name, last_version, version)
        else:
            update_pack_metadata(exs[0], datas)

    return count


def create_pack(item, name, version, datas):
    """
    Create a package with his firt version
    """
    logger.debug('create %s %s' % (name, version))

    try:
        summary = datas['info']['summary'][:250]
    except:
        summary = ''

    try:
        upload_time = datas['urls'][0]['upload_time']
    except:
        upload_time = datetime.today()

    pack = Package.objects.create(name=name,
                                  latest_version=version,
                                  link=item['link'],
                                  summary=summary,
                                  description=item['description'][:2000],
                                  pypi_downloads=count_downloads(datas))

    PackageVersion.objects.create(package=pack,
                                  version=version,
                                  link=item['link'],
                                  description=item['description'][:2000],
                                  pubdate=upload_time)


def count_downloads(datas):
    """
    datas may be None
    """
    downloads = 0
    if datas:
        if 'urls' in datas:
            for url in datas['urls']:
                downloads += url['downloads']
    return downloads


def update_pack(item, pack, version, datas):
    """
    Update a package in database

    item : Array of string
    pack : Object Package
    version : string
    """
    try:
        summary = datas['info']['summary'][:250]
    except:
        summary = ''

    try:
        upload_time = datas['urls'][0]['upload_time']
    except:
        upload_time = datetime.today()

    logger.debug('package %s : update from %s to %s' % (pack.name,
                                                        pack.latest_version,
                                                        version))



    pack.latest_version = version
    pack.link = item['link']
    pack.summary = summary,
    pack.description = item['description'][:2000]
    pack.pypi_downloads = count_downloads(datas)
    pack.save()

    PackageVersion.objects.create(package=pack,
                                  version=version,
                                  link=item['link'],
                                  description=item['description'][:2000],
                                  pubdate=upload_time)


def update_pack_metadata(pack, datas):
    """
    Update datas package in database

    pack : Object Package
    version : string
    """
    downval = count_downloads(datas)
    pack.pypi_downloads = downval
    pack.save()

    logger.debug('package {} : update datas down : {}'.format(pack.name, downval))
    insert_atomic('package_{}_downloads'.format(pack.id), downval)


def mail_subscribers(pack_name, oldver, newver):
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
            sendmail_subscriber.delay(pack_name, sub, oldver, newver)


@task
def sendmail_subscriber(pack_name, subscr, oldver, newver):
    """
    Send email to subscribers

    pack_name : string
    subscr : Object PackSubscr
    """
    logger.debug('package {} : sendmail to {}'.format(pack_name, subscr.email))
    parms = {'package': pack_name,
             'email': subscr.email,
             'uuid': subscr.uuid,
             'old_version': oldver,
             'new_version': newver}

    body = render_to_string('emails/subscribers/update_body.txt', parms)
    subject = render_to_string('emails/subscribers/update_subject.txt', parms)

    result = send_mail(subject.rstrip(),
                       body,
                       settings.EMAIL_FROM,
                       [subscr.email],
                       fail_silently=True)
    logger.debug('package {} : sendmail return {}'.format(pack_name, result))
