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
from django import forms
from django.forms.widgets import Textarea
from django.forms.widgets import TextInput


class ReqForm(forms.Form):  # pylint: disable=R0924

    content = forms.CharField(required=True,
                              widget=Textarea())
    
    def clean(self):
        cleaned_data = self.cleaned_data
        return cleaned_data


class disPackForm(forms.Form):  # pylint: disable=R0924


    name = forms.CharField(max_length=50,
                           required=True,
                           widget=TextInput(attrs={'class' : 'input-large'}))
    
    version = forms.CharField(max_length=50,
                              required=True,
                              widget=TextInput(attrs={'class' : 'input-small'}))

    package_version = forms.CharField(max_length=50,
                                      required=True,
                                      widget=TextInput(attrs={'class' : 'input-small'}))

    link = forms.CharField(max_length=350,
                           required=True,
                           widget=TextInput(attrs={'class' : 'input-xlarge'}))
    
    def clean(self):
        cleaned_data = self.cleaned_data
        return cleaned_data
