import csv
import json
import os
import requests
import sys
import re
import orodja
import time
from datetime import datetime
import Shranjevalnik


# URL glavne strani 
myanime_fp_url = 'https://myanimelist.net/anime/'

# Mapa za shranjevanje
anime_directory = 'Anime'

# Datoteka v katero bomo shranili glavno stran
fp_filename = 'index_anime.html'

#Json file
anime_json = 'Anime.json'

#ime CSV datoteke v katero bomo shranili podatke
csv_filename = 'anime.csv'

#stevilo idjev, ki jih bomo preverili
st_strani = 15000 # "preberemo id zadnje datoteke v mapi Anime"

# ---------------------------------------------------------------------------------------


Animeji = []


vzorec_bloka = re.compile(
        r'<h2>Alternative Titles</h2>'
        r'(.*?)<div class="clearfix mauto mt16" style="width:160px;padding-right:10px">',
        re.DOTALL
)
                        
vzorec_name = r'<link rel="preconnect" href="https://cdn.myanimelist.net" crossorigin="anonymous" />\n{1,3}<title>\n'r'(?P<name>[^\n]*)'r'\s+- MyAnimeList.net'
vzorec_id = r'<link rel="canonical" href="https://myanimelist.net/anime/'r'(?P<id>\d+)'r'/[^\n]*/>.*?'
vzorec_episodes = r'<span class="dark_text">Episodes:</span>\n\s+' r'(?P<episodes>.*)'r'\n\s+</div>\n\n<div>\n\s+<span class="dark_text">Status:</span>'
vzorec_studio = r'<span class="dark_text">Studios:</span>\n\s+<a href=".+">' r'(?P<studio>.*)'r'</a>  </div>'
vzorec_source = r'<span class="dark_text">Source:</span>\n\s+'r'(?P<source>[^\n]*)'r'\n.*<span class="dark_text">Genres:</span>'
vzorec_genres = r'<span itemprop="genre" style="display: none">(?P<genre>.{1,10})</span><a href="/anime/genre/\d+/.{1,10}" title=".{1,10}">.{1,10}</a>,?'
vzorec_rating = r'<span class="dark_text">Rating:</span>\n\s+'r'(?P<rating>\S*)'r'\s.*<h2>Statistics</h2>'
vzorec_score = r'<span class="dark_text">Score:</span>\n\s+<span itemprop="ratingValue" class="score-label score-\d">'r'(?P<score>.*)'r'</span><sup>1</sup>'
vzorec_aired = r'<div class="information-block di-ib clearfix"><span class="information season"><a href="https://myanimelist.net/anime/season/\d{4}/\w*">(?P<season>\d{4})</a>.*?'



vzorec_anime = re.compile(
    r'<link rel="preconnect" href="https://cdn.myanimelist.net" crossorigin="anonymous" />\n{1,3}<title>\n'r'(?P<name>[^\n]*)'r'\s+- MyAnimeList.net.*?'
    r'<link rel="canonical" href="https://myanimelist.net/anime/'r'(?P<id>\d+)'r'/[^\n]*/>.*?'
    r'<span class="dark_text">Episodes:</span>\n\s+' r'(?P<episodes>.*)'r'\n\s+</div>\n\n<div>\n\s+<span class="dark_text">Status:</span>.*?'
    r'<span class="dark_text">Aired:</span>\n\s+'r'(?P<aired>[^\n]*)'r'\n.*<span class="dark_text">Producers:</span>.*?'
    r'<span class="dark_text">Studios:</span>\n\s+<a href=".+">'r'(?P<studio>.*)'r'</a>  </div>.*?'
    r'<span class="dark_text">Source:</span>\n\s+'r'(?P<source>[^\n]*)'r'\n.*<span class="dark_text">Genres:</span>.*?'
    r'<span itemprop="genre" style="display: none">(?P<genre>.{1,10})</span><a href="/anime/genre/\d+/.{1,10}" title=".{1,10}">.{1,10}</a>,?.*?'
    r'<span class="dark_text">Rating:</span>\n\s+'r'(?P<rating>\S*)'r'\s.*<h2>Statistics</h2>.*?'
    r'<span class="dark_text">Score:</span>\n\s+<span itemprop="ratingValue" class="score-label score-\d">'r'(?P<score>.*)'r'</span><sup>1</sup>.*?'
    ,re.DOTALL
)
seznam_id = range(st_strani)
# seznam_OK_id = [element for element in seznam_id if element not in Error_404]

# print(f"Seznam OK ID = {seznam_OK_id}")

def precisti_podatke(slovar):
    anime = slovar
    anime['id'] = int(anime['id'])
    if anime["name"].find("&#039;") > 0:
        anime["name"] = anime["name"].replace("&#039;", "'")
    if anime["name"].find("&amp;") > 0:
        anime["name"] = anime["name"].replace("&amp;", "&")
    if len(anime["episodes"]) != 7: 
        anime['episodes'] = int(anime['episodes'])
    else: 
        anime['episodes'] = "Unknown"
    anime['genre'] = anime['genre'].strip().split(', ')
    anime['score'] = float(anime['score'])
    aired = anime["aired"]
    anime["leto"] = [int(s) for s in aired.split() if s.isdigit()][0]
    b = []
    b += anime["aired"]
    if b[-1] == "?":
        anime["status"] = "Curently Airing"
    else:
        anime["status"] = "Finished Airing"
    aired_sez = aired.split(" ")
    if aired_sez[0] == "Jan" or aired_sez[0] == "Feb" or aired_sez[0] == "Mar":
        anime["season"] = "Winter"
    elif aired_sez[0] == "Apr" or aired_sez[0] == "May" or aired_sez[0] == "Jun":
        anime["season"] = "Spring"
    elif aired_sez[0] == "Jul" or aired_sez[0] == "Aug" or aired_sez[0] == "Sep":
        anime["season"] = "Summer"
    else:
        anime["season"] = "Fall"
    return None



zanri = []

def extract_genres(slovar):
    for zanr in range(len(slovar["genre"])):
        new_d = {}
        new_d["id"] = slovar["id"]  
        new_d["genre"] = slovar["genre"][zanr]  
        zanri.append(new_d)  
    del slovar["genre"]

for noi in range(st_strani + 1):
    path1 = os.path.join(anime_directory, 'Anime-id{}.html'.format(noi)) 
    if os.path.exists(path1) == True: 
        ime_datoteke = 'Anime-id{}.html'.format(noi)
        path = os.path.join(anime_directory, ime_datoteke) 
        vsebina = orodja.vsebina_datoteke(path)
        genres_vzorec = re.compile(vzorec_genres, re.DOTALL)
        for zadetek in re.finditer(vzorec_anime, vsebina):
            genres = re.findall(genres_vzorec, vsebina)
            slovar = zadetek.groupdict()
            slovar["genre"] = ', '.join(genres)
            precisti_podatke(slovar)
            extract_genres(slovar)
            Animeji.append(slovar)
            print('ID:  {}   ----   Successfully saved "{}" in Anime.json.'.format(noi, slovar["name"]))
    else:
        pass


# print(Animeji) 
# print(zanri)      

orodja.zapisi_json(Animeji, anime_json)

orodja.zapisi_csv(Animeji, Animeji[0].keys(), csv_filename)

csv_zanri = "zanri.csv"
orodja.zapisi_csv(zanri, zanri[0].keys(),csv_zanri)

print("Task completed")