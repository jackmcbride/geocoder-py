import folium
import pandas
import io


def color_producer(employees):
    if employees < 10:
        return "green"
    elif employees < 20:
        return "orange"
    else:
        return "red"
    

def generate_webmap():
    df=pandas.read_csv("geocoding_data.csv")
    df.columns = map(str.lower, df.columns)

    if "employees" in df:
        emp = list(df["employees"])
    
    lat = list(df["latitude"])
    lon = list(df["longitude"])
    name = list(df["name"])

    geo_map = folium.Map(location = [df["latitude"][0], df["longitude"][0]], zoom_start=11, tiles="Mapbox Bright")

    fgv = folium.FeatureGroup(name="Business")

    for lt, ln, em, nm in zip(lat, lon, emp, name):
        fgv.add_child(folium.CircleMarker(location=[lt,ln], radius=6,
        popup="%s: ~%s employees" % (nm, em), fill=True, fill_opacity=0.7, color="grey", fill_color=color_producer(em)))
    
    geo_map.add_child(fgv)
    geo_map.add_child(folium.LayerControl())
    geo_map.save("templates/webmap.html")

