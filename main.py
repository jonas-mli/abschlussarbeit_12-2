
##############################################
##############################################
### Informatik Abschlussarbeit KGS Turismo ###
##############################################
##############################################

#Vorwort:
# Diese Arbeit ist in mehrere Module Aufgeteilt. In dieser Hauptdatei befindet sich alles notwendige 
# für das Spiel (sozusagen der Ablauf). Das Modul funktionen beinhaltet dann alles möglichen Definitionen,
# um main.py ausführen zu können sowie dieses zu kürzen. Sound.py beeinhaltet 2 dicts für das importieren
#von Tönen. 

     ############################################################################################
    ############################################################################################
   ###   In /Dokumente/ befindet sich die Datei "Erkenntnisse 6 Wissenswertes.txt"!         ###
  ###   Diese hilft neue Konzepte, die ggf. im Code erhalten sind, besser zu verstehen!    ###                           #
 ############################################################################################
############################################################################################

##############################
# Modul funktionen einbinden
##############################

from funktionen import * 

def main(): #ganze Datei muss in main() sein (notwendig für multiprocess) 
#multiprocessing für windows, sonst funktioniert das spiel nicht
     global zoom, WEG_SKALIERT, bilder_s
     multiprocessing.freeze_support()

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
    
     
     bilder = [(GRAS, (-1900, -800)), 
               (STRECKE, (0, 0)),
               (ZIEL_LINIE, (ziel_pos_skaliert[0], ziel_pos_skaliert[1])),
               (BANDE, (0, 0))] #Liste mit Hintergrundobjekten 
     zoom_skalieren(bilder, zoom) #Neue Liste heisst bilder_s
     print(bilder_s)


##########################
# Autoklassen definieren
##########################

     def zei(gui, bilder_s, spieler_auto): #Zei = Kurzform für Zeichnen (ebene, bilderliste, spielerauto)
          for bild, pos in bilder_s:
               n_pos = [pos[p] + kam_offs[p] for p in range(2)] #neue position #n_pos = [pos[p] + kam_offs[p] for p in range(2)]
               gui.blit(bild,n_pos) #

#          kamera_rect = pygame.Rect(-BREITE, -HOEHE, BREITE *100, HOEHE*100)
#    
#          for bild, pos in bilder_s:
#               n_pos = [pos[p] + kam_offs[p] for p in range(2)]
#               bild_rect = bild.get_rect(topleft=n_pos)
               
#               if kamera_rect.colliderect(bild_rect):
#                    gui.blit(bild, n_pos)

          spieler_auto.zei(gui)
          gegner_auto.zei(gui)

          rundenzeit_text = monogram.render(f"Rundenzeit: {rundenzeit /1000:.2f}", 1, menü_grün)
          GUI.blit(rundenzeit_text, (600, HOEHE - rundenzeit_text.get_height()))

          pygame.display.update() # Aktualisiert Bildschirm


     class SpielerAuto(AbstraktAuto): #Attribute für Spielerauto
          AUTOBILD_PFAD = "Texturen/Porsche.png" 
          SKALIERUNG = 0.035
          START_POS = START_POS
          def __init__(self,max_v,rotations_v):
               #self.start_offset_x = 0 # Ist wie START_POS (benötigt da während Programmierung der Kameraperspektive Probleme auftraten)
               #self.start_offset_y = 0 #
               super().__init__(max_v, rotations_v)
               self.motor_sound = sfx["s.car_engine"]
               self.motor_sound.set_volume(0.5)
               self.moving = False
               
          
     #     def zei(self, gui):
     #          auto_skaliert = porsche
     #          auto_pos_skaliert = ((self.x - kam_offs[0]) * zoom, (self.y - kam_offs[1]) * zoom)
     #          blit_rotieren(gui, auto_skaliert, ((self.x + kam_offs[0]) * zoom, (self.y + kam_offs[1]) * zoom), self.winkel) #blit_rotieren(gui, self.bild, (self.x + kam_offs[0], self.y + kam_offs[1]), self.winkel)


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
          AUTOBILD_PFAD = "Texturen/Ferrari.png"
          SKALIERUNG = 0.03
          START_POS = (360, 400)

          def __init__(self, max_v, rotations_v, weg=[]):
               super().__init__(max_v, rotations_v) #Nutzt Eigenschaften von __init__ von der Abstrakten Autoklasse
               self.weg = weg
               self.wp = 0 #wp = Wegpunkt
               self.v = max_v
               

          def zei_wp(self, gui, weg, kam_offs):
     #          for p in self.weg:
     #               punkt_x = p[0] - kam_offs[0]
     #               punkt_y = p[1] - kam_offs[1]
     #               punkte_neu = (punkt_x, punkt_y)
     #               pygame.draw.circle(fenster, rot, p, 5) #(fenster,farbe,koordinaten/mitte, radius)
               for punkt in weg:
               # Wegpunkt relativ zur Kamera berechnen
                    punkt_relativ = (punkt[0] + kam_offs[0], punkt[1] + kam_offs[1])
                    # Nur zeichnen, wenn der Punkt im sichtbaren Bereich ist
     #               if 0 <= punkt_relativ[0] <= BREITE and 0 <= punkt_relativ[1] <= HOEHE:
                         #pygame.draw.circle(gui, (255, 0, 0), punkt_relativ, 5)

          def zei(self, gui):
     #          super().zei(gui)

               auto_pos_relativ = (self.x + kam_offs_x, self.y + kam_offs_y)
               blit_rotieren(gui, self.bild, auto_pos_relativ, self.winkel)

               self.zei_wp(gui, WEG_SKALIERT, kam_offs)
          
          def winkel_berechnen(self):
               naechster_p_x, naechster_p_y = self.weg[self.wp]
               x_diff = naechster_p_x - self.x
               y_diff = naechster_p_y - self.y

               if y_diff == 0: 
                    ziel_rad_winkel = math.pi/2 
               else: 
                    ziel_rad_winkel = math.atan(x_diff/y_diff)

               if naechster_p_y > self.y:
                    ziel_rad_winkel  += math.pi

               delta_winkel = self.winkel - math.degrees(ziel_rad_winkel)
               if delta_winkel >= 180:
                    delta_winkel -= 360
               
               if delta_winkel > 0:
                    self.winkel -= min(self.rotations_v, abs(delta_winkel))
               
               else: 
                    self.winkel += min(self.rotations_v, abs(delta_winkel))
                    
          def naechster_wegpunkt(self):
               ziel_p = self.weg[self.wp]
               rect = pygame.Rect(self.x, self.y, self.bild.get_width(), self.bild.get_height())
               
               if rect.collidepoint(*ziel_p):
                    self.wp += 1

          def bewegen(self):
               if self.wp >= len(self.weg):
                    return
               
               self.winkel_berechnen()
               self.naechster_wegpunkt()
               super().bewegen()
 
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

          #musik_spielen(menu_musik)

          if not pygame.mixer.music.get_busy() or pygame.mixer.music.get_pos() == -1: #Musik 
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
                              if not pygame.mixer.music.get_busy() or pygame.mixer.music.get_pos() == -1:
                                   musik_spielen(spiel_musik,-1,aktuelle_lautstaerke)  
                              m_aktiv = False  
                              GUI.fill(weiss)
                              allg.rundenstart = pygame.time.get_ticks()

                         if button_e_rect.collidepoint(mouse_pos):
                              sfx_spielen("s.klick")
                              menu = e_menu(hauptmenu)
                              if menu:
                                   menu()
                                   return 

                         if button_anleitung_rect.collidepoint(mouse_pos):
                              sfx_spielen("s.klick")
                              webbrowser.open("https://github.com/jonas-mli/abschlussarbeit_12-2?tab=readme-ov-file#spielanleitung")                              


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

          aktuelle_lautstaerke = pygame.mixer.music.get_volume()
          pygame.mixer.music.set_volume(aktuelle_lautstaerke)
          if not pygame.mixer.music.get_busy() or pygame.mixer.music.get_pos() == -1:
               musik_spielen(menu_musik)

          #musik_spielen(menu_musik)

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
                                   if not pygame.mixer.music.get_busy() or pygame.mixer.music.get_pos() == -1:
                                        musik_spielen(menu_musik,-1,aktuelle_lautstaerke)
                                   GUI.fill(weiss)
                                   return True  
                              
                              if button_e_rect.collidepoint(mouse_pos):
                                   sfx_spielen("s.klick")
                                   menu = e_menu(pause_menu)
                                   if menu:
                                        menu()
                                        return

                              if button_anleitung_rect.collidepoint(mouse_pos):
                                   sfx_spielen("s.klick")
                                   webbrowser.open("https://github.com/jonas-mli/abschlussarbeit_12-2?tab=readme-ov-file#spielanleitung")                              


                              if button_hauptmenu_rect.collidepoint(mouse_pos):
                                   sfx_spielen("s.klick")
                                   hauptmenu()  
                                   return False  
          
#####################
# Einstellungsmenü
#####################

     def e_menu(menu):
          global zoom # Weil global definiert statt in Funktion
          global WEG_SKALIERT

          e_aktiv = True
          m_iteration = 0

          BUTTON_BREITE = 300
          BUTTON_HOEHE = 50

          button_zurueck_rect = pygame.Rect(48 ,690, 100, 100)
          button_musik_zurueck_rect = pygame.Rect(1340, 670, 100, 100)
          button_musik_vor_rect = pygame.Rect(1470, 670, 100, 100)

          pygame.display.set_caption("KGS Turismo - Einstellungen")

          while e_aktiv == True:
               clock.tick(FPS)
               GUI.blit(HINTERGRUND_EINSTELLUNGSMENU,(0, -90))
               allg.slider_zoom.zei(GUI)
               allg.slider_lautstaerke.zei(GUI)

               text_zoom = monogram.render(f"{allg.slider_zoom.wert:.1f}", True, creme)
               GUI.blit(text_zoom, (BREITE // 2 - text_zoom.get_width() // 2,520 ))
               allg.zoom = allg.slider_zoom.wert

               text_lautstaerke = schrift.render(f"{int(allg.slider_lautstaerke.wert * 100)}%", True, creme)
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
                    
                    if event.type == pygame.MOUSEBUTTONUP:
                         if zoom != allg.slider_zoom.wert:
#                              zoom_alt = zoom
                              zoom = allg.slider_zoom.wert
#                              zoom_faktor = zoom / zoom_alt

                              WEG_SKALIERT = WEG_zoom(WEG, zoom) #neue skalierung nach neuem zoomwert
                              bilder_s = zoom_skalieren(bilder, zoom)
                              aktualisiere_masken()

                              spieler_auto.skaliere_auto(zoom)
                              spieler_auto.aktualisiere_geschwindigkeit(zoom)
                              
                              gegner_auto.skaliere_auto(zoom)
                              gegner_auto.aktualisiere_geschwindigkeit(zoom)

                         allg.lautstaerke = allg.slider_lautstaerke.wert
                         pygame.mixer.music.set_volume(allg.lautstaerke)

##############
# Spiel-loop
##############

     FPS = 60
     WEG = [(91, 245), (79, 123), (97, 79), (161, 103), (454, 288), (525, 310), (538, 256), (463, 130), (455, 84), (509, 72), (715, 56), (759, 88), (758, 152), (833, 158), (947, 128), (1081, 73), (1148, 111), (1337, 84), (1540, 70), (1574, 227), (1561, 286), (1464, 336), (1370, 343), (1174, 241), (1062, 228), (789, 280), (722, 305), (762, 349), (865, 390), (982, 415), (1074, 429), (1511, 472), (1563, 486), (1570, 518), (1556, 641), (1526, 677), (1480, 706), (1395, 718), (1079, 707), (949, 679), (717, 532), (633, 497), (563, 524), (498, 610), (429, 677), (357, 731), (269, 770), (201, 743), (168, 683), (142, 606), (124, 501), (116, 459), (113, 414), (100, 328)]
     WEG_SKALIERT = WEG_zoom(WEG, zoom)

     allg = Allg()
     spieler_auto = SpielerAuto(8,10) # Spielerauto(Max_Geschwindigkeit, Max_Rotationsgeschwindigkeit)
     gegner_auto = Gegner(3, 5, WEG_SKALIERT)
     game_processor = GameProcessor()
     game_processor.init_pool()

     aktiv = True 
     pausiert = False
     clock = pygame.time.Clock() #Zum Regeln der Spielgeschwindigkeit

     hauptmenu()
     aktualisiere_masken()
     aktuelle_lautstaerke = pygame.mixer.music.get_volume()
     pygame.mixer.music.set_volume(aktuelle_lautstaerke)
     if not pygame.mixer.music.get_busy() or pygame.mixer.music.get_pos() == -1:
          musik_spielen(spiel_musik,-1,aktuelle_lautstaerke)

     GUI.fill((148,196,52))
     pygame.display.update()

     kam_offs_x = -(spieler_auto.x - (BREITE // 2))
     kam_offs_y = -(spieler_auto.y - (HOEHE // 2))
     kam_offs = (kam_offs_x, kam_offs_y) 



     while aktiv:   
          if not pausiert: #aktives spiel   
               clock.tick(FPS)  # Clock begrenzt den Loop auf fps anzahl
               zeit_aktuell = pygame.time.get_ticks() # misst aktuelle Zeit
               rundenzeit = (zeit_aktuell - allg.rundenstart) - allg.pausenzeit 
               pygame.display.set_caption("KGS Turismo - Spiel")

               physik_ergebnisse = game_processor.process_physics(spieler_auto, gegner_auto, bilder_s)
               spieler_auto.x, spieler_auto.y = physik_ergebnisse[0]
               gegner_auto.x, gegner_auto.y = physik_ergebnisse[1]
               
               kam_offs_x = -(spieler_auto.x - (BREITE // 2)) #Kamera offset von x
               kam_offs_y = -(spieler_auto.y - (HOEHE // 2))
               kam_offs = (kam_offs_x, kam_offs_y)

               #print(f"X:{spieler_auto.x}, Y:{spieler_auto.y}")
               #GUI.fill(weiss) #renderingoptimierung

               sichtbare_bilder = [
               (bild, coords) for bild, coords in bilder_s 
               if -bild.get_width() <= coords[0] + kam_offs[0] <= BREITE and
                    -bild.get_height() <= coords[1] + kam_offs[1] <= HOEHE
               ]

               for bild, coords in sichtbare_bilder:
                    n_pos = [coords[p]+ kam_offs[p] for p in range(2)]
                    GUI.blit(bild, n_pos) 
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
               gegner_auto.bewegen()
               
               if spieler_auto.kollidieren(BANDE_MASKE) != None:
                    spieler_auto.rueckstoss()

               gegner_schnittP = gegner_auto.kollidieren(ZIEL_LINIE_MASKE, *ziel_pos_skaliert)
     #          if gegner_auto != None:
     #               print("Gegner gewinnt")

               ziel_schnittP = spieler_auto.kollidieren(ZIEL_LINIE_MASKE, *ziel_pos_skaliert)
               if ziel_schnittP != None: #* spaltet Tupel in 2 individuelle Koordinaten also (ZIEL_LINIE_MASKE,x,y)
                    rundenzeit_sekunden = rundenzeit / 1000
                    allg.speichere_highscore(rundenzeit_sekunden)
     #               rundenzeit_text = monogram.render(f"{rundenzeit /1000:.2f}", True, rot)
                    allg.zeige_highscores(GUI)
                    allg.rundenstart = pygame.time.get_ticks()

     #               GUI.blit(rundenzeit_text, (BREITE // 2 - rundenzeit_text.get_width() // 2, HOEHE // 2))

                    pygame.display.update()
                    pygame.time.delay(3000)
#                    allg.rundenstart = pygame.time.get_ticks()
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

     #print(gegner_auto.weg)     
     pygame.quit()

if __name__ == '__main__':
    main()