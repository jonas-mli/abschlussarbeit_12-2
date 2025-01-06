##########################################
# Informatik Abschlussarbeit KGS Turismo
# Stand: 29.12.2024 13:51 Uhr
##########################################

################
# Bibliotheken
################

import pygame
from sound import *
from funktionen import * 

###########################################
# Fenster & Texturen als Konstanten laden
###########################################
# Texturenpfade als Konstanten definieren (CAPS weil Konstante)
# Bei Bedarf mit Funktion bild_skalieren(bild, wert) skalieren 

BREITE, HOEHE = STRECKE.get_width(), STRECKE.get_height() # Weil Spielfenster von Strecke ausgefüllt werden soll 
GUI = pygame.display.set_mode((BREITE, HOEHE)) #Spielfenster
GRAS = textur_kacheln(GUI,pygame.image.load("Texturen/Gras.jpg")) #Muss gier definiert werden, weil von GUI abhängig



bilder = [(GRAS, (-10 + OFFSET_X, -30 + OFFSET_Y)), 
          (STRECKE, (0 + OFFSET_X, 0 + OFFSET_Y)),
          (ZIEL_LINIE, (ZIEL_POS[0] + OFFSET_X, ZIEL_POS[1] + OFFSET_Y)),
          (BANDE, (0 + OFFSET_X, 0 + OFFSET_Y))] #Liste mit Hintergrundobjekten 

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("KGS Turismo - Hauptmenü") # Gibt den Spielfenstertitel an

##########################
# Autoklassen definieren
##########################

def zei(gui, bilder, spieler_auto): #Zei = Kurzform für Zeichnen (ebene, bilderliste, spielerauto)
     for x, pos in bilder:
          n_pos = [pos[p] + kam_offs[p] for p in range(2)] #neue position
          gui.blit(x, n_pos)
     spieler_auto.zei(gui)
     pygame.display.update() # Aktualisiert Bildschirm


class SpielerAuto(AbstraktAuto): #Attribute für Spielerauto
     AUTOBILD = PORSCHE
     START_POS = (0 , 0)
     
     def __init__(self,max_v,rotations_v):
          self.start_offset_x = 0 # Ist wie START_POS (benötigt da während Programmierung der Kameraperspektive Probleme auftraten)
          self.start_offset_y = 0 #
          super().__init__(max_v, rotations_v)


class Gegner(AbstraktAuto):
     AUTOBILD = FERRARI
     START_POS = (10, 180)

     def __init__(self, max_v, rotations_v, weg=[]):
          super().__init__(max_v, rotations_v) #Nutzt Eigenschaften von __init__ von der Abstrakten Autoklasse
          self.weg = weg
          self.wp = 0 #wp = Wegpunkt
          self.v = max_v
          

     def zei_wp(self, fenster):
          for p in self.weg:
               pygame.draw.circle(fenster, rot, p, 5) #(fenster,farbe,koordinaten/mitte, radius)

     
#############
# Hauptmenü 
#############

menu_musik = "m.chilly"
spiel_musik = "m.short_chiptune_loop"

def hauptmenu():
     BUTTON_BREITE = 250
     BUTTON_HOEHE = 50
     m_aktiv = True
     pygame.display.set_caption("KGS Turismo - Hauptmenü")

     text1 = schrift.render("Spiel starten", True, (schwarz))
     text2 = schrift.render("Spiel beenden", True, (schwarz))

     button_start_rect = pygame.Rect(BREITE // 2 - BUTTON_BREITE // 2, HOEHE // 2 - 60, BUTTON_BREITE, BUTTON_HOEHE)
     button_stop_rect = pygame.Rect(BREITE // 2 - BUTTON_BREITE // 2, HOEHE // 2 + 20, BUTTON_BREITE, BUTTON_HOEHE)

     musik_spielen(menu_musik)

     while m_aktiv:
          clock.tick(FPS)
          #GUI.fill(dunkelblau)
          GUI.blit(HINTERGRUND_HAUPTMENU,(0,-75))


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
#Pausenmenü
############

schrift = pygame.font.SysFont("Arial", 40, False, False)

def pause_menu():
    BUTTON_BREITE = 250
    BUTTON_HOEHE = 50
    pausiert = True
    pygame.display.set_caption("KGS Turismo - Pausemenü")
    
    text_weiter = schrift.render("Weiter", True, (0, 0, 0))
    text_hauptmenu = schrift.render("Hauptmenü", True, (0, 0, 0))
    


    button_weiter_rect = pygame.Rect(BREITE // 2 - BUTTON_BREITE // 2, HOEHE // 2 - 60, BUTTON_BREITE, BUTTON_HOEHE)
    button_hauptmenu_rect = pygame.Rect(BREITE // 2 - BUTTON_BREITE // 2, HOEHE // 2 + 20, BUTTON_BREITE, BUTTON_HOEHE)

    musik_spielen(menu_musik)

    while True:
          clock.tick(FPS)
          GUI.blit(HINTERGRUND_PAUSENMENU, (0,-75))

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
spieler_auto = SpielerAuto(4,4) # Spielerauto(Max_Geschwindigkeit, Max_Rotationsgeschwindigkeit)
aktiv = True 
pausiert = False
clock = pygame.time.Clock() #Zum Regeln der Spielgeschwindigkeit

hauptmenu()

GUI.fill(weiss)
pygame.display.update()

musik_spielen(spiel_musik)

kam_offs_x = 0 #Kamera offset von x
kam_offs_y = 0 #Kamera offset von y 

while aktiv:   
     if not pausiert: #aktives spiel   
          clock.tick(FPS)  # Clock begrenzt den Loop
          pygame.display.set_caption("KGS Turismo - Spiel")

          
          kam_offs_x = -(spieler_auto.x - (BREITE // 2)) #Kamera offset von x
          kam_offs_y = -(spieler_auto.y - (HOEHE // 2))
          kam_offs = (kam_offs_x, kam_offs_y)

          #print(f"X:{spieler_auto.x}, Y:{spieler_auto.y}")

          zei(GUI, bilder, spieler_auto) # Zeichne(GUI, bilder, auto,)
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

          if spieler_auto.kollidieren(BANDE_MASKE) != None:
               spieler_auto.rueckstoss()

          if spieler_auto.kollidieren(ZIEL_LINIE_MASKE, *ZIEL_POS) != None: #* spaltet Tupel in 2 individuelle Koordinaten also (ZIEL_LINIE_MASKE,x,y)
               print("finnisches Ziel")
     
     else: #pause situation
          fortsetzen = pause_menu()
          if fortsetzen: 
               pausiert = False
          
          else:
               spieler_auto = SpielerAuto(4, 3)
               pausiert = False
     
pygame.quit()