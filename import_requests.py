import requests
from bs4 import BeautifulSoup
from supabase_py import create_client, Client
# # WeatherDetailsListItem--label--2ZacS This is labels for general data
# # WeatherDetailsListItem--wxData--kK35q This is general data for day



locationCodes = ['USNJ0291', 'USPA1290', 'USNY0996', 'USMA0046', 'USPA1276', 'USCA0987', 'USCA0638', 'USIL0225', 'USDC0001', 'USFL0316']
highLowSet = set()

def getLocationData():
    for location in locationCodes:
        url = 'https://weather.com/weather/today/l/' + location
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        dataElements = soup.find_all(class_='WeatherDetailsListItem--wxData--kK35q')
        locationName = soup.find(class_='CurrentConditions--location--1YWj_').text
        highLowSet.add((locationName,dataElements[0].text))

def printLocationData():
    for location, temps in highLowSet:
        print(f'{location}: {temps}')

url = 'https://rwuiwmxmiopyovvrgpkm.supabase.co'
key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ3dWl3bXhtaW9weW92dnJncGttIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTI4NjY1MDQsImV4cCI6MjAyODQ0MjUwNH0.LJ46wnMzEGJMWB46VvSPuGE7It5CCApXTB6dbiCyFI0'
supabase: Client = create_client(url, key)


def exportToSupabase():
     for location, temps in highLowSet:
          highLow = temps.split('/')
          high = highLow[0]+'°'
          low = highLow[1]
          data = {
               'location': location,
               'high': high,
               'low': low
          }
          response = supabase.table('weather_data_high_low').insert(data).execute()


def main():
    getLocationData()
    printLocationData()
    #exportToSupabase()

main()