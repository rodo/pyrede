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
from uuid import uuid4
from django.core.cache import cache
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from pyrede.utils.reqparser import requ_parser
from pyrede.drp.models import DisPack
from pyrede.drp.models import Distribution
from pyrede.drp.models import Lookup
from pyrede.drp.models import Package
from pyrede.drp.models import RelatedPackage
from pyrede.drp.models import PackageVersion
from pyrede.drp.models import PackSubscr
from pyrede.drp.models import DebianITP
from pyrede.drp.forms import ReqForm
from pyrede.drp.forms import DisPackForm
from pyrede.drp.forms import UpdateDisPackForm
from pyrede.drp.forms import SubForm
from pyrede.drp.tasks import look4_pypi_missing
from pyrede.drp.tasks import logg_pypi
from pyrede.drp.utils import stats

logger = logging.getLogger(__name__)


class PackageList(ListView):
    paginate_by = 17
    template_name = 'packages.html'
    context_object_name = 'packages'

    def get_queryset(self):
        qryst = Package.objects.all().order_by("-pypi_downloadstm")
        return qryst

class DistributionDetail(DetailView):
    model = Distribution

    def get_context_data(self, **kwargs):
        context = super(DistributionDetail, self).get_context_data(**kwargs)
        self.dist = Distribution.objects.all()[0]
        context['var'] = len(kwargs)
        return context


class DistributionPackages(ListView):
    model = DisPack

    def get_queryset(self):
        dist = get_object_or_404(Distribution, pk=self.kwargs['pk'])
        qryst = DisPack.objects.filter(distribution=dist)
        return qryst


class PackageDetail(DetailView):

    model = Package

    def get_slug_field(self):
        return 'name'

    def get_context_data(self, **kwargs):
        context = super(PackageDetail, self).get_context_data(**kwargs)
        context['dispacks'] = DisPack.objects.filter(package=self.object)
        context['nb_subscribers'] = PackSubscr.objects.filter(package=self.object).count()
        context['last_update'] = PackageVersion.objects.filter(package=self.object).order_by('-pubdate')[0]
        context['form'] = SubForm()
        context['versions'] = PackageVersion.objects.filter(package=self.object).order_by('-pk')[:10]
        context['itps'] = DebianITP.objects.filter(package=self.object)
        context['related'] = RelatedPackage.objects.filter(Q(one=self.object) | Q(two=self.object))
        return context


def userreq(request):
    """
    Main page containing the form to lookup used on homepage
    """
    queryset = Package.objects.all().order_by('-pk')[:7]
    lkups = Lookup.objects.all().order_by('-pk')[:4]
    distributions = Distribution.objects.filter(official=None).order_by('-pk')
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
    A json view of a pypi package
    """
    key = 'json_pypi_{}'.format(slug)
    cval = cache.get(key)
    if cval is None:
        try:
            pypi = Package.objects.get(name__iexact=slug)
            datas = lookup(pypi)
        except:
            alt = Package.objects.filter(name__contains=slug.lower())
            pyalt = [{'id': x.id, 'name': x.name} for x in alt]
            datas = {'result': 0,
                     'nb_alt': len(alt),
                     'alt': pyalt}

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

        if dpack.distribution.official:
            distri = dpack.distribution.official
            official_id = distri.id
        else:
            official_id = 0

        dist = {'id': dpack.distribution.id,
                'name': dpack.distribution.name,
                'version': dpack.distribution.version_name,
                'official': official_id,
                }

        jpack.append({'name': dpack.name,
                      'version': dpack.version,
                      'provide': dpack.package_version,
                      'distribution': dist})

    datas = {'result': 1,
             'name': pypi.name,
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
    pckexists = 0
    if form.is_valid():
        datas = requ_parser(form.cleaned_data['content'])
        for odist in distros:
            if odist.id == int(form.cleaned_data['distribution']):
                dist = odist
        lkup = Lookup.objects.create(content=form.cleaned_data['content'],
                                     distribution=dist,
                                     nb_line=len(datas))
        for pack in datas:
            try:
                pobj = Package.objects.get(name=pack[0])
                pckexists = 1
            except Package.DoesNotExist:
                try:
                    look4_pypi_missing.delay(pack[0])
                except:
                    logger.error("Error in lauching task look4_pypi_missing.delay(pack[0])")

            if pckexists:
                logg_pypi.delay(pobj, lkup)

        return redirect('/analyze/%s/' % lkup.id)
    else:
        logger.error("form is not valid")
        return userreq(request)


def analyze_get(request, pk):
    """
    Read an existing analyze
    """
    lkup = get_object_or_404(Lookup, pk=pk)
    datas = requ_parser(lkup.content)
    for pack in datas:
        try:
            Package.objects.get(name=pack[0])
        except Package.DoesNotExist:
            try:
                look4_pypi_missing.delay(pack[0])
            except:
                logger.error("Error in lauching task look4_pypi_missing.delay(pack[0])")

    return render(request,
                  'analyze.html',
                  {'founds': datas,
                   'lookup': lkup
                   })


def analyzereq(request, pk, dist):
    """
    Output a requirements.txt file based on distribution verison number
    """
    qryset = Package.objects.all().order_by('-pk')[:7]
    lkup = get_object_or_404(Lookup, pk=pk)
    distro = get_object_or_404(Distribution, pk=dist)
    datas = requ_parser(lkup.content)
    result = []
    for pack in datas:
        known = DisPack.objects.filter(package__name=pack[0],
                                       distribution=distro)
        if len(known) == 1:
            result.append([pack[0], known[0].package_version])
        else:
            result.append([pack[0]])

    return render(request,
                  'requirements.txt',
                  {'pk': pk,
                   'founds': result,
                   'ori': datas,
                   'distro': distro,
                   'lkup': lkup.content,
                   },
                  content_type='text/plain')


def subscribe(request, slug):
    """
    Add a distribution package for a pypi package
    """
    pypi = Package.objects.get(name=slug)

    if request.method == 'POST':
        form = SubForm(request.POST)
        if form.is_valid():
            PackSubscr.objects.get_or_create(package=pypi,
                                             email=form.cleaned_data['email'],
                                             uuid=str(uuid4()))
            return redirect('/pypi/{}/'.format(pypi.name))


def unsubscribe(request, slug, uuid):
    """
    Unsubscribe from a pypi package updates
    """
    pypi = Package.objects.get(name=slug)
    PackSubscr.objects.filter(package=pypi, uuid=uuid).delete()
    return redirect('/pypi/{}/'.format(pypi.name))


@login_required
def adddispack(request, slug):
    """
    Add a distribution package for a pypi package
    """
    errors = None
    pypi = Package.objects.get(name=slug)
    dispacks = DisPack.objects.filter(package=pypi)
    distros = Distribution.objects.all().order_by('name', '-version_number')
    dists = [(r.id, "%s %s" % (r.name, r.version_name)) for r in distros]

    if request.method == 'POST':
        form = DisPackForm(dists, request.POST)
        errors, referer = post_dispack(form, dists, request, distros, pypi)
    else:
        form = DisPackForm(dists)
        try:
            referer = request.META['HTTP_REFERER']
        except KeyError:
            referer = ''

    return render(request,
                  'add_dispack.html',
                  {'form': form,
                   'package': pypi,
                   'dispacks': dispacks,
                   'referer': referer,
                   'errors': errors
                   })


@login_required
def updispack(request, pk, new_version):
    """
    Add a distribution package for a pypi package
    """
    errors = None
    dispack = DisPack.objects.get(pk=pk)
    distros = Distribution.objects.all().order_by('name', '-version_number')
    dists = [(dispack.distribution.id, "%s %s" % (dispack.distribution.name, dispack.distribution.version_name))]

    if request.method == 'POST':
        form = UpdateDisPackForm(request.POST)
        if form.is_valid():
            datas = form.cleaned_data
            dispack.version = datas['version']
            dispack.package_version = datas['package_version']
            dispack.save()
    else:
        new_pack_version = new_version.split('-')[0]

        form = UpdateDisPackForm(initial={'version': new_version,
                                          'package_version': new_pack_version})
        try:
            referer = request.META['HTTP_REFERER']
        except KeyError:
            referer = ''

    return render(request,
                  'update_dispack.html',
                  {'form': form,
                   'dist': dists[0],
                   'dispack': dispack,
                   'errors': errors,
                   'new_version': new_version,
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


@login_required
def profile(request):
    """The profile wiew
    """
    template_name = 'profile.html'

    return render(request,
                  template_name,
                  {})


def robots(request):
    """
    The robots.txt
    """
    return render(request,
                  'robots.txt',
                  content_type='text/plain')
