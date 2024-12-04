import requests
import csv

# Replace with your own API key and list of sensor IDs
API_KEY = '43418ADC-5C99-11EE-A77F-42010A800009'
SENSOR_IDS = ['176247', '176209', '185075', '176215'
]  # Replace with actual sensor IDs

# path

path = r'C:\Users\jacks\Documents\UNM\P50\INBRE\Stations/'

# Output CSV file name
output_file = path + 'sensor_locations.csv'

# PurpleAir API endpoint base URL
base_url = 'https://api.purpleair.com/v1/sensors/'

# Headers including the API key for authentication
headers = {
    'X-API-Key': API_KEY
}

# Open CSV file for writing
with open(output_file, mode='w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    # Write header row
    csv_writer.writerow(['Sensor ID', 'Latitude', 'Longitude'])
    
    # Loop through each sensor ID
    for sensor_id in SENSOR_IDS:
        url = f'{base_url}{sensor_id}'
        try:
            # Send a GET request to the API
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors

            # Parse the JSON response
            data = response.json()
            sensor_data = data.get('sensor', {})

            # Extract latitude and longitude
            latitude = sensor_data.get('latitude')
            longitude = sensor_data.get('longitude')

            if latitude is not None and longitude is not None:
                # Write to CSV
                csv_writer.writerow([sensor_id, latitude, longitude])
                print(f"Sensor ID: {sensor_id} - Latitude: {latitude}, Longitude: {longitude}")
            else:
                print(f"Latitude or longitude data is missing for sensor {sensor_id}.")
        except requests.exceptions.HTTPError as err:
            # Handle HTTP errors (e.g., invalid API key, sensor not found)
            print(f"HTTP error occurred for sensor {sensor_id}: {err}")
        except requests.exceptions.RequestException as err:
            # Handle other request exceptions
            print(f"Error occurred for sensor {sensor_id}: {err}")
        except ValueError:
            # Handle JSON decoding errors
            print(f"Error decoding JSON response for sensor {sensor_id}.")

print(f"Data has been written to {output_file}.")

