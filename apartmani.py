from datetime import datetime
import konzola
#import main
import rezervacije


def recnik_apartmani():
    with open("apartmani.txt", 'r', encoding="utf-8") as fajl:
        ucitaj = fajl.readlines()
        for linija in ucitaj:
            lista = linija.replace('\n', "").split("|")
            dostupnosti_po_datumu = []
            dostupnosti_po_datumu_str = lista[7]
            if dostupnosti_po_datumu_str:
                intervali_str = dostupnosti_po_datumu_str.split('"')
                for interval_str in intervali_str:
                    datum1_str, datum2_str = interval_str.split(",")
                    datum1 = datetime.strptime(datum1_str, "%d.%m.%Y")
                    datum2 = datetime.strptime(datum2_str, "%d.%m.%Y")
                    dostupnosti_po_datumu.append((datum1, datum2))
            oprema = []
            oprema_str = lista[10]
            oprema.append(oprema_str)
            apartmani_recnik = {
                'sifra': int(lista[0]),
                'tip': lista[1],
                'broj_soba': int(lista[2]),
                'broj_gostiju': int(lista[3]),
                'adresa': lista[4],
                'grad': lista[5],
                'postanski_broj': lista[6],
                'dostupnost_po_datumu': dostupnosti_po_datumu,
                'domacin': lista[8],
                'cena_po_noci': float(lista[9]),
                'dodatna_oprema': oprema,
                'status': lista[11]
            }
            apartmani.append(apartmani_recnik)
        return apartmani


def sacuvaj():
    with open("apartmani.txt", "w",  encoding="utf-8") as fajl:
        for a in apartmani:
            dostupnost_po_datumu = a["dostupnost_po_datumu"]
            intervali_str = []
            for datum1, datum2 in dostupnost_po_datumu:
                datum1_str = datum1.strftime("%d.%m.%Y")
                datum2_str = datum2.strftime("%d.%m.%Y")
                intervali_str.append(datum1_str+","+datum2_str)
            dostupnost_po_datumu_str = '"'.join(intervali_str)
            oprema = a['dodatna_oprema']
            oprema_lista = []
            for o in oprema:
                oprema_lista.append(o)
            oprema_str = ", ".join(oprema_lista)
            fajl.write(str(a['sifra'])+"|"+a['tip']+"|"+str(a['broj_soba'])+"|"+str(a['broj_gostiju'])+"|"+a['adresa']+"|"+a['grad']+"|"
                       +str(a['postanski_broj'])+"|"+dostupnost_po_datumu_str+"|"+a['domacin']+"|"+str(a['cena_po_noci'])
                       +"|"+oprema_str+"|"+a['status']+"\n")


def nadji_po_sifri(sifra):
    for apartman in apartmani:
        if apartman['sifra'] == sifra:
            return apartman
    return None


def nadji_opremu_po_sifri(oprema_sifra):
    for oprema in dodatna_oprema:
        if oprema['sifra'] == oprema_sifra:
            return oprema
    return None


def ucitavanje_dodatne_opreme():
    with open("sadrzajapartmana.txt", 'r', encoding="utf-8") as fajl:
        ucitaj = fajl.readlines()
        for linija in ucitaj:
            lista = linija.replace('\n', "").split("|")
            recnik_oprema = {
                'sifra': int(lista[0]),
                'sadrzaj': lista[1]
            }
            dodatna_oprema.append(recnik_oprema)
        return dodatna_oprema


def print_meni_dodatna_oprema():
    for oprema in dodatna_oprema:
        print("|{:15}|{:20}".format(str(oprema['sifra']),
                                    oprema['sadrzaj']))
    print("="*40)


def oprema_naslov():
    print("|{:15}|{:20}".format("Sifra", "Sadrzaj"))
    print("="*40)


def pretraga_apartmana():
    apartmani_naslov()
    for apartman in apartmani:
        if apartman['status'] == "Aktivan":
            podaci_apartmani(apartman)
    print("=" * 209 + "|")


def podaci_apartmani(apartman):
    dostupnost_po_datumu = apartman["dostupnost_po_datumu"]
    intervali_str = []
    for datum1, datum2 in dostupnost_po_datumu:
        datum1_str = datum1.strftime("%d.%m.%Y")
        datum2_str = datum2.strftime("%d.%m.%Y")
        intervali_str.append(datum1_str + "," + datum2_str)
    dostupnost_po_datumu_str = '"'.join(intervali_str)
    oprema = apartman['dodatna_oprema']
    oprema_lista = []
    for o in oprema:
        oprema_lista.append(o)
    oprema_str = ", ".join(oprema_lista)
    print("|{:15}|{:15}|{:15}|{:23}|{:15}|{:16}|{:60}|{:42}{:}".format(
                                                                                apartman['tip'],
                                                                                str(apartman['broj_soba']),
                                                                                str(apartman['broj_gostiju']),
                                                                                apartman['adresa'],
                                                                                apartman['grad'],
                                                                                str(apartman['cena_po_noci']),
                                                                                dostupnost_po_datumu_str,
                                                                                oprema_str,
                                                                                "|"
                                                                                ))


def apartmani_naslov():

    print("|{:15}|{:15}|{:15}|{:23}|{:15}|{:16}|{:60}|{:42}{:}".format("Tip", "Broj soba", "Broj gostiju", "Adresa",
                                                                       "Grad", "Cena po noci",
                                                                       "Dostupnost po vremenu", "Dodatni sadrzaj", "|"))
    print("=" * 209 + "|")


def pretraga_po_mestu(mesto):
    lista = []
    for apartman in apartmani:
        if mesto in apartman['grad']:
            if apartman['status'] == "Aktivan":
                lista.append(apartman)
    return lista


def pretraga_po_broju_soba_(min, max):
    lista = []
    for apartman in apartmani:
        if (min == '' or int(apartman['broj_soba']) >= int(min)) and (max == '' or int(apartman['broj_soba']) <= int(max)):
            if apartman['status'] == "Aktivan":
                lista.append(apartman)
    return lista


def pretraga_po_broju_osoba_(min, max):
    lista = []
    for apartman in apartmani:
        if (min == '' or int(apartman['broj_gostiju']) >= int(min)) and (max == '' or int(apartman['broj_gostiju']) <= int(max)):
            if apartman['status'] == "Aktivan":
                lista.append(apartman)
    return lista


def pretraga_po_ceni_(min, max):
    lista = []
    for apartman in apartmani:
        if (min == '' or int(apartman['cena_po_noci']) >= int(min)) and (max == '' or int(apartman['cena_po_noci']) <= int(max)):
            if apartman['status'] == "Aktivan":
                lista.append(apartman)
    return lista


def pretraga_po_datumu(datum1, datum2):
    lista = []

    for apartman in apartmani:
        dostupnosti = apartman['dostupnost_po_datumu']
        for interval in dostupnosti:
            pocetni_datum, krajnji_datum = interval
            if (datum1 == "" or datum1 <= pocetni_datum) and (datum2 == "" or pocetni_datum <= krajnji_datum <= datum2):
                if apartman['status'] == "Aktivan":
                    lista.append(apartman)
                    break
    return lista


def pretraga_visekriterijumska(mesto, min_br_soba, max_br_soba, br_osoba_min, br_osoba_max, cena_min, cena_max,
                               datum1, datum2):
    rezultat1 = pretraga_po_mestu(mesto)
    rezultat2 = pretraga_po_broju_soba_(min_br_soba, max_br_soba)
    rezultat3 = pretraga_po_broju_osoba_(br_osoba_min, br_osoba_max)
    rezultat4 = pretraga_po_ceni_(cena_min, cena_max)
    rezultat5 = pretraga_po_datumu(datum1, datum2)
    rezultat_pretrage = [x for x in rezultat1 if x in rezultat2 and x in rezultat3 and x in rezultat4 and x in rezultat5]
    rezultat = ""
    for apartman in rezultat_pretrage:
        oprema_str = ""
        dostupnost_po_datumu_str = ""
        dostupnost_po_datumu = apartman["dostupnost_po_datumu"]
        intervali_str = []
        for datum1, datum2 in dostupnost_po_datumu:
            datum1_str = datum1.strftime("%d.%m.%Y")
            datum2_str = datum2.strftime("%d.%m.%Y")
            intervali_str.append(datum1_str + "," + datum2_str)
        dostupnost_po_datumu_str = '"'.join(intervali_str)
        oprema = apartman['dodatna_oprema']
        oprema_lista = []
        for o in oprema:
            oprema_lista.append(o)
        oprema_str = ", ".join(oprema_lista)
        rezultat += "|{:15}|{:15}|{:15}|{:23}|{:15}|{:16}|{:60}|{:42}{:}".format(
            apartman['tip'],
            str(apartman['broj_soba']),
            str(apartman['broj_gostiju']),
            apartman['adresa'],
            apartman['grad'],
            str(apartman['cena_po_noci']),
            dostupnost_po_datumu_str,
            oprema_str, "|") + "\n"
    return rezultat


def kreiranje_dodatne_opereme():
    oprema = {}
    oprema_naslov()
    print_meni_dodatna_oprema()
    sifra = konzola.unos_ceo_broj("Unesite sifru dodatne opreme(mora se uneti broj): ")
    sadrzaj = input("Unesite sadrzaj dodatne opreme odvojen zarezima(npr: Kuhinja, Garaza, Parking, Wi-Fi, Klima uredjaj, Pegla, Terasa): ").lower().capitalize()
    oprema['sifra'] = sifra
    oprema['sadrzaj'] = sadrzaj
    validnost_operma(oprema)


def validnost_operma(oprema):
    for oprema_d in dodatna_oprema:
        if oprema_d['sifra'] == oprema['sifra']:
            print("Uneta sifra je vec dodeljena!")
            return False
        elif len(oprema['sadrzaj']) <= 4:
            print("Unos sadzaja mora biti duzi od 3 slova!")
            return False
        elif oprema['sifra'] == "":
            print("Unos nije ispravan!")
            return False
        elif oprema['sadrzaj'] == "":
            print("Unos nije ispravan!")
            return False
        elif oprema['sadrzaj'] == oprema_d['sadrzaj']:
            print("Ovakva dodatna oprema je vec postojeca!")
            return False
    print("Uspesno kreirana dodatna oprema!")
    upisi_opremu(oprema)


def upisi_opremu(oprema):
    if oprema:
        with open("sadrzajapartmana.txt", 'a', encoding="utf-8") as fajl:
            fajl.write(str(oprema['sifra']) + "|" + oprema['sadrzaj'] + "\n")
        dodatna_oprema.append(oprema)
    return


def brisanje_dodatne_opreme():
    while True:
        oprema_naslov()
        print_meni_dodatna_oprema()
        unos = konzola.unos_ceo_broj("Unesite sifru opreme koju zelite obrisati: ")
        for oprema in dodatna_oprema:
            if unos == oprema['sifra']:
                dodatna_oprema[:] = [oprema for oprema in dodatna_oprema if oprema.get('sifra') != unos]
                print("Uspesno obrisana dodatna oprema!")
                ponovno_upisivanje_opreme(dodatna_oprema)
                return


def ponovno_upisivanje_opreme(nakon_brisanja):
    with open('sadrzajapartmana.txt', 'w', encoding="utf-8") as fajl:
        for oprema in nakon_brisanja:
            fajl.write(str(oprema['sifra']) + "|" + oprema['sadrzaj'] + "\n")
    return


def dodavanje_apartmana(korisnicko_ime_domacin):
    danas = datetime.today()
    #print(danas)
    novi_apartman = {}
    sifra = konzola.unos_ceo_broj("Unesite sifru apartmana(broj): ")
    apartman = nadji_po_sifri(sifra)
    if apartman:
        print("Apartman sa tom sifrom postoji!")
        return
    tip_apartmana = konzola.provera_za_tip("Unesite tip apartmana(soba, ceo apartman): ")
    broj_soba = konzola.unos_ceo_broj("Unesite broj soba: ")
    broj_gostiju = konzola.unos_ceo_broj("Unesite broj gostiju: ")
    adresa = konzola.provera_unosa_kratka_rec("Unesite ulicu i broj apartmana: ")
    grad = konzola.provera_unosa_kratka_rec("Unesite grad u kojem se apartman nalazi: ")
    postanski_broj = konzola.unos_ceo_broj("Unesite postanski broj apartmana: ")
    dostupnosti = konzola.provera_datuma()
    cena = konzola.unos_ceo_broj("Unesite cenu po noci: ")
    oprema_lista = konzola.dodatna_oprema()
    novi_apartman['sifra'] = sifra
    novi_apartman['tip'] = tip_apartmana
    novi_apartman['broj_soba'] = broj_soba
    novi_apartman['broj_gostiju'] = broj_gostiju
    novi_apartman['adresa'] = adresa
    novi_apartman['grad'] = grad
    novi_apartman['postanski_broj'] = postanski_broj
    novi_apartman['domacin'] = korisnicko_ime_domacin
    novi_apartman['cena_po_noci'] = cena
    novi_apartman['status'] = "Neaktivan"
    novi_apartman['dodatna_oprema'] = oprema_lista
    novi_apartman['dostupnost_po_datumu'] = dostupnosti
    apartmani.append(novi_apartman)
    print("Uspesno dodat apartman pod sifrom '"+ str(sifra) +"'.")
    sacuvaj()


def meni_apartman_izmena():
    print("Podaci koji se mogu menjati:")
    print("===============================")
    print("1. Tip")
    print("2. Broj soba")
    print("3. Broj gostiju")
    print("4. Adresa")
    print("5. Grad")
    print("6. Postanski broj")
    print("7. Domacin")
    print("8. Dostupnost po datumu")
    print("9. Cena po noci")
    print("10. Dodatna oprema")
    print("11. Status apartmana")
    print("x. Kraj izmena")
    print("===============================")


def izmena_apartmana(korisnicko_ime_domacina):
    domacin_korisnicko_ime = korisnicko_ime_domacina
    sifra = konzola.unos_ceo_broj("Unesite sifru apartmana kojeg zelite menjati: ")
    apartman = nadji_po_sifri(sifra)
    if not apartman:
        print("Apartman sa tom šifrom ne postoji.")
        return
    if domacin_korisnicko_ime != apartman['domacin']:
        print("Nije moguce izmeniti tudji apartman!")
        return False
    for rezervacija in rezervacije.rezervacije:
        if apartman['sifra'] == rezervacija['sifra_apartman'] and (rezervacija['status'] == "Kreirana" or rezervacija['status'] == "Potvrdjena"):
            print("Nije moguce promeniti apartman koji ima rezervacije!")
            return False

    while True:
        meni_apartman_izmena()
        izbor = input("Izbor podataka koji se mogu izmeniti: ").lower()
        if izbor == "1":
            tip = konzola.provera_za_tip("Unesite tip apartmana: ")
            apartman['tip'] = tip
        elif izbor == "2":
            broj_soba = konzola.unos_ceo_broj("Unesite broj soba: ")
            apartman["broj_soba"] = broj_soba
        elif izbor == "3":
            broj_gostiju = konzola.unos_ceo_broj("Unesite broj gostiju:")
            apartman["broj_gostiju"] = broj_gostiju
        elif izbor == "4":
            adresa = konzola.provera_unosa_kratka_rec("Unesite adresu: ")
            apartman['adresa'] = adresa
        elif izbor == "5":
            grad = konzola.provera_unosa_kratka_rec("Unesite ime grada: ")
            apartman['grad'] = grad
        elif izbor == "6":
            postanski_broj = konzola.unos_ceo_broj("Unesite postanski broj: ")
            apartman['postanski_broj'] = postanski_broj
        elif izbor == "7":
            domacin = konzola.provera_unosa_kratka_rec("Unesite korisnicko ime domacina: ").lower()
            apartman['domacin'] = domacin
        elif izbor == "8":
            dostupnosti = konzola.provera_datuma()   #return dostupnosti
            apartman['dostupnost_po_datumu'] = dostupnosti
        elif izbor == "9":
            cena = konzola.unos_ceo_broj("Unesite cenu po noci: ")
            apartman['cena_po_noci'] = cena
        elif izbor == "10":
            oprema = konzola.dodatna_oprema()
            apartman['dodatna_oprema'] = oprema
        elif izbor == "11":
            status = konzola.provera_unosa_status("Unesite status apartmana(Aktivan/Neaktivan): ")
            apartman['status'] = status
        elif izbor == "x":
            break
        else:
            print("Pogresan unos!")
    print("Uspesno izmenjeni podaci apartmana!")
    sacuvaj()


def brisanje_apartmana(domacin_korisnicko_ime):
    korisnicko_ime_domacin = domacin_korisnicko_ime
    sifra = konzola.unos_ceo_broj("Unesite sifru apartmana: ")
    apartman = nadji_po_sifri(sifra)
    if not apartman:
        print("Nema apartmana sa tom sifrom!")
        return False
    if korisnicko_ime_domacin != apartman['domacin']:
        print("Nije moguce obrisati tudji apartman!")
        return False

    if apartman:
        apartmani.remove(apartman)
        sacuvaj()
        rezervacija = rezervacije.nadji_rezervaciju_sifra(sifra)
        print("Apartman je uspesno obrisan!")
        if rezervacija:
            rezervacije.brisanje_rezervacija(rezervacija)
        else:
            pass

    else:
        print("Apartman sa tom šifrom ne postoji.")


def provera_dostupnosti():
    danas = datetime.now().date()
    for a in apartmani:
        for interval in a['dostupnost_po_datumu']:
            pocetni, krajnji = interval
            if krajnji.date() <= danas:
                lista = list(a['dostupnost_po_datumu'])
                lista.remove(interval)
                a['dostupnost_po_datumu'] = lista
                sacuvaj()

def prikaz_apartmana_sa_sifrom():
    print("|{:15}|{:20}|{:20}|{:20}|{:30}|{:23}|{:15}|".format("Sifra apartmana", "Tip", "Broj soba", "Broj gostiju", "Grad", "Adresa", "Cena po noci"))
    print("-"*151)
    for a in apartmani:
        print("|{:15}|{:20}|{:20}|{:20}|{:30}|{:23}|{:15}|".format(str(a['sifra']),
                                                                 a['tip'],
                                                                 str(a['broj_soba']),
                                                                 str(a['broj_gostiju']),
                                                                 a['grad'],a['adresa'],
                                                                 a['cena_po_noci'],
                                                                 "\n"))
    print("-"*151)



apartmani = []
dodatna_oprema = []
recnik_apartmani()
ucitavanje_dodatne_opreme()
