from datetime import datetime, timedelta
import random
import konzola
import apartmani
import korisnici
import main


def ucitaj():
    rezervacije = []
    with open("rezervacije.txt", 'r', encoding="utf-8") as fajl:
        for linija in fajl:
            linija = linija.strip()
            sifra, sifra_apartman, datum_rezervacije_str, broj_nocenja, cena, gost, status, dodatni_gosti = linija.split("|")
            sifra = int(sifra)
            sifra_apartman = int(sifra_apartman)
            datum_rezervacije = datetime.strptime(datum_rezervacije_str, "%d.%m.%Y")
            broj_nocenja = int(broj_nocenja)
            cena = float(cena)

            rezervacija = {
                "sifra": sifra,
                "sifra_apartman": sifra_apartman,
                "datum_rezervacije": datum_rezervacije,
                "broj_nocenja": broj_nocenja,
                "cena": cena,
                "gost": gost,
                "status": status,
                "dodatni_gosti": dodatni_gosti
            }
            rezervacije.append(rezervacija)
    return rezervacije


def nadji_rezervaciju_sifra(sifra):   #za brisanje
    for rezervacija in rezervacije:
        if rezervacija['sifra_apartman'] == sifra:
            rezervacije.remove(rezervacija)
    return rezervacije    #lista = [rezervacija for rezervacija in rezervacije if rezervacija['sifra_apartman'] != sifra]
            #return lista


def korisnik_ima_rezervaciju(korisnicko_ime):
    for rezervacija in rezervacije:
        if rezervacija["gost"] == korisnicko_ime:
            return True
    return False


def sacuvaj():
    with open("rezervacije.txt", "w", encoding="utf-8") as fajl:
        for r in rezervacije:
            fajl.write(str(r['sifra'])+"|"+str(r['sifra_apartman']) + "|"+r['datum_rezervacije'].strftime('%d.%m.%Y')+"|"+str(r['broj_nocenja'])+"|"
                       +str(r['cena'])+"|"+r['gost']+"|"+r['status']+"|"+r['dodatni_gosti']+"\n")


def rezervacija_apartmana():
    apartmani.prikaz_apartmana_sa_sifrom()
    while True:
        sifra = konzola.unos_ceo_broj("Unesite šifru apartmana: ")
        apartman = apartmani.nadji_po_sifri(sifra)
        if not apartman:
            print("Apartman sa unetom sifrom nije postojeci!")
            continue
        if apartman["status"] != "Aktivan":
            print("Apartman nije aktivan.")
            continue
        danasnji_datum = datetime.now()
        datum_30_dana_posle = danasnji_datum + timedelta(days=30)
        intervali = apartman["dostupnost_po_datumu"]
        intervali_30_dana_pre = []
        for interval in intervali:
            pocetni_datum, krajnji_datum = interval
            if pocetni_datum.date() <= datum_30_dana_posle.date():
                intervali_30_dana_pre.append(interval)
        if not intervali_30_dana_pre:
            print("Nema dostupnih termina za ovaj apartman.")
            continue
        for index, interval in enumerate(intervali_30_dana_pre):
            pocetni_datum, krajnji_datum = interval
            print(str(index+1) + ".", pocetni_datum.strftime("%d.%m.%Y"), "-", krajnji_datum.strftime("%d.%m.%Y"))

        try:
            izbor = konzola.unos_ceo_broj("Unesite redni broj termina: ")
            interval = intervali_30_dana_pre[izbor-1]
            pocetni_datum, krajnji_datum = interval
            broj_nocenja = konzola.unos_ceo_broj("Unesite broj noćenja: ")
            if pocetni_datum + timedelta(days=broj_nocenja) > krajnji_datum:
                print("Prevazilazi krajnji datum.")
                return
        except IndexError:
            print("Upisali ste broj termina koji nije postojeci!")
            break
        fleg = 0
        dodatni_gosti_lista = []
        dodatni_gosti_unos = ""
        while dodatni_gosti_unos not in ["da","ne"]:
            dodatni_gosti_unos = input("Da li zelite uneti dodatne goste?(da/ne)(maksimum za ovaj apartman je " + str(apartman['broj_gostiju']) + "):").lower()
            if dodatni_gosti_unos == "da" and fleg == 0:
                if len(dodatni_gosti_lista) > apartman['broj_gostiju']:
                    print("Ovaj apartman ne moze primiti toliko gostiju!")
                    return
                ime_prezime_gosta = input("Unesite ime i prezime gosta: ")
                dodatni_gosti_lista.append(ime_prezime_gosta)
                fleg = 1
                while True:
                    dodatni_gosti_unos = input("Da li zelite uneti jos dodatnih gostiju?(da/ne)").lower()
                    if dodatni_gosti_unos == "da" and fleg == 1:
                        ime_prezime_gosta = input("Unesite ime i prezime gosta: ")
                        dodatni_gosti_lista.append(ime_prezime_gosta)
                    if dodatni_gosti_unos == "ne":
                        break


        potvrda = ""
        while potvrda not in ['da', 'ne']:
            potvrda = input("Potvrda zakazivanja(da/ne): ").lower()
            if potvrda == "da":
                sifra = random.randint(0, 1000)
                korisnicko_ime = korisnici.logovan_korisnik["korisnicko_ime"]
                cena = broj_nocenja*apartman["cena_po_noci"]*0.95 if korisnik_ima_rezervaciju(korisnicko_ime) else broj_nocenja*apartman["cena_po_noci"]
                rezervacija = {
                    "sifra": sifra,
                    "sifra_apartman": apartman["sifra"],
                    "datum_rezervacije": pocetni_datum,
                    "broj_nocenja": broj_nocenja,
                    "cena": cena,
                    "gost":korisnicko_ime,
                    "status": "Kreirana",
                    "dodatni_gosti": ",".join(dodatni_gosti_lista)
                }
                indeks_pozicija = intervali.index(interval)
                if (pocetni_datum + timedelta(days=broj_nocenja)).date() == krajnji_datum.date():
                    intervali.pop(indeks_pozicija)
                else:
                    intervali[indeks_pozicija] = (pocetni_datum + timedelta(days=broj_nocenja), krajnji_datum)
                rezervacije.append(rezervacija)
                sacuvaj()
                apartmani.sacuvaj()
                print("Uspešno napravljena rezervacija.")
            elif potvrda == "ne":
                print("Prekinuto rezervisanje!")
                return
        nastavak = ""
        while nastavak not in ['da', 'ne']:
            nastavak = input("Da li zelite nastaviti?(da/ne)")
            if nastavak == "ne":
                return
            elif nastavak == "da":
                break
            else:
                print("Pogresan unos!")
                continue
        continue


def brisanje_rezervacija(rezervacije):
    with open("rezervacije.txt", "w", encoding="utf-8") as fajl:
        for r in rezervacije:
            fajl.write(str(r['sifra'])+"|"+str(r['sifra_apartman'])+"|"+r['datum_rezervacije'].strftime('%d.%m.%Y')+"|"+str(r['broj_nocenja'])+"|"
                       +str(r['cena'])+"|"+r['gost']+"|"+r['status']+"|"+r['dodatni_gosti']+"\n")
    return


def top_10_najpopularnijih_gradiva():
    prebrojavanje = {}
    danasnji_datum = datetime.now()
    godinu_dana_pre = danasnji_datum - timedelta(days=365)
    for r in rezervacije:
        if not r:
            print("Nema rezervacija!")
            break
        if r['datum_rezervacije'] >= godinu_dana_pre and (r['status'] == "Potvrdjena" or r['status'] == "Zavrsena"):
            sifra_apartmana = r['sifra_apartman']
            apartman = apartmani.nadji_po_sifri(sifra_apartmana)
            if not apartman:
                print("Nema rezervacija!")
                break
            grad = apartman['grad']
            if grad in prebrojavanje:
                prebrojavanje[grad] += 1
            else:
                prebrojavanje[grad] = 1

    sortirano_prebrojavanje = sorted(list(prebrojavanje.items()), key=lambda gb: gb[1], reverse=True) #sortirana lista torki
    if len(sortirano_prebrojavanje) > 10:
        sortirano_prebrojavanje = sortirano_prebrojavanje[:10]
    if sortirano_prebrojavanje:
        print("|{:10}|{:}".format("Grad","Broj rezervacija"))
        print("------------------------------")
        for grad, brojac in sortirano_prebrojavanje:
            print("|{:10}|{:}".format(grad, brojac))
        print("------------------------------")
        print()
        print("1. Nazad na meni.")
        while True:
            nazad = input(">>>")
            if nazad == "1":
                return
            else:
                continue

    else:
        print("Nema podataka za prikazivanje!")
        return



def nadji_po_sifri(sifra):
    for r in rezervacije:
        if r["sifra"] == sifra:
            return r
    return None

def ponistavanje_rezervacije(korisnicko_ime):
    sifra = konzola.unos_ceo_broj("Unesi šifru rezervacije: ")
    rezervacija = nadji_po_sifri(sifra)

    if not rezervacija:
        print("Nema rezervacija pod tom sifrom!")
        return
    apartman = apartmani.nadji_po_sifri(rezervacija["sifra_apartman"])
    if korisnicko_ime != rezervacija['gost']:
        print("Nije moguce ponistiti tudju rezervaciju!")
        return
    if korisnicko_ime == rezervacija['gost']:
        if rezervacija['status'] == "Odustanak":
            print("Ova rezervacija je vec ponistena!")
            return
        rezervacija["status"] = "Odustanak"
        sacuvaj()
        print("Rezervacija je uspesno ponistena!")
        dostupnosti = apartman["dostupnost_po_datumu"]
        for interval in dostupnosti:
            pocetni_datum, krajnji_datum = interval
            if rezervacija["datum_rezervacije"] < pocetni_datum:
                indeks_pozicija = dostupnosti.index(interval)
                dostupnosti[indeks_pozicija] = (pocetni_datum - timedelta(days=rezervacija["broj_nocenja"]), krajnji_datum)
                break
        apartmani.sacuvaj()
    else:
        print("Vas nalog nema rezervaciju pod ovom sifrom!")
        return


def potvrda_rezervacija(korisnicko_ime):
    if not main.pregled_rezervacija(korisnicko_ime):
        return
    potvrda = konzola.unos_ceo_broj("Unesite sifru rezervacije koju zelite da potvrdite: ")
    rezervacija = nadji_po_sifri(potvrda)
    if not rezervacija:
        print("Nema rezervacija pod tom sifrom!")
        return
    apartman = apartmani.nadji_po_sifri(rezervacija["sifra_apartman"])
    if korisnicko_ime != apartman['domacin']:
        print("Nije moguce ponistiti tudju rezervaciju!")
        return
    if korisnicko_ime == apartman['domacin']:
        if rezervacija['status'] == "Potvrdjena":
            print("Ova rezervacija je vec potvrdjena!")
            return
    if rezervacija['status'] == "Kreirana":
        rezervacija["status"] = "Potvrdjena"
        print("Potvrda rezervacije pod sifrom", ""+"'" + str(rezervacija['sifra']) + "' je uspesno izvrsena!" )
        sacuvaj()


def odbijanje_rezervacije(korisnicko_ime):
    if not main.pregled_rezervacija(korisnicko_ime):
        return
    sifra = konzola.unos_ceo_broj("Upisite sifru rezervacije koju zelite da odbijete: ")
    rezervacija = nadji_po_sifri(sifra)
    if not rezervacija:
        print("Nema rezervacija sa ovom sifrom!")
        return
    apartman = apartmani.nadji_po_sifri(rezervacija['sifra_apartman'])
    if apartman['domacin'] == korisnicko_ime and rezervacija['status'] == "Odbijena":
        print("Ova rezervacija je vec odbijena!")
        return

    if apartman['domacin'] != korisnicko_ime:
        print("Nije moguce odbiti rezervaciju tudjeg apartmana!")
        return

    if apartman['domacin'] == korisnicko_ime and rezervacija['status'] == "Kreirana":
        rezervacija['status'] = "Odbijena"
        print("Rezervacija uspesno odbijena!")
        sacuvaj()

        dostupnost = apartman['dostupnost_po_datumu']
        for interval in dostupnost:
            pocetni_datum, krajnji_datum = interval
            if rezervacija["datum_rezervacije"] < pocetni_datum:
                indeks_pozicija = dostupnost.index(interval)
                dostupnost[indeks_pozicija] = (pocetni_datum - timedelta(days=rezervacija["broj_nocenja"]), krajnji_datum)
                break
        apartmani.sacuvaj()
    else:
        print("Nije moguce odbijiti rezervaciju tudjeg apartmana!")
        return


def pregled_rezervacija(korisnicko_ime):
    pregled_rezervacija = []
    for apartman in apartmani.apartmani:
        for r in rezervacije:
            if r['status'] == "Kreirana" and apartman['domacin'] == korisnicko_ime and apartman['sifra'] == r['sifra_apartman']:
                pregled_rezervacija.append(r)
    return pregled_rezervacija


def print_rezervacija_podaci(p):
    print("|{:30}|{:25}|{:25}|{:15}|{:25}|{:30}|{:15}|{:15}".format(str(p['sifra']),str(p['sifra_apartman']), p['datum_rezervacije'].strftime('%d.%m.%Y')
                                            , str(p['broj_nocenja']), str(p['cena']), p['gost'], p['status'], p['dodatni_gosti']))



def rezervacije_naslov():
    print("|{:30}|{:25}|{:25}|{:15}|{:25}|{:30}|{:15}|{:15}".format("Sifra rezervacije", "Sifra apartmana", "Datum rezervacije", "Broj nocenja", "Cena", "Gost"
                                               , "Status", "Dodatni gosti"))
    print("="*190)


def pregled_rezervacija_ulogovanog_gosta(korisnicko_ime):
    gost_rezervacija = []
    for rezervacija in rezervacije:
        if korisnicko_ime == rezervacija['gost']:
            gost_rezervacija.append(rezervacija)
    return gost_rezervacija



def apartmani_za_dan_realizacije():
    datum = konzola.unos_datum("Unesite datum(dd/mm/yyyy): ")
    filtrirani_apartmani = []
    for r in rezervacije:
        if r['datum_rezervacije'].date() == datum and r['status'] == "Potvrdjena":
            sifra_apartmana = r['sifra_apartman']
            a = apartmani.nadji_po_sifri(sifra_apartmana)
            filtrirani_apartmani.append(a)
    print()
    if filtrirani_apartmani:
        apartmani.apartmani_naslov()
        for a in filtrirani_apartmani:
            apartmani.podaci_apartmani(a)
        print("="*209 + "|")
        print()
    else:
        print("Nema podataka za dati unos!")
        return



def godisnji_pregled_angazovanja_domacina():
    prebrojavanje = {}
    ukupna_zarada = 0

    danasnji_datum = datetime.now()
    godinu_dana_pre = danasnji_datum - timedelta(days=365)

    for r in rezervacije:
        if r['datum_rezervacije'] >= godinu_dana_pre and (r['status'] == "Zavrsena" or r['status'] == "Potvrdjena"):
            a = apartmani.nadji_po_sifri(r['sifra_apartman'])
            gost = a['domacin']
            if gost in prebrojavanje:
                prebrojavanje[gost][0] += 1
                prebrojavanje[gost][1] += r['cena']

            else:
                prebrojavanje[gost] = [1, r['cena']]
            ukupna_zarada += r['cena']
    print()
    print("|{:30}|{:30}|{:15}|".format("Korisnicko ime", "Broj rezervacija", "Zarada"))
    print("-"*100)
    for korisnicko_ime, par in prebrojavanje.items():
        broj_rezervacija, zarada = par
        print("|{:30}|{:30}|{:15}|".format(korisnicko_ime, str(broj_rezervacija), str(zarada)))
    print("-"*100)
    print("Ukupna zarada:", ukupna_zarada)
    print()



def rezervacije_za_dan_i_domacina():
    datum = konzola.unos_datum("Unesite datum(dd/mm/yyyy): ")
    domacin = input("Unesite korisničko ime domacina: ")
    broj_rezervacija = 0
    cena = 0
    for r in rezervacije:
        sifra_apartmana = r['sifra_apartman']
        apartman = apartmani.nadji_po_sifri(sifra_apartmana)
        if r['datum_rezervacije'].date() == datum and apartman['domacin'] == domacin and r['status'] == 'Potvrdjena':
            broj_rezervacija += 1
            cena += r['cena']
    print()
    print("------------------------------------")
    print("Broj rezervacija:", broj_rezervacija)
    print("Cena:", cena)
    print("------------------------------------")
    print()

def zastupljenost_gradova():
    prebrojavanje = {}

    for r in rezervacije:
        sifra_apartmana = r['sifra_apartman']
        apartman = apartmani.nadji_po_sifri(sifra_apartmana)
        grad = apartman['grad']
        if grad in prebrojavanje:
            prebrojavanje[grad] += 1
        else:
            prebrojavanje[grad] = 1

    ukupno = sum(prebrojavanje.values())
    print()
    print("|{:15}|{:30}|{:16}|".format("Grad", "Grad/Broj rezervacija", "Procenat"))
    print("-" * 65)
    for grad, brojac in prebrojavanje.items():
        print("|{:15}|{:30}|{:15}%|".format(grad, str(brojac) + "/" + str(ukupno), round((brojac/ukupno)*100)))
    print("-"*65)
    print()


def potvrdjenih_rez_za_izabranog_domacina():
    domacin = konzola.provera_unosa_kratka_rec("Unesite korisnicko ime domacina: ").lower()
    odgovarajuci_domacini = []
    for r in rezervacije:
        if r['status'] == "Potvrdjena":
            a = apartmani.nadji_po_sifri(r['sifra_apartman'])
            if domacin == a['domacin']:
                odgovarajuci_domacini.append(a)
    print()
    if odgovarajuci_domacini:
        apartmani.apartmani_naslov()
        for domacini in odgovarajuci_domacini:
            apartmani.podaci_apartmani(domacini)
        print("="*209 + "|")
        print()
    else:
        print("Nema podataka za dati unos!")
        return

def mesecni_pregled_angazovanja_domacina():
    pregled_angazovanja = {}
    danas = datetime.now().date()
    pre_30_dana = danas - timedelta(days=30)
    #broj_rezervacija = 0
    #zarada = 0
    for r in rezervacije:
        if (r['status'] == "Potvrdjena" or r['status'] == "Zavrsena") and r['datum_rezervacije'].date() >= pre_30_dana:
            a = apartmani.nadji_po_sifri(r['sifra_apartman'])
            domacin = a['domacin']
            if domacin in pregled_angazovanja:
                pregled_angazovanja[domacin][0] += 1
                pregled_angazovanja[domacin][1] += r['cena']
            else:
                pregled_angazovanja[domacin] = [1, r['cena']]
    print()
    print("|{:30}|{:30}|{:15}|".format("Domacin", "Broj rezervacija", "Zarada"))
    print("-" * 100)
    for domacin, par in pregled_angazovanja.items():
        br_rezervacija, cena = par
        print("|{:30}|{:30}|{:15}|".format(domacin, str(br_rezervacija), str(cena)))
    print("-" * 100)
    print()


def zavrsena_rezervacija_provera():
    danas = datetime.now()
    for r in rezervacije:
        if r['status'] == "Potvrdjena" or r['status'] == "Kreirana":
            if timedelta(r['broj_nocenja']) + r['datum_rezervacije'].date() == danas.date():
                r['status'] = "Zavrsena"
                sacuvaj()




rezervacije = ucitaj()

