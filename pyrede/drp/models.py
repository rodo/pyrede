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
from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_save
from django.db.models.signals import post_delete
from django.dispatch import receiver
from pyrede.drp.mailtasks import mail_all_subscribers


class Package(models.Model):
    """
    A package from Pypi
    """
    name = models.CharField(max_length=300,
                            unique=True,
                            blank=True)

    latest_version = models.CharField(max_length=30)

    link = models.CharField(max_length=300)

    description = models.CharField(max_length=1000)

    nbdispack = models.IntegerField(default=0)

    pypi_downloads = models.IntegerField(default=0)

    def __str__(self):
        return '%s %s' % (self.name, self.latest_version)

    def save(self, *args, **kwargs):
        key = 'json_pypi_{}'.format(self.name)
        cache.delete(key)
        super(Package, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return "/pypi/{}/".format(self.name)


class PackageVersion(models.Model):
    """
    The package
    """
    package = models.ForeignKey(Package)
    version = models.CharField(max_length=30)

    link = models.CharField(max_length=300)

    description = models.CharField(max_length=1000)

    pubdate = models.DateTimeField()

    def save(self, *args, **kwargs):
        key = 'json_pypi_{}'.format(self.package.name)
        cache.delete(key)
        super(PackageVersion, self).save(*args, **kwargs)


class Distribution(models.Model):
    """
    A distribution
    """
    name = models.CharField(max_length=30,
                            blank=True)

    version_name = models.CharField(max_length=30,
                                    blank=True)

    version_number = models.CharField(max_length=30)

    query_link = models.CharField(max_length=250)

    repo = models.URLField(max_length=250,
                           blank=True,
                           null=True)

    official = models.ForeignKey('self',
                                 blank=True,
                                 null=True,
                                 related_name="related_official")

    def __str__(self):
        return '%s %s' % (self.name, self.version_name)

    class Meta:
        unique_together = ('name', 'version_name')


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

    link = models.URLField(max_length=350)

    link_valid = models.BooleanField(default=False)

    class Meta:
        unique_together = ('name', 'version', 'distribution')

    def save(self, *args, **kwargs):
        key = 'json_pypi_{}'.format(self.package.name)
        cache.delete(key)
        super(DisPack, self).save(*args, **kwargs)


class PackSubscr(models.Model):
    """
    A package subscription
    """
    package = models.ForeignKey(Package)
    email = models.EmailField(max_length=1000)
    date_creation = models.DateTimeField(editable=False, auto_now_add=True)
    uuid = models.CharField(max_length=36)


class Lookup(models.Model):
    """
    A lookup made by a user
    """
    content = models.CharField(max_length=1000)
    distribution = models.ForeignKey(Distribution)
    nb_line = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    date_lookup = models.DateTimeField(editable=False, auto_now_add=True)


class PypStats(models.Model):
    """
    Statistiques on PyPi Package
    """
    package = models.ForeignKey(Package)
    lookup = models.ForeignKey(Lookup)
    date_lookup = models.DateTimeField(editable=False, auto_now_add=True)


@receiver(post_save, sender=DisPack)
def create_dispack(sender, instance, created, **kwargs):
    """Update number of dispack available"""
    count = DisPack.objects.filter(package=instance.package.id).count()
    pack = Package.objects.get(pk=instance.package.id)
    pack.nbdispack = count
    pack.save()
    if created == 1:
        subscrs = PackSubscr.objects.filter(package=pack)
        mail_all_subscribers.delay(subscrs, instance)


@receiver(post_delete, sender=DisPack)
def update_dispack(sender, instance, **kwargs):
    """Update number of dispack available"""
    count = DisPack.objects.filter(package=instance.package.id).count()
    pack = Package.objects.get(pk=instance.package.id)
    pack.nbdispack = count
    pack.save()
