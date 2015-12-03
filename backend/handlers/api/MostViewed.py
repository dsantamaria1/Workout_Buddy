import json

import webapp2
from domain.Stream import Stream

class MostViewed(webapp2.RequestHandler):
    def get(self):
        #stream_id, st, ed
        stream = Stream.query().order(-Stream.views)
        r = [{'name': p.name, 'cover': p.cover, 'view': p.views} for p in stream]
        self.response.write(json.dumps(r))
