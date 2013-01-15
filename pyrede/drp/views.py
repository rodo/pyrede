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
"""
The django views
"""
import json
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import ListView
from django.views.generic import DetailView
from pyrede.drp.models import Package
from pyrede.drp.models import DisPack
from pyrede.drp.forms import ReqForm
from pyrede.utils.reqparser import requ_parser


class PackageList(ListView):
    queryset = Package.objects.all().order_by("name")
    paginate_by = 17
    template_name = 'packages.html'
    context_object_name = 'packages'


class PackageDetail(DetailView):

    model = Package

    def get_slug_field(self):
        return 'name'

    def get_context_data(self, **kwargs):
        context = super(PackageDetail, self).get_context_data(**kwargs)
        context['dispacks'] = DisPack.objects.filter(package=self.object)
        return context


def userreq(request):
    """
    The user post a file
    """
    queryset = Package.objects.all().order_by("name")[:10]
    form = ReqForm()
    return render(request,
                  'form.html',
                  {'form': form,
                   'dispacks': queryset
                   })


def jsonpypi(request, slug):
    """
    A json view of pypi
    """
    try:
        pypi = Package.objects.get(name=slug)
        datas = lookup(pypi)
    except:
        datas = {'result': 0}


    response = HttpResponse(mimetype='application/json; charset=utf-8')

    response.write(json.dumps(datas))

    return response


def lookup(pypi):
    """
    look if packages exists
    """
    jpack = []
    dispacks = DisPack.objects.filter(package=pypi)

    for dpack in dispacks:
        jpack.append({'name': dpack.name,
                      'version': dpack.version,
                      'provide': dpack.package_version,
                      'distribution': {'name': dpack.distribution.name,
                                       'version': dpack.distribution.version_name
                                       }
                      })

    datas = {'result': 1, 
             'pipy': { 'id': pypi.id,
                       'nbpack': pypi.nbdispack},
             'found': len(dispacks),
             'packages': jpack}
    
    

    return datas

def analyze(request):
    """
    The user post a file
    """
    queryset = Package.objects.all().order_by("name")[:10]
    if request.method == 'POST':
        form = ReqForm(request.POST)
        if form.is_valid():
            data = requ_parser(form.cleaned_data['content'])

            return render(request,
                          'analyze.html',
                          {'form': form,
                           'dispacks': queryset,
                           'founds': data,
                           'jfound': data
                           })


    else:
        return redirect('/')
