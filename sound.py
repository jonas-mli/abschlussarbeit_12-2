# Alle Soundeffekte und Lieder sind lizenzfrei
import pygame 

pygame.mixer.init()

######################
# Soundeffekte (sfx)
######################

sfx = {
    "s.car_engine":pygame.mixer.Sound("Sounds/sfx/car_engine.mp3"),
    "s.car_engine2":pygame.mixer.Sound("Sounds/sfx/car_engine2.mp3"),
    "s.countdown":pygame.mixer.Sound("Sounds/sfx/countdown.mp3"),
    "s.lose":pygame.mixer.Sound("Sounds/sfx/lose.mp3"),
    "s.lose2":pygame.mixer.Sound("Sounds/sfx/lose2.mp3"),
    "s.powerup":pygame.mixer.Sound("Sounds/sfx/powerup.mp3"),
    "s.sound_sfx":pygame.mixer.Sound("Sounds/sfx/sound_sfx.mp3"),
    "s.win":pygame.mixer.Sound("Sounds/sfx/win.mp3"),
    "s.win2":pygame.mixer.Sound("Sounds/sfx/win2.mp3"),
}

#########
# Musik
#########




musik = {
    "menu.musik1":"Sounds/musik/menu.mp3",
    "m.8bit_bach":"Sounds/musik/8bit_bach.mp3",
    "m.8bit_mondlicht_sonate":"Sounds/musik/8bit_mondlicht_sonate.mp3",
    "m.8bit_mix":"Sounds/musik/8bit_mix.mp3",
    "m.beep_boop":"Sounds/musik/beep_boop.mp3",
    "m.chase":"Sounds/musik/chase.mp3",
    "m.chiptune":"Sounds/musik/chiptune.mp3",
    "m.colorful_potions":"Sounds/musik/colorful_potions.mp3",
    "m.chilly":"Sounds/musik/chilly.mp3",
    "m.night_city":"Sounds/musik/night_city.mp3",
    "m.retro_streets":"Sounds/musik/retro_streets.mp3",
    "m.short_chiptune_loop":"Sounds/musik/short_chiptune_loop.mp3",
}