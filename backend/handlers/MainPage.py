import webapp2
from jinja import JINJA_ENVIRONMENT

class MainPage(webapp2.RequestHandler):

    def get(self):
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render())
