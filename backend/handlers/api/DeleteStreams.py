import json
import time

import webapp2
from domain.Stream import Stream

class DeleteStreams(webapp2.RequestHandler):
    def post(self):
        #stream_id, st, ed
        stream_id = [int(p) for p in self.request.get('stream_id', allow_multiple=True)]
        Stream.delete_streams(stream_id)
        time.sleep(0.1)
        self.redirect('/manage')
