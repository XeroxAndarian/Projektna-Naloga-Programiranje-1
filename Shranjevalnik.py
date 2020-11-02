import csv
import json
import os
import requests
import sys
import re
import orodja


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
st_strani = 10

Error_404 = []

def download_anime_page_id(st_strani):
    '''Shrani anime, ki je v bazi spletne strani pod id'''
    for i in range(st_strani):
        url = ('https://myanimelist.net/anime/{}'.format(i))
        ime_datoteke = 'Anime-id{}.html'.format(i)
        path = os.path.join(anime_directory, ime_datoteke)
        orodja.shrani_spletno_stran(url, path)
        #vsebina = orodja.vsebina_datoteke(ime_datoteke)
        #print(vsebina)
    return None




def filter_404(st_strani):
    '''Nekatere id-ji so "prazni" in v tem primeru nm spletna stran vrne napako 404. Ker ne želimo imeti te datoteke shranjene, bomo vse tipe takih datotek odstranili.'''
    
    for i in range(st_strani):
        ime_datoteke = 'Anime-id{}.html'.format(i)
        path = os.path.join(anime_directory, ime_datoteke)
        with open(path, encoding='utf-8') as dat:
            if '404 Not Found' in dat.read():
                print("Error Found in File {}. Unwanted file removed".format(ime_datoteke))
                dat.close()
                os.remove(path)
                Error_404.append(i)
    return None


def download_anime_and_filter_404(st_strani):
    '''Downloada vse strani od 1 do zeljenega stevila strani in izbrise vse datoteke, ki so "prazne" oz. so datoteke strani, katerih id se nima dolocenega svojega animeja.'''
    download_anime_page_id(st_strani + 1)
    filter_404(st_strani + 1)
    return 

download_anime_and_filter_404(st_strani)

print(f"Error_404 = {Error_404}" )
Animeji = []


vzorec_bloka = re.compile(
        r'<h2>Alternative Titles</h2>'
        r'(.*?)<div class="clearfix mauto mt16" style="width:160px;padding-right:10px">',
        re.DOTALL
)

test_vzorec = re.compile(r'>English:</span>'r'.*?'r'<')

vzorec_anime = re.compile(
        r'.*'
        r'>English:</span>(?P<name>.*?)<.*?' #name
        r'">Episodes:</span>(?P<episodes>.*?)<.*?' #episodes count 
        r'">Aired:</span>(?P<aired>.*?)<.*?' #airing from to 
        r'>Studios:</span>.*title="(?P<studio>.*?)".*?' #studio 
        r'">Source:</span>(?P<source>.*?)<.*?' #source 
        # genre
        r'">Rating:</span>(?P<rating>.*?)<.*?' #rating
        r'">Score:</span>.*>(?P<score>.*?)<.*?' #score
)
seznam_id = range(st_strani)
seznam_OK_id = [element for element in seznam_id if element not in Error_404]

print(f"Seznam OK ID = {seznam_OK_id}")

for noi in seznam_OK_id:
    ime_datoteke = 'Anime-id{}.html'.format(noi)
    path = os.path.join(anime_directory, ime_datoteke) 
    vsebina = orodja.vsebina_datoteke(path)
    for zadetek in re.finditer(test_vzorec, vsebina):
        Animeji.append(zadetek.groupdict())
        

orodja.zapisi_json(Animeji, anime_json)


ime_datoteke_test = 'Anime-id1.html'
path_test = os.path.join(anime_directory, ime_datoteke_test) 
vsebina_test = orodja.vsebina_datoteke(path_test)
test = re.findall(test_vzorec, vsebina)
print(test)

