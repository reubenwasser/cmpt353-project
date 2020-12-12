
from geopy.geocoders import Nominatim
import geopandas as gpd
from haversine import haversine, Unit
import sys
import pandas as pd
import re

print(" For specific categories enter category out of the listed ones, for all types of reccomendations type 'None' ", "\n")
print("  -> Botanical gardens, -> Aquarium", "\n",
" -> Attraction, -> Artwork", "\n",
" -> Hotel, ->  Museum", "\n", 
" -> Viewpoint", "\n")
#val = input("Enter your value: ") 
#print(val)
val2 = input("Enter number")
val2 = float(val2)



def get_location(lat,lon,geolocator):
        co = (lat, lon)
        location = geolocator.reverse(co)
        return location
 
def get_coords(lat,lon):
        co = (lat,lon)
        return co 
 
def nearby_locations(pt, typep, place, rec, df2, tour, places):
        for j in df2['coords']:
                rec.append(haversine(pt, j))
                tour.append(typep)
                places.append(place)
  


def matching(typeo):
        if typeo == val:  
          return 1
        else:
          return 0   

def recommendations():
        print("This might take some time... but we try our best :)")

        #Creating intial dataframes
        best= gpd.read_file('./data_extraction/data/best_destinations_vancouver.geojson').reset_index(drop = True)
        df2 = pd.read_csv('./get_attractions/results/joined_data.csv').reset_index(drop = True)
        geoloc = Nominatim(user_agent="test_app")
        df = best.loc[:, ['lat','lng','tourism']]
        df = df.dropna(subset=['lat'])
        rec = []
        tour = []
        places = [] 
        
        #get all the resulting columns.
        df['location_name'] = df.apply(lambda x: get_location(x.lat, x.lng, geoloc), axis=1)
        df['coords'] = df.apply(lambda x: get_coords(x.lat, x.lng), axis=1)
        df2['coords'] = df2.apply(lambda x: get_coords(x.lat, x.lon), axis=1)
        
        df.apply(lambda x: nearby_locations(x.coords, x.tourism, x.location_name, rec, df2, tour, places), axis = 1)
        

        data = {'distance':rec, 
                'type':tour,
                'location': places} 
        
        #dataframe as a result of haversine.
        df_rec = pd.DataFrame(data) 
        df_rec = df_rec.sort_values(by=['type'], ascending = True)

        #creating the dataframe with all the recommendations.
        indexNames = df_rec[df_rec['distance'] <= val2]
        indexNames = indexNames.reset_index(drop = True)
        
        
        
        indexNames['location'] = indexNames['location'].astype('str')
        #indexNames['result'] = indexNames['type'].apply(matching)
        
        
        
        
        #labels = []
        #labels.append('result')
        #labels.append('distance')
        
        
        #indexNames = indexNames.loc[lambda x: x.result == 0] 
        
             

        #print("Locations you visited : ")
        #print(df2['location'], "\n")
        indexNames = indexNames.drop_duplicates(subset = 'location',keep = 'first')
        print("Our recommendations based on the locations you visited", "\n")
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
              print(indexNames)
































#Tried a different implementation
########################################################################################

# import geopandas as gpd
# import pandas as pd
# from itertools import combinations
# from shapely.geometry import LineString
# import folium
# import webbrowser


# def recommendations():
#         print("This might take some time... but we try our best :)")

#         #Creating intial dataframes
#         attractions = gpd.read_file('./data/best_destinations_vancouver.geojson')
#         df = pd.read_csv('./get_attractions/results/joined_data.csv')

#         photos = gpd.GeoDataFrame(
#                 df, geometry=gpd.points_from_xy(df.lat, df.lon), crs="epsg:26910")

#         #reproject both dataframes to NAD_83 - UTM timezone 10N, best projection for Vancouver
#         attractions = attractions.to_crs('epsg:26910')  
#         photos = photos.to_crs('epsg:26910')  
#         # photos.crs = "EPSG:4326"  
#         # photos = photos.geometry.to_crs({'init': 'EPSG:4326'})  
#         # photos = photos.to_crs({'init': 'epsg:26910'})  

#         photos.to_file("output.geojson", driver="GeoJSON")
#         print(photos)

#         print(photos.crs)
#         print(attractions.crs)

#         photos['geometry'] = photos.geometry.buffer(0.002)

#         # photos.plot()

#         print(attractions)
#         print(photos)

#         attractions.to_file("output1.geojson", driver="GeoJSON")























