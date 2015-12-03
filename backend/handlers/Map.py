import webapp2
from jinja import JINJA_ENVIRONMENT

class Map(webapp2.RequestHandler):
    def get(self):
        stream_id = self.request.get('stream_id')
        if not stream_id:
            stream_id = 0
        data = {'stream_id': stream_id}

        template = JINJA_ENVIRONMENT.get_template('map.html')
        self.response.write(template.render(data))
