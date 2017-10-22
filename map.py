import folium
import pandas
import io
import math


def color_producer(df, employees):
    if employees < df["employees"].max() * 0.25:
        return "red"
    if employees < df["employees"].max() * 0.5:
        return "orange"
    elif employees < df["employees"].max() * 0.75:
        return "yellow"
    else:
        return "green"


def set_zoom(df):
    
    if len(df) < 10:
        return 11
    elif len(df) < 20:
        return 10
    elif len(df) < 40:
        return 9
    elif len(df) < 60:
        return 7
    elif len(df) < 80:
        return 5
    else:
        return 3

    

def generate_webmap(file):
    df=pandas.read_csv(file)
    df.columns = map(str.lower, df.columns)

    if "employees" in df:
        emp = list(df["employees"])
    
    df = df[pandas.notnull(df['latitude'])]
    
    lat = list(df["latitude"])
    lon = list(df["longitude"])
    name = list(df["name"])
    addr = list(df["address"])
    
    
    geo_map = folium.Map(location = [lat[0], lon[0]], zoom_start=set_zoom(df), tiles="Mapbox Bright")

    fgv = folium.FeatureGroup(name="Business")

    if "employees" in df:
        for lt, ln, em, ad, nm in zip(lat, lon, emp, addr, name):
            fgv.add_child(folium.CircleMarker(location=[lt,ln], radius=6,
            popup="%s: %s, Employees: %s" % (nm, ad, em), fill=True, fill_opacity=0.7, fill_color=color_producer(df, em)))
    
    else:
        for lt, ln, ad, nm in zip(lat, lon, addr, name):
            fgv.add_child(folium.CircleMarker(location=[lt,ln], radius=6,
            popup="%s: %s" % (nm, ad), fill=True, fill_opacity=0.7, fill_color=color_producer(df, em)))


    geo_map.add_child(fgv)
    geo_map.add_child(folium.LayerControl())
    geo_map.save("templates/webmap.html")


