import re
import orodja

vzorec_bloka = re.compile(
        r'<h2>Alternative Titles</h2>'
        r'(.*?)<div class="clearfix mauto mt16" style="width:160px;padding-right:10px">',
        re.DOTALL
)


vzorec_anime = re.compile(
        r'id="myinfo_anime_id" value="(?P<id>.*?)".+?' #id
        r'<h2>Alternative.*</span>(?P<name>.*?)<.*?' #name
        r'">Episodes:</span>(?P<episodes>.*?)<.*?' #episodes count 
        r'">Aired:</span>(?P<aired>.*?)<.*?' #airing from to 
        r'>Studios:</span>.*title="(?P<studio>.*?)".*?' #studio 
        r'">Source:</span>(?P<source>.*?)<.*?' #source 
        r'' #genre
        r'">Rating:</span>(?P<rating>.*?)<.*?' #rating
        r'">Score:</span>.*>(?P<score>.*?)<.*?' #score
)
# 
# vzorec_osebe = re.compile(
#     r'<a\s+href="/name/nm(?P<id>\d+)/?[^>]*?>(?P<ime>.+?)</a>',
#     flags=re.DOTALL
# )
# 
# vzorec_povezave = re.compile(
#     r'<a.*?>(.+?)</a>',
#     flags=re.DOTALL
# )
# 
# vzorec_zasluzka = re.compile(
#     r'Gross:.*?data-value="(?P<zasluzek>(\d|,)+)"',
#     flags=re.DOTALL
# )
# 
# vzorec_metascore = re.compile(
#     r'<span class="metascore.*?">(?P<metascore>\d+)',
#     flags=re.DOTALL
# )
# 
# vzorec_oznake = re.compile(
#     r'<span class="certificate">(?P<oznaka>.+?)</span>',
#     flags=re.DOTALL
# )
# 
# vzorec_daljsi_povzetek = re.compile(
#     r'<a href="/title/tt\d+/plotsummary.*?&nbsp;&raquo;',
#     flags=re.DOTALL
# )
# 
# vzorec_igralcev = re.compile(
#     r'Stars?:(?P<igralci>.+?)</p>.*?',
#     flags=re.DOTALL
# )
# 
# def izloci_osebe(niz):
#     osebe = []
#     for oseba in vzorec_osebe.finditer(niz):
#         osebe.append({
#             'id': int(oseba.groupdict()['id']),
#             'ime': oseba.groupdict()['ime'],
#         })
#     return osebe


def izloci_podatke_animeja(blok):
    anime = vzorec_anime.search(blok).groupdict()
    # anime['id'] = int(anime['id'])
    # anime['episodes'] = int(anime['episodes'])
    # anime['name'] = float(anime['name'])
    # anime['aired'] = float(anime['aired'])
    # anime['studio'] = float(anime['studio'])
    # anime['source'] = float(anime['source'])
    # anime['rating'] = float(anime['rating'])
    print(anime)
    return anime


def anime_na_strani(stran):
    url = (
        'https://myanimelist.net/anime/{}'.format(stran)
    )
    ime_datoteke = 'anime-{}.html'.format(stran)
    orodja.shrani_spletno_stran(url, ime_datoteke)
    vsebina = orodja.vsebina_datoteke(ime_datoteke)
    for blok in vzorec_bloka.finditer(vsebina):
        print(izloci_podatke_animeja(blok.group(0)))
        yield izloci_podatke_animeja(blok.group(0))
        
def anime_na_strani2(st_strani):
    for i in range(st_strani):
        url = ('https://myanimelist.net/anime/{}'.format(i))
        ime_datoteke = 'anime-{}.html'.format(i)
        orodja.shrani_spletno_stran(url, ime_datoteke)
        vsebina = orodja.vsebina_datoteke(ime_datoteke)
        print(vsebina)
    return None

anime_na_strani2(5)

# def izloci_gnezdene_podatke(filmi):
#    REZISER, IGRALEC = 'R', 'I'
#    osebe, vloge, zanri = [], [], []
#    videne_osebe = set()
#
#    def dodaj_vlogo(film, oseba, vloga, mesto):
#        if oseba['id'] not in videne_osebe:
#            videne_osebe.add(oseba['id'])
#            osebe.append(oseba)
#        vloge.append({
#            'film': film['id'],
#            'oseba': oseba['id'],
#            'vloga': vloga,
#            'mesto': mesto,
#        })
#
#
#    for film in filmi:
#        for zanr in film.pop('zanri'):
#            zanri.append({'film': film['id'], 'zanr': zanr})
#        for mesto, oseba in enumerate(film.pop('reziserji'), 1):
#            dodaj_vlogo(film, oseba, REZISER, mesto)
#        for mesto, oseba in enumerate(film.pop('igralci'), 1):
#            dodaj_vlogo(film, oseba, IGRALEC, mesto)
#
#    osebe.sort(key=lambda oseba: oseba['id'])
#    vloge.sort(key=lambda vloga: (vloga['film'], vloga['vloga'], vloga['mesto']))
#    zanri.sort(key=lambda zanr: (zanr['film'], zanr['zanr']))
#
#    return osebe, vloge, zanri
# 
# 
# filmi = []
# for st_strani in range(1, 41):
#     for film in filmi_na_strani(st_strani, 250):
#         filmi.append(film)
# filmi.sort(key=lambda film: film['id'])
# orodja.zapisi_json(filmi, 'obdelani-podatki/filmi.json')
# osebe, vloge, zanri = izloci_gnezdene_podatke(filmi)
# orodja.zapisi_csv(
#     filmi,
#     ['id', 'naslov', 'dolzina', 'leto', 'ocena', 'metascore', 'glasovi', 'zasluzek', 'oznaka', 'opis'], 'obdelani-podatki/filmi.csv'
# )
# orodja.zapisi_csv(osebe, ['id', 'ime'], 'obdelani-podatki/osebe.csv')
# orodja.zapisi_csv(vloge, ['film', 'oseba', 'vloga', 'mesto'], 'obdelani-podatki/vloge.csv')
# orodja.zapisi_csv(zanri, ['film', 'zanr'], 'obdelani-podatki/zanri.csv')
