import webapp2, json
from domain.Session import Session
from domain.WorkoutLogs import WorkoutLogs

class LogWorkout(webapp2.RequestHandler):
    def get(self):
        email = self.request.get('email')
        workoutLogs = WorkoutLogs.query_by_id(email)
        exerciseDict = {}
        repsDict = {}
        dateDict = {}
        categoryDict = {}
        cntr = 0
        print "11111"
        print workoutLogs.WoHistory

        for hist in workoutLogs.WoHistory: # get list of workouts
            if hist != None:
                session = Session.query_by_id(hist)
                exerciseDict[cntr] = session.exercises
                repsDict[cntr] = session.reps
                dateDict[cntr] = session.started
                categoryDict[cntr] = session.category
                cntr += 1

        self.response.write(json.dumps({"exercises": exerciseDict, "reps": repsDict,
                                        "category": categoryDict})) #"date": dateDict,


    def post(self):
        email = self.request.get('email')
        session_id = int(self.request.get('session_id'))
        session = Session.query_by_id(session_id)
        session.completed=True
        workoutLogs = WorkoutLogs.query_by_id(email)

        print workoutLogs
        if workoutLogs == None:
            print "creating log"
            workoutLogs = WorkoutLogs(id=email)
            workoutLogs.WoHistory.append(session_id)
        else:
            workoutLogs.WoHistory.append(session_id)

        workoutLogs.put()
        session.put()
