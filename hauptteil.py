##########################################
# Informatik Abschlussarbeit KGS Turismo
# Stand: 13.12.2024 21:08 Uhr
##########################################


#######################################################
# Quelle: https://www.youtube.com/watch?v=L3ktUWfAMPg
#######################################################


################
# Bibliotheken
################

import math 
import time
import pygame
from werkzeuge import bild_skalieren, blit_rotieren, textur_kacheln


############################
# Fenster & Texturen laden 
############################

# Texturenpfade als Konstanten definieren (CAPS weil Konstante)
# Bei Bedarf mit Funktion bild_skalieren(bild, wert) skalieren 

#GRAS = bild_skalieren(pygame.image.load("Texturen/Gras.jpg"), 0.85) 

STRECKE = bild_skalieren(pygame.image.load("Texturen/Strecke.png"), 0.85)

#STRECKEN_GRENZE = pygame.image.load("Texturen/Strecken_Grenze.png")
ZIEL_LINIE = pygame.image.load("Texturen/Ziel_Linie.png")

FERRARI = bild_skalieren(pygame.image.load("Texturen/Ferrari.png"), 0.05)
PORSCHE = pygame.image.load("Texturen/Porsche.png")

BREITE, HOEHE = STRECKE.get_width(), STRECKE.get_height() # Weil Spielfenster von Strecke ausgefüllt werden soll 
GUI = pygame.display.set_mode((BREITE, HOEHE)) #Spielfenster
GRAS = textur_kacheln(GUI,pygame.image.load("Texturen/Gras.jpg"))

bilder = [(GRAS, (-10, -30)), (STRECKE, (0, 0))]

pygame.display.set_caption("KGS Turismo - Hauptmenü") # Vielleicht KGS Rennspiel? / Gibt den Spielfenstertitel an

##################
# Autos zeichnen
##################

def zei(gui, bilder, spieler_auto): #Zei = Kurzform für Zeichnen
     for x, pos in bilder:
          gui.blit(x, pos)
     spieler_auto.zei(gui)
     pygame.display.update() # Aktualisiert Bildschirm


class AbstractCar: #Generell Auto Klasse (Namen muss geändert werden)      
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


class SpielerAuto(AbstractCar): #Attribute für Spielerauto
     AUTOBILD = FERRARI
     START_POS = (40, 120)

def spieler_bewegen(spielerauto):
     if taste[pygame.K_a]:
          spieler_auto.rotieren(links=True)
     if taste[pygame.K_d]:
          spieler_auto.rotieren(rechts=True)
     if taste[pygame.K_w]:
          spieler_auto.vorwaerts_bewegen()
     

##############
# Spiel-loop
##############

spieler_auto = SpielerAuto(8,5) # Spielerauto(Max_Geschwindigkeit, Max_Rotationsgeschwindigkeit)
aktiv = True 
clock = pygame.time.Clock() #Zum Regeln der Spielgeschwindigkeit
FPS = 60

while aktiv: #Spielengine
     clock.tick(FPS)  # Clock begrenzt den Loop

     zei(GUI, bilder, spieler_auto)
     GUI.blit(ZIEL_LINIE, (10, 200))  # Fenster.maleBild(Textur, (Position))
     GUI.blit(FERRARI, (40, 120))
    
     for event in pygame.event.get():
          if event.type == pygame.QUIT:
            aktiv = False
            break
     
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
            


pygame.quit()