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
    bounds.save()
    return HttpResponseRedirect(reverse('get_bounds', args=[bounds.id]))


def get_bounds(request, bounds_id):

    bounds = Bound.objects.get(id=bounds_id)

    first = 0
    last = 192
    panoramio_url = "http://www.panoramio.com/map/get_panoramas.php?set=public&from=%i&to=%i&minx=%s&miny=%s&maxx=%s&maxy=%s&size=square"
    panoramio_url = panoramio_url % (first, last,  bounds.min_x, bounds.min_y, bounds.max_x, bounds.max_y)
    #print panoramio_url
    json = get_json(panoramio_url)
    photos = json.get('photos')
    response = []
    for p in photos:
        item = {"photo_url":p.get('photo_file_url')}
        response.append(item)
    return render_to_response('get_bounds.html',{'response':response, 'colors':RANDOM_COLORS, 'numbers':RANDOM_0_TO_255},context_instance=RequestContext(request))

def get_colourlovers_patterns(request):
    url = 'http://www.colourlovers.com/api/palettes/top&format=json'
    palettes = get_json(url)
    import random
    i = random.randint(0,19)
    print palettes[i].get("colors")

def get_json(url):
    req = urllib2.Request(url)
    opener = urllib2.build_opener()
    f = opener.open(req)
    json = simplejson.load(f)
    return json

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i+lv/3], 16) for i in range(0, lv, lv/3))
