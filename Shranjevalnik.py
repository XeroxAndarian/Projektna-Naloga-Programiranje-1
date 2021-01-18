import csv
import json
import os
import requests
import sys
import re
import orodja
import time
import random
import datetime
import math



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
prejsni_konec_nah = 750 # "useless"
st_strani_nah = 200 # "useless"


# ------------------------------------------------------------------------------------------------------------------------------

A =    27800      # prejsni_konec
B =    100           # stevilo strani na interval
C =    43000          # skupno stevilo zeljenih strani

Error_404 = []

def clock_work(prejsni_konec, stevilo_strani, cycle_count):
    '''Zazene celotno operacijo downloadanja, pri tem opisuje napredek in med prenasanjem pazi na pavze, da se izmuzne varnostnemu sistemu spletne strani, ki zeli preverjati ali je uporabnik clovek. '''
    print("Starting in 90s. Settings: Start at ID: {}, number of cycles: {}, downloads per cycle: {}".format(prejsni_konec, cycle_count, stevilo_strani))
    print("Estimated time untill the end of all cycles .... approx. {}s  at {}".format(cycle_count * 360 + 60 + cycle_count * B * 0.65, datetime.datetime.now() + datetime.timedelta(seconds = cycle_count * 360 + 60 + cycle_count * B * 0.65))) 
    time.sleep(60)
    print("Starting cylcle 1/{} in 30s. Starting at ID: {}, downloading {} per cycle.".format(cycle_count, prejsni_konec, stevilo_strani))
    time.sleep(20)
    print(f"Starting cylcle 1/{cycle_count} in 10s.")
    time.sleep(5)
    print("First cycle begins in 5s...")
    time.sleep(1)
    print("4...")
    time.sleep(1)
    print("3...")
    time.sleep(1)
    print("2...")
    time.sleep(1)
    print("1...")
    time.sleep(1)
    print("First cycle begins! Estimated finish time: {}".format(datetime.datetime.now() + datetime.timedelta(seconds = cycle_count * B * 0.65)))
    novi_konec = prejsni_konec
    for i in range(cycle_count + 1):
        interval = random.randint(300, 360)
        download_anime_and_filter_404(stevilo_strani, novi_konec)
        novi_konec += stevilo_strani
        i += 1
        if i < cycle_count:
            print("Finished cycle [{}/{}] at {}....    Taking a break for {}s...".format(i, cycle_count , datetime.datetime.now(), interval))
            print("Time untill the end of all cycles .... approx. {}s    at  {} ".format((cycle_count - i) * interval + (cycle_count - i) * B * 0.65, datetime.datetime.now() + datetime.timedelta(seconds = (cycle_count - i) * 360  + (cycle_count - i) * B * 0.65)))
            time.sleep(interval - 60)
            print("Next cycle begins in 60s...")
            time.sleep(30)
            print("Next cycle begins in 30s...")
            time.sleep(20)
            print("Next cycle begins in 10s...")
            time.sleep(5)
            print("Next cycle begins in 5s...")
            time.sleep(1)
            print("4...")
            time.sleep(1)
            print("3...")
            time.sleep(1)
            print("2...")
            time.sleep(1)
            print("1...")
            time.sleep(1)
            print("Next cycle begins! Estimated finish time: {}".format(datetime.datetime.now() + datetime.timedelta(seconds = cycle_count * B * 0.65)))
        else:
            print("All cycles completed at {}! {} files downloaded! Last ID: {}  ^_^ ".format(datetime.datetime.now() , stevilo_strani * cycle_count, novi_konec))
    return novi_konec



def download_anime_page_id(st_strani, zacetek):
    '''Shrani anime, ki je v bazi spletne strani pod id'''
    for i in range(st_strani):
        url = ('https://myanimelist.net/anime/{}'.format(zacetek + i))
        ime_datoteke = 'Anime-id{}.html'.format(zacetek + i)
        path = os.path.join(anime_directory, ime_datoteke)
        orodja.shrani_spletno_stran(url, path)
        #vsebina = orodja.vsebina_datoteke(ime_datoteke)
        #print(vsebina)
    return None




def filter_404(st_strani, zacetek):
    '''Nekatere id-ji so "prazni" in v tem primeru nm spletna stran vrne napako 404. Ker ne želimo imeti te datoteke shranjene, bomo vse tipe takih datotek odstranili.'''
    
    for i in range(st_strani):
        ime_datoteke = 'Anime-id{}.html'.format(zacetek + i)
        path = os.path.join(anime_directory, ime_datoteke)
        with open(path, encoding='utf-8') as dat:
            if '404 Not Found' in dat.read():
                print("Error 404 Found in File {}. ---------->  File removed.".format(ime_datoteke))
                dat.close()
                os.remove(path)
                Error_404.append(i)
    return None


def download_anime_and_filter_404(st_strani, zacetek):
    '''Downloada vse strani od 1 do zeljenega stevila strani in izbrise vse datoteke, ki so "prazne" oz. so datoteke strani, katerih id se nima dolocenega svojega animeja.'''
    download_anime_page_id(st_strani + 1, zacetek)
    filter_404(st_strani + 1, zacetek)
    return 

D = math.ceil(float((C - A) / B))


# clock_work(A, B, D)


