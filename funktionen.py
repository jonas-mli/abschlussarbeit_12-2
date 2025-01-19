
#######################
# Import Bibliotheken
#######################

import pygame
import os
import time
import math 
import multiprocessing
import concurrent.futures
from functools import partial
from sound import *


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
creme = 250, 240, 195

################
# Schriftarten
################

monogram = pygame.font.Font("Texturen/fonts/monogram/monogram.ttf", 45)
schrift = pygame.font.SysFont("monogram", 40, False, False)
tacho_schrift = pygame.font.Font("Texturen/fonts/7Segment/dseg7-regular-normal.ttf", 45)
rundenzeit_schrift = pygame.font.Font("Texturen/fonts/monogram/monogram.ttf", 60)
monogram_gross = pygame.font.Font("Texturen/fonts/monogram/monogram.ttf", 65)

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
    kachel_ebene = pygame.Surface((BREITE*8, HOEHE*4))

    for y in range(0, HOEHE + textur_hoehe *4 , textur_hoehe):
        for x in range(0, BREITE + textur_breite *8, textur_breite): #+100 um überzustehen 
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
     global BANDE_MASKE, ZIEL_LINIE_MASKE, BANDE, ZIEL_LINIE
     original_bande = pygame.image.load("Texturen/Bande.png")
     original_ziel = pygame.image.load("Texturen/Ziel_Linie.png")

     BANDE = bild_skalieren(original_bande, 0.9777 * zoom)
     ZIEL_LINIE = bild_skalieren(original_ziel, zoom)
     
     BANDE_MASKE = pygame.mask.from_surface(BANDE)
     ZIEL_LINIE_MASKE = pygame.mask.from_surface(ZIEL_LINIE)

def WEG_zoom(weg , zoom): 
     return[(int(x * zoom), int(y * zoom)) for x,y in weg]

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
    kmh = abs(int(spieler_auto.v * 12))
    text = monogram.render(f"{kmh} km/h", True, menü_grün)    
    gui.blit(text, (pos_x - text.get_width() // 2, pos_y - text.get_height() // 2))

##############
# Konstanten 
##############

zoom = 1

STRECKE = bild_skalieren(pygame.image.load("Texturen/Strecke.png"), 0.85)
BREITE, HOEHE = STRECKE.get_width(), STRECKE.get_height() ## Weil Spielfenster von Strecke ausgefüllt werden soll wegen circular import doppelt

BANDE = bild_skalieren(pygame.image.load("Texturen/Bande.png"), 0.9777 * zoom) #füroriginal 1.84
BANDE_MASKE = pygame.mask.from_surface(BANDE)

ZIEL_LINIE = bild_skalieren(pygame.image.load("Texturen/Ziel_Linie.png"), 1 * zoom) #Bande muss Linie Übermalen

ZIEL_POS = (60,400)
START_POS = (370, 960) #(auto)

ziel_pos_skaliert = (ZIEL_POS[0]* zoom, ZIEL_POS[1] * zoom)
ZIEL_LINIE_MASKE = pygame.mask.from_surface(ZIEL_LINIE)

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
          self.original_bild = pygame.image.load(self.AUTOBILD_PFAD)
          self.skaliere_auto(zoom)
          self.basis_max_v = max_v #basis v und rot_v vor zoom
          self.basis_rotations_v = rotations_v
          self.basis_beschleunigung = 0.3
          self.aktualisiere_geschwindigkeit(zoom)
          self.v = 0
          self.winkel = 0
          self.x, self.y = self.START_POS
          

     def aktualisiere_geschwindigkeit(self, zoom_faktor):
          self.max_v = self.basis_max_v # optimierter als  self.max_v = self.basis_max_v / zoom_faktor 
          self.rotations_v = self.basis_rotations_v #besser als self.rotations_v = self.basis_rotations_v / zoom_faktor
          self.beschleunigung = self.basis_beschleunigung

          self.bewegungs_faktor = 1 / zoom_faktor if zoom_faktor > 1 else 1 # skalierter gesschw.faktor für zoom
          #if hasattr(self, 'v'): #debugging geschwindigkeitsanpassugn
          #  self.v = self.v / zoom_faktor

     def skaliere_auto(self, zoom_faktor):
        self.bild = bild_skalieren(self.original_bild, self.SKALIERUNG * zoom_faktor)

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
          vertikale = math.cos(radianten) * self.v * self.bewegungs_faktor 
          horizontale = math.sin(radianten) * self.v * self.bewegungs_faktor

          self.y -= vertikale #Wegen Winkel muss subtrahiert werden
          self.x -= horizontale
     
     def reibung(self):
          self.v = max(self.v - self.beschleunigung / 1.001, 0)
          self.bewegen()

     def kollidieren(self, maske, x=0, y=0):
          auto_maske = pygame.mask.from_surface(self.bild)
          offset = (int(self.x - x), int(self.y - y))

          if maske is None: #debugging für maske und zoom
               print("Warnung: Maske ist None")
               return None
        
          try:
               schnittP = maske.overlap(auto_maske, offset) #= schnittpunkt
               return schnittP
          
          except Exception as e:
               print(f"Fehler bei Kollisionserkennung: {e}")
               return None


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
          self.slider_zoom = self.Slider(BREITE // 2 - 150, 500, 300, 1, 3, self.zoom)
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
            pygame.draw.rect(gui, menü_grün, self.rect)  
            pygame.draw.rect(gui, creme, self.knopf)  

        def events(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN and self.knopf.collidepoint(event.pos):
                self.bewegen = True

            elif event.type == pygame.MOUSEBUTTONUP:
                self.bewegen = False

            elif event.type == pygame.MOUSEMOTION and hasattr(self, 'bewegen') and self.bewegen: # hasattr = hat das attribut sich zu bewegen
                self.knopf.centerx = max(self.rect.left, min(event.pos[0], self.rect.right))
                self.wert = self.min_wert + (self.knopf.centerx - self.rect.left) / self.breite * (self.max_wert - self.min_wert)


     def speichere_highscore(self,zeit):
          highscores = Allg.lade_highscores()
          highscores.append(zeit)
          highscores.sort()
          highscores = highscores[:5]
          with open("highscores.txt", "w") as file:
               for score in highscores:
                    file.write(f"{score:.2f}\n")

     def lade_highscores():
          highscores = []
          # Wenn die Datei existiert, lade die Zeiten
          if os.path.exists("highscores.txt"):
               with open("highscores.txt", "r") as file:
                    for line in file:
                         highscores.append(float(line.strip()))
          return highscores
 
     def zeige_highscores(self, gui):
          highscores = Allg.lade_highscores()
          y_pos = 50
          titel = monogram_gross.render("TOP 5 RUNDENZEITEN", True, menü_grün)
          gui.blit(titel, (BREITE // 2 - titel.get_width() // 2, y_pos))
          
          for i, score in enumerate(highscores, 1):
               y_pos += 50
               text = monogram.render(f"{i}. {score:.2f} Sekunden", True, menü_grün)
               gui.blit(text, (BREITE // 2 - text.get_width() // 2, y_pos))


class GameProcessor: # klasse für multiprocessing
    # Siehe https://docs.python.org/3/library/multiprocessing.html & https://docs.python.org/3/library/concurrent.futures.html 
    
     def __init__(self):
        self.pool = None #debugging und errorhandling
        
     def init_pool(self):
        try:
            self.pool = concurrent.futures.ProcessPoolExecutor(
                max_workers=multiprocessing.cpu_count()
            )
        except Exception as e:
            print(f"fehler beim initialisieren von porcess pool: {e}")
            self.pool = None


     def process_physics(self, spieler_auto, gegner_auto, bilder_s):
        futures = []
        
        futures.append(self.pool.submit( #spieler
            self.update_player_physics, 
            spieler_auto.x, spieler_auto.y, 
            spieler_auto.v, spieler_auto.winkel
        ))
        
        futures.append(self.pool.submit( # gegner
            self.update_opponent_physics,
            gegner_auto.x, gegner_auto.y,
            gegner_auto.v, gegner_auto.winkel
        ))
        
        results = [f.result() for f in futures] #auf ergebnisse warten
        return results


     @staticmethod #dekorateur (siehe /Dokumente/Erkenntnisse & Wissenswertes.txt)
     def update_player_physics(x, y, v, winkel): #berechnungen für spielrer
        radianten = math.radians(winkel)
        vertikale = math.cos(radianten) * v
        horizontale = math.sin(radianten) * v
        return x - horizontale, y - vertikale


     @staticmethod #dekorateur 
     def update_opponent_physics(x, y, v, winkel): #berechnungen für gegner
        radianten = math.radians(winkel)
        vertikale = math.cos(radianten) * v
        horizontale = math.sin(radianten) * v
        return x - horizontale, y - vertikale