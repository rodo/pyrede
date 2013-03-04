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
Tasks for pyrede/drp
"""
import logging
from celery.task import task
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


@task
def mail_all_subscribers(subscrs, dispack):
    """
    Send email to subscribers

    pack : Package
    """
    logger.debug('package %s : found %d subscriber' % (dispack.name,
                                                       len(subscrs)))
    for sub in subscrs:
        sendmail_new_dispack.delay(dispack, sub)


@task
def sendmail_new_dispack(dispack, subscr):
    """
    Send email to subscribers

    pack_name : string
    subscr : Object PackSubscr
    """
    logger.debug('package {} : sendmail to {}'.format(dispack.name,
                                                      subscr.email))

    parms = {'package': dispack.package,
             'dispack': dispack,
             'email': subscr.email,
             'uuid': subscr.uuid}

    subject_template = 'emails/subscribers/newdispack_subject.txt'

    body = render_to_string('emails/subscribers/newdispack_body.txt', parms)
    subject = render_to_string(subject_template, parms)

    result = send_mail(subject.rstrip(),
                       body,
                       settings.EMAIL_FROM,
                       [subscr.email],
                       fail_silently=True)
    logger.debug('package {} : sendmail return {}'.format(dispack.name,
                                                          result))
