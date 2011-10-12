from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render_to_response
import simplejson
import urllib2
from django.conf import settings
from main.models import Bound
# Create your views here.
RANDOM_COLORS = ['a','b','c','d','e','f']
RANDOM_0_TO_255 = range(0, 256)

def map(request):
    return render_to_response('map.html', {}, context_instance=RequestContext(request))

def save_bounds(request):
    minx = request.POST.get('minx')
    miny = request.POST.get('miny')
    maxx = request.POST.get('maxx')
    maxy = request.POST.get('maxy')
    bounds = Bound()
    bounds.min_x = minx
    bounds.min_y = miny
    bounds.max_x = maxx
    bounds.max_y = maxy
    bounds.user = request.user
    bounds.save()
    return HttpResponseRedirect(reverse('get_bounds', args=[bounds.id]))


def get_bounds(request, bounds_id):

    bounds = Bound.objects.get(id=bounds_id)

    return render_to_response('get_bounds.html',{
        'bounds':bounds,
    },context_instance=RequestContext(request))