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
    req = urllib2.Request(panoramio_url)
    opener = urllib2.build_opener()
    f = opener.open(req)
    json = simplejson.load(f)
    #print json
    photos = json.get('photos')
    response = []
    for p in photos:
        item = {"photo_url":p.get('photo_file_url')}
        response.append(item)
    return render_to_response('get_bounds.html',{'response':response},context_instance=RequestContext(request))

def twitt(request):
    from oauthtwitter import OAuthApi
    import pprint
    twitter = OAuthApi(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET_KEY)
    temp_credentials = twitter.getRequestToken()
    #print twitter.getAuthorizationURL(temp_credentials)
    access_token = twitter.getAccessToken(temp_credentials, "wmDcSUb2pEAWqrcIPZYthmGXDhKRLbnrXibhpMIp8")
    #print access_token

    #print "oauth_token: " + access_token['oauth_token']
    #print "oauth_token_secret: " + access_token['oauth_token_secret']
    twitter = OAuthApi(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET_KEY, access_token['oauth_token'], access_token['oauth_token_secret'])
    user_timeline = twitter.GetUserTimeline()

    #pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(user_timeline)


    import twitter
    api = twitter.Api(consumer_key=settings.TWITTER_CONSUMER_KEY,
                        consumer_secret=settings.TWITTER_CONSUMER_SECRET_KEY,
                        access_token_key='1tGyHYXvJUAkSWDy0rjCTzDwY2ZKafk3my8xuztvY',
                        access_token_secret='s20QqPpTflBdjrpBcAQiIf4aDFulKSC4oj85JFwb80')

    s = api.PostUpdate('I love python-twitter!')
    return HttpResponse(s.text)
