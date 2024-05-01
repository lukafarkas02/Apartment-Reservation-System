# import re
import konzola


def ucitaj_korisnike():
    with open("korisnici.txt", 'r', encoding="utf=8") as fajl:
        ucitaj = fajl.readlines()
        for lista in ucitaj:
            lista = lista[:-1]
            podaci = lista.split("|")
            korisnik = {
                'korisnicko_ime': podaci[0],
                'lozinka': podaci[1],
                'ime': podaci[2],
                'prezime': podaci[3],
                'pol': podaci[4],
                'broj_telefona': podaci[5],
                'email_adresa': podaci[6],
                'uloga': podaci[7],
                'status': podaci[8]
            }
            korisnici.append(korisnik)
        return korisnici


def cuvanje_korisnika():
    with open("korisnici.txt", 'w', encoding="utf-8") as fajl:
        for korisnik in korisnici:
            fajl.write(korisnik['korisnicko_ime']+"|"+korisnik['lozinka']+"|"+korisnik['ime']+"|"+korisnik['prezime']+"|"+korisnik['pol']+"|"
                       + korisnik['broj_telefona']+"|"+korisnik['email_adresa']+"|"+korisnik['uloga']+"|"+korisnik['status']+ "\n")
    return


def logovanje():
    while True:
        korisnicko_ime = input("Unesite korisnicko ime: ")
        lozinka = input("Unesite lozinku: ")
        #print(blokirani_korisnici)
        '''
        for blokiran in blokirani_korisnici:
            if korisnicko_ime == blokiran['korisnicko_ime']:
                return blokiran
        '''
        for korisnik in korisnici:
            if korisnicko_ime == korisnik['korisnicko_ime'] and lozinka == korisnik['lozinka']:
                global logovan_korisnik
                logovan_korisnik = korisnik
                return korisnik
        else:
            print("Pogresno korisnicko ime/lozinka!")
            continue


def registracija_meni():
    korisnik = {}
    korisnicko_ime = input("Unesite korisnicko ime: ").lower()
    lozinka = input("Unesite lozinku: ").lower()
    ime = konzola.provera_unosa_kratka_rec("Unesite ime: ").lower().capitalize()
    prezime = konzola.provera_unosa_kratka_rec("Unesite prezime: ").lower().capitalize()
    pol = konzola.provera_unosa_kratka_rec("Unesite pol: ").lower()
    broj_telefona = input("Unesite broj telefona: ")
    email_adresa = input("Unesite email adresu: ").lower()
    korisnik['korisnicko_ime'] = korisnicko_ime
    korisnik['lozinka'] = lozinka
    korisnik['ime'] = ime
    korisnik['prezime'] = prezime
    korisnik['pol'] = pol
    korisnik['broj_telefona'] = broj_telefona
    korisnik['email_adresa'] = email_adresa
    korisnik['uloga'] = "gost"
    korisnik['status'] = "neblokiran"
    provera_validnosti(korisnik)


def provera_validnosti(registrovani_korisnik):
    for korisnik in korisnici:
        if registrovani_korisnik['korisnicko_ime'] == korisnik['korisnicko_ime']:
            print("Korisnicko ime je vec u upotrebi!")
            return False
    if registrovani_korisnik['korisnicko_ime'] == "" or len(registrovani_korisnik['korisnicko_ime']) < 3:
        print("Korisnicko ime mora da sadrzi najmanje 3 karaktera!")
        return False
    if registrovani_korisnik['lozinka'] == "" or len(registrovani_korisnik['lozinka']) < 5:
        print("Lozinka mora sadrzati najmanje 5 karaktera!")
        return False
    if registrovani_korisnik['pol'] != "musko" and registrovani_korisnik['pol'] != "zensko":
        print("Pogresan unos pola(musko/zensko)! ")
        return False
    if "@" not in registrovani_korisnik['email_adresa'] or ".com" not in registrovani_korisnik['email_adresa'] or "gmail" not in registrovani_korisnik['email_adresa'] or not (30 > len(registrovani_korisnik['email_adresa']) > 10):
        print("Email adresa ne podrzva odgovarajuci format!")
        return False
    if not registrovani_korisnik['broj_telefona'].isdigit() or not (8 < len(registrovani_korisnik['broj_telefona']) < 12):
        print("Broj telefona nije u odgovarajucem formatu!")
        return False
    if registrovani_korisnik['uloga'] == "gost":
        print("Registracija je uspesno izvrsena.\nDobrodosli " + registrovani_korisnik['korisnicko_ime'] + "!")
        registracija(registrovani_korisnik)
    if registrovani_korisnik['uloga'] == "domacin":
        print("Registracija novog domacina je uspesno izvrsena.")
        registracija(registrovani_korisnik)


def registracija(korisnik):
    if korisnik:
        with open("korisnici.txt", 'a', encoding="utf-8") as fajl:
            fajl.write(korisnik['korisnicko_ime'] + "|" + korisnik['lozinka'] + "|" + korisnik['ime'] + "|"
                       + korisnik['prezime'] + "|" + korisnik['pol'] + "|" + korisnik['broj_telefona'] + "|" +
                       korisnik['email_adresa'] + "|" + korisnik['uloga'] + "|" + korisnik['status'] + "\n")

        ucitaj_korisnike()
    return


def blokiranje_():
    korisnicko_ime = input("Unesite korisnicko ime korisnika kojeg zelite da blokirate: ")
    for korisnik in korisnici:
        if korisnicko_ime == korisnik['korisnicko_ime'] and korisnik['uloga'] != "administrator" and korisnik['status'] == "neblokiran":
            if korisnik['uloga'] == "gost" or korisnik['uloga'] == "domaćin":
                korisnik['status'] = "blokiran"
                blokirani_korisnici.append(korisnik)
                print("Korsnik je uspesno blokiran!")
                sacuvaj_blok()
                return korisnik
    else:
        print("Nije moguce blokirati unetog korisnika!")
        return


def odblokiranje_korisnika():
    #print(blokirani_korisnici)
    korisnicko_ime = input("Unesite korisnicko ime korisnika kojeg zelite da odblokirate: ")
    for blok in blokirani_korisnici:
        for korisnik in korisnici:
            if korisnicko_ime == blok['korisnicko_ime'] and korisnicko_ime == korisnik['korisnicko_ime'] and korisnik['status'] == "blokiran":
                blokirani_korisnici.remove(blok)
                korisnik['status'] = "neblokiran"
                print("Korisnik je uspesno odblokiran!")
                sacuvaj_blok()
                return korisnik
    else:
        print("Korsnik koji ste uneli nije blokiran!")
        return


def sacuvaj_blok():
    with open("blokirani.txt", 'w', encoding="utf-8") as fajl:
        for blok in blokirani_korisnici:
            fajl.write(blok['korisnicko_ime']+"|"+blok['lozinka']+"|"+blok['ime']+"|"+blok['prezime']+"|"+blok['pol']+"|"
                       + blok['broj_telefona']+"|"+blok['email_adresa']+"|"+blok['uloga']+"|"+blok['status']+"\n")
    cuvanje_korisnika()
    return


def ucitaj_blokirane():
    with open("blokirani.txt", 'r', encoding="utf-8") as fajl:
        ucitaj = fajl.readlines()
        for linija in ucitaj:
            linija = linija[:-1]
            podaci = linija.split("|")
            korisnik = {
                'korisnicko_ime': podaci[0],
                'lozinka': podaci[1],
                'ime': podaci[2],
                'prezime': podaci[3],
                'pol': podaci[4],
                'broj_telefona': podaci[5],
                'email_adresa': podaci[6],
                'uloga': podaci[7],
                'status': podaci[8]
            }
            blokirani_korisnici.append(korisnik)
        return blokirani_korisnici


def registracija_domacina():
    korisnik = {}
    korisnicko_ime = input("Unesite korisnicko ime: ").lower()
    lozinka = input("Unesite lozinku: ").lower()
    ime = konzola.provera_unosa_kratka_rec("Unesite ime: ").lower().capitalize()
    prezime = konzola.provera_unosa_kratka_rec("Unesite prezime: ").lower().capitalize()
    pol = input("Unesite pol: ").lower()
    broj_telefona = input("Unesite broj telefona: ")
    email_adresa = input("Unesite email adresu: ").lower()
    korisnik['korisnicko_ime'] = korisnicko_ime
    korisnik['lozinka'] = lozinka
    korisnik['ime'] = ime
    korisnik['prezime'] = prezime
    korisnik['pol'] = pol
    korisnik['broj_telefona'] = broj_telefona
    korisnik['email_adresa'] = email_adresa
    korisnik['uloga'] = "domacin"
    korisnik['status'] = "neblokiran"
    provera_validnosti(korisnik)



korisnici = []
blokirani_korisnici = []
ucitaj_korisnike()
ucitaj_blokirane()
logovan_korisnik = None
