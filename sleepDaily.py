import requests
import json
import pandas as pd

token =  "<insert token here>"
header = {'Authorization' : 'Bearer {}'.format(token)}
sleep_r = requests.get("https://api.fitbit.com/1.2/user/-/sleep/date/today.json", headers=header).json()


sleep_break = sleep_r['sleep']

#Breakdown of json data for sleep data
sleep_data = []
for data in sleep_break:
    sleep_row = {
        "Date Of Sleep": data["dateOfSleep"],
        "Duration": data["duration"],
        "Efficency": data["efficiency"],
        "End Time": data["endTime"],
        "Minutes Asleep": data["minutesAsleep"],
        "Minutes Awake": data["minutesAwake"],
        "Minutes to Fall Asleep": data['minutesToFallAsleep'],
        "Start Time": data["startTime"]
        }
    sleep_data.append(sleep_row)

# Convert the data to a Pandas DataFrame
sleep_df = pd.DataFrame(sleep_data)

print(sleep_df)