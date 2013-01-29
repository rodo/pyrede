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
from pyrede.provider.tasks import sendmail_test

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    args = '<email>'
    help = 'Send a test email to <email>'

    def handle(self, *args, **options):
        """
        Handle the command
        """
        sendmail_test.delay(args[0])