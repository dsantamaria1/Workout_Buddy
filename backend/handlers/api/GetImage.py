import json

import webapp2
from domain.Photo import Photo

class GetImage(webapp2.RequestHandler):
    def get(self):
        photo_id = int(self.request.get('photo_id'))
        photo = Photo.query_by_id(photo_id)
        if photo:
            self.response.headers['Content-Type'] = 'image/png'
            self.response.out.write(photo.image)
        else:
            self.response.out.write('No image')
