# Projektna-Naloga-Programiranje-1
Repository za projektno nalogo iz predmeta programiranje 1

Animeji
==================

Analiziral bom celotno zbirko animejev na MyAnimeList (cca 17000 serij, filmov itd.)

[MyAnimeList](https://myanimelist.net/)

Za vsak anime bom zajel:
- naslov 
- Število Episod
- Pričetek in konec prenašanja
- Studio
- Vir (Manga, Original, LN, VN, ...)
- Žanri
- Rating 
- Status
- Ocena


Vprašanja, ki bi jih raziskoval:
- Ali so ocene animejev tipa TV kaj odvisne od števila epizod (ker se recimo gledalec bolj naveže na serijo in mu je zato potem bolj všeč)?
- Kateri studiji največkrat proizvedejo anime z najvišjimi ocenami?
- Ali kakšen izmed žanrov prevladuje pri bolje ocenjenih animejih?
- Ali so ocene odvsine od vira?

Ugotovitev: Na oceno vpliva vglavnem samo izgled in zgodba

opomba: Če ima anime (predvsem serije) več sezon, se vsaka upošteva posebej 

opomba 2: Modra bom tekom projekta dodal kakšno vprašanje, ali pa katero od teh razširil / spremenil.
_____________________________________________________________________________________________

## Podatki

Podatki so shranjeni v dveh datotekah: 
anime.csv - podatki o posameznem aimeju:
- id (dolocen s strani spletne strani)
- naslov (Ang., če ne obstaja, potem Jap. ampak v Romanji obliki (taki, da jo znamo angleško govoreči ljudje prebrati))
- studio
- vir
- rating
- status
- ocena
- leto izzida
- zacetek (in konec) predvajanja

zaporedje: name,id,episodes,aired,studio,source,rating,score,leto,status,season

zanri.csv - zanri, ki pripada dolocenemu animeju z id

Vzorec: 41800 -> skupaj nanese to ves "uporaben" anime database, ki ga premore MAL. (cca 17 000 animejev)

Opomba: html-jev ni shranjenih, saj ji je skupaj 40000 in zasedejo preveč prostora.


## Navodila za uporabo
Zaženite `Shranjevalink.py`. Vodil vas bo skozi konzolo, vzemite si čas, prenašal bo podatke kar nekaj časa. Shranil jih bo v `Anime` mapo.
Ko boste vse podatke prenesli, Zaženite `zajem in obdelava strani.py`. ta bo ustvaril `anime.csv` in `Anime.json`.
Za ponovno analizo, odprite `analiza.ipynb` in reanalizirajte podatke.
