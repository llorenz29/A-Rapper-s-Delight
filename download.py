from urllib.request import Request, urlopen, quote # Python 3
from bs4 import BeautifulSoup
from difflib import SequenceMatcher as sm # For comparing similarity of lyrics
import requests
import json
import os
from pathlib import Path
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# Import client access token from environment variable
import lyricsgenius as genius
token = "SECRET"

# So it will not timeout
genius_obj = genius.Genius(token, timeout=600) 



# We want to reject songs that have already been added to artist collection
def songsAreSame(s1, s2):    
    # Idea credit: https://bigishdata.com/2016/10/25/talkin-bout-trucks-beer-and-love-in-country-songs-analyzing-genius-lyrics/
    # Compare lyric content using SequenceMatcher
    seqA = sm(None, s1.lyrics, s2['lyrics'])
    seqB = sm(None, s2['lyrics'], s1.lyrics)
    return seqA.ratio() > 0.5 or seqB.ratio() > 0.5

# def songInArtist(new_song):    
#     # artist_lyrics is global (works in Jupyter notebook)
#     for song in artist_lyrics['artists'][-1]['songs']:
#         if songsAreSame(new_song, song):
#             return True
#     return False

def getListFromRanker_Selenium():
    
    s=Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s)
    driver.get("https://www.ranker.com/crowdranked-list/the-greatest-rappers-of-all-time")
    
    #to load
    time.sleep(1)
    pg = driver.find_element(By.TAG_NAME,"body")
    no_of_pagedowns = 200

    while no_of_pagedowns >=0:
        pg.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.4)
        no_of_pagedowns-=1
        print("runnin...")
        print(no_of_pagedowns)

    artist_elements = driver.find_elements(By.CLASS_NAME,"gridItem_name__wCyGi")
    artist_names = [a.text for a in artist_elements[:-1]]
    driver.quit()
    return artist_names

def downloadLyrics(artist_names, max_songs=None):
    artist_objects = []
    # Check to see if the artist lyrics have already been downloaded
    directory_path = '/Users/lukelorenz/Desktop/IndependentProjects/2021/Rappa'


    for name in artist_names:
        name_written = False
        for file in Path(directory_path).glob('*.json'):
            if(name in file.name):
                name_written = True
                print("Already searched {name}".format(name=name))
                print(file.name)
        if(not name_written):        
            artist_objects.append(genius_obj.search_artist(name,max_songs=200))
            genius_obj.save_artists(artist_objects, overwrite=True)

def main():
    
    print("Running...")
    artist_names = getListFromRanker_Selenium(url)
    
    print(artist_names)
    print(len(artist_names))
    downloadLyrics(artist_names)
    print("Done")

if __name__ == '__main__':
    main()