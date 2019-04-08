import folium
import pandas

data = pandas.read_csv("Volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
name = list(data["NAME"])
elev = list(data["ELEV"])

html = """<h4><a href="https://www.google.com/search?q=%%22%s Volcano%%22" target="_blank">%s Volcano</h4></a>
Height: %s m
"""

def color_def(elev):
    if elev < 1100:
        return 'green'
    elif elev < 2001:
        return 'orange'
    else:
        return 'red'

map = folium.Map(location=[38.5, -99], zoom_start=6, tiles="Mapbox Bright")

fgv = folium.FeatureGroup(name="Volcanoes")

for lt, ln, nm, el in zip(lat, lon, name, elev):
    iframe = folium.IFrame(html=html % (nm, nm, el), width=200, height=100)
    fgv.add_child(folium.CircleMarker(location=[lt, ln], popup=folium.Popup(iframe),
    radius=7, fill_opacity=0.6, color='grey', fill_color=color_def(el)))

fgp = folium.FeatureGroup(name="Population")
fgp.add_child(folium.GeoJson(data=(open('world.json', 'r', encoding='utf-8-sig').read()),
style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000
else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

map.add_child(fgp)
map.add_child(fgv)
map.add_child(folium.LayerControl())
map.save("Map1.html")
