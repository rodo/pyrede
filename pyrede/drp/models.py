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
drp Models for Pyrede
"""
import logging
from datetime import datetime
from datetime import timedelta
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models


class Package(models.Model):
    """
    The package
    """
    name = models.CharField(max_length=300,
                              verbose_name='artiste name',
                              blank=True)

    version = models.CharField(max_length=30)

    link = models.CharField(max_length=300)

    description = models.CharField(max_length=1000)


class Deb(models.Model):
    """
    The package
    """
    name = models.CharField(max_length=300,
                              verbose_name='artiste name',
                              blank=True)

    version = models.CharField(max_length=30)
