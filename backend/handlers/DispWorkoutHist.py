import webapp2, requests
from jinja import JINJA_ENVIRONMENT
from handlers.api.GetPath import GetPath
from handlers.api.LogWorkout import LogWorkout
from google.appengine.api import users

class DispWorkoutHist(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        BASE = GetPath(self.request.url, self.request.path)
        if user:
            print "user is %s" % user
            resp = requests.get(BASE+"/api/logWorkout",
                                 params={"user": user})
            template_values = resp.json()
            print template_values
            template = JINJA_ENVIRONMENT.get_template('workoutLog.html')
            self.response.write(template.render(template_values))
