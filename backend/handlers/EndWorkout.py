import webapp2, requests
from jinja import JINJA_ENVIRONMENT
from handlers.api.GetPath import GetPath
from handlers.api.LogWorkout import LogWorkout
from google.appengine.api import users

class EndWorkout(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        session_id = self.request.get('session_id')
        BASE = GetPath(self.request.url, self.request.path)
        if user:
            print "user is %s" % user
            resp = requests.post(BASE+"/api/logWorkout",
                                 params={"session_id": session_id, "user": user})
            self.redirect('/dispWorkoutHist')
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
            template_values = {
                'user' : user,
                'login_logout_url' : url,
                'url_linktext': url_linktext
            }
            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
