import pygame

from core.area import Area
from gamedata.tiletypes import tile_kinds
from components.usables import Chopable

night_event = pygame.event.custom_type()
day_event = pygame.event.custom_type()
day_duration = 10000
spawned_enemy_amount = 0
left_enemies_amount = 0
wave_count = 1

def play():
    Area('load.map', tile_kinds)
    pygame.time.set_timer(night_event, day_duration)

def start_day():
    pygame.time.set_timer(night_event, day_duration)
    #pygame.time.set_timer(day_event, 0)
    from core.engine import engine
    engine.clear_color = (50, 150, 50)
    from core.area import area
    for e in area.entities:
        if e.has(Chopable):
            e.get(Chopable).regen()
    from core.area import area
    area.save_file()
    global wave_count
    wave_count += 1

def quit_game():
    pygame.time.set_timer(night_event, 0)
    from core.engine import engine
    engine.clear_color = (50, 150, 50)

def start_night():
    pygame.time.set_timer(night_event, 0)
    from core.engine import engine
    engine.clear_color = (20, 20, 50)
    print('Start night')
    for i in range(wave_count):
        from core.area import area
        area.add_entity(4, i+1, 1, ['enemies/skeleton.png'])
    global spawned_enemy_amount
    spawned_enemy_amount = wave_count
    global left_enemies_amount
    left_enemies_amount = spawned_enemy_amount
    #pygame.time.set_timer(day_event, 10000)

def decrease_enemy_count():
    global left_enemies_amount
    left_enemies_amount -=1
    if left_enemies_amount <= 0:
        start_day()
