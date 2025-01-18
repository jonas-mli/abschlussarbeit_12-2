##########################################
# Informatik Abschlussarbeit KGS Turismo
##########################################

################
# Bibliotheken
################

import pygame
import time
import os 
from sound import *
from funktionen import * 

###########################################
# Fenster & Texturen als Konstanten laden
###########################################
# Texturenpfade als Konstanten definieren (CAPS weil Konstante)
# Bei Bedarf mit Funktion bild_skalieren(bild, wert) skalieren 
pygame.display.set_caption("KGS Turismo - Hauptmenü") # Gibt den Spielfenstertitel an
pygame.display.set_icon(ICON)

BREITE, HOEHE = STRECKE.get_width(), STRECKE.get_height() 
GUI = pygame.display.set_mode((BREITE, HOEHE)) #Spielfenster
#pygame.display.set_mode((BREITE, HOEHE), pygame.RESIZABLE| pygame.NOFRAME)
GRAS = textur_kacheln(GUI,pygame.image.load("Texturen/Gras.jpg")) #Muss gier definiert werden, weil von GUI abhängig
START_POS = (370, 960) #(auto)

bilder = [(GRAS, (-1000, -300)), 
          (STRECKE, (0, 0)),
          (ZIEL_LINIE, (ZIEL_POS[0], ZIEL_POS[1])),
          (BANDE, (0, 0))] #Liste mit Hintergrundobjekten 



zoom_skalieren(bilder, zoom) #Neue Liste heisst bilder_s

print(bilder_s)



##########################
# Autoklassen definieren
##########################

def zei(gui, bilder_s, spieler_auto): #Zei = Kurzform für Zeichnen (ebene, bilderliste, spielerauto)
     for bild, pos in bilder_s:
          n_pos = [pos[p] + kam_offs[p] for p in range(2)] #neue position
          gui.blit(bild, n_pos)
     spieler_auto.zei(gui)
     gegner_auto.zei(gui)

     rundenzeit_text = monogram.render(f"Rundenzeit: {rundenzeit /1000:.2f}", 1, weiss)
     GUI.blit(rundenzeit_text, (600, HOEHE - rundenzeit_text.get_height()) )

     pygame.display.update() # Aktualisiert Bildschirm


class SpielerAuto(AbstraktAuto): #Attribute für Spielerauto
     AUTOBILD = PORSCHE 
     START_POS = START_POS
     def __init__(self,max_v,rotations_v):
          #self.start_offset_x = 0 # Ist wie START_POS (benötigt da während Programmierung der Kameraperspektive Probleme auftraten)
          #self.start_offset_y = 0 #
          super().__init__(max_v, rotations_v)
          self.motor_sound = sfx["s.car_engine"]
          self.motor_sound.set_volume(0.5)
          self.moving = False
     
     def zei(self, gui):
          blit_rotieren(gui, self.bild, (self.x + kam_offs[0], self.y + kam_offs[1]), self.winkel)
  
     def vorwaerts_bewegen(self):
          if not pygame.mixer.Channel(0).get_busy():
            pygame.mixer.Channel(0).play(self.motor_sound)
          super().vorwaerts_bewegen()
#     def timer(self):
#          self.gestartet = True 
#          self.zeit = time.time()
  
#     def rundenzeit(self):
#          if not self.gestartet:
#               return 0
#          return self.zeit - time.time()


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
               punkte_neu = (p[0]+ kam_offs_x, )
               pygame.draw.circle(fenster, rot, p, 5) #(fenster,farbe,koordinaten/mitte, radius)

     def zei(self, gui):
          super().zei(gui)
          self.zei_wp(gui)
 
#############
# Hauptmenü 
#############

menu_musik = "menu.musik1"
spiel_musik = "m.short_chiptune_loop"

def hauptmenu():
     BUTTON_BREITE = 250
     BUTTON_HOEHE = 80
     m_aktiv = True
     pygame.display.set_caption("KGS Turismo - Hauptmenü")

     text1 = monogram.render("Spiel starten", True, (schwarz))
     text2 = monogram.render("Spiel beenden", True, (schwarz))

     button_start_rect = pygame.Rect(BREITE // 2 - (BUTTON_BREITE + 30) // 2, (HOEHE + 20) // 2 + 80, BUTTON_BREITE + 40, BUTTON_HOEHE + 30) #(pos x, posy, breite, Hoehe)
     button_stop_rect = pygame.Rect(BREITE // 2 - (BUTTON_BREITE + 300) // 2, HOEHE // 2 + 245, BUTTON_BREITE +300, BUTTON_HOEHE)
     button_e_rect = pygame.Rect(48 ,690, 100, 100)
     button_anleitung_rect = pygame.Rect(1320, 510, 300, 300)

     musik_spielen(menu_musik)

     while m_aktiv:
          clock.tick(FPS)
          #GUI.fill(dunkelblau)
          GUI.blit(HINTERGRUND_HAUPTMENU, (0, -90))

          mouse_pos = pygame.mouse.get_pos()
          
          if button_start_rect.collidepoint(mouse_pos) or button_stop_rect.collidepoint(mouse_pos) or button_e_rect.collidepoint(mouse_pos) or button_anleitung_rect.collidepoint(mouse_pos):
               pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

          else:
               pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

#          pygame.draw.rect(GUI, weiss, button_start_rect)
#          pygame.draw.rect(GUI, weiss, button_stop_rect)
#          pygame.draw.rect(GUI, weiss, button_e_rect)
#          pygame.draw.rect(GUI,weiss,button_anleitung_rect)

          #GUI.blit(text1, (button_start_rect.x + button_start_rect.width // 2 - text1.get_width() // 2, button_start_rect.y + button_start_rect.height // 2 - text1.get_height() // 2))
          #GUI.blit(text2, (button_stop_rect.x + (button_stop_rect.width // 2) - text2.get_width() // 2, button_stop_rect.y + button_stop_rect.height // 2 - text2.get_height() // 2))
          
          pygame.display.update()

          for event in pygame.event.get():
               if event.type == pygame.QUIT:  #fenster schließen
                    pygame.quit()
                    quit()

               if event.type == pygame.MOUSEBUTTONDOWN:  
                       
                    if button_start_rect.collidepoint(mouse_pos):
                         sfx_spielen("s.klick")
                         musik_spielen(spiel_musik)  
                         m_aktiv = False  
                         GUI.fill(weiss)

                    if button_e_rect.collidepoint(mouse_pos):
                         sfx_spielen("s.klick")
                         menu = e_menu(hauptmenu)
                         if menu:
                               menu()
                               return 
                                             
                    if button_stop_rect.collidepoint(mouse_pos):
                         sfx_spielen("s.klick")  
                         pygame.quit()
                         quit()


############
#Pausenmenü
############



def pause_menu():
     BUTTON_BREITE = 250
     BUTTON_HOEHE = 80
     pausiert = True
     pygame.display.set_caption("KGS Turismo - Pausemenü")

     text_weiter = schrift.render("Weiter", True, (0, 0, 0))
     text_hauptmenu = schrift.render("Hauptmenü", True, (0, 0, 0))
    


     button_weiter_rect = pygame.Rect(BREITE // 2 - (BUTTON_BREITE + 80) // 2, (HOEHE) // 2 + 80, BUTTON_BREITE + 80, BUTTON_HOEHE + 30) #(pos x, posy, breite, Hoehe)
     button_hauptmenu_rect = pygame.Rect(BREITE // 2 - (BUTTON_BREITE + 300) // 2, HOEHE // 2 + 235, BUTTON_BREITE +300, BUTTON_HOEHE +10)
     button_e_rect = pygame.Rect(48 ,690, 100, 100)
     button_anleitung_rect = pygame.Rect(1320, 510, 300, 300)

     musik_spielen(menu_musik)

     while True:
          clock.tick(FPS)
          GUI.blit(HINTERGRUND_PAUSENMENU, (0,-90))

          mouse_pos = pygame.mouse.get_pos()
          
          if button_weiter_rect.collidepoint(mouse_pos) or button_hauptmenu_rect.collidepoint(mouse_pos) or button_e_rect.collidepoint(mouse_pos) or button_anleitung_rect.collidepoint(mouse_pos):
               pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

          else:
               pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

 #         pygame.draw.rect(GUI, weiss, button_weiter_rect)
#          pygame.draw.rect(GUI, weiss, button_hauptmenu_rect)
          
          #GUI.blit(text_weiter, (button_weiter_rect.x + button_weiter_rect.width // 2 - text_weiter.get_width() // 2, button_weiter_rect.y + button_weiter_rect.height // 2 - text_weiter.get_height() // 2))
          #GUI.blit(text_hauptmenu, (button_hauptmenu_rect.x + button_hauptmenu_rect.width // 2 - text_hauptmenu.get_width() // 2, button_hauptmenu_rect.y + button_hauptmenu_rect.height // 2 - text_hauptmenu.get_height() // 2))
          
          pygame.display.update()

          for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                         pygame.quit()
                         quit()
                    
                    if event.type == pygame.MOUSEBUTTONDOWN:
                         mouse_pos = pygame.mouse.get_pos()
                         if button_weiter_rect.collidepoint(mouse_pos):
                              sfx_spielen("s.klick")
                              musik_spielen(spiel_musik)
                              GUI.fill(weiss)
                              return True  
                         
                         if button_e_rect.collidepoint(mouse_pos):
                              sfx_spielen("s.klick")
                              menu = e_menu(pause_menu)
                              if menu:
                                   menu()
                                   return
                     
                         if button_hauptmenu_rect.collidepoint(mouse_pos):
                              sfx_spielen("s.klick")
                              hauptmenu()  
                              return False  
     
#####################
# Einstellungsmenü
#####################

def e_menu(menu):
     global zoom # Weil global definiert statt in Funktion
     m_iteration = 0

     BUTTON_BREITE = 300
     BUTTON_HOEHE = 50
     e_aktiv = True

     button_zurueck_rect = pygame.Rect(48 ,690, 100, 100)
     button_musik_zurueck_rect = pygame.Rect(1340, 670, 100, 100)
     button_musik_vor_rect = pygame.Rect(1470, 670, 100, 100)

     pygame.display.set_caption("KGS Turismo - Einstellungen")

     while e_aktiv == True:
          clock.tick(FPS)
          GUI.blit(HINTERGRUND_EINSTELLUNGSMENU,(0, -90))
          allg.slider_zoom.zei(GUI)
          allg.slider_lautstaerke.zei(GUI)

          text_zoom = monogram.render(f"{allg.slider_zoom.wert:.1f}", True, weiss)
          GUI.blit(text_zoom, (BREITE // 2 - text_zoom.get_width() // 2,520 ))
          allg.zoom = allg.slider_zoom.wert

          text_lautstaerke = schrift.render(f"{int(allg.slider_lautstaerke.wert * 100)}%", True, weiss)
          GUI.blit(text_lautstaerke, (BREITE // 2 - text_lautstaerke.get_width() // 2, 720))
          pygame.mixer.music.set_volume(allg.slider_lautstaerke.wert)

#          pygame.draw.rect(GUI, weiss, button_musik_vor_rect)
#          pygame.draw.rect(GUI, schwarz, button_musik_zurueck_rect)

          mouse_pos = pygame.mouse.get_pos()
          
          if button_zurueck_rect.collidepoint(mouse_pos) or button_musik_zurueck_rect.collidepoint(mouse_pos) or button_musik_vor_rect.collidepoint(mouse_pos):
               pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

          else:
               pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

          pygame.display.update()

          for event in pygame.event.get():
               if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
         
               elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                         e_aktiv = False
                    elif event.key == pygame.K_PLUS:  
                         allg.slider_zoom.wert += 1
                         aktualisiere_masken()
                    
                    elif event.key == pygame.K_MINUS:  
                         allg.slider_zoom.wert -= 1
                         aktualisiere_masken()

               elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button_zurueck_rect.collidepoint(mouse_pos): 
                         sfx_spielen("s.klick")
                         e_aktiv = False
                         return menu   

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                         e_aktiv = False
                         return menu
                    
                    if button_musik_zurueck_rect.collidepoint(mouse_pos):
                        sfx_spielen("s.klick")
                        m_iteration = (m_iteration - 1) % len(musik_liste) 
                        musik_spielen(musik_liste[m_iteration])

                    if button_musik_vor_rect.collidepoint(mouse_pos):
                         sfx_spielen("s.klick")
                         m_iteration = (m_iteration + 1) % len(musik_liste) 
                         musik_spielen(musik_liste[m_iteration])                                
                    
               allg.slider_zoom.events(event)
               allg.slider_lautstaerke.events(event) 

##############
# Spiel-loop
##############

FPS = 60
allg = Allg()
spieler_auto = SpielerAuto(26,8) # Spielerauto(Max_Geschwindigkeit, Max_Rotationsgeschwindigkeit)
gegner_auto = Gegner(6, 4)
aktiv = True 
pausiert = False
clock = pygame.time.Clock() #Zum Regeln der Spielgeschwindigkeit

hauptmenu()

GUI.fill(weiss)
pygame.display.update()

musik_spielen(spiel_musik)

kam_offs_x = -(spieler_auto.x - (BREITE // 2))
kam_offs_y = -(spieler_auto.y - (HOEHE // 2))
kam_offs = (kam_offs_x, kam_offs_y) 

aktualisiere_masken()

while aktiv:   
     if not pausiert: #aktives spiel   
          clock.tick(FPS)  # Clock begrenzt den Loop auf fps anzahl
          zeit_aktuell = pygame.time.get_ticks() # misst aktuelle Zeit
          rundenzeit = (zeit_aktuell - allg.rundenstart) - allg.pausenzeit 
          pygame.display.set_caption("KGS Turismo - Spiel")

          
          kam_offs_x = -(spieler_auto.x - (BREITE // 2)) #Kamera offset von x
          kam_offs_y = -(spieler_auto.y - (HOEHE // 2))
          kam_offs = (kam_offs_x, kam_offs_y)

          #print(f"X:{spieler_auto.x}, Y:{spieler_auto.y}")

          auto_maske = pygame.mask.from_surface(spieler_auto.bild)
          

          zei(GUI, bilder_s, spieler_auto) # Zeichne(GUI, bilder, auto,)
          tacho(GUI, BREITE - 100, HOEHE - 20, spieler_auto)
          pygame.display.update()

          for event in pygame.event.get():
               if event.type == pygame.QUIT:
                    aktiv = False
                    break
               
               if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    gegner_auto.weg.append(pos)

               if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                         pausiert = True
          
          spieler_bewegen(spieler_auto)
          
          if spieler_auto.kollidieren(BANDE_MASKE) != None:
               spieler_auto.rueckstoss()

          
          ziel_schnittP = spieler_auto.kollidieren(ZIEL_LINIE_MASKE, *ZIEL_POS)
          if ziel_schnittP != None: #* spaltet Tupel in 2 individuelle Koordinaten also (ZIEL_LINIE_MASKE,x,y)
               rundenzeit_text = monogram.render(f"{rundenzeit /1000:.2f}", True, rot)
               GUI.blit(rundenzeit_text, (BREITE // 2 - rundenzeit_text.get_width() // 2, HOEHE // 2))
               pygame.display.update()
               pygame.time.delay(3000)
               allg.rundenstart = pygame.time.get_ticks()
               allg.pausenzeit = 0
               print(ziel_schnittP)
               if ziel_schnittP[1] == 0:
                    spieler_auto.rueckstoss()
               else:
                    spieler_auto.ziel()
                    
     else: #pause situation
          if allg.pausenstart == 0:
               allg.pausenstart = pygame.time.get_ticks()
          else:
               allg.pausenzeit += pygame.time.get_ticks() - allg.pausenstart 
               allg.pausenstart = 0
          fortsetzen = pause_menu()
          if fortsetzen: 
               pausiert = False               
          
          else:
               pausiert = False

print(gegner_auto.weg)     
pygame.quit()