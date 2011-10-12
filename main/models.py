from django.db import models
from django.contrib.auth.models import User
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField
from utils import get_json, download_image
import Image, os
from django.conf import settings

class Bound(models.Model):
    user = models.ForeignKey(User, related_name='bounds')

    min_x = models.FloatField()
    min_y = models.FloatField()
    max_x = models.FloatField()
    max_y = models.FloatField()

    image = models.ImageField(upload_to='static/backgrounds', null=True, blank=True)

    installed = models.BooleanField(default=False)

    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    def __unicode__(self):
        return self.user.username

    """ get panoramio JSON for the images into the geo bounds """
    def get_panoramas(self):
        init = 1
        end = 101
        panoramio_size = 'square'
        panoramio_url = "http://www.panoramio.com/map/get_panoramas.php?set=public&from=%i&to=%i&minx=%s&miny=%s&maxx=%s&maxy=%s&size=%s"
        panoramio_url = panoramio_url % (init, end,  self.min_x, self.min_y, self.max_x, self.max_y, panoramio_size)

        json = get_json(panoramio_url)
        photos = json.get('photos')

        return photos

    def make_background(self):
        photos = self.get_panoramas()
        image_list = []
        for p in photos:
            url = p.get('photo_file_url')
            name = url.split('/').pop()
            print 'downloading %s ...' % name
            download_image(url, self.id, name)
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

        statics_path = settings.MEDIA_ROOT
        downloads_path = os.path.join(settings.DOWNLOAD_IMAGE_PATH, str(self.id))

        for i in range(0, (grid*grid)):

            if i % grid == 0:
                y = ycar * sizey
                ycar = ycar + 1
                xcar = 0
            else:
                xcar = xcar + 1

            x = sizex * xcar

            img = Image.open( os.path.join(downloads_path, image_list[i]) )
            blank_image.paste(img, (x,y))


        negro = Image.open( os.path.join(statics_path, 'negro.jpg') )
        blank_image.save( os.path.join(statics_path, 'backgrounds', '%i.jpg' % self.id) , quality=100)
        image = Image.blend(blank_image, negro, 0.5)
        image.save( os.path.join(statics_path, 'backgrounds', '%i_black.jpg' % self.id) , quality = 100)
        image = Image.open(os.path.join(statics_path, 'backgrounds', '%i_black.jpg' % self.id))
        self.image = image.filename

        self.save()


    