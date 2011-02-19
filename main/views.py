from django.template.context import RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response
import simplejson
import urllib2
from django.conf import settings
# Create your views here.

def map(request):
    return render_to_response('map.html', {}, context_instance=RequestContext(request))

def get_panoramio_pics(request):
    first = 0
    last = 200
    minx = request.GET.get('minx')
    miny = request.GET.get('miny')
    maxx = request.GET.get('maxx')
    maxy = request.GET.get('maxy')
    panoramio_url = "http://www.panoramio.com/map/get_panoramas.php?set=public&from=%i&to=%i&minx=%s&miny=%s&maxx=%s&maxy=%s&size=square"
    #panoramio_url = panoramio_url % (first, last,  -74.9, 10.8,  -74.6, 11.0)
    panoramio_url = panoramio_url % (first, last,  minx, miny, maxx, maxy)
    #print panoramio_url
    req = urllib2.Request(panoramio_url)
    opener = urllib2.build_opener()
    f = opener.open(req)
    json = simplejson.load(f)
    #print json
    photos = json.get('photos')
    response = ''
    for p in photos:
        tag = '<img src="%s" title="%s">' % ( p.get('photo_file_url'),p.get('photo_title'))
        response = response + tag
    return HttpResponse(response)

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