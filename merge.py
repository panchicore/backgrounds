import Image
import simplejson
import urllib2, urllib

def get_json(url):
    req = urllib2.Request(url)
    opener = urllib2.build_opener()
    f = opener.open(req)
    json = simplejson.load(f)
    return json

def download_image(url, name):
	image = urllib.URLopener()
	image.retrieve(url, 'pics3/%s' % name)

panoramio = True
image_list = []

if panoramio:
	

	init = 1
	end = 101
	panoramio_size = 'square'

	bounds = ((10.822515257716793, -74.97756958007818), (11.092165893502013, -74.63424682617193))
	panoramio_url = "http://www.panoramio.com/map/get_panoramas.php?set=public&from=%i&to=%i&minx=%s&miny=%s&maxx=%s&maxy=%s&size=%s"
	panoramio_url = panoramio_url % (init, end,  bounds[0][1], bounds[0][0], bounds[1][1], bounds[1][0], panoramio_size)
	print panoramio_url

	json = get_json(panoramio_url)
	photos = json.get('photos')

	for p in photos:
		url = p.get('photo_file_url')
		name = url.split('/').pop()
		print 'downloading %s ...' % name
		download_image(url, name)
		image_list.append(name)
		print 'total: %i' % len(image_list)



grid = 10
sizex = 60
sizey = 60
xy = (sizex * grid, sizey * grid)
	
blank_image = Image.new("RGB", xy)

ycar = 0
xcar = 0
y = 0
x = 0

for i in range(0, (grid*grid)):

	if i % grid == 0:
		y = ycar * sizey
		ycar = ycar + 1
		xcar = 0
	else:
		xcar = xcar + 1
		
	x = sizex * xcar
	
	img = Image.open('pics3/%s' % image_list[i])
	blank_image.paste(img, (x,y))
	
negro = Image.open('negro.jpg')
blank_image.save('ok3.jpg', quality=100)
image = Image.blend(blank_image, negro, 0.5)
image.save('ok3_x.jpg', quality = 100)