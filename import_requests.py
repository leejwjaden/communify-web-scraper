import requests
from bs4 import BeautifulSoup
from supabase_py import create_client, Client
from datetime import date
# # WeatherDetailsListItem--label--2ZacS This is labels for general data
# # WeatherDetailsListItem--wxData--kK35q This is general data for day

# Dictionary with the keys corresponding to their location codes
highLowList = []
## Uses pre-determined list of location codes and adds specific data to a list containing location and it's relevant data
def getLocationData(locationCodes):
    for location in locationCodes:
        url = 'https://weather.com/weather/today/l/' + locationCodes[location]
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        dataElements = soup.find_all(class_='WeatherDetailsListItem--wxData--kK35q')
        locationName = soup.find(class_='CurrentConditions--location--1YWj_').text
        highLowList.append((locationName,dataElements[0].text))


# Collects the location id, name, and code from our Supabase location table
def getLocationAttributes():
    query = supabase.table('locations').select('id', 'location_name', 'location_code').execute()
    return(query)

# Prints location data to logs
def printLocationData():
    for location, temps in highLowList:
        print(f'{location}: {temps}')

url = 'https://rwuiwmxmiopyovvrgpkm.supabase.co'
key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ3dWl3bXhtaW9weW92dnJncGttIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTI4NjY1MDQsImV4cCI6MjAyODQ0MjUwNH0.LJ46wnMzEGJMWB46VvSPuGE7It5CCApXTB6dbiCyFI0'
supabase: Client = create_client(url, key)

def exportDate():
    currentDate = getDate() 

#Checks if current date is in our date table
def checkDate(table, column, date):
    query = supabase.table(table).select('id').filter(column, 'eq', date).limit(1).execute()
    return len(query) > 0



# Gets the current date(M/D/YR) which will be added to the date table
def getDate():
    today = date.today().strftime("%m/%d/%y")
    return today

# # Accesses data within highLow list and splits the high and low temperatures. Imports this data into supabase
def exportToSupabase():
    currentDate = getDate()
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


# When using in GCP, two arguements will need to be included in the main function (ie. main(data, context))
def main():
    print(checkDate('dates', 'date', getDate()))
    highLowList = []
    locationCodes = {}
    attributes = getLocationAttributes()['data']
    for location in attributes:
        locationCodes[location['location_name']] = location['location_code']
    getLocationData(locationCodes)
    printLocationData()
    # exportToSupabase()
main()