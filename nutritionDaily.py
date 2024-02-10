import requests
import pandas as pd

token = "<insert token here>"
header = {'Authorization' : 'Bearer {}'.format(token)}
nutrition_r = requests.get("https://api.fitbit.com/1/user/-/foods/log/caloriesIn/date/today/1d.json", headers=header).json()

# Access the nutrition field inside the response
nutrition_break = nutrition_r['foods-log-caloriesIn']

# Extract relevant fields from the JSON data and create a list of dictionaries
nutrition_data = []
for data in nutrition_break:
    nutrition_row = {
        "Date": data["dateTime"],
        "Calories": data["value"]
    }
    nutrition_data.append(nutrition_row)

# Create a Pandas DataFrame from the list of dictionaries
df = pd.DataFrame(nutrition_data)

# Print the DataFrame
print(df)