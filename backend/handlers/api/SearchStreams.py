import json

import webapp2
from domain.Stream import Stream

class SearchStreams(webapp2.RequestHandler):
    def get(self):
        query = self.request.get('query')
        stream = Stream.query_by_name(query)
        r = [{'name': p.name, 'cover': p.cover, 'stream_id': p.key.id()} for p in stream]
        self.response.write(json.dumps({"r":r}))
