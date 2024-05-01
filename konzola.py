from datetime import datetime
import apartmani


def unos_ceo_broj(poruka):
    while True:
        try:
            broj = int(input(poruka))
            return broj
        except ValueError:
            print("Morate uneti ceo broj.")

def provera_za_tip(tip):
    lista = ["Ceo apartman", "Soba"]
    while True:
        unos = input(tip).capitalize()
        if unos == lista[0] or unos == lista[1]:
            return unos
        else:
            print("Tip apartmana nije validan!")
            continue


def unos_datum(poruka):
    while True:
        try:
            datum_str = input(poruka)
            datum = datetime.strptime(datum_str, "%d/%m/%Y")
            return datum.date()
        except ValueError:
            print("Morate uneti datum u formatu dd/mm/yyyy.")


def provera_datuma():
    danas = datetime.today()
    dostupnosti = []
    while True:
        print("Unesite datum po principu od/do u odgovarajucem formatu(d.m.Y):")
        datum1_str = input(">>>")
        datum2_str = input(">>>")
        try:
            datum1 = datetime.strptime(datum1_str, "%d.%m.%Y")
            datum2 = datetime.strptime(datum2_str, "%d.%m.%Y")
            if danas < datum1 < datum2:
                dostupnosti.append((datum1, datum2))
            else:
                print("Pogresan opseg datuma!")
                continue
        except ValueError:
            print("Loš format.")
            continue
        print("Unesite 'x' ako ste zavrsili sa unosenjem datuma(enter za nastavak): ")
        nastavak = ""
        while nastavak != "x":
            nastavak = input(">>>")
            if nastavak == "x":
                return dostupnosti
            elif nastavak == "":
                break


def provera_unosa_status(poruka):
    stanje_apartmana = ["Aktivan", "Neaktivan"]
    while True:
        unos = input(poruka).capitalize()
        if unos == stanje_apartmana[0] or unos == stanje_apartmana[1]:
            return unos
        else:
            print("Unos stanja apartmana nije validan")
            continue

def dodatna_oprema():
    oprema_lista = []
    fleg = 0
    while True:
        try:
            apartmani.oprema_naslov()
            apartmani.print_meni_dodatna_oprema()
            print("Unesite sifru dodatne opreme koju zelite da dodate: ")
            oprema = int(input(">>>"))
            d_oprema = apartmani.nadji_opremu_po_sifri(oprema)
            if fleg == 1:
                if not d_oprema:
                    print("Uneta sifra nije postojeca!")
                    continue
                for o in oprema_lista:
                    if d_oprema['sadrzaj'] == o:
                        oprema_lista.remove(d_oprema['sadrzaj'])
                        print("Dati apartman vec sadrzi tu opremu!")
            if d_oprema:
                oprema_lista.append(d_oprema['sadrzaj'])
                fleg = 1
            else:
                print("Uneta sifra nije postojeca!")
                continue

        except ValueError:
            print("Niste uneli ceo broj!")
            continue
        print("Ukoliko ste zavrsili sa upisivanjem unesite 'x'(enter za nastavak): ")
        izlaz = ""
        while izlaz != 'x':
            izlaz = input(">>>")
            if izlaz == "x":
                return oprema_lista
            elif izlaz == "":
                break

def provera_unosa_kratka_rec(poruka):
    while True:
        unos = input(poruka)
        if len(unos) < 3:
            print("Duzina unetog podatka mora biti duzine najmanje 3 karaktera: ")
            continue
        else:
            return unos
