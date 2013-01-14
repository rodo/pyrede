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
from django.db import models


class Package(models.Model):
    """
    A package from Pypi
    """
    name = models.CharField(max_length=300,
                            blank=True)

    latest_version = models.CharField(max_length=30)

    link = models.CharField(max_length=300)

    description = models.CharField(max_length=1000)


class PackageVersion(models.Model):
    """
    The package
    """
    package = models.ForeignKey(Package)
    version = models.CharField(max_length=30)

    link = models.CharField(max_length=300)

    description = models.CharField(max_length=1000)

    pubdate = models.DateTimeField()


class Distribution(models.Model):
    """
    The package
    """
    name = models.CharField(max_length=30,
                            blank=True)

    version_name = models.CharField(max_length=30,
                                    blank=True)

    version_number = models.CharField(max_length=30)


class DisPack(models.Model):
    """
    A package from a distribution
    """
    name = models.CharField(max_length=300,
                            blank=True)

    version = models.CharField(max_length=30)

    distribution = models.ForeignKey(Distribution)
    package = models.ForeignKey(Package)
    package_version = models.CharField(max_length=30)
