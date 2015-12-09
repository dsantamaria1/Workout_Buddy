import webapp2, json
from domain.Session import Session
from domain.WorkoutLogs import WorkoutLogs

class LogWorkout(webapp2.RequestHandler):
    def post(self):
        user = self.request.get('user')
        session_id = int(self.request.get('session_id'))
        session = Session.query_by_id(session_id)
        session.completed=True
        workoutLogs = WorkoutLogs.query_by_id(user)

        print workoutLogs
        if workoutLogs == None:
            print "creating log"
            workoutLogs = WorkoutLogs(id=user)
            workoutLogs.WoHistory.append(session_id)
        else:
            workoutLogs.WoHistory.append(session_id)

        workoutLogs.put()
        session.put()
