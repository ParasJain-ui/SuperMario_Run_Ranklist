from datetime import time
from apscheduler.schedulers.blocking import BlockingScheduler
import pandas
import requests as re
from db_access import Database
import time

db=Database()

scheduler = BlockingScheduler()
TIME_STAMP = 1643913000 #unix time stamp for 4th feb 2022
END_TIME = 1645813800
proxy = {
'http' : '',
'https' : ''
}
cols=["Name","Roll No.","Year","Codeforces Handle","Questions_Solved","ratings"]
# reading the existing data
data = pandas.DataFrame(db.show_data(),columns=cols)
# print(data)
# counting the number of Questions for a particular user
def helper(r, i, handle):
    try:
        s = set()
        json_data = r. json()
        try:
            for j in range(len(json_data["result"])):
                try:
                    if (json_data["result"][j]["verdict"] == "OK" and 
                        json_data["result"][j]["problem"]["rating"] >= max (data['ratings'][i], 1200) and
                        json_data["result"][j]["creationTimeSeconds"]>=TIME_STAMP and
                        json_data["result"][j]["creationTimeSeconds"] <= END_TIME and
                        json_data["result"][j]["author"]["ghost"]==False):
                        s.add(str(json_data["result"][j]["problem"]["name"]))
                except:
                    pass
            count = len(list(s))
        except:
            count = list(db.show(handle))[0][4]
            pass
    except:
        count = list(db.show(handle))[0][4]
    return count

#schedule 1
@scheduler.scheduled_job('interval',minutes = 8)
def update_sheet():
    print ("Start")
    for i in range(len(data["Name"])):
        temp = data["Codeforces Handle"][i].split("/")[-1].split(" ")
        if len(temp)>2:
            temp = ""
        else:
            if len(temp[0]):
                temp = temp[0]
            else:
                temp = temp[1]
        time.sleep(1)
        url = "https://codeforces.com/api/user.status?handle="+temp+"&from=1&count=100000"
        r = re.get(url, proxies=proxy)
        x = helper(r, i, data["Codeforces Handle"][i])
        db.update(x, data["Codeforces Handle"][i])
        print(i, data["Codeforces Handle"][i],"->",x)
        if(r.json()["status"]!="OK"):
            print(r.json())

scheduler.start()

#if __name__=='__main__':
#    update_sheet()
