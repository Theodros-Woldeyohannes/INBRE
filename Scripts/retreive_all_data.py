
import pandas as pd
import requests as rq
import datetime as dt
import os
from io import StringIO

# List of sensors, corresponding names, and date ranges
sensors_info = [
    ('149972', 'C2 - Site A', '2021-09-11', '2021-09-13'),
    ('105200', 'Albuqeruque', '2023-08-07', '2023-08-09'),
    ('170533', 'Albuquerque - Site B', '2021-03-15', '2021-03-17'),
    ('78031', 'Austin', '2023-08-15', '2023-08-17'),
    ('115313', 'Bend', '2023-08-01', '2023-08-03'),
    ('104690', 'Casper', '2023-08-20', '2023-08-22'),
    ('156841', 'Dekalb Co.', '2021-08-16', '2021-08-18'),
    ('127155', 'Dundas', '2023-05-21', '2023-05-23'),
    ('57157', 'Glendale', '2023-08-11', '2023-08-13'),
    ('51959', 'Houston', '2023-08-10', '2023-08-12'),
    ('137120', 'Irvine', '2020-10-25', '2020-10-27'),
    ('165605', 'Jefferson', '2023-05-10', '2023-05-12'),
    ('181053', 'Kansas City', '2023-05-18', '2023-05-20'),
    ('110634', 'Las Cruces - Site A', '2023-07-21', '2023-07-23'),
    ('2938', 'Las Cruces - Site B', '2021-11-20', '2021-11-22'),
    ('37693', 'Oakland', '2023-08-08', '2023-08-10'),
    ('12799', 'Pender Co.', '2021-02-13', '2021-02-15'),
    ('193773', 'Pensacola', '2023-08-14', '2023-08-16'),
    ('57157', 'Phoenix', '2021-06-06', '2021-06-08'),
    ('72315', 'Pitt Co.', '2023-08-05', '2023-08-07'),
    ('31619', 'Raleigh', '2022-11-25', '2022-11-27'),
    ('171959', 'Richmond', '2023-04-10', '2023-04-12'),
    ('156491', 'Rio Rancho - Site A', '2023-06-20', '2023-06-22'),
    ('55967', 'Rio Rancho - Site B', '2022-08-24', '2022-08-26'),
    ('36659', 'Roseburg', '2020-08-19', '2020-08-21'),
    ('197593', 'Salt River Reservation', '2019-10-24', '2019-10-26'),
    ('52019', 'Simi Valley', '2021-09-30', '2021-10-02'),
    ('121385', 'St. Clair Co.', '2023-08-12', '2023-08-14'),
    ('91785', 'Tuscon', '2021-04-29', '2021-05-01'),
    ('192023', 'Vinton', '2023-07-31', '2023-08-02'),
    ('186825', 'Wellford - Fire 1', '2023-07-14', '2023-07-16'),
    ('124793', 'Wellford - Fire 2', '2019-09-25', '2019-09-27'),
    ('115035', 'C2 - Site C', '2021-09-15', '2021-09-17')
]

# Define the base URL and headers
base_url = 'https://api.purpleair.com/v1/sensors/'
headers = {'X-API-Key': '43418ADC-5C99-11EE-A77F-42010A800009'}

# Create a new folder for the data
folderpath = r'C:\Users\mehdi\OneDrive\Bureau\P_AirData'
os.makedirs(folderpath, exist_ok=True)

# Loop through each sensor
for sensor_info in sensors_info:
    sensor_num, station_name, start_date_str, end_date_str = sensor_info

    # Convert date strings to UNIX timestamp
    start_timestamp = int(dt.datetime.strptime(start_date_str, '%Y-%m-%d').timestamp())
    end_timestamp = int(dt.datetime.strptime(end_date_str, '%Y-%m-%d').timestamp())

    # Build the URL for the sensor
    url = f'{base_url}{sensor_num}/history/csv'

    payload = {
        'fields': 'humidity_a, temperature_a, pressure_a, pm1.0_atm, pm2.5_atm, pm10.0_atm',
        'start_timestamp': start_timestamp,
        'end_timestamp': end_timestamp
    }

    # Make the API call
    r = rq.get(url=url, headers=headers, params=payload)

    # Check if the API call was successful (status code 200)
    if r.status_code == 200:
        # Read the CSV data into a DataFrame
        result = pd.read_csv(StringIO(r.text))

        # Convert UNIX time to UTC and then to local time (Mountain)
        result['time_stamp_UTC'] = pd.to_datetime(result['time_stamp'], unit='s', utc=True).dt.tz_convert('US/Mountain')

        # Sort the DataFrame by timestamp
        df = result.sort_values(by=['time_stamp'], ascending=False)

        # Extract the date from the timestamp for creating daily folders
        date_str = df['time_stamp_UTC'].iloc[0].strftime('%Y-%m-%d') if not df.empty else dt.datetime.now().strftime('%Y-%m-%d')

        # Create a folder for each day including the station name
        day_folder = os.path.join(folderpath, f'{date_str} - {station_name}')
        os.makedirs(day_folder, exist_ok=True)

        # Create a filename based on the sensor name
        filename = f'{station_name}-{sensor_num}.csv'

        # Full path for the CSV file
        filepath = os.path.join(day_folder, filename)

        # Save the DataFrame to the CSV file
        df.to_csv(filepath, index=False, header=True)

    else:
        print(f"Failed to retrieve data for sensor {sensor_num}. Status code: {r.status_code}")
