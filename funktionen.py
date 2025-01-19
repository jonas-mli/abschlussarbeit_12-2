
##########
# Import
##########

import pygame
import math 
from sound import musik, sfx


##################
# initialisieren
##################

pygame.init()
pygame.mixer.init()


##########
# Farben
##########

schwarz = 0, 0, 0
weiss = 255, 255, 255
dunkelgrau = 30, 30, 30
rot = 200, 0, 0
dunkelblau = 0, 30, 80
menü_grün = 0, 80, 50


################
# Schriftarten
################

monogram = pygame.font.Font("Texturen/fonts/monogram/monogram.ttf", 45)
schrift = pygame.font.SysFont("monogram", 40, False, False)
tacho_schrift = pygame.font.Font("Texturen/fonts/7Segment/dseg7-regular-normal.ttf", 45)
rundenzeit_schrift = pygame.font.Font("Texturen/fonts/monogram/monogram.ttf", 60)


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

bilder_s = []
def zoom_skalieren(bilder, zoom):         
     for bild, pos in bilder:
        bild_s = bild_skalieren(bild, zoom)
        bilder_s.append((bild_s, pos))
     return bilder_s

def textur_kacheln(gui, textur, y_pos=0, x_pos=0): # x/y_pos ist um ggf. die Textur zu verschieben 
    # So oft zeichnen, wie es nötig ist, um die Breite des Bildschirms zu füllen
    textur_breite, textur_hoehe = textur.get_size()
    kachel_ebene = pygame.Surface((BREITE*4, HOEHE*4))

    for y in range(0, HOEHE + textur_hoehe *2 , textur_hoehe):
        for x in range(0, BREITE + textur_breite *2, textur_breite): #+100 um überzustehen 
            kachel_ebene.blit(textur, (x + x_pos, y + y_pos))

    return kachel_ebene 

def grau_farbverlauf(gui, breite, hoehe):
    for y in range(hoehe):  
        grau_wert = 255 - int((y / hoehe) * 255)  
        farbe = (grau_wert, grau_wert, grau_wert)  
        pygame.draw.line(gui, farbe, (0, y), (breite, y))  

def sfx_spielen(effekt):
     if effekt in sfx:
          sfx[effekt].play()

def musik_spielen(song, loop=-1, lautstaerke=0.8):
    if song in musik:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(musik[song])
        pygame.mixer.music.set_volume(lautstaerke)
        pygame.mixer.music.play(loop)

def aktualisiere_masken():
    global BANDE_MASKE, ZIEL_LINIE_MASKE
    BANDE_MASKE = pygame.mask.from_surface(bild_skalieren(BANDE, 1))
    ZIEL_LINIE_MASKE = pygame.mask.from_surface(bild_skalieren(ZIEL_LINIE, 1))


def spieler_bewegen(spieler_auto):
     taste = pygame.key.get_pressed()
     bewegt = False 

     if spieler_auto.v != 0 and taste[pygame.K_a]:
          spieler_auto.rotieren(links=True)

     if spieler_auto.v != 0 and taste[pygame.K_d]:
          spieler_auto.rotieren(rechts=True)

     if taste[pygame.K_w]:
          bewegt = True
          spieler_auto.vorwaerts_bewegen()

     if spieler_auto.v <= 0 and taste[pygame.K_s]:
          bewegt = True
          spieler_auto.rueckwarts_bewegen()

#     if bewegt == True:
#          sfx_spielen("s.car_engine")

     if spieler_auto.v > 0 and taste[pygame.K_s]:
          spieler_auto.bremsen()

     if not bewegt:
          spieler_auto.reibung()

def tacho(gui, pos_x, pos_y, spieler_auto):    
#    hintergrund_f = (dunkelgrau)            
#    rahmen_f = (rot)         
#    radius = 60

    text_f = (weiss)
    kmh = abs(int(spieler_auto.v * 12))

    text = monogram.render(f"{kmh} km/h", True, text_f)

#    pygame.draw.rect(gui, hintergrund_f, (pos_x, pos_y))  
#    pygame.draw.circle(gui, rahmen_f, (pos_x, pos_y), radius, 4)       
    gui.blit(text, (pos_x - text.get_width() // 2, pos_y - text.get_height() // 2))



##############
# Konstanten 
##############

zoom = 1

STRECKE = bild_skalieren(pygame.image.load("Texturen/Strecke.png"), 0.85)
BREITE, HOEHE = STRECKE.get_width(), STRECKE.get_height() ## Weil Spielfenster von Strecke ausgefüllt werden soll wegen circular import doppelt

BANDE = bild_skalieren(pygame.image.load("Texturen/Bande.png"), 0.9777) #füroriginal 1.84
BANDE_MASKE = pygame.mask.from_surface(bild_skalieren(BANDE,zoom))

ZIEL_LINIE = bild_skalieren(pygame.image.load("Texturen/Ziel_Linie.png"), 0.2 * zoom) #Bande muss Linie Übermalen
ZIEL_POS = (230,1100)
ZIEL_LINIE_MASKE = pygame.mask.from_surface(bild_skalieren(ZIEL_LINIE,zoom))

FERRARI = bild_skalieren(pygame.image.load("Texturen/Ferrari.png"), 0.03 * zoom)
PORSCHE = bild_skalieren(pygame.image.load( "Texturen/Porsche.png"), 0.03 * zoom)

HINTERGRUND_HAUPTMENU = bild_skalieren(pygame.image.load("Texturen/Hauptmenü.png"),1.28)
HINTERGRUND_PAUSENMENU = bild_skalieren(pygame.image.load("Texturen/Pausenmenü.png"), 1.28)
HINTERGRUND_EINSTELLUNGSMENU = bild_skalieren(pygame.image.load("Texturen/Einstellungsmenü.png"),1.28)

ICON = pygame.image.load("Texturen/Icon.png")

############################
# Abstraktklasse definieren
#############################
# Wird benötigt, um generelle Eigenschaften von Autos dem Spieler-, als auch dem Gegnerauto zuzuweisen. Da diese aber andere Eigenschaften haben, sind diese in den jeweiligen Klassen definiert
class AbstraktAuto: # Siehe objektorientierte Programmierung       
#Klassen sind wie Eigenschaften für eine bestimmte Sache. Sachen können mehrere Klassen besitzen und Klassen können ineinander vererbt werden (siehe class SpielerAuto)
   
     def __init__(self, max_v, rotations_v): #self verweist auf sich selber, der rest sind standard Abhängigkeiten wie von Funktionen gewöhnt
          self.bild = self.AUTOBILD
          self.max_v = max_v
          self.v = 0
          self.rotations_v = rotations_v
          self.winkel = 0
          self.x, self.y = self.START_POS
          self.beschleunigung = 0.3
 

     def rotieren(self, links = False, rechts = False):
          if links:
               self.winkel += self.rotations_v
          if rechts: 
               self.winkel -= self.rotations_v
    
     def zei(self, gui):
          blit_rotieren(gui, self.bild, (self.x, self.y), self.winkel)

     def vorwaerts_bewegen(self):
          self.v = min(self.v + self.beschleunigung, self.max_v)
          self.bewegen()

     def rueckwarts_bewegen(self):
          self.v = max(self.v - self.beschleunigung, -self.max_v/2)
          self.bewegen()

     def bremsen(self):
          self.v = max(self.v - (self.v * 0.15 ) , 0)
          self.bewegen()
     
     def bewegen(self):
          radianten = math.radians(self.winkel) # In Radianten konvertieren, weil Computer besser damit rechnen
          vertikale = math.cos(radianten) * self.v 
          horizontale = math.sin(radianten) * self.v

          self.y -= vertikale #Wegen Winkel muss subtrahiert werden
          self.x -= horizontale
     
     def reibung(self):
          self.v = max(self.v - self.beschleunigung / 1.001, 0)
          self.bewegen()

     def kollidieren(self, maske, x=0, y=0):
          auto_maske = pygame.mask.from_surface(self.bild)
          offset = (int(self.x - x), int(self.y - y))

          schnittP = maske.overlap(auto_maske, offset) #Schnittpunkt

#          print('kollision')
#          print(f"offset: {offset}, spieler: ({self.x}, {self.y}), hindernis: ({x}, {y})")
#          print(f"Hindernis-Maske: {maske.get_size()}, Offset: {offset}")          
          return schnittP 
          
     def rueckstoss(self):
          self.v = - 0.6* self.v
          self.bewegen()

     def ziel(self):
          self.x, self.y = self.START_POS
          self.winkel = 0

class Allg:
     """= Allgemein für alle generelle funktionen des spiels wie bspw. der Rundentimer"""
     
     def __init__(self):
          # alles für rundentimer
          self.rundenstart = pygame.time.get_ticks()
          self.pausenstart = 0
          self.rundenzeit = 0 
          self.pausenzeit = 0
          self.gestartet = False 
          # alles für slider
          self.zoom = zoom
          self.lautstaerke = 0.8
#          self.lautstaerke = pygame.mixer.music.get_volume()
          self.slider_zoom = self.Slider(BREITE // 2 - 150, 500, 300, 1, 5, self.zoom)
          self.slider_lautstaerke = self.Slider(BREITE // 2 - 150, 700, 300, 0, 1, self.lautstaerke)

          
     class Slider:
        def __init__(self, x, y,breite, min_wert, max_wert, start_wert):
            self.rect = pygame.Rect(x, y, breite, 20)  #für hintergrund
            self.knopf = pygame.Rect(x, y - 5, 10, 30)  # knopf
            self.min_wert = min_wert
            self.max_wert = max_wert
            self.wert = start_wert
            self.breite = breite
            self.knopf.centerx = x + int((start_wert - min_wert) / (max_wert - min_wert) * breite)

        def zei(self, gui):
            pygame.draw.rect(gui, schwarz, self.rect)  # Hintergrund
            pygame.draw.rect(gui, weiss, self.knopf)  # Knopf

        def events(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN and self.knopf.collidepoint(event.pos):
                self.bewegen = True

            elif event.type == pygame.MOUSEBUTTONUP:
                self.bewegen = False

            elif event.type == pygame.MOUSEMOTION and hasattr(self, 'bewegen') and self.bewegen: # hasattr = hat das attribut sich zu bewegen
                self.knopf.centerx = max(self.rect.left, min(event.pos[0], self.rect.right))
                self.wert = self.min_wert + (self.knopf.centerx - self.rect.left) / self.breite * (self.max_wert - self.min_wert)
