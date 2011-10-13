from django.http import HttpResponseRedirect, Http404
from django.template.context import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django_extensions.db.fields import UUIDField
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
    bounds.make_background()
    return HttpResponseRedirect(reverse('get_bounds', args=[bounds.uuid]))


def get_bounds(request, bounds_uuid):
    bounds = Bound.objects.get(uuid=bounds_uuid)
    return render_to_response('get_bounds.html',{'bounds':bounds},context_instance=RequestContext(request))

def set_background(request, bounds_uuid):
    if request.method == 'POST':
        bound = Bound.objects.get(uuid=bounds_uuid)
        bound.set_as_twitter_background()

        if request.POST.has_key('twitt'):
            bound.send_twitt()

        return HttpResponse('OK')
    return Http404