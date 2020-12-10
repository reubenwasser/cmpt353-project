#uses the already generated 'joined_data.csv' to print out the locations user visited and
#suggests all the nearby locations user could visit based on the dataset from the scraped values.

#NOTE : using the pics2 as the sample for geotagged pictures.

from geopy.geocoders import Nominatim
import geopandas as gpd
from haversine import haversine, Unit
import sys
import pandas as pd


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

def recommendations():
        print("This might take some time... but we try our best :)")

        #Creating intial dataframes
        best= gpd.read_file('./data_extraction/data/best_destinations_vancouver.geojson')
        df2 = pd.read_csv('./get_attractions/results/joined_data.csv')
        geoloc = Nominatim(user_agent="test_app")
        df = best.loc[:, ['lat','lng','tourism']]
        df = df.dropna(subset=['lat'])
        rec = []
        tour = []
        places = [] 
        
        #get all the resulting columns.
        df['location_name'] = df.apply(lambda x: get_location(x.lat, x.lng, geoloc), axis=1)
        print(df.location_name)
        df['coords'] = df.apply(lambda x: get_coords(x.lat, x.lng), axis=1)
        df2['coords'] = df2.apply(lambda x: get_coords(x.lat, x.lon), axis=1)
        # print(df2)
        df.apply(lambda x: nearby_locations(x.coords, x.tourism, x.location_name, rec, df2, tour, places), axis = 1)
        # print(rec)
        # print(tour)
        # print(places)

        data = {'distance':rec, 
                'type':tour,
                'location': places} 
        
        #dataframe as a result of haversine.
        df_rec = pd.DataFrame(data) 
        df_rec = df_rec.sort_values(by=['type'], ascending = True)

        #creating the dataframe with all the recommendations.
        indexNames = df_rec[df_rec['distance'] <= 2]

        print("Locations you visited : ")
        print(df2['location'], "\n")
        print("Our recommendations based on the locations you visited", "\n")
        print("Note for Team: Non-specific type reccomendations, Remove this once implemented")
        print(indexNames)


#WORK IN PROGRESS!
#########################################################################################

#print(" For specific categories enter category out of the listed ones, for all types of reccomendations type 'None' ", "\n")
#print("  -> Botanical gardens, -> Aquarium", "\n",
#" -> Attraction, -> Artwork", "\n",
#" -> Hotel, ->  Museum", "\n", 
#" -> Viewpoint", "\n")
#val = input("Enter your value: ") 
#print(val)


#def matching(df_str, df_place):
# if df_str == val:  
#  rec_list.append(df_place)

#indexNames['type'].apply(matching, df_place = indexNames['location'])
#print(rec_list)


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























