import operator
import pygame
import sys
import betoltesek


class NevPont:
    """Minden értékhez tartozik így majd egy név és pontszám"""
    def _init_(self, nev, pontszam):
        self.nev = nev
        self.pontszam = pontszam


class Objektum:
    def __init__(self, szelesseg, magassag, kep):
        self.szelesseg = szelesseg
        self.magassag = magassag
        self.kep = kep


def szamokmegjelenitese(felulet, eredmenyszamlalo, szamok):
    """Ennek segítségével jeleníti meg számokat a képernyőn a (szám)képekből"""
    if eredmenyszamlalo < 10:
        betoltesek.kepmegjelenites(felulet, szamok[eredmenyszamlalo])
    else:
        for i in range(len(str(eredmenyszamlalo))):
            szam = str(eredmenyszamlalo)[i]
            if i != 0:
                szamok[int(szam)].szelesseg += 38
            betoltesek.kepmegjelenites(felulet, szamok[int(szam)])
            szamok[int(szam)].szelesseg = 216


def szamlalas(cso):
    """Amennyiben a madár a cső végében van, hozzáad egy pontot az eredményhez (legalábbis +1-et ad vissza)"""
    if 100 < cso.szelesseg + 52 < 101.7:
        return 1
    else:
        return 0


def listaban():
    """Visszad egy listát, amely tartalmazza rendezve az eddigi eredményeket"""
    osszeseredmeny = []
    try:
        with open('eredmenyek.txt') as f:
            for line in f:
                sor = line.rstrip("\n")
                darabok = sor.split(" ")
                mostanieredmeny = NevPont()
                mostanieredmeny.nev = darabok[0]
                mostanieredmeny.pontszam = int(darabok[1])
                osszeseredmeny.append(mostanieredmeny)
        rendezetteredmenyek = sorted(osszeseredmeny, key=operator.attrgetter("pontszam"))
        return rendezetteredmenyek
    except FileNotFoundError:
        return FileNotFoundError


def nagytabla(felulet):
    """A nagy eredménytábla betöltője"""
    narancs = pygame.Color('#FE6148')
    font = pygame.font.SysFont('Cooper Black', 25)
    if listaban() is not FileNotFoundError:
        legjobb5 = [NevPont()] * 5

        nevszelesseg = 80
        pontszelesseg = 320
        eredmenymagassag = 100

        if len(listaban()) >= 5:
            kiirtszamokdb = len(legjobb5)
        else:
            kiirtszamokdb = len(listaban())

        for i in range(kiirtszamokdb):
            legjobb5[i].pontszam = font.render(str(listaban()[len(listaban()) - i - 1].pontszam),
                                               True, narancs)
            legjobb5[i].nev = font.render(str(listaban()[len(listaban()) - i - 1].nev), True,
                                          narancs)
            felulet.blit(legjobb5[i].nev, (nevszelesseg, eredmenymagassag))
            felulet.blit(legjobb5[i].pontszam, (pontszelesseg, eredmenymagassag))
            eredmenymagassag += 100
    else:
        megnincseredmeny = font.render("Még nincs eredmény", True, narancs)
        felulet.blit(megnincseredmeny, (100, 200))


def kiir(nev, eredmeny):
    """Kiírja a nevet és eredményt egy txt fájlba"""
    f = open('eredmenyek.txt', 'a')
    f.write('{} {}\n'.format(nev, eredmeny))
    f.close()


def nevbeker(felulet):
    """Bekéri a játékos nevét"""
    narancs = pygame.Color('#FE6148')
    sarga = pygame.Color('#DED894')
    font = pygame.font.SysFont('Cooper Black', 25)
    pygame.display.update()
    user_input = betoltesek.szovegbeolvasas(90, 245, 180, 40, sarga, narancs, font, felulet)
    if user_input is None:
        pygame.quit()
        sys.exit()
    else:
        return user_input


def maxpontszame(eredmenyszamlalo):
    """Megnézi, hogy a játékos rekordot ért-e el."""
    if listaban() is not FileNotFoundError:
        max = listaban()[len(listaban()) - 1].pontszam
        if max >= eredmenyszamlalo:
            return False
        elif eredmenyszamlalo > max:
            return True
    else:
        return True


def legjobbnev(eredmenyszamlalo, nev):
    """Megnézi, hogy a játékos a rekorder-e, ha igen akkor az ő nevét adja vissza,
    ellenkező esetben az eddigi rekorderét"""
    if maxpontszame(eredmenyszamlalo) is True:
        return nev
    else:
        return listaban()[len(listaban()) - 1].nev


def maxpontnevkiiras(felulet, eredmenyszamlalo, kiiras):
    """Kiírja a maxpontszámot, illetve az eddigi rekorder nevét is amennyibe az nem a mostani játékos"""
    font = pygame.font.SysFont('Cooper Black', 25)
    narancs = pygame.Color('#FE6148')
    if maxpontszame(eredmenyszamlalo) is True:
        maxpont = eredmenyszamlalo
    else:
        maxpont = listaban()[len(listaban()) - 1].pontszam
        if kiiras is False:
            felulet.blit(
                font.render(str(listaban()[len(listaban()) - 1].nev), True, narancs),
                (90, 310))
    felulet.blit(font.render(str(maxpont), True, narancs), (300, 310))


def jatekosnevmegjelenites(felulet, nev, legjobbnev):
    """Kiírja a rekorder nevét, akár a játékosét is amennyiben ő az."""
    font = pygame.font.SysFont('Cooper Black', 25)
    narancs = pygame.Color('#FE6148')
    felulet.blit(font.render(nev, True, narancs), (90, 245))
    felulet.blit(font.render(legjobbnev, True, narancs), (90, 310))


def pontszam(felulet, eredmenyszamlalo):
    """Jelenlegi pontszám kiírása az eredménytáblára"""
    narancs = pygame.Color('#FE6148')
    font = pygame.font.SysFont('Cooper Black', 25)
    pontszam = font.render(str(eredmenyszamlalo), True, narancs)
    felulet.blit(pontszam, (300, 245))
