import pygame
import pygame.gfxdraw


class Objektum:
    def __init__(self, szelesseg, magassag, kep):
        self.szelesseg = szelesseg
        self.magassag = magassag
        self.kep = kep


def szovegbeolvasas(x, y, width, height, bg_color, fg_color, font, felulet):
    """Beolvassa a szöveget: esetünkben a nevet"""
    clip = felulet.get_clip()
    destination = pygame.Rect(x, y, width, height)
    felulet.set_clip(destination)

    user_input = ''
    enter = False
    quit = False

    while (not quit) and (not enter):
        # szöveg kirajzolása
        pygame.gfxdraw.box(felulet, destination, bg_color)
        pygame.gfxdraw.rectangle(felulet, destination, fg_color)
        text = font.render(user_input + '|', True, fg_color)
        felulet.blit(text, destination)
        pygame.display.update()

        event = pygame.event.wait()
        if event.type == pygame.KEYDOWN:
            # enter: bevitel vége
            if event.key == pygame.K_RETURN:
                enter = True
            # backspace: utolsó karakter törlése
            elif event.key == pygame.K_BACKSPACE:
                user_input = user_input[:-1]
            # egyébként meg hozzáadjuk a beírt szöveghez
            else:
                if len(user_input) <= 8 and event.unicode != " ":
                    user_input += event.unicode

        if event.type == pygame.QUIT:
            # visszatesszük a sorba, mert sok mindent nem tudunk vele kezdeni
            pygame.event.post(event)
            quit = True

    felulet.set_clip(clip)

    if quit is False:
        return user_input
    else:
        return None


def kep(kepnev):
    """Ennek segítségével olvassa be a képeket egyszerűen egy név megadásával,
    amennyiben azok .png formátumban vannak"""
    png = (str(kepnev) + ".png")
    if kepnev != "favicon":
        return pygame.image.load(png).convert_alpha()
    else:
        return pygame.image.load(png)


def kepmegjelenites(ablak, nev):
    """Ennek segítségével jeleníti meg az adott objektumot a képernyőn"""
    return ablak.blit(nev.kep, [nev.szelesseg, nev.magassag])


def ablak():  # Pygame betöltés és favicon betöltés
    """Ezzel tölti be a pygame-t illetve az ablak faviconját, címét"""
    pygame.init()
    pygame.display.set_caption("Flappy Bird")
    favicon = kep("favicon")
    pygame.display.set_icon(favicon)


def szamok():
    """Ezzel tölti be az összes számot ami kép formátumú"""
    szamok = [Objektum(0, 0, 0)] * 10
    for i in range(10):
        kepnev = str(i)
        szamok[i] = Objektum(198, 100, kep(kepnev))
    return szamok
