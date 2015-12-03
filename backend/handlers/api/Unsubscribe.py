import json
import time

import webapp2
from domain.Subscribe import Subscribe

class Unsubscribe(webapp2.RequestHandler):
    def post(self):
        stream_ids = [int(p) for p in self.request.get('stream_id', allow_multiple=True)]
        Subscribe.delete_subscribe(stream_ids, self.request.get('user_id'))
        time.sleep(0.1)
        self.redirect('/manage')
