import requests
import json
import pandas as pd
import boto3

def lambda_handler(event = None, context = None):
    token = "<insert token here>"
    header = {'Authorization' : 'Bearer {}'.format(token)}
    header_us = {'Authorization' : 'Bearer {}'.format(token), 'accept-language' : 'en_US'}
    
    # Make all the requests
    steps_r = requests.get("https://api.fitbit.com/1/user/-/activities/steps/date/today/1d.json", headers=header).json()
    sleep_r = requests.get("https://api.fitbit.com/1.2/user/-/sleep/date/today.json", headers=header).json()
    nutrition_r = requests.get("https://api.fitbit.com/1/user/-/foods/log/caloriesIn/date/today/1d.json", headers=header).json()
    water_r = requests.get("https://api.fitbit.com/1/user/-/foods/log/water/date/today/1d.json", headers=header_us).json()
    # Since Heart data is mixed between two different clusters its structure to get data is different. It levarges the JSON package to get data.
    heart_r = requests.get("https://api.fitbit.com/1/user/-/activities/heart/date/today/1d.json", headers=header).json()
    
    #Breakdown a Layer of JSON data
    steps_break = steps_r["activities-steps"]
    sleep_break = sleep_r["sleep"]
    nutrition_break = nutrition_r['foods-log-caloriesIn']
    water_break = water_r['foods-log-water']
    heart_break = heart_r.get('activities-heart', [])
    

    
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
    
    # Convert the DataFrame to CSV format
    steps_csv_data = steps_df.to_csv(index=False).encode('utf-8')
    
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
    
    # Convert the DataFrame to CSV format
    sleep_csv_data = sleep_df.to_csv(index=False).encode('utf-8')
    
    #Breakdown of json data for nutrition data
    nutrition_data = []
    for data in nutrition_break:
        nutrition_row = {
        "Date": data["dateTime"],
        "Calories": data["value"]
        }
        nutrition_data.append(nutrition_row)
    
    # Convert the data to a Pandas DataFrame
    nutrition_df = pd.DataFrame(nutrition_data)
    
    # Convert the DataFrame to CSV format
    nutrition_csv_data = nutrition_df.to_csv(index=False).encode('utf-8')
    
    #Breakdown of json data for water data
    water_data = []
    for data in water_break:
        water_row = {
        "Date": data["dateTime"],
        "Ounces": data["value"]
        }
        water_data.append(water_row)
    
    # Convert the data to a Pandas DataFrame
    water_df = pd.DataFrame(water_data)
    
    # Convert the DataFrame to CSV format
    water_csv_data = water_df.to_csv(index=False).encode('utf-8')
    
    # Hold data in a dictionary
    heart_data = {}
    
    for data in heart_break:
        date_time = data.get('dateTime')
        resting_heart_rate = data.get('value', {}).get('restingHeartRate')
        heart_data[date_time] = resting_heart_rate
    
    # Create a Pandas DataFrame from the dictionary
    heart_df = pd.DataFrame(list(heart_data.items()), columns=['Date', 'Resting Heart Rate'])
    
    # Convert the DataFrame to CSV format
    heart_csv_data = heart_df.to_csv(index=False).encode('utf-8')
    
    
    # Initialize the S3 client
    s3 = boto3.client('s3')

    # Define the S3 bucket name
    bucket_name = 'api-test-cj'
    
    # Define CSV data and their corresponding keys
    csv_data = {
        'steps': steps_csv_data,
        'sleep': sleep_csv_data,
        'nutrition': nutrition_csv_data,
        'water': water_csv_data,
        'heart': heart_csv_data
    }
    
    # Iterate over the CSV data and upload to S3
    for key, data in csv_data.items():
        object_key = "csv/" + key + ".csv"
        s3.put_object(
            Bucket=bucket_name,
            Key=object_key,
            Body=data,
            ContentType='text/csv'
        )

    return {
        'statusCode': 200,
        'body': 'CSV data stored in S3'
    }

print(lambda_handler())
