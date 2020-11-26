import geopandas as gpd
import matplotlib.pyplot as plt

plt.rcParams['figure.figsize'] = (20,10)


df_places = gpd.read_file('best_destinations_vancouver.geojson')
df_try = gpd.read_file('shoreline-2002.geojson')

ax = df_try.plot(color='green')

df_places.plot(ax=ax, scheme='quantiles', cmap='OrRd')
plt.show()


#get a picture
#get its lat and lon
#guess the place.
