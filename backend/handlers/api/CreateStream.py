import json

import webapp2
import time
from domain.Stream import Stream


class CreateStream(webapp2.RequestHandler):
    def post(self):
        name = self.request.get('name')
        email = self.request.get('email')
        #Empty Name
        if len(name) == 0:
            self.response.write(json.dumps({'status_code': 100, 'key': "0"}))
            return
        #name exists (non-case sensitive)
        if Stream.name_exist(name):
            self.response.write(json.dumps({'status_code': 101, 'key': "0"}))
            return

        author = self.request.get('author')
        tags = self.request.get('tags').split()
        cover = self.request.get('cover_url')
        woType = self.request.get('woType') #dsm TODO: get_all or get
        stream = Stream(name=name, author=author, tags=tags, email=email, cover=cover, views=0, photos=[],
                        woType=woType)
        key = stream.put()
        self.response.write(json.dumps({'status_code': 0, 'key': key.id()}))
