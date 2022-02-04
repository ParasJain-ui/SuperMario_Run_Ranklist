from apscheduler.schedulers.blocking import BlockingScheduler
import pandas
import requests as re

scheduler = BlockingScheduler()
TIME_STAMP=1643932800 #unix time stamp for 4th feb 2022
proxy = {
'http' : '',
'https' : ''
}
# reading the existing data
data = pandas.read_csv("handles")

# counting the number of Questions for a particular user
def helper(r, i):
    count = 0
    json_data = r. json()
    try:
        for j in range(len(json_data["result"])):
            try:
                if (json_data["result"][j]["verdict"] == "OK" and 
                    json_data["result"][j]["problem"]["rating"] >= max (data['ratings'][i], 1000) and
                    json_data["result"][j]["problem"]["startTimeSeconds"]>=TIME_STAMP and
                    json_data["result"][j]["author"]["ghost"]==False):
                    count += 1
            except:
                pass
    except:
        pass
    return count

#schedule 1
@scheduler.scheduled_job('interval',hours=1)
def update_sheet():
    for i in range(len(data["Name"])):
        url = "https://codeforces.com/api/user.status?handle="+data["Codeforces Handle"][i]+"&from=1&count=100000"
        r = re.get(url, proxies=proxy)
        data['Questions_Solved'][i] = helper(r, i)
        d = data.sort_values('Questions_Solved', ascending= False)
        d.to_csv('handles', index = False)
        print(i)

scheduler.start()