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
from django.core.cache import cache
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
from pyrede.drp.forms import SubForm
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
        context['form'] = SubForm()
        return context


def userreq(request):
    """
    Main page containing the form
    """
    queryset = Package.objects.all().order_by('-pk')[:7]
    lkups = Lookup.objects.all().order_by('-pk')[:4]
    distributions = Distribution.objects.all().order_by('-pk')
    #for dist in distributions:
    dists = [(r.id, "%s %s" % (r.name, r.version_name)) for r in distributions]
    form = ReqForm(dists)

    return render(request,
                  'form.html',
                  {'form': form,
                   'packages': queryset,
                   'lookups': lkups,
                   'stats': stats()
                   })


def jsonpypi(request, slug):
    """
    A json view of pypi
    """
    key = 'json_pypi_{}'.format(slug)
    cval = cache.get(key)
    if cval is None:
        try:
            pypi = Package.objects.get(name=slug)
            datas = lookup(pypi)
        except:
            datas = {'result': 0}
        # cache for one hour
        cache.set(key, str(datas), 3600)
    else:
        datas = eval(cval)

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
        dist = {'id': dpack.distribution.id,
                'name': dpack.distribution.name,
                'version': dpack.distribution.version_name}

        jpack.append({'name': dpack.name,
                      'version': dpack.version,
                      'provide': dpack.package_version,
                      'distribution': dist})

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
    if pk == 0:
        if request.method == 'POST':
            return analyze_post(request)
        else:
            return redirect('/')
    else:
        return analyze_get(request, pk)


def analyze_post(request):
    """
    User POST a content to analyze
    """
    distros = Distribution.objects.all().order_by('-pk')
    dists = [(r.id, "%s %s" % (r.name, r.version_name)) for r in distros]
    form = ReqForm(dists, request.POST)
    if form.is_valid():

        datas = requ_parser(form.cleaned_data['content'])
        for odist in distros:
            if odist.id == int(form.cleaned_data['distribution']):
                dist = odist
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
        return render(request,
                      'form.html',
                      {'form': form})


def analyze_get(request, pk):
    """
    Read an existing analyze
    """
    qryset = Package.objects.all().order_by('-pk')[:7]
    lkup = Lookup.objects.get(pk=pk)
    datas = requ_parser(lkup.content)
    for pack in datas:
        try:
            Package.objects.get(name=pack[0])
        except Package.DoesNotExist:
            look4_pypi_missing.delay(pack[0])

    return render(request,
                  'analyze.html',
                  {'dispacks': qryset,
                   'founds': datas,
                   'lookup': lkup
                   })


def adddispack(request, slug):
    """
    Add a distribution package for a pypi package
    """
    errors = None
    pypi = Package.objects.get(name=slug)
    dispacks = DisPack.objects.filter(package=pypi)
    distros = Distribution.objects.all().order_by('-pk')
    dists = [(r.id, "%s %s" % (r.name, r.version_name)) for r in distros]

    if request.method == 'POST':
        form = DisPackForm(dists, request.POST)
        errors, referer = post_dispack(form, dists, request, distros, pypi)
    else:
        form = DisPackForm(dists)
        referer = request.META['HTTP_REFERER']

    return render(request,
                  'add_dispack.html',
                  {'form': form,
                   'package': pypi,
                   'dispacks': dispacks,
                   'referer': referer,
                   'errors': errors
                   })


def post_dispack(form, dists, request, distros, pypi):
    """
    """
    errors = None

    if form.is_valid():
        datas = form.cleaned_data
        referer = datas['referer']
        for odist in distros:
            if odist.id == int(datas['distribution']):
                dist = odist

        link = dist.query_link.format(datas['name'])

        try:
            DisPack.objects.create(name=datas['name'],
                                   version=datas['version'],
                                   package_version=datas['package_version'],
                                   link=link,
                                   distribution=dist,
                                   package=pypi)
        except:
            errors = 'Error'

        if errors is not None:
            check_dispack_link.delay(dispack)
        return errors, referer
    else:
        return errors, None


def about(request):
    """
    About page
    """
    return render(request, 'about.html')
