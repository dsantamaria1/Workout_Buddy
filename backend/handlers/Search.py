from google.appengine.api import users

import webapp2
import requests, json
from jinja import JINJA_ENVIRONMENT
from domain.Stream import Stream
from handlers.api.SearchStreams import SearchStreams
from handlers.api.GetPath import GetPath

class Search(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()
        if user is None:
            self.redirect('/')
            return

        BASE = GetPath(self.request.url, self.request.path)
        query = self.request.get('query')
        if query is None:
            query = 'a'
        re = requests.get(BASE+"/api/search", params={"query": query}, timeout=10)

        streams = []
        if re:
            streams = re.json()["r"][:5]

        url = users.create_logout_url(self.request.uri)
        url_linktext = 'Logout'
        template_values = {
            'login_logout_url' : url,
            'url_linktext': url_linktext,
            'streams': streams,
            'query':query,
        }
        template = JINJA_ENVIRONMENT.get_template('search.html')
        self.response.write(template.render(template_values))
