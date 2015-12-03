import json, time

import webapp2
from domain.Subscribe import Subscribe

class SubscribeOp(webapp2.RequestHandler):
    def post(self):
        user = self.request.get('user_id')
        stream = self.request.get('stream_id')
        sub = Subscribe(user=user, stream=stream)
        sub.put()
        time.sleep(0.05)
        self.redirect('/view?stream_id='+str(stream))
