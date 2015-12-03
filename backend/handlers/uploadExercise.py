import webapp2
from jinja import JINJA_ENVIRONMENT

class uploadExercise(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('uploadExercise.html')
        self.response.write(template.render())
