Izbirna laboratorijska Vaja 7B (20 točk)

Zahteve zaključka

Implementacija kodiranja in dekodiranja slik po postopku QOI
Quite OK Image Format (QOIF) je postopek za brezizgubno kodiranje slik, temelječ na različnih postopkih kodiranja, 
ki izrabljajo odvečnost in ponavljajoče vzorce v tipičnih zaporedjih pikslov. QOI format zapisa je bil zasnovan z namenom 
preprostosti implementacije in ima specifikacijo, dolgo eno (1) stran. Velikosti kompresiranih datotek naj bi bile v povprečju 
nekoliko večje od zapisa .png, postopek kodiranja in dekodiranja pa bistveno manj računsko zahteven.

Naloga 1: implementacija kodiranja QOI datotek
Spišite program, ki vhodno sliko v poljubnem zapisu (kot npr.: BMP, PNG, JPG) prekodira v zapis QOI. Za branje slik v drugih 
zapisih lahko uporabite obstoječe knjižnjice, kot npr. libpng, libjpeg, openCV. Za preverjanje pravilnosti kodirane datoteke 
lahko uporabite referenčni QOI-PNG pretvornik, ki mora biti sposoben prebrati vaše datoteke.

Pri implementaciji kodiranja lahko postopoma dodajate feature-je QOI formata: za začetek lahko npr. celotno sliko
kodirate z 24-bitnimi RGB chunk-i, nato pa postopoma implementirate ostale operacije, ki jih zapis podpira, ter 
glede na vsebino vhodne slike med njimi izbirate. Kot končni rezultat naloge mora vaš kodirnik producirati datoteke, 
ki jih referenčni dekodirnik sprejme in pravilno dekodira, velikost kodiranih datotek pa mora biti primerljiva tistim, 
ki jih generira referenčni kodirnik.

Naloga 2: implementacija dekodiranja QOI datotek
Spišite program, ki vhodno sliko v QOI zapisu dekodira, grafično prikaže, in po možnosti shrani v drugačnem 
zapisu (kot npr.: BMP, PNG, JPG). Za sharanjevanje slik v drugih zapisih lahko uporabite obstoječe knjižnjice, 
kot npr. libpng, libjpeg, openCV. Preverite, da vaš program za dekodiranje pravilno odpre obstoječe slike v 
zapisu QOI ter jih shrani v druge formate z ekvivalentno vsebino.

Naloga 3: ovrednotenje učinkovitosti zapisa QOI datotek
Z vašim kodirnikom in dekodirnikom obdelajte zbirko slik Kodak Dataset. Preverite, da program vse slike 
pravilno kodira in dekodira brez napak: izmerite srednjo kvadratno napako med RGB vrednostmi pikslov PNG in 
QOI verzije vsake izmed slik, ki mora biti za vse enaka 0. Primerjajte povprečne velikosti datotek med zapisi BMP, PNG in QOI. 
Primerjajte povprečni čas kodiranja in dekodiranja med vašo implementacijo in referenčnim QOI programom.

QOK: https://qoiformat.org/
Kodak: https://www.kaggle.com/datasets/sherylmehta/kodak-dataset?resource=download