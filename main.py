##########################################
# Informatik Abschlussarbeit KGS Turismo
# Stand: 14.12.2024 23:12 Uhr
##########################################

################
# Bibliotheken
################

import math 
import pygame
from sound import *
from werkzeuge import *

##########
# Farben
##########

schwarz = 0, 0, 0
weiss = 255, 255, 255
dunkelgrau = 30, 30, 30
rot = 200, 0, 0
dunkelblau = 0, 30, 80

############################
# Fenster & Texturen laden 
############################

# Texturenpfade als Konstanten definieren (CAPS weil Konstante)
# Bei Bedarf mit Funktion bild_skalieren(bild, wert) skalieren 


STRECKE = bild_skalieren(pygame.image.load("Texturen/Strecke.png"), 0.85)
#STRECKEN_GRENZE = bild_skalieren(pygame.image.load("Texturen/Strecken_Grenze.png"), .95)
#STRECKEN_GRENZE_MASKE = pygame.mask.from_surface(STRECKEN_GRENZE)
ZIEL_LINIE = pygame.image.load("Texturen/Ziel_Linie.png")
FERRARI = bild_skalieren(pygame.image.load("Texturen/Ferrari.png"), 0.05)
PORSCHE = pygame.image.load("Texturen/Porsche.png")
BREITE, HOEHE = STRECKE.get_width(), STRECKE.get_height() # Weil Spielfenster von Strecke ausgefüllt werden soll 
GUI = pygame.display.set_mode((BREITE, HOEHE)) #Spielfenster
GRAS = textur_kacheln(GUI,pygame.image.load("Texturen/Gras.jpg"))

bilder = [(GRAS, (-10, -30)), (STRECKE, (0, 0))]

pygame.init()
#pygame.mixer.init()

pygame.display.set_caption("KGS Turismo - Hauptmenü") # Gibt den Spielfenstertitel an

##################
# Autos zeichnen
##################

def zei(gui, bilder, spieler_auto, ziel_linie): #Zei = Kurzform für Zeichnen
     for x, pos in bilder:
          gui.blit(x, pos)
     spieler_auto.zei(gui)
     gui.blit(ziel_linie, (10, 200))
     pygame.display.update() # Aktualisiert Bildschirm
        

class SpielerAuto(AbstractCar): #Attribute für Spielerauto
     AUTOBILD = FERRARI
     START_POS = (40, 120)

     
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
    #hintergrund_f = (dunkelgrau)            
    #rahmen_f = (rot)         
    #radius = 60

    text_f = (weiss)
    kmh = abs(int(spieler_auto.v * 20))
    schrift = pygame.font.SysFont("Arial", 24, True)
    text = schrift.render(f"{kmh} km/h", True, text_f)

    #pygame.draw.circle(gui, hintergrund_f, (pos_x, pos_y), radius)  
    #pygame.draw.circle(gui, rahmen_f, (pos_x, pos_y), radius, 4)       
    gui.blit(text, (pos_x - text.get_width() // 2, pos_y - text.get_height() // 2))


#############
# Hauptmenü 
#############

menu_musik = "m.chilly"
spiel_musik = "m.short_chiptune_loop"

def hauptmenu():
     m_aktiv = True 
     text1 = schrift.render("Spiel starten", True, (schwarz))
     text2 = schrift.render("Spiel beenden", True, (schwarz))

     BUTTON_BREITE = 250
     BUTTON_HOEHE = 50

     button_start_rect = pygame.Rect(BREITE // 2 - BUTTON_BREITE // 2, HOEHE // 2 - 60, BUTTON_BREITE, BUTTON_HOEHE)
     button_stop_rect = pygame.Rect(BREITE // 2 - BUTTON_BREITE // 2, HOEHE // 2 + 20, BUTTON_BREITE, BUTTON_HOEHE)

     musik_spielen(menu_musik)

     while m_aktiv:
          clock.tick(FPS)
          #GUI.fill(dunkelblau)
          grau_farbverlauf(GUI, BREITE, HOEHE)

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
                         musik_spielen(spiel_musik)  
                         m_aktiv = False  
                    
                    if button_stop_rect.collidepoint(mouse_pos):  
                         pygame.quit()
                         quit()


############
#Pausemenü
############

schrift = pygame.font.SysFont("Arial", 40, False, False)

def pause_menu():
    pausiert = True
    
    text_weiter = schrift.render("Weiter", True, (0, 0, 0))
    text_hauptmenu = schrift.render("Hauptmenü", True, (0, 0, 0))
    
    BUTTON_BREITE = 250
    BUTTON_HOEHE = 50

    button_weiter_rect = pygame.Rect(BREITE // 2 - BUTTON_BREITE // 2, HOEHE // 2 - 60, BUTTON_BREITE, BUTTON_HOEHE)
    button_hauptmenu_rect = pygame.Rect(BREITE // 2 - BUTTON_BREITE // 2, HOEHE // 2 + 20, BUTTON_BREITE, BUTTON_HOEHE)

    musik_spielen(menu_musik)

    while True:
          clock.tick(FPS)
          grau_farbverlauf(GUI, BREITE, HOEHE)

          pygame.draw.rect(GUI, weiss, button_weiter_rect)
          pygame.draw.rect(GUI, weiss, button_hauptmenu_rect)
          
          GUI.blit(text_weiter, (button_weiter_rect.x + button_weiter_rect.width // 2 - text_weiter.get_width() // 2, button_weiter_rect.y + button_weiter_rect.height // 2 - text_weiter.get_height() // 2))
          GUI.blit(text_hauptmenu, (button_hauptmenu_rect.x + button_hauptmenu_rect.width // 2 - text_hauptmenu.get_width() // 2, button_hauptmenu_rect.y + button_hauptmenu_rect.height // 2 - text_hauptmenu.get_height() // 2))
          
          pygame.display.update()

          for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                         pygame.quit()
                         quit()
                    
                    if event.type == pygame.MOUSEBUTTONDOWN:
                         mouse_pos = pygame.mouse.get_pos()
                         if button_weiter_rect.collidepoint(mouse_pos):
                              musik_spielen(spiel_musik)
                              return True  
                         
                         if button_hauptmenu_rect.collidepoint(mouse_pos):
                              hauptmenu()  
                              return False  
     

##############
# Spiel-loop
##############

FPS = 60
spieler_auto = SpielerAuto(4,3) # Spielerauto(Max_Geschwindigkeit, Max_Rotationsgeschwindigkeit)
aktiv = True 
pausiert = False
clock = pygame.time.Clock() #Zum Regeln der Spielgeschwindigkeit

pygame.display.set_caption("KGS Turismo - Spiel")
hauptmenu()

GUI.fill(weiss)
pygame.display.update()


musik_spielen(spiel_musik)

while aktiv:   
     if not pausiert:    
          clock.tick(FPS)  # Clock begrenzt den Loop

          zei(GUI, bilder, spieler_auto,ZIEL_LINIE) # Zeiche(GUI, bilder, auto, ziellinie)
          tacho(GUI, BREITE - 100, HOEHE - 20, spieler_auto)
          pygame.display.update()

          for event in pygame.event.get():
               if event.type == pygame.QUIT:
                    aktiv = False
                    break

               if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                         pausiert = True
          
          spieler_bewegen(spieler_auto)

#          if spieler_auto.kollidieren(STRECKEN_GRENZE_MASKE,) != None:
#          spieler_auto.rueckstoss()
     
     else: #pause situation
          fortsetzen = pause_menu()
          if fortsetzen: 
               pausiert = False
          
          else:
               spieler_auto = SpielerAuto(4, 3)
               pausiert = False
     

pygame.quit()