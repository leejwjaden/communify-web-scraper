import requests
from bs4 import BeautifulSoup
from supabase_py import create_client, Client
# # WeatherDetailsListItem--label--2ZacS This is labels for general data
# # WeatherDetailsListItem--wxData--kK35q This is general data for day

# Dictionary with the keys corresponding to their location codes
locationCodes = {'Maplewood': 'USNJ0291', 'Pittsburgh': 'USPA1290', 'Manhattan': 'USNY0996', 'Boston': 'USMA0046', 'Philadelphia': 'USPA1276',
                 'San Francisco': 'USCA0987', 'Los Angeles': 'USCA0638', 'Chicago': 'USIL0225', 'Washington': 'USDC0001', 'Miami': 'USFL0316'}
# locationCodes = ['USNJ0291', 'USPA1290', 'USNY0996', 'USMA0046', 'USPA1276', 'USCA0987', 'USCA0638', 'USIL0225', 'USDC0001', 'USFL0316']
highLowList = []

## Uses pre-determined list of location codes and adds specific data to a list containing location and it's relevant data
def getLocationData():
    for location in locationCodes:
        url = 'https://weather.com/weather/today/l/' + locationCodes[location]
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        dataElements = soup.find_all(class_='WeatherDetailsListItem--wxData--kK35q')
        locationName = soup.find(class_='CurrentConditions--location--1YWj_').text
        highLowList.append((locationName,dataElements[0].text))


def printLocationData():
    for location, temps in highLowList:
        print(f'{location}: {temps}')

url = 'https://rwuiwmxmiopyovvrgpkm.supabase.co'
key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ3dWl3bXhtaW9weW92dnJncGttIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTI4NjY1MDQsImV4cCI6MjAyODQ0MjUwNH0.LJ46wnMzEGJMWB46VvSPuGE7It5CCApXTB6dbiCyFI0'
supabase: Client = create_client(url, key)

# # Accesses data within highLow list and splits the high and low temperatures. Imports this data into supabase
def exportToSupabase():
     for location, temps in highLowList:
          highLow = temps.split('/')
          high = highLow[0]+'°'
          low = highLow[1]
          data = {
               'location': location,
               'high': high,
               'low': low
          }
          response = supabase.table('weather_data_high_low').insert(data).execute()

# When using in GCP, two arguements will need to be included in the main function
def main():
    highLowList = []
    getLocationData()
    printLocationData()
    #exportToSupabase()

main()