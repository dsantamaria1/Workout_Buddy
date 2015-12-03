from google.appengine.api import users

import webapp2
import requests, json
from jinja import JINJA_ENVIRONMENT
from handlers.api.GetPath import GetPath
from handlers.api.AllStreams import AllStreams

class Treading(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()
        if user is None:
            self.redirect('/')
            return

        url = users.create_logout_url(self.request.uri)
        url_linktext = 'Logout'
        template_values = {
            'login_logout_url' : url,
            'url_linktext': url_linktext
        }
        BASE = GetPath(self.request.url, self.request.path)
        re = requests.get(BASE+"/api/allstreams")
        allstreams = []
        if re:
            allstreams = sorted(re.json(), key=lambda p: p['views'], reverse=True)
        template_values = {"allstreams" : allstreams,
                           'login_logout_url' : url,
                           'url_linktext': url_linktext}
        template = JINJA_ENVIRONMENT.get_template('view.html')
        self.response.write(template.render(template_values))
