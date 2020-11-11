# Projektna-Naloga-Programiranje-1
Repository za projektno nalogog iz predmeta programiranje 1

Animeji
==================

Analiziral bom celotno zbirko animejev na MyAnimeList (cca 12000 serij, filmov itd.)

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

opomba: Če ima anime (predvsem serije) več sezon, se vsaka upošteva posebej 

opomba 2: Modra bom tekom projekta dodal kakšno vprašanje, ali pa katero od teh razširil / spremenil.
_____________________________________________________________________________________________

##Podatki

Podatki so shranjeni v dveh datotekah: 
anime.csv - podatki o posameznem aimeju:
- id (dolocen s strani spletne strani)
- naslov (Ang, ce ne obstaja, potem Jap ampak v Romanji obliki (taki, da jo znamo anglesko govoreci ljudje prebrati))
- studio
- vir
- rating
- status
- ocena
- leto izzida
- zacetek (in konec) predvajanja

zanri.csv - zanri, ki pripada dolocenemu animeju z id

Edit: Verjetno bom še povečal vzorec (max id 15000 ---> 40800)

Opomba: shranjenih je le prvih nekaj html datotek, saj jih je vse skupaj okrog 6000 (za časa 11.11.2020; predvideno jih bo še več, samo da jih "nakopljem")

