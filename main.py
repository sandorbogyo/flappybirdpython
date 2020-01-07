import pygame
import random
import sys
import eredmenyek
import betoltesek


class Objektum:
    def __init__(self, szelesseg, magassag, kep):
        self.szelesseg = szelesseg
        self.magassag = magassag
        self.kep = kep


class Valasztas:
    fomenu = 1
    jatek = 2
    gamover = 3
    eredmeny = 4


def elforgatas(kep, fok):
    """Ennek segítségével elforgathatok egy képet így például a madarat miután meghal"""
    try:
        return pygame.transform.rotate(kep, fok)
    except:
        pass


def talajgeneralas(felulet, talaj, folyamatosvagynem):
    """Ezzel tölti be a talajt, illetve lehet állítani,
    hogy folyamatosan balra menjen vagy állandó állapotban legyen („mozgó háttér”)"""
    if talaj.szelesseg > -432 and folyamatosvagynem is False:
        talaj.szelesseg = talaj.szelesseg - 1.7
    else:
        talaj.szelesseg = 0
    felulet.blit(talaj.kep, [talaj.szelesseg, talaj.magassag])


def madarbetoltes(felulet, madar, jatekvege):
    """Ezzel jeleníti és tölti be a madarat: ha él akkor az eredeti képet,
    ha nem, akkor pedig a halott elforgatott képet"""
    if jatekvege is False:
        betoltesek.kepmegjelenites(felulet, madar)
    else:
        meghaltmadar = Objektum(madar.szelesseg, madar.magassag, elforgatas(madar.kep, -80))
        betoltesek.kepmegjelenites(felulet, meghaltmadar)


def jatekinditouzenet(start, felulet, uzenet):
    """A játék indítása előtti üzenetet tölti be """
    if start is False:
        betoltesek.kepmegjelenites(felulet, uzenet)


def belementazoszlopba(madar, cso):
    """Ennek segítségével ellenőrzi, hogy a madár beleütközött-e a csövekbe vagy nem"""
    if (cso.magassag - 120 > madar.magassag > cso.magassag - 120 - 700) or (
            cso.magassag - 40 < madar.magassag < cso.magassag + 700):
        if 100 < cso.szelesseg < 151:
            return True


def halalutanfold(madar, talaj, jatekvege):
    """Amennyiben meghalt a madár és a levegőben volt, lefelé esik amíg nem ér a pálya aljára."""
    if madar.magassag < talaj.magassag - 36 and jatekvege is True:
        return 10
    else:
        return 0


def madarlefele(madar, talaj, madarklikk):
    """Ennek segítségével tart folyamatosan lefelé a madár."""
    if madar.magassag < talaj.magassag - 36 and madarklikk is False:
        return madar.magassag + 2.3
    else:
        return madar.magassag


def madartalajhozert(madar, talaj, jatekvege):
    """Amennyiben a madár a talajhoz ér, vége a játéknak."""
    if madar.magassag >= talaj.magassag - 36:
        return True
    else:
        return jatekvege


def madarfelklikkutan(madar, madarklikk, jatekvege):
    """Amennyiben a játékos klikkelt, a madár elkezd felfelé menni."""
    if madarklikk is True and jatekvege is False:
        return madar.magassag - 2
    else:
        return madar.magassag


def madarelerteaklikkmagassagot(madarklikk, jatekvege, madar, ujmadarmagassag):
    """Amennyiben a játékos klikkelt, és a madár felért a klikkmagassághoz, a klikket false tesszük."""
    if madarklikk is True and jatekvege is False and madar.magassag <= ujmadarmagassag:
        return False
    else:
        return madarklikk


def kimentapalyarol(madarmagassag):
    """Amennyiben a játékos megpróbál felül kimenni a pályáról, visszaállítja a legfelső lehetséges pozícióba"""
    if madarmagassag < 0:
        return 0
    else:
        return madarmagassag


def csoszelesseg(cso, jatekvege):
    """Ez felel a folyamatosan mozgó csövekért, hogy balra mozogjanak amíg el nem tűnik a képernyőről.
    Miután eltűnt újra elindulnak a pálya jobb oldaláról"""
    if jatekvege is False:
        if -52 < cso.szelesseg:
            return cso.szelesseg - 1.7
        else:
            return 432
    else:
        return cso.szelesseg


def csomagassag(cso, jatekvege):
    """Ez felel azért, hogy milyen magasan helyezkedjen el az alsó cső"""
    if jatekvege is False:
        if cso.szelesseg == 432:
            return random.randint(180, 600)
        else:
            return cso.magassag
    else:
        return cso.magassag


def csogeneralas(felulet, cso, start, jatekvege):
    """Ez tölti be a képernyőre az alsó cső-t, illetve magasságának függvényében tölti be a felső csövet"""
    if start is True:
        cso.szelesseg = csoszelesseg(cso, jatekvege)
        cso.magassag = csomagassag(cso, jatekvege)
        betoltesek.kepmegjelenites(felulet, cso)
        cso2 = Objektum(cso.szelesseg, cso.magassag - 120 - 700, elforgatas(cso.kep, 180))
        betoltesek.kepmegjelenites(felulet, cso2)


def klikkeltobjektum(objektum, event, szel, mag):
    """Ennek segítségével tudom ellenőrizni, hogy rákattintottak-e egy objektumra."""
    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos
        if objektum.szelesseg <= x <= objektum.szelesseg + szel:
            if objektum.magassag <= y <= objektum.magassag + mag:
                return True
            else:
                return False
        else:
            return False
    else:
        return False


def fomenu():

    # Betöltjük az ablakot, illetve a képeket
    betoltesek.ablak()
    felulet = pygame.display.set_mode((432, 768))
    madar = Objektum(180, 300, betoltesek.kep("madar"))
    hatter = Objektum(0, 0, betoltesek.kep("hatter"))
    talaj = Objektum(0, 600, betoltesek.kep("talaj"))
    start = Objektum(60, 450, betoltesek.kep("startgomb"))
    eredmeny = Objektum(260, 450, betoltesek.kep("eredmenygomb"))
    flappybird = Objektum(78, 100, betoltesek.kep("flappybird"))

    # Kiléptek?
    quit = False

    # Betöltöjük a modult ami felel az FPS-ért
    ora = pygame.time.Clock()

    while not quit:

        # Ez felel az FPS-ért
        ora.tick(120)

        # Megnézzük, hogy rákattintottak-e az egyik menügombra
        for event in pygame.event.get():
            # Ha rákattintottak az X-re, kilép
            if event.type == pygame.QUIT:
                quit = True
            if klikkeltobjektum(start, event, 117, 66) is True:
                return 2
            if klikkeltobjektum(eredmeny, event, 117, 66) is True:
                return 4

        # Háttér megjelenítése
        betoltesek.kepmegjelenites(felulet, hatter)

        # Talaj generálása
        talajgeneralas(felulet, talaj, False)

        # Megjelenítjük a gombokat és a Flappy Bird feliratot
        betoltesek.kepmegjelenites(felulet, start)
        betoltesek.kepmegjelenites(felulet, eredmeny)
        betoltesek.kepmegjelenites(felulet, flappybird)

        # Megjelenítjük a madarat
        betoltesek.kepmegjelenites(felulet, madar)

        pygame.display.flip()

    # Kilépés amennyiben a felhasználó X-elt
    pygame.quit()
    sys.exit()


def jatek():

    # Betöltjük az ablakot, illetve a képeket
    betoltesek.ablak()
    felulet = pygame.display.set_mode((432, 768))
    madar = Objektum(100, 384, betoltesek.kep("madar"))
    cso = Objektum(432, random.randint(180, 600), betoltesek.kep("cso"))
    hatter = Objektum(0, 0, betoltesek.kep("hatter"))
    uzenet = Objektum(78, 250, betoltesek.kep("uzenet"))
    talaj = Objektum(0, 600, betoltesek.kep("talaj"))

    # Számok betöltése
    szamok = betoltesek.szamok()

    # Kilépés, jatekvege, és start figyelés
    quit = False
    jatekvege = False
    start = False

    # Klikkeltek már?
    madarklikk = False

    # Eredmény számlálója
    eredmenyszamlalo = 0

    # Betöltöjük a modult ami felel az FPS-ért
    ora = pygame.time.Clock()

    while not quit:

        # Ez felel az FPS-ért
        ora.tick(120)

        # Space illetve egérklikk figyelése
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                start = True
                madarklikk = True
                # Idáig kell eljutnia klikkelés után
                ujmadarmagassag = madar.magassag - 55

            # A pálya tetejét nézi, hogy ne lehessen kimenni
            madar.magassag = kimentapalyarol(madar.magassag)

            # Ha rákattintottak az X-re, kilép
            if event.type == pygame.QUIT:
                quit = True

        # Háttér megjelenítése
        betoltesek.kepmegjelenites(felulet, hatter)

        # Talaj generálása
        talajgeneralas(felulet, talaj, jatekvege)

        # Ha elkezdődött a játék, a madár lefelé tart, klikkeléskor felfelé, de ha hozzáér a talajhoz, vége a játéknak
        if start is True:
            madar.magassag = madarlefele(madar, talaj, madarklikk)
            jatekvege = madartalajhozert(madar, talaj, jatekvege)
            madar.magassag = madarfelklikkutan(madar, madarklikk, jatekvege)
            madarklikk = madarelerteaklikkmagassagot(madarklikk, jatekvege, madar, ujmadarmagassag)

        # Csövek generálása
        csogeneralas(felulet, cso, start, jatekvege)

        # A madár megjelenítése
        madarbetoltes(felulet, madar, jatekvege)

        # Betölti a segítő üzenetet a jtáék indítása előtt
        jatekinditouzenet(start, felulet, uzenet)

        # Számok megjelenítése
        if jatekvege is False:
            eredmenyek.szamokmegjelenitese(felulet, eredmenyszamlalo, szamok)

        # Itt vizsgáljuk, hogy belemente az oszlopba
        if belementazoszlopba(madar, cso) is True:
            jatekvege = True

        # Megnézi, hogy a madár a földön van-e már vagy oda kell rakni halál után
        madar.magassag += halalutanfold(madar, talaj, jatekvege)

        # Számlálás
        eredmenyszamlalo += eredmenyek.szamlalas(cso)

        # Ha vége a játéknak meghívja a gameovert
        if jatekvege is True and madar.magassag >= talaj.magassag - 36:
            jatekvegefelulet = gamover(talaj, cso, madar, hatter, eredmenyszamlalo)
            if jatekvegefelulet == 2:
                return 2
            elif jatekvegefelulet == 4:
                return 4

        pygame.display.flip()

    # Kilépés amennyiben a felhasználó X-elt
    pygame.quit()
    sys.exit()


def gamover(talaj, cso, madar, hatter, eredmenyszamlalo):

    # Betöltjük az ablakot, illetve a képeket
    betoltesek.ablak()
    felulet = pygame.display.set_mode((432, 768))
    jatekvegefelirat = Objektum(72, 100, betoltesek.kep("jatekvege"))
    startgomb = Objektum(60, 450, betoltesek.kep("startgomb"))
    eredmenygomb = Objektum(260, 450, betoltesek.kep("eredmenygomb"))
    eredmenyrovid = Objektum(67, 200, betoltesek.kep("eredmenyrovid"))

    # Kilépés figyelő illetve megnézzük, hogy már bekértük-e a nevet, és kiírtuk-e fájlba is az eredményt
    quit = False
    nevmegjelenites = False
    kiiras = False

    while not quit:

        # Megnézzük, hogy rákattintottak-e az egyik menügombra
        for event in pygame.event.get():
            if klikkeltobjektum(startgomb, event, 117, 66) is True:
                return 2
            if klikkeltobjektum(eredmenygomb, event, 117, 66) is True:
                return 4
            # Ha rákattintottak az X-re, kilép
            if event.type == pygame.QUIT:
                quit = True

        # Háttér megjelenítése
        betoltesek.kepmegjelenites(felulet, hatter)

        # Talaj generálása
        talajgeneralas(felulet, talaj, True)
        csogeneralas(felulet, cso, True, True)

        # A madár megjelenítése
        madarbetoltes(felulet, madar, True)

        # Menügombok, és az eredménytábla megjelenítése
        betoltesek.kepmegjelenites(felulet, jatekvegefelirat)
        betoltesek.kepmegjelenites(felulet, startgomb)
        betoltesek.kepmegjelenites(felulet, eredmenygomb)
        betoltesek.kepmegjelenites(felulet, eredmenyrovid)

        # Jelenlegi pontszám kiírása az eredménytáblára
        eredmenyek.pontszam(felulet, eredmenyszamlalo)

        # Kiírja a maxpontszámot, illetve az eddigi rekorder nevét is amennyibe az nem a mostani játékos
        eredmenyek.maxpontnevkiiras(felulet, eredmenyszamlalo, kiiras)

        # Név bekérése egyszer majd megjelenítés
        if nevmegjelenites is False:
            nev = eredmenyek.nevbeker(felulet)
            legjobbnev = eredmenyek.legjobbnev(eredmenyszamlalo, nev)
            nevmegjelenites = True

        # Kiírja a rekorder nevét, akár a játékosét is amennyiben ő az.
        eredmenyek.jatekosnevmegjelenites(felulet, nev, legjobbnev)

        # Név és eredmény kiírása txtbe egyszer
        if kiiras is False:
            eredmenyek.kiir(nev, str(eredmenyszamlalo))
            kiiras = True

        pygame.display.flip()

    # Kilépés amennyiben a felhasználó X-elt
    pygame.quit()
    sys.exit()


def eredmeny():

    # Betöltjük az ablakot, illetve a képeket
    betoltesek.ablak()
    felulet = pygame.display.set_mode((432, 768))
    hatter = Objektum(0, 0, betoltesek.kep("hatter"))
    start = Objektum(150, 650, betoltesek.kep("startgomb"))
    eredmenynagy = Objektum(20, 10, betoltesek.kep("eredmenynagy"))

    # Kilépés már?
    quit = False

    while not quit:
        for event in pygame.event.get():
            # Ha rákattintottak az X-re, kilép
            if event.type == pygame.QUIT:
                quit = True
            # Menügomb figyelése
            if klikkeltobjektum(start, event, 117, 66) is True:
                return 2

        # Háttér, startgomb és eredménytábla képének megjelenítése
        betoltesek.kepmegjelenites(felulet, hatter)
        betoltesek.kepmegjelenites(felulet, start)
        betoltesek.kepmegjelenites(felulet, eredmenynagy)

        # Nagytáblán az eredmények megjelenítése névvel és ppntszámmal
        eredmenyek.nagytabla(felulet)

        pygame.display.flip()

    # Kilépés az X-re
    pygame.quit()
    sys.exit()


def main():

    valasztas = Valasztas.fomenu

    while True:
        if valasztas == Valasztas.fomenu:
            valasztas = fomenu()
        elif valasztas == Valasztas.jatek:
            valasztas = jatek()
        elif valasztas == Valasztas.eredmeny:
            valasztas = eredmeny()


main()
