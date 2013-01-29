# -*- coding: utf-8 -*-  pylint: disable-msg=R0801
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
from pyrede.drp.models import Distribution
from pyrede.drp.models import DisPack
from django.contrib import admin


class DistributionAdmin(admin.ModelAdmin):
    """
    Custom Admin for Distribution
    """
    list_display = ('name', 'version_name')


class DisPackAdmin(admin.ModelAdmin):
    """
    Custom Admin for DisPack
    """
    list_display = ('name', 'distribution')
    list_filter = ['distribution']


admin.site.register(Distribution, DistributionAdmin)
admin.site.register(DisPack, DisPackAdmin)
