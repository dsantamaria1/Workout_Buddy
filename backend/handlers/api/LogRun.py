import webapp2, json, re, datetime
from domain.Run import Run
from domain.RunLogs import RunLogs

class LogRun(webapp2.RequestHandler):
    def get(self):
        email = self.request.get('email')
        runLogs = RunLogs.query_by_id(email)

        runDict = {}
        keyList = []
        testList = []
        if runLogs != None:
            tempList = list(runLogs.RunHistory)
            tempList.reverse()
            if len(tempList) > 5:
                tempList2 = list(tempList[:5])
            else:
                tempList2 = list(tempList)
            print tempList2
            for run in tempList2:
                print run
                runHist = Run.query_by_id(run) #run is key_id(), runHist is Run object
                date = str(runHist.date)
                testList.append(str(runHist.date))
                temp = date.split("-",1)[1]
                date_s = temp.split(" ",1)[0]
                runDict[date] = runHist.time
                date = re.sub("-","/" ,date_s)
                keyList.append(date)

        self.response.write(json.dumps({"dateList": keyList, "timeDict": runDict, "testList": testList}))

    def post(self):
        time_s = self.request.get("time")
        email = self.request.get('email')

        time = float(time_s)
        run = Run(time=time)
        key = run.put()

        runLogs = RunLogs.query_by_id(email)
        if runLogs == None:
            print "creating run log"
            runLogs = RunLogs(id=email)
            runLogs.RunHistory.append(key.id())
        else:
            runLogs.RunHistory.append(key.id())

        runLogs.put()
