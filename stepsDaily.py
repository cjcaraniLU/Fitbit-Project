import requests
import json
import pandas as pd
# JAN 07 token
token = "<insert token here>"
header = {'Authorization' : 'Bearer {}'.format(token)}
steps_r = requests.get("https://api.fitbit.com/1/user/-/activities/steps/date/today/1d.json", headers=header).json()

steps_break = steps_r["activities-steps"]
 #Breakdown of json data for steps data
steps_data = []
for data in steps_break:
    steps_row = {
        "Date": data["dateTime"],
        "Steps": data["value"]
        }
    steps_data.append(steps_row)

# Convert the data to a Pandas DataFrame
steps_df = pd.DataFrame(steps_data)


# Display the DataFrame
print(steps_df)
