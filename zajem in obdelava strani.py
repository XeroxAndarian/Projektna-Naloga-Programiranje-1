import csv
import json
import os
import requests
import sys
import re
import orodja
import time
import datetime
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
start = 0
st_strani = 43045 # "preberemo id zadnje datoteke v mapi Anime max = 43045"


# Jan, Feb, Mar -----> winter -------> 1
# Apr, May, Jun -----> spring -------> 2
# Jul, Aug, Sep -----> summer -------> 3
# Oct, Nov, Dec -----> fall   -------> 4
# ---------------------------------------------------------------------------------------


Animeji = []
seasons = ["Winter", "Spring", "Summer", "Fall"]

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

def number_from_string(string):
    seznam = list(string.split(" "))
    seznam2 = []
    seznam3 = []
    seznam4 = []
    for i in seznam:
        if i.find("1") == 0 or i.find("2") == 0:
            seznam3.append(i)
        else:
            seznam2.append(i)
    for j in seznam3:
        if len(j) == 4:
            seznam4.append(j)
    return int(seznam4[0])



vzorec_anime = re.compile(
    r'<link rel="preconnect" href="https://cdn.myanimelist.net" crossorigin="anonymous" />\n{1,3}<title>\n'r'(?P<name>[^\n]*)'r'\s+- MyAnimeList.net.*?'
    r'<link rel="canonical" href="https://myanimelist.net/anime/'r'(?P<id>\d+)'r'/[^\n]*/>.*?'
    r'<span class="dark_text">Episodes:</span>\n\s+' r'(?P<episodes>.*)'r'\n\s+</div>\n\n<div>\n\s+<span class="dark_text">Status:</span>\n\s+'r'(?P<status>[^\d]+)'r'\n\s*</div>.*?'
    r'<span class="dark_text">Aired:</span>\n\s+'r'(?P<aired>[^\n]*)'r'\n.*<span class="dark_text">Producers:</span>.*?'
    r'<span class="dark_text">Studios:</span>\n\s+(None found, )?<a href=".+">'r'(?P<studio>.*)'r'</a>  </div>.*?'
    r'<span class="dark_text">Source:</span>\n\s+'r'(?P<source>[^\n]*)'r'\n.*<span class="dark_text">Genres:</span>.*?'
    r'<span itemprop="genre" style="display: none">(?P<genre>.{1,10})</span><a href="/anime/genre/\d+/.{1,10}" title=".{1,10}">.{1,10}</a>,?.*?'
    r'<span class="dark_text">Rating:</span>\n\s+'r'(?P<rating>[^\n]*)'r'\s.*<h2>Statistics</h2>.*?'
    r'<span class="dark_text">Score:</span>\n\s+<span .+ score-(\d|na)">'r'(?P<score>.*)'r'</span><sup>1</sup>.*?'
    ,re.DOTALL
)
seznam_id = range(st_strani)
# seznam_OK_id = [element for element in seznam_id if element not in Error_404]

# print(f"Seznam OK ID = {seznam_OK_id}")

def precisti_podatke(slovar):
    anime = slovar
    for key in anime:
        if anime[key].find("&#039;") > 0:
            anime[key] = anime[key].replace("&#039;", "'")
        if anime[key].find("&amp;") > 0:
            anime[key] = anime[key].replace("&amp;", "&")
        if anime[key].find("&quot;") > 0:
            anime[key] = anime[key].replace("&quot;", '"')
    anime['id'] = int(anime['id'])
    if anime["episodes"] == "Unknown": 
        anime['episodes'] = None
    else: 
        anime['episodes'] = int(anime['episodes'])
    anime['genre'] = anime['genre'].strip().split(', ')
    if anime['score'] == "N/A":
        anime['score'] = None
    else :
        anime['score'] = float(anime['score'])
    if anime['studio'] == "add some":
        anime['studio'] = None
    air = anime['aired'].replace(",","").strip().split(" ")
    if anime['aired'] == "Not available":
        anime['aired'] = None
        anime['year'] = None
    elif len(air) == 1:
        anime['aired'] = air[0] 
        anime['year'] = air[0] 
    elif len(air) == 2:
        anime['aired'] = air[0]
        anime['year'] = air[1]  
    elif "to" not in air:
        anime['aired'] = air[0] + " " + air[1] + ", " + air[2]
        anime['year'] = air[2]
    else:
        p = air.index("to")
        if p == 2:
            anime['aired'] = air[0] + " " +  air[1]
        else:
            anime['aired'] = air[0] + " " + air[1] + ", " + air[2]
        anime['finished airing'] = air[-3] + " " + air[-2] + ", " + air[-1]
        anime['year'] = air[(p - 1)]
       
    
    if air[0] in ["Jan", "Feb", "Mar"]:
        anime['season'] = "Winter"
    if air[0] in ["May", "Jun", "Apr"]:
        anime['season'] = "Spring"
    if air[0] in ["Jul", "Sep", "Aug"]:
        anime['season'] = "Summer"
    if air[0] in ["Oct", "Nov", "Dec"]:
        anime['season'] = "Fall"
        
    
    
    

    return None



zanri = []

def extract_genres(slovar):
    for zanr in range(len(slovar["genre"])):
        new_d = {}
        new_d["id"] = slovar["id"]  
        new_d["genre"] = slovar["genre"][zanr]  
        zanri.append(new_d)  
    del slovar["genre"]


print("Obdelava zajetih podatkov se bo začela čez 30s. Predviden zaključek ob: {} ".format(datetime.datetime.now() + datetime.timedelta(seconds = (st_strani - start) * 0.5 + 30)))
time.sleep(0) #default 20
print("Obdelava se prične čez 10s.")
time.sleep(5)
print("Obdelava se prične šez 5s...")
time.sleep(1)
print("4...")
time.sleep(1)
print("3...")
time.sleep(1)
print("2...")
time.sleep(1)
print("1...")
time.sleep(1)
print("Obdelava zajetih podatkov se je začela. Predviden zaključek ob: {} ".format(datetime.datetime.now() + datetime.timedelta(seconds = (st_strani - start) * 0.5)))
counter = 0
for noi in range(start, st_strani + 1):
    path1 = os.path.join(anime_directory, 'Anime-id{}.html'.format(noi))
    if os.path.exists(path1) == True: 
        ime_datoteke = 'Anime-id{}.html'.format(noi)
        path = os.path.join(anime_directory, ime_datoteke) 
        vsebina = orodja.vsebina_datoteke(path)
        genres_vzorec = re.compile(vzorec_genres, re.DOTALL)
        for zadetek in re.finditer(vzorec_anime, vsebina):
            counter += 1
            genres = re.findall(genres_vzorec, vsebina)
            slovar = zadetek.groupdict()
            slovar["genre"] = ', '.join(genres)
            precisti_podatke(slovar)
            extract_genres(slovar)
            Animeji.append(slovar)
            print('ID:  {}   ----   Successfully saved "{}".'.format(noi, slovar["name"]))
    else:
        pass


# print(Animeji) 
# print(zanri)      
orodja.zapisi_json(Animeji, anime_json)
 
orodja.zapisi_csv(Animeji, Animeji[0].keys(), csv_filename)

csv_zanri = "zanri.csv"
orodja.zapisi_csv(zanri, zanri[0].keys(),csv_zanri)

print("Obdelava končana. Število obdelanih datotek: {}.".format(counter))
