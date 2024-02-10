
import requests
import json
import pandas as pd

token = "<insert token here>"
header2 = {'Authorization' : 'Bearer {}'.format(token), 'accept-language' : 'en_US'}
water_r = requests.get("https://api.fitbit.com/1/user/-/foods/log/water/date/today/1d.json", headers=header2).json()

# Access the 'activities' field inside the response
water_break = water_r['foods-log-water']

# Extract relevant fields from the JSON data and create a list of dictionaries
water_data = []
for data in water_break:
    water_row = {
        "Date": data["dateTime"],
        "Ounces": data["value"]
    }
    water_data.append(water_row)

# Create a Pandas DataFrame from the list of dictionaries
df = pd.DataFrame(water_data)

# Print the DataFrame
print(df)





