import requests
from bs4 import BeautifulSoup

# # WeatherDetailsListItem--label--2ZacS This is labels for general data
# # WeatherDetailsListItem--wxData--kK35q This is general data for day



locationCodes = ['USNJ0291', 'USPA1290', 'USNY0996', 'USMA0046', 'USPA1276', 'USCA0987', 'USCA0638', 'USIL0225', 'USDC0001', 'USFL0316']
highLowSet = set()

for location in locationCodes:
    url = 'https://weather.com/weather/today/l/' + location
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    dataElements = soup.find_all(class_='WeatherDetailsListItem--wxData--kK35q')
    locationName = soup.find(class_='CurrentConditions--location--1YWj_').text
    highLowSet.add((locationName,dataElements[0].text))

for location, temps in highLowSet:
    print(f'{location}: {temps}')

print("test")