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
        best= gpd.read_file('./data/best_destinations_vancouver.geojson')
        df2 = pd.read_csv('./get_attractions/results/joined_data.csv')
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
        indexNames = df_rec[df_rec['distance'] <= 14]


        print("Locations you visited : ")
        print(df2['location'], "\n")
        print("Our reccomendations based on the locations you visited", "\n")
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
























