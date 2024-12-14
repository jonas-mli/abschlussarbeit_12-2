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
import pygame
from werkzeuge import bild_skalieren, blit_rotieren, textur_kacheln


##########
# Farben
##########

schwarz = 0, 0, 0
weiss = 255, 255, 255

############################
# Fenster & Texturen laden 
############################

# Texturenpfade als Konstanten definieren (CAPS weil Konstante)
# Bei Bedarf mit Funktion bild_skalieren(bild, wert) skalieren 


STRECKE = bild_skalieren(pygame.image.load("Texturen/Strecke.png"), 0.85)

#STRECKEN_GRENZE = pygame.image.load("Texturen/Strecken_Grenze.png")
#STRECKEN_GRENZE_MASKE = pygame.mask.from_surface(STRECKEN_GRENZE)
ZIEL_LINIE = pygame.image.load("Texturen/Ziel_Linie.png")

FERRARI = bild_skalieren(pygame.image.load("Texturen/Ferrari.png"), 0.05)
PORSCHE = pygame.image.load("Texturen/Porsche.png")

BREITE, HOEHE = STRECKE.get_width(), STRECKE.get_height() # Weil Spielfenster von Strecke ausgefüllt werden soll 
GUI = pygame.display.set_mode((BREITE, HOEHE)) #Spielfenster
GRAS = textur_kacheln(GUI,pygame.image.load("Texturen/Gras.jpg"))

bilder = [(GRAS, (-10, -30)), (STRECKE, (0, 0))]

pygame.init()
pygame.display.set_caption("KGS Turismo - Hauptmenü") # Gibt den Spielfenstertitel an

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

#     def kollidieren(self, maske, x=0, y=0):
#          auto_maske = pygame.mask.from_surface(self.img)
#          offset = (int(), int())
          

class SpielerAuto(AbstractCar): #Attribute für Spielerauto
     AUTOBILD = FERRARI
     START_POS = (40, 120)

     def reibung(self):
          self.v = max(self.v - self.beschleunigung / 1.2, 0)
          self.bewegen()

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


#############
# Hauptmenü
#############

schrift = pygame.font.SysFont("Arial", 40, False, False)



def hauptmenu():
     m_aktiv = True 
     text1 = schrift.render("Spiel starten", True, (schwarz))
     text2 = schrift.render("Spiel beenden", True, (schwarz))
     button_start_rect = pygame.Rect(BREITE // 2 - 100, HOEHE // 2 - 60, 200, 50) 
     button_stop_rect = pygame.Rect(BREITE // 2 - 100, HOEHE // 2 + 20, 200, 50)

     while m_aktiv:
          clock.tick(FPS)
          GUI.fill(schwarz)

          pygame.draw.rect(GUI, weiss, button_start_rect)
          pygame.draw.rect(GUI, weiss, button_stop_rect)
          GUI.blit(text1, (button_start_rect.x + button_start_rect.width // 2 - text1.get_width() // 2, button_start_rect.y + button_start_rect.height // 2 - text1.get_height() // 2))
          GUI.blit(text2, (button_stop_rect.x + (button_stop_rect.width // 2) - text2.get_width() // 2, button_stop_rect.y + button_stop_rect.height // 2 - text2.get_height() // 2))
          pygame.display.update()

          for event in pygame.event.get():
               if event.type == pygame.QUIT:  #fenster schließen
                    pygame.quit()
                    quit()

               if event.type == pygame.MOUSEBUTTONDOWN:  
                    mouse_pos = pygame.mouse.get_pos()   
                    if button_start_rect.collidepoint(mouse_pos):  
                         m_aktiv = False  
                    if button_stop_rect.collidepoint(mouse_pos):  
                         pygame.quit()
                         quit()


##############
# Spiel-loop
##############

FPS = 60
spieler_auto = SpielerAuto(4,3) # Spielerauto(Max_Geschwindigkeit, Max_Rotationsgeschwindigkeit)
aktiv = True 
clock = pygame.time.Clock() #Zum Regeln der Spielgeschwindigkeit

pygame.display.set_caption("KGS Turismo - Spiel")
hauptmenu()

GUI.fill(weiss)
pygame.display.update()

while aktiv: #Spielengine
     
     clock.tick(FPS)  # Clock begrenzt den Loop

     zei(GUI, bilder, spieler_auto)
     GUI.blit(ZIEL_LINIE, (10, 200))  # Fenster.maleBild(Textur, (Position))
     GUI.blit(FERRARI, (40, 120))
    
     for event in pygame.event.get():
          if event.type == pygame.QUIT:
            aktiv = False
            break
     
     spieler_bewegen(spieler_auto)


pygame.quit()