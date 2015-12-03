from google.appengine.api import users

import webapp2
import requests, json
from jinja import JINJA_ENVIRONMENT
from handlers.api.GetPath import GetPath
from handlers.api.AllStreams import AllStreams
from handlers.api.ViewStream import ViewStream

from domain.Stream import Stream
from domain.Photo import Photo
from domain.Subscribe import Subscribe

class View(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()
        if user is None:
            self.redirect('/')
            return

        url = users.create_logout_url(self.request.uri)
        url_linktext = 'Logout'

        #if stream_id is None
        stream_id = self.request.get('stream_id')
        BASE = GetPath(self.request.url, self.request.path)
        if stream_id:
            st = self.request.get('st')
            if len(st)==0:
                st = 1

            data = {"stream_id": stream_id, "st":st}
            print data
            re = requests.get(BASE+"/api/view", params=data)
            allphotos = []
            st = 1
            multipage = True
            if re:
                allphotos = re.json()['images'] #get three photo each time.
                st = re.json()['ed']
                if re.json()['size'] < 4:
                    multipage = False
            #if user doesn't own the stream, he should not upload photo
            user_id = user.user_id()
            disableModify = True
            if str(Stream.query_by_id(int(stream_id)).author) == str(user_id):
                disableModify = False
            #subscribe
            subscribed = Subscribe.subscribed(stream_id, user_id)

            template_values = {
                'login_logout_url' : url,
                'url_linktext': url_linktext,
                'allphotos':allphotos,
                'disableModify': disableModify,
                'stream_id': stream_id,
                'user_id': user.user_id(),
                'subscribed': subscribed,
                'st': st,
                'multipage': multipage,
            }

            template = JINJA_ENVIRONMENT.get_template('viewstream.html')
            self.response.write(template.render(template_values))
        else:
            re = requests.get(BASE+"/api/allstreams")
            allstreams = []
            if re:
                allstreams = re.json()["allstreams"]

            template_values = {"allstreams" : allstreams,
                               "img_1": 'http://ohtoptens.com/wp-content/uploads/2015/06/Flower-Images-and-Wallpapers3.jpg',
                               'login_logout_url' : url,
                               'url_linktext': url_linktext
            }
            template = JINJA_ENVIRONMENT.get_template('view.html')
            self.response.write(template.render(template_values))
