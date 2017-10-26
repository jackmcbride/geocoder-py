import pandas
import requests
from geopy.geocoders import Nominatim


def generate_table(file):
    df=pandas.read_csv(file)
    df.columns = map(str.lower, df.columns)

    gc=Nominatim(scheme='http')

    df["coordinates"]=df["address"].apply(gc.geocode, timeout=10)
    df['latitude'] = df['coordinates'].apply(lambda x: x.latitude if x != None else None)
    df['longitude'] = df['coordinates'].apply(lambda x: x.longitude if x != None else None)

    df=df.drop("coordinates",1)
    df=df.drop("id",1)

    df.columns = map(str.capitalize, df.columns)
    df.to_csv(file,index=None)

    with open('templates/table.html', 'w') as fo:
        fo.write('<head><link href = "../static/main.css" rel="stylesheet"/> </head>')
        df.to_html(fo)
    