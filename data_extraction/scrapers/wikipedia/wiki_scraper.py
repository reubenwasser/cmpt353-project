import requests
from bs4 import BeautifulSoup
import random
import wikipedia
import pandas as pd
from time import sleep


# Goes through each wikipadia page in the array of titles and gets title, content, image url, lat and long attributes and returns this as a dataframe
def getWikiAtrributes(DataFrame, Titles):
    for article in Titles:
        try:
            info = wikipedia.page(article)
        except wikipedia.exceptions.DisambiguationError as e:
            print("DisambiguationError: following options appear for article: \n")
            print(e.options)
        except wikipedia.exceptions.PageError:
            print("Article not found for: " + article)
        except requests.exceptions.ConnectionError:
            requests.status_code = "Connection refused"
            print(DataFrame)
            sleep(30)
        try:
            DataFrame = DataFrame.append({'title': article, 'content': info.content, 'images': info.images, 'lat': info.coordinates[0], 'lng': info.coordinates[1]}, ignore_index=True)
        except:
            print("Attributes missing for: " + article) 
    return(DataFrame)
    
# Gets pages within a radius of 10 km (MAXIMUM) of the coordinates given
PAGES = wikipedia.geosearch(49.2827, -123.1207, title=None, results=100000, radius=10000)

#Create dataframe 
df = pd.DataFrame(columns=['title', 'content', 'images', 'lat', 'lng' ])

# Get attributes
wikipediaAttributes = getWikiAtrributes(df, PAGES)

print(wikipediaAttributes)

# Save to CSV
wikipediaAttributes.to_csv('../../data/wikipedia.csv')


