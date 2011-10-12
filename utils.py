import os
import urllib
import urllib2
import simplejson
from django.conf import settings

__author__ = 'panchicore'

def get_json(url):
    req = urllib2.Request(url)
    opener = urllib2.build_opener()
    f = opener.open(req)
    json = simplejson.load(f)
    return json

def download_image(url, id, name):
    image = urllib.URLopener()
    download_path = os.path.join(settings.DOWNLOAD_IMAGE_PATH, str(id))
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    image.retrieve(url, os.path.join(download_path, name) )