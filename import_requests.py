## This is a html webscraper that takes data from weather.com and exports the highs and lows of locations to a database (Supabase)
## Meant to be run at 12 noon everday on Google Cloud Platform

import requests
from bs4 import BeautifulSoup
from supabase_py import create_client, Client
from datetime import date
# # WeatherDetailsListItem--label--2ZacS This is labels for general data
# # WeatherDetailsListItem--wxData--kK35q This is general data for day


url = 'https://rwuiwmxmiopyovvrgpkm.supabase.co'
key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ3dWl3bXhtaW9weW92dnJncGttIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTI4NjY1MDQsImV4cCI6MjAyODQ0MjUwNH0.LJ46wnMzEGJMWB46VvSPuGE7It5CCApXTB6dbiCyFI0'
supabase: Client = create_client(url, key)

highLowList = []

## Uses pre-determined list of location codes and adds specific data to a list containing location and it's relevant data
def getLocationData(locationCodes):
    try:
        for location in locationCodes:
            url = 'https://weather.com/weather/today/l/' + locationCodes[location]
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            dataElements = soup.find_all(class_='WeatherDetailsListItem--wxData--kK35q')
            locationName = soup.find(class_='CurrentConditions--location--1YWj_').text
            highLowList.append((locationName,dataElements[0].text))
    except Exception as e:
        print(f'Error getting location data: {e}' )


# Collects the location id, name, and code from our Supabase location table
def getLocationAttributes():
    try:
        query = supabase.table('locations').select('id', 'location_name', 'location_code').execute()
        return(query)
    except Exception as e:
        print(f'Error getting location attributes: {e}')

# Prints location data to logs
def printLocationData():
    for location, temps in highLowList:
        print(f'{location}: {temps}')


#Checks if current date is in our date table
def checkDate(table, column, date):
    try:
        query = supabase.table(table).select('id').filter(column, 'eq', date).limit(1).execute()
        return len(query['data']) > 0
    except Exception as e:
        print(f'Error getting date: {e}')



# Gets the current date(M/D/YR) which will be added to the date table
def getDate():
    today = date.today().strftime("%m/%d/%y")
    return today

#Retrieves the ID of our date
def getDateID(date):
    try:
        query = supabase.table('dates').select('id').filter('date', 'eq', date).limit(1).execute()
        return(query)
    except Exception as e:
        print(f'Error getting date ID: {e}')

# # Accesses data within highLow list and splits the high and low temperatures. Imports this data into supabase
def exportToSupabase(locationIDs, currentDate):
    for location, temps in highLowList:
        locationID = locationIDs[location]
        dateID = getDateID(currentDate)['data'][0]['id']
        highLow = temps.split('/')
        high = highLow[0]
        high = int(high[:-1])
        low = highLow[1]
        low = int(low[:-1])
        data = {
            'location_id': locationID,
            'date_id': dateID,
            'high_temp': high,
            'low_temp': low
            }
        try:
            response = supabase.table('highlowdata').insert(data).execute()
        except Exception as e:
            print(f'Error while exporting to Supabase: {e}')
        


# When using in GCP, two arguements will need to be included in the main function (ie. main(data, context))
def main():
    currentDate = getDate()
    if not checkDate('dates', 'date', currentDate):
        data = {
            'date': currentDate
            }
        response = supabase.table('dates').insert(data).execute()
    else:
        return # Prevents duplicate exporting of the same location, same day
    print('proceeding')
    highLowList = []
    locationCodes = {}
    locationIDs = {}
    attributes = getLocationAttributes()['data']
    for location in attributes:
        locationCodes[location['location_name']] = location['location_code']
        locationIDs[location['location_name']] = location['id']
    getLocationData(locationCodes)
    printLocationData()
    exportToSupabase(locationIDs, currentDate)

main()