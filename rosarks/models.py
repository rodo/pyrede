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
rosarks models
"""
from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_save
from django.db.models.signals import post_delete
from django.dispatch import receiver
from rosarks.tasks import delta_bymonth


class AtomicValue(models.Model):
    """
    The smallest part of data
    """
    create = models.DateTimeField(editable=False, auto_now_add=True)
    ref = models.CharField(max_length=1000, db_index=True)
    value = models.IntegerField(default=0)


class ConsolidateValue(models.Model):
    """
    The datas consolidates
    """
    create = models.DateTimeField(editable=False, auto_now_add=True)
    ref = models.CharField(max_length=1000)
    value = models.IntegerField(default=0)


@receiver(post_save, sender=AtomicValue)
def consolidate(sender, instance, created, **kwargs):
    """Update number of dispack available"""
    if created == 1:
        delta_bymonth.delay(instance)
        Consolidate.objects.create(ref=instance.ref,
                                   value=value)
