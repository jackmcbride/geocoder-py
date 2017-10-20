import pandas
import requests

def generate_table(file):
    #Google API key
    api_key = "AIzaSyBd9F3yew2L3FDRwjbXNZ1xY5DGOsLHG08"

    df = pandas.read_csv(file)
    latitudes = []
    longitudes = []

    df.columns = map(str.lower, df.columns)

    if 'address' not in df:
        return "Error"

    #Fetch geocode data for each address using Google API
    for address in df["address"]:
        api_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(address, api_key))
        api_response_dict = api_response.json()

        if api_response_dict['status'] == 'OK':
            latitudes.append(api_response_dict['results'][0]['geometry']['location']['lat'])
            longitudes.append(api_response_dict['results'][0]['geometry']['location']['lng'])
        else:
            latitudes.append(None)
            longitudes.append(None)

    latitudes = pandas.Series(latitudes)
    longitudes = pandas.Series(longitudes)

    df["latitude"] = latitudes.values
    df["longitude"] = longitudes.values

    df.columns = map(str.title, df.columns)

    df.to_csv("geocoding_data.csv")

    with open('templates/table.html', 'w') as fo:
        fo.write('<head><link href = "../static/main.css" rel="stylesheet"/> </head>')
        df.to_html(fo)
    