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
import logging
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import ListView
from django.views.generic import DetailView
from pyrede.utils.reqparser import requ_parser
from pyrede.drp.models import DisPack
from pyrede.drp.models import Distribution
from pyrede.drp.models import Lookup
from pyrede.drp.models import Package
from pyrede.drp.forms import ReqForm
from pyrede.drp.forms import DisPackForm
from pyrede.drp.tasks import look4_pypi_missing
from pyrede.drp.utils import stats

logger = logging.getLogger(__name__)


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
    Main page containing the form
    """
    queryset = Package.objects.all().order_by('-pk')[:7]
    distributions = Distribution.objects.all().order_by('-pk')
    #for dist in distributions:
    dists = [(r.id, "%s %s" % (r.name, r.version_name)) for r in distributions]
    form = ReqForm(dists)

    return render(request,
                  'form.html',
                  {'form': form,
                   'packages': queryset,
                   'stats': stats()
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
                      'distribution': {'id': dpack.distribution.id,
                                       'name': dpack.distribution.name,
                                       'version': dpack.distribution.version_name
                                       }
                      })

    datas = {'result': 1,
             'pipy': {'id': pypi.id,
                      'nbpack': pypi.nbdispack},
             'found': len(dispacks),
             'packages': jpack}

    return datas


def analyze(request, pk=0):
    """
    The user post a file
    """
    queryset = Package.objects.all().order_by('-pk')[:7]
    if pk == 0:
        if request.method == 'POST':
            distributions = Distribution.objects.all().order_by('-pk')
            dists = [(r.id, "%s %s" % (r.name, r.version_name)) for r in distributions]
            form = ReqForm(dists, request.POST)
            if form.is_valid():
                datas = requ_parser(form.cleaned_data['content'])
                for odist in distributions:
                    if odist.id == int(form.cleaned_data['distribution']):
                        dist=odist
                lkup = Lookup.objects.create(content=form.cleaned_data['content'],
                                             distribution=dist)
                for pack in datas:
                    try:
                        Package.objects.get(name=pack[0])
                    except Package.DoesNotExist:
                        look4_pypi_missing.delay(pack[0])

                return redirect('/analyze/%s/' % lkup.id)
            else:
                logger.error("form is not valid")
                if form.errors:
                    for field in form:
                        print field.name, field.errors
                return redirect('/')
        else:
            return redirect('/')
    else:
        lkup = Lookup.objects.get(pk=pk)
        datas = requ_parser(lkup.content)
        for pack in datas:
            try:
                Package.objects.get(name=pack[0])
            except Package.DoesNotExist:
                look4_pypi_missing.delay(pack[0])

        return render(request,
                      'analyze.html',
                      {'dispacks': queryset,
                       'founds': datas,
                       'jfound': datas,
                       'lookup': lkup
                       })


def adddispack(request, slug):
    """
    Add a distribution package for a pypi package
    """
    pypi = Package.objects.get(name=slug)
    dispacks = DisPack.objects.filter(package=pypi)
    distributions = Distribution.objects.all().order_by('-pk')
    dists = [(r.id, "%s %s" % (r.name, r.version_name)) for r in distributions]

    if request.method == 'POST':

        form = DisPackForm(dists, request.POST)
        if form.is_valid():
            for odist in distributions:
                if odist.id == int(form.cleaned_data['distribution']):
                    dist=odist

            referer = form.cleaned_data['referer']
            link = "http://packages.debian.org/{}/{}".format(form.cleaned_data['name'],
                                                             dist.version_name)
            try:
                DisPack.objects.create(name=form.cleaned_data['name'],
                                       version=form.cleaned_data['version'],
                                       package_version=form.cleaned_data['package_version'],
                                       link=link,
                                       distribution=dist,
                                       package=pypi)
            except:
                return render(request,
                              'add_dispack.html',
                              {'form': form,
                               'package': pypi,
                               'dispacks': dispacks,
                               'referer': referer,
                               'errors': 'Error'
                               })
    else:
        form = DisPackForm(dists)
        referer = request.META['HTTP_REFERER']

    return render(request,
                  'add_dispack.html',
                  {'form': form,
                   'package': pypi,
                   'dispacks': dispacks,
                   'referer': referer
                   })


def about(request):
    """
    About page
    """
    return render(request,
                  'about.html')
