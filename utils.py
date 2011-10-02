import urllib
import urllib2
import simplejson

__author__ = 'panchicore'

def get_json(url):
    req = urllib2.Request(url)
    opener = urllib2.build_opener()
    f = opener.open(req)
    json = simplejson.load(f)
    return json

def download_image(url, name):
    image = urllib.URLopener()
    image.retrieve(url, 'pics3/%s' % name)