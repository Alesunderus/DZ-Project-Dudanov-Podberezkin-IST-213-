import pygame

from core.area import Area
from gamedata.tiletypes import tile_kinds
from components.usables import Chopable

night_event = pygame.event.custom_type()
day_event = pygame.event.custom_type()

def play():
    Area('load.map', tile_kinds)
    pygame.time.set_timer(night_event, 10000)

def start_day():
    pygame.time.set_timer(night_event, 10000)
    pygame.time.set_timer(day_event, 0)
    from core.engine import engine
    engine.clear_color = (50, 150, 50)
    from core.area import area
    for e in area.entities:
        if e.has(Chopable):
            e.get(Chopable).regen()

def quit_game():
    pygame.time.set_timer(night_event, 0)
    from core.engine import engine
    engine.clear_color = (50, 150, 50)

def start_night():
    pygame.time.set_timer(night_event, 0)
    from core.engine import engine
    engine.clear_color = (20, 20, 50)
    print('Start night')
    from core.area import area
    area.add_entity(4, 1, 1, ['enemies/skeleton.png'])
    pygame.time.set_timer(day_event, 10000)