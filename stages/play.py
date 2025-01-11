import random

import pygame

from core.area import Area
from gamedata.tiletypes import tile_kinds
from components.usables import Chopable
from gamedata.enemy_types import enemy_types

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
    global wave_count
    wave_count += 1
    from core.area import area
    area.save_file()

def quit_game():
    pygame.time.set_timer(night_event, 0)
    global spawned_enemy_amount
    spawned_enemy_amount = 0
    from core.engine import engine
    engine.clear_color = (50, 150, 50)

def start_night():
    pygame.time.set_timer(night_event, 0)
    from core.engine import engine
    engine.clear_color = (20, 20, 50)
    print('Start night')
    enemies_can_spawn = []
    global wave_count, spawned_enemy_amount
    wave_points = wave_count
    for i,enemy in enumerate(enemy_types):
        if enemy.first_wave <= wave_count:
            enemies_can_spawn.append(i)
    print(len(enemies_can_spawn))
    while wave_points > 0:
        enemy_cost = 10000
        random_enemy = 0
        while enemy_cost > wave_points:
            if len(enemies_can_spawn) > 1:
                random_enemy = random.randint(0, len(enemies_can_spawn)-1)
            else:
                random_enemy = 0
            enemy_cost = enemy_types[enemies_can_spawn[random_enemy]].spawn_cost
        from core.area import area
        area.add_entity(4, spawned_enemy_amount+2, 1, ['enemies/skeleton.png',str(random_enemy)])
        wave_points -= enemy_cost
        spawned_enemy_amount +=1
        print('b')
    global left_enemies_amount
    left_enemies_amount = spawned_enemy_amount
    #pygame.time.set_timer(day_event, 10000)

def decrease_enemy_count():
    global left_enemies_amount, spawned_enemy_amount
    left_enemies_amount -=1
    if left_enemies_amount <= 0:
        spawned_enemy_amount = 0
        start_day()

def set_wave_count(count):
    global wave_count
    wave_count = count
