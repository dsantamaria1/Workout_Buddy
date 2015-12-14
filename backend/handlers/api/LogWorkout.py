import webapp2, json, re
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
        if workoutLogs != None:
            tempList = list(workoutLogs.WoHistory)
            tempList.reverse()
            if len(tempList) > 5:
                tempList2 = list(tempList[:5])
            else:
                tempList2 = list(tempList)

            for hist in tempList2: # get list of workouts
                print "found workout history"
                session = Session.query_by_id(hist) #hist is session_id
                exerciseDict[cntr] = session.exercises
                repsDict[cntr] = session.reps
                p = re.compile(r'.*:.*:..')
                m = p.search(str(session.started))
                dateDict[cntr] = m.group(0)
                categoryDict[cntr] = session.category
                cntr += 1

        self.response.write(json.dumps({"exercises": exerciseDict, "reps": repsDict,
                                        "category": categoryDict, "date": dateDict}))


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
