import requests
import json
import pandas as pd

token = "<insert token here>"
header = {'Authorization' : 'Bearer {}'.format(token)}
heart_r = requests.get("https://api.fitbit.com/1/user/-/activities/heart/date/today/1d.json", headers=header).json()

# Access the 'activities' field inside the response
heart_data_list = heart_r.get('activities-heart', [])

heart_data_dict = {}

for entry in heart_data_list:
    date_time = entry.get('dateTime')
    resting_heart_rate = entry.get('value', {}).get('restingHeartRate')
    heart_data_dict[date_time] = resting_heart_rate

# Create a Pandas DataFrame from the dictionary
df = pd.DataFrame(list(heart_data_dict.items()), columns=['Date', 'Resting Heart Rate'])

# Print the DataFrame
print(df)