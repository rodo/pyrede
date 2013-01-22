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
Test to send an email
"""
import logging
import feedparser
from celery.task import task
from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    args = '<ircnick>'
    help = 'Import recursively all ogg file in a directory'

    def handle(self, *args, **options):
        """
        Handle the command
        """
        sendmail_test.delay(args[0])
            

@task
def sendmail_test(email):
    """
    email : string
    """
    logger.debug('package %s : sendmail to %s' % (pack_name,
                                                  subscr.email))

    
    send_mail("mail test",
              "test body",
              settings.EMAIL_FROM,
              [subscr.email],
              fail_silently=True)
