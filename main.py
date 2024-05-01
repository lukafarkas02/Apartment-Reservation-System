#from datetime import datetime
from korisnici import *
from apartmani import *
import rezervacije
import apartmani


def print_meni():
    print("======= *TRAVEL* ===============")
    print()
    print("1. Prijava na sistem.")
    print("2. Registracija.")
    print()
    print("3. Pregled aktivnih apartmana.")
    print("4. Pretraga apartmana.")
    print("5. Visekriterijumska pretraga apartmana.")
    print("6. Prikaz 10 najpopularnijih gradova.")
    print("7. Izlaz")
    print()
    print("==================================")


def meni():
    while True:
        komanda = opcije_unosa()
        if komanda == "1":
            korisnik = logovanje()
            if korisnik['status'] != "blokiran":
                print("Dobrodosli " + korisnik['korisnicko_ime'] + "!")
                if korisnik['uloga'] == "gost":
                    meni_gost(korisnik['korisnicko_ime'])
                elif korisnik['uloga'] == "domacin":
                    meni_domacin(korisnik['korisnicko_ime'])
                elif korisnik['uloga'] == "administrator":
                    meni_administrator()
            else:
                print("Vas nalog je blokiran!")
        elif komanda == "2":
            registracija_meni()
        elif komanda == "3":
            pretraga_apartmana()
            izbor()
        elif komanda == "4":
            meni_pretraga_apartmana()
        elif komanda == "5":
            visekriterijumska_pretraga()
        elif komanda == "6":
            rezervacije.top_10_najpopularnijih_gradiva()
        elif komanda == "7":
            exit()


def opcije_unosa():
    komanda = ""
    print_meni()
    while komanda not in [str(x) for x in range(1, 8)]:
        komanda = input(">>>")
        return komanda


def opcije_unos_gost():
    komanda = ""
    print_meni_gost()
    while komanda not in [str(x) for x in range(1, 6)]:
        komanda = input(">>>")
        return komanda


def opcije_unos_domacin():
    komanda = ""
    print_meni_domacin()
    while komanda not in [str(x) for x in range(1, 6)]:
        komanda = input(">>>")
        return komanda


def opcije_unos_administrator():
    komanda = ""
    print_meni_administrator()
    while komanda not in [str(x) for x in range(1, 10)]:
        komanda = input(">>>")
        return komanda


def izbor():
    print("1. Povratak na glavni meni.")
    print("2. Izlaz iz aplikacije")
    izbor = ""
    while izbor not in ["1", "2"]:
        izbor = input(">>>")
        if izbor == "1":
            meni()
        elif izbor == "2":
            exit()
        else:
            print("Pogresan unos")


def print_meni_gost():
    print("="*20)
    print("1. Izlazak iz aplikacije.")
    print("2. Odjava sa sistema.")
    print()
    print("3. Rezervisanje apartmana.")
    print("4. Pregled rezervacija.")
    print("5. Ponistavanje rezervacije.")
    print("="*20)


def meni_gost(korisnik):
    korisnicko_ime = korisnik
    while True:
        komanda = opcije_unos_gost()
        if komanda == "1":
            exit()
        elif komanda == "2":
            odjava_sa_sistema()
        elif komanda == "3":
            rezervacije.rezervacija_apartmana()
        elif komanda == "4":
            ucitaj_pregled_rezervacije(korisnicko_ime)
            izbor2(korisnicko_ime)
        elif komanda == "5":
            ucitaj_pregled_rezervacije(korisnicko_ime)
            rezervacije.ponistavanje_rezervacije(korisnicko_ime)

def ucitaj_pregled_rezervacije(gost):
    korisnicko_ime = gost
    ulogovan_gost = rezervacije.pregled_rezervacija_ulogovanog_gosta(korisnicko_ime)
    if ulogovan_gost:
        rezervacije.rezervacije_naslov()
        for rezervacija in ulogovan_gost:
            rezervacije.print_rezervacija_podaci(rezervacija)
        print("=" * 190)
    else:
        print("Nema podataka o rezervacijama za ovaj nalog!")


def izbor2(korisnicko_ime):
    gost = korisnicko_ime
    while True:
        print("1. Nazad.")
        opcija = input(">>>")
        if opcija == "1":
            meni_gost(gost)


def odjava_sa_sistema():
    return meni()


def meni_pretraga_apartmana():
    while True:
        komanda = izbor_opcija_pretrage_apartmana()
        if komanda == "1":
            pretraga_apartmana_po_mestu()
        elif komanda == "2":
            datum_pretraga()
        elif komanda == "3":
            pretraga_po_broju_soba()
        elif komanda == "4":
            pretraga_po_broju_osoba()
        elif komanda == "5":
            pretraga_po_ceni()
        elif komanda == "6":
            izbor()


def print_meni_pretraga_apartmana():
    print("="*20)
    print("1. Pretraga po mestu(prefiksno ili deo): ")
    print("2. Pretraga po vremenu dostupnosti: ")
    print("3. Pretraga po broju soba: ")
    print("4. Pretraga po broju osoba: ")
    print("5. Pretraga po ceni: ")
    print("6. Izlaz")
    print("="*20)


def izbor_opcija_pretrage_apartmana():
    komanda = ""
    print_meni_pretraga_apartmana()
    while komanda not in [str(x) for x in range(1, 7)]:
        komanda = input(">>>")
        return komanda


def pretraga_apartmana_po_mestu():
    mesto = input("Unesite mesto (deo/prefiks): ").capitalize()
    lista = pretraga_po_mestu(mesto)
    if lista:
        apartmani_naslov()
        for apartman in lista:
            podaci_apartmani(apartman)
        print("=" * 209 + "|")
    else:
        print("Nema podataka za dati unos! ")


def pretraga_po_broju_soba():
    while True:
        try:
            minimalno = input("Unesite broj soba(minimalni): ")
            maximalno = input("Unesitr broj soba(maksimalni): ")
            lista = pretraga_po_broju_soba_(minimalno, maximalno)
            if lista:
                apartmani_naslov()
                for apartman in lista:
                    podaci_apartmani(apartman)
                print("="*209 + "|")
                break
            else:
                print("Nema podataka za dati unos!")
                break
        except ValueError:
            print("Niste uneli broj!")
            continue


def pretraga_po_broju_osoba():
    while True:
        try:
            minimalno = input("Unesite broj osoba(minimalni): ")
            maximalno = input("Unesitr broj osoba(maksimalni): ")
            lista = pretraga_po_broju_osoba_(minimalno, maximalno)
            if lista:
                apartmani_naslov()
                for apartman in lista:
                    podaci_apartmani(apartman)
                print("=" * 209 + "|")
                break
            else:
                print("Nema podataka za dati unos!")
                break
        except ValueError:
            print("Niste uneli broj!")
            continue


def pretraga_po_ceni():
    while True:
        try:
            minimalno = input("Unesite cenu(minimalna): ")
            maximalno = input("Unesitr cenu(maksimalna): ")
            lista = pretraga_po_ceni_(minimalno, maximalno)
            if lista:
                apartmani_naslov()
                for apartman in lista:
                    podaci_apartmani(apartman)
                print("=" * 209 + "|")
                break
            else:
                print("Nema podataka za dati unos!")
                break
        except ValueError:
            print("Niste uneli broj!")
            continue


def datum_pretraga():
    while True:
        datum1_str = input("Unesite pocetni datum formata(%d.%m.%Y):")
        datum2_str = input("Unesite krajni datum formata(%d.%m.%Y):")
        try:
            datum1 = datetime.strptime(datum1_str, "%d.%m.%Y")
            datum2 = datetime.strptime(datum2_str, "%d.%m.%Y")
            lista = pretraga_po_datumu(datum1, datum2)
            if lista:
                apartmani_naslov()
                for apartman in lista:
                    podaci_apartmani(apartman)
                print("="*209 + "|")
                break
            else:
                print("Nema podataka za dati unos!")
                break
        except ValueError:
            print("Los format vremena!")
            continue

def visekriterijumska_pretraga():
    mesto = input("Unesite mesto (deo/prefiks): ").capitalize()
    min_br_soba = konzola.unos_ceo_broj("Unesite broj soba (minimalni): ")
    max_br_soba = konzola.unos_ceo_broj("Unesite broj soba (maksimalni): ")
    br_osoba_min = konzola.unos_ceo_broj("Unesite broj osoba (minimalni): ")
    br_osoba_max = konzola.unos_ceo_broj("Unesite broj osoba (maksimalni): ")
    cena_min = konzola.unos_ceo_broj("Unesite cenu (minimalnu): ")
    cena_max = konzola.unos_ceo_broj("Unesite cenu (maksimalnu): ")
    while True:
        datum1_str = input("Unesite pocetni datum formata(%d.%m.%Y):")
        datum2_str = input("Unesite krajni datum formata(%d.%m.%Y):")
        try:
            datum1 = datetime.strptime(datum1_str, "%d.%m.%Y")
            datum2 = datetime.strptime(datum2_str, "%d.%m.%Y")
            rezultat_pretrage = pretraga_visekriterijumska(mesto, min_br_soba, max_br_soba, br_osoba_min, br_osoba_max,
                                                           cena_min, cena_max, datum1, datum2)

            if rezultat_pretrage == "":
                print("Uneti podaci nisu postojeci!")
                return
            else:
                print()
                apartmani_naslov()
                print(rezultat_pretrage.strip())
                print("=" * 209 + "|")
                izbor()
                #print(pretraga_visekriterijumska(mesto, min_br_soba, max_br_soba, br_osoba_min, br_osoba_max, cena_min,
                                                 #cena_max, datum1, datum2))
        except ValueError:
            print("Los format vremena!")
            continue
    return


def print_meni_domacin():
    print("="*20)
    print("1. Izlazak iz aplikacije. ")
    print("2. Odjava sa sistema.")
    print()
    print("3. Dodavanje apartmana.")
    print("4. Izmena podataka o apartmanu.")
    print("5. Brisanje apartmana.")
    print("6. Pregled nepotvrdjenih(kreiranih) rezervacija.")
    print("7. Potvrda ili odbijanje rezervacije.")
    print("="*20)


def meni_domacin(korisnicko_ime):
    domacin_korisnicko_ime = korisnicko_ime
    while True:
        komanda = opcije_unos_domacin()
        if komanda == "1":
            exit()
        elif komanda == "2":
            odjava_sa_sistema()
        elif komanda == "3":
            dodavanje_apartmana(domacin_korisnicko_ime)
        elif komanda == "4":
            apartmani.prikaz_apartmana_sa_sifrom()
            izmena_apartmana(domacin_korisnicko_ime)
        elif komanda == "5":
            apartmani.prikaz_apartmana_sa_sifrom()
            brisanje_apartmana(domacin_korisnicko_ime)
        elif komanda == "6":
            pregled_rezervacija(domacin_korisnicko_ime)  #prosledim korisnicko ime domacina npr bosko07
        elif komanda == "7":
            potvrda_ili_odbijanje_meni(domacin_korisnicko_ime)


def print_potvrda_ili_odbijanje_meni():
    print("1. Potvrda rezervacija. ")
    print("2. Ponistavanje rezervacija. ")
    print("3. Nazad. ")
    print("=============================")


def potvrda_ili_odbijanje_meni(domacin):
    korisnicko_ime_domacin = domacin
    while True:
        print_potvrda_ili_odbijanje_meni()
        komanda = input(">>>")
        if komanda == "1":
            rezervacije.potvrda_rezervacija(korisnicko_ime_domacin)
        elif komanda == "2":
            rezervacije.odbijanje_rezervacije(korisnicko_ime_domacin)
        elif komanda == "3":
            meni_domacin(korisnicko_ime_domacin)


def pregled_rezervacija(domacin_korisnicko_ime):
    pregled = rezervacije.pregled_rezervacija(domacin_korisnicko_ime)  #prosledim korisnicko ime domacina
    if pregled:
        rezervacije.rezervacije_naslov()
        for rezervacija in pregled:
            rezervacije.print_rezervacija_podaci(rezervacija)
        print("=" * 190)
        return True
    else:
        print("Nema podataka o rezervacijama za vase apartmane!")
        return False



def print_meni_administrator():
    print("="*20)
    print("1. Izlazak iz aplikacije.")
    print("2. Odjava sa sistema.")
    print()
    print("3. Pretraga rezervacija.")
    print("4. Registracija novih domacina.")
    print("5. Kreiranje dodatne opreme.")
    print("6. Brisanje dodatne opreme.")
    print("7. Blokiranje korisnika.")
    print("8. Odblokiranje korisnika.")
    print("9. Izvestavanje.")
    print("="*20)


def meni_administrator():
    while True:
        komanda = opcije_unos_administrator()
        if komanda == "1":
            exit()
        elif komanda == "2":
            odjava_sa_sistema()
        elif komanda == "3":
            meni_pretraga_adminstratora()
        elif komanda == "4":
            registracija_domacina()
        elif komanda == "5":
            kreiranje_dodatne_opereme()
            izbor_za_administratora_pisanje()
        elif komanda == "6":
            brisanje_dodatne_opreme()
            izbor_za_administratora_brisanje()
        elif komanda == "7":
            blokiran = blokiranje_()
        elif komanda == "8":
            odblokiranje_korisnika()
        elif komanda == "9":
            meni_izvestavanje()


def print_pretraga_administrator():
    print("1. Pretraga potvrdjenih rezervacija: ")
    print("2. Pretraga nepotvrdjenih rezervacija: ")
    print("3. Pretraga rezervacija po adresi apartmana: ")
    print("4. Pretraga rezervacija po korisnickom imenu domacina: ")
    print("5. Izlaz iz pretraga")
    print("-----------------------------------------------------------")


def meni_pretraga_adminstratora():
    while True:
        print_pretraga_administrator()
        komanda = input(">>>")
        if komanda == "1":
            ucitaj_pretragu_potvrdjena_rezervacija()
        elif komanda == "2":
            ucitaj_pretragu_odbijena_rezervacija()
        elif komanda == "3":
            pretraga_rezervacije_adresa()
        elif komanda == "4":
            pretraga_rezervacije_po_domacinu()
        elif komanda == "5":
            meni_administrator()
        else:
            print("Pogresan unos!")


def pretraga_potvrdjena_rezervacija():
    lista = []
    for potvrdjen in rezervacije.rezervacije:
        if potvrdjen['status'] == "Potvrdjena":
            lista.append(potvrdjen)
    return lista


def ucitaj_pretragu_potvrdjena_rezervacija():
    lista = pretraga_potvrdjena_rezervacija()
    if lista:
        rezervacije.rezervacije_naslov()
        for potvrdjen in lista:
            rezervacije.print_rezervacija_podaci(potvrdjen)
        print("="*190)
    else:
        print("Trenutno nema potvrdjenih rezervacija!")
        return


def pretraga_odbijena_rezervacija():
    lista = []
    for rezervacija in rezervacije.rezervacije:
        if rezervacija['status'] == "Odbijena":
            lista.append(rezervacija)
    return lista


def ucitaj_pretragu_odbijena_rezervacija():
    lista = pretraga_odbijena_rezervacija()
    if lista:
        rezervacije.rezervacije_naslov()
        for odbijena in lista:
            rezervacije.print_rezervacija_podaci(odbijena)
        print("=" * 190)
    else:
        print("Trenutno nema odbijenih rezervacija!")
        return


def pretraga_po_rezervacije_adresi_apartmana(pretraga):
    lista = []
    for rezervacija in rezervacije.rezervacije:
        for apartman in apartmani.apartmani:
            if rezervacija['sifra_apartman'] == apartman['sifra'] and pretraga == apartman['adresa']:
                lista.append(rezervacija)
    return lista


def pretraga_rezervacije_adresa():
    pretraga = input("Unesite adresu apartmana: ")
    lista = pretraga_po_rezervacije_adresi_apartmana(pretraga)
    if lista:
        rezervacije.rezervacije_naslov()
        for adresa in lista:
            rezervacije.print_rezervacija_podaci(adresa)
        print("="*190)
    else:
        print("Nema rezervacija za unetu adresu apartmana.")
        return


def pretraga_rezervacija_po_domacinu_apartmana(pretraga):
    lista = []
    for rezervacija in rezervacije.rezervacije:
        for apartman in apartmani.apartmani:
            if rezervacija['sifra_apartman'] == apartman['sifra'] and pretraga == apartman['domacin']:
                lista.append(rezervacija)
    return lista


def pretraga_rezervacije_po_domacinu():
    pretraga = input("Unesite korisnicko ime domacina: ")
    lista = pretraga_rezervacija_po_domacinu_apartmana(pretraga)
    if lista:
        rezervacije.rezervacije_naslov()
        for domacin in lista:
            rezervacije.print_rezervacija_podaci(domacin)
        print("="*190)
    else:
        print("Nema rezervacija pod unetim domacinom!")
        return


def izbor_za_administratora_brisanje():
    while True:
        print("1. Meni administratora.")
        print("2. Nastavite sa brisanjem.")
        print("3. Izlaz iz aplikacije.")
        print("=========================")
        izbor = input("Izaberite opciju:")
        if izbor == "1":
            meni_administrator()
        elif izbor == "2":
            brisanje_dodatne_opreme()
        elif izbor == "3":
            exit()

def izbor_za_administratora_pisanje():
    while True:
        print("1. Meni administratora.")
        print("2. Nastavite sa dodavanjem.")
        print("3. Izlaz iz aplikacije.")
        print("=========================")
        izbor = input("Izaberite opciju:")
        if izbor == "1":
            meni_administrator()
        elif izbor == "2":
            kreiranje_dodatne_opereme()
        elif izbor == "3":
            exit()


def print_meni_izvestavanje():
    print("1. Lista potvrdjenih rezervisanih apartmana za izabran dan realizacije.")
    print("2. Lista potvrdjenih apartmana za izabranog domacina.")
    print("3. Godisnji pregled angazovanja domacina.")
    print("4. Mesecni pregled anagazovanja po domacinu.")
    print("5. Ukupan broj i cena potvrdjenih rezervacija za izabrani dan i izabranog domacina.")
    print("6. Pregled zastupljenosti pojedinacnih gradova u odnosu na ukupan broj rezervacija.")
    print("7. Povratak na meni administratora.")
    print("="*70)


def meni_izvestavanje():
    while True:
        print_meni_izvestavanje()
        komanda = input("Izaberite neku od opcija: ")
        if komanda == "1":
            rezervacije.apartmani_za_dan_realizacije()
        elif komanda == "2":
            rezervacije.potvrdjenih_rez_za_izabranog_domacina()
        elif komanda == "3":
            rezervacije.godisnji_pregled_angazovanja_domacina()
        elif komanda == "4":
            rezervacije.mesecni_pregled_angazovanja_domacina()
        elif komanda == "5":
            rezervacije.rezervacije_za_dan_i_domacina()
        elif komanda == "6":
            rezervacije.zastupljenost_gradova()
        elif komanda == "7":
            meni_administrator()
        else:
            print("Unos nije validan!")


if __name__ == '__main__':
    rezervacije.zavrsena_rezervacija_provera()
    apartmani.provera_dostupnosti()
    meni()
