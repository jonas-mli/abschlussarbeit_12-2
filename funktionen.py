
##########
# Import
##########

import pygame
import math 
from sound import musik, sfx


##########
# Farben
##########

schwarz = 0, 0, 0
weiss = 255, 255, 255
dunkelgrau = 30, 30, 30
rot = 200, 0, 0
dunkelblau = 0, 30, 80


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

    for y in range(0, HOEHE + textur_hoehe + 100 , textur_hoehe):
        for x in range(0, BREITE + textur_breite + 100, textur_breite): #+100 um überzustehen 
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

     if spieler_auto.v > 0 and taste[pygame.K_s]:
          spieler_auto.bremsen()

     if not bewegt:
          spieler_auto.reibung()

def tacho(gui, pos_x, pos_y, spieler_auto):    
#    hintergrund_f = (dunkelgrau)            
#    rahmen_f = (rot)         
#    radius = 60

    text_f = (weiss)
    kmh = abs(int(spieler_auto.v * 31))
    schrift = pygame.font.SysFont("Arial", 24, True)
    text = schrift.render(f"{kmh} km/h", True, text_f)

#    pygame.draw.rect(gui, hintergrund_f, (pos_x, pos_y))  
#    pygame.draw.circle(gui, rahmen_f, (pos_x, pos_y), radius, 4)       
    gui.blit(text, (pos_x - text.get_width() // 2, pos_y - text.get_height() // 2))



##############
# zusätzliche Texturen als Konstanten laden
##############

STRECKE = pygame.image.load("Texturen/Strecke.png")
BREITE, HOEHE = STRECKE.get_width(), STRECKE.get_height() #wegen circular import doppelt

STRECKE = bild_skalieren(pygame.image.load("Texturen/Strecke.png"), 0.85)
BANDE = bild_skalieren(pygame.image.load("Texturen/Bande.png"), 1.84)
BANDE_MASKE = pygame.mask.from_surface(BANDE)

ZIEL_LINIE = pygame.image.load("Texturen/Ziel_Linie.png") #Bande muss Linie Übermalen
ZIEL_POS = (10,200)
ZIEL_LINIE_MASKE = pygame.mask.from_surface(ZIEL_LINIE)

FERRARI = bild_skalieren(pygame.image.load("Texturen/Ferrari.png"), 0.05)
PORSCHE = bild_skalieren(pygame.image.load( "Texturen/Porsche.png"), 0.07)


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
          self.winkel = 00
          self.x, self.y = self.START_POS
          self.beschleunigung = 0.1

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
          self.v = max(self.v - self.beschleunigung / 1.2, 0)
          self.bewegen()

     def kollidieren(self, maske, x=0, y=0):
          auto_maske = pygame.mask.from_surface(self.bild)
          offset = (int(self.x  - x), int(self.y - y))
          schnittP = maske.overlap(auto_maske, offset) #Schnittpunkt 

          return schnittP
     
     def rueckstoss(self):
          self.v = -self.v
          self.bewegen()