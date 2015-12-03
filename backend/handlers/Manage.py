from google.appengine.api import users

import webapp2
import requests, json

from jinja import JINJA_ENVIRONMENT
from domain.Stream import Stream
from handlers.api.UserManagement import UserManagement
from handlers.api.GetPath import GetPath

class Manage(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()
        if user is None:
            self.redirect('/')
            return

        BASE = GetPath(self.request.url, self.request.path)
        re = requests.get(BASE+"/api/management", params={"user_id":user.user_id()}, timeout=10)

        own_stream = []
        sub_stream = []
        if re:
            res = re.json()
            for r in res['own_stream']:
                s = Stream.query_by_id(int(r))
                own_stream.append({
                    "id": r,
                    "name": s.name,
                    "size": len(s.photos),
                    "updated_time": s.updated_time,
                    "views": s.views
                })
            
            for r in res['sub_stream']:
                s = Stream.query_by_id(int(r))
                sub_stream.append({
                    "id": r,
                    "name": s.name,
                    "size": len(s.photos),
                    "updated_time": s.updated_time,
                    "views": s.views
                })

        url = users.create_logout_url(self.request.uri)
        url_linktext = 'Logout'
        template_values = {
            'login_logout_url' : url,
            'url_linktext': url_linktext,
            'own_stream': own_stream,
            'sub_stream': sub_stream,
            'user_id': user.user_id(),
        }
        template = JINJA_ENVIRONMENT.get_template('manage.html')
        self.response.write(template.render(template_values))
