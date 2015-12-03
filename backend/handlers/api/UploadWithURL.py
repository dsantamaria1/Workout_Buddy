import json

import webapp2
from google.appengine.api import images

from domain.Stream import Stream
from domain.Photo import Photo

class UploadWithURL(webapp2.RequestHandler):
    def post(self):
        img = self.request.get('image')
        stream_id = self.request.get('stream_id')
        comment = self.request.get('comment')
        photo = Photo(image=img, stream_id=stream_id, comment=comment)
        key = photo.put()
        print img, stream_id, comment
        stream = Stream.query_by_id(int(stream_id))
        if len(stream.cover) == 0:
            stream.cover = str(key.id())
        stream.photos.append(key.id())
        stream.put()
