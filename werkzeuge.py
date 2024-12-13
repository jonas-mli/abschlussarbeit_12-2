import pygame

#############
#Konstanten
#############

STRECKE = pygame.image.load("Texturen/Strecke.png")
BREITE, HOEHE = STRECKE.get_width(), STRECKE.get_height() #wegen circular import doppelt


##############
# Funktionen
##############

def blit_rotieren(gui, bild, oben_links, winkel):
    rotiertes_bild = pygame.transform.rotate(bild, winkel)
    neues_rechteck = rotiertes_bild.get_rect(center = bild.get_rect(topleft = oben_links).center) #benötigt um Viereck des Bildes zu rotieren, ohne x und y Koordinaten zu verändern oder Bild zu verzerren. Erklärung: Neues Riereck soll zentriert zu Viereck des Bildes an der Stekke oben Links sein 
    gui.blit(rotiertes_bild, neues_rechteck.topleft)


def bild_skalieren(bild, wert):
    groesse = round(bild.get_width() * wert), round(bild.get_height() * wert)
    return pygame.transform.scale(bild, groesse)


def textur_kacheln(gui, textur, y_pos=0, x_pos=0): # x/y_pos ist um ggf. die Textur zu verschieben 
    # So oft zeichnen, wie es nötig ist, um die Breite des Bildschirms zu füllen
    textur_breite, textur_hoehe = textur.get_size()
    kachel_ebene = pygame.Surface((BREITE, HOEHE))

    for y in range(0, HOEHE, textur_hoehe):
        for x in range(0,BREITE, textur_breite): 
            kachel_ebene.blit(textur, (x + x_pos, y + y_pos))

    return kachel_ebene
