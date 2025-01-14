import random

import pygame

from core.area import Area
from gamedata.tiletypes import tile_kinds
from components.usables import Chopable, Minable
from components.physics import Body
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
    rocks_left = 0
    for e in area.entities:
        if e.has(Minable):
            rocks_left+=1
    rocks_to_spawn = 5 - rocks_left
    print(f'Rocks to spawn {rocks_to_spawn}')
    if rocks_to_spawn > 0:
        for i in range(rocks_to_spawn):
            print(f'Rocks to spawn {i}')
            placement_valid = False
            while not placement_valid:
                new_rock = area.add_entity(2, random.randint(0,35), random.randint(15, 28), [])
                print(f'Rock entity {new_rock}')
                placement_valid = new_rock.get(Body).is_position_valid()
                if not placement_valid:
                    new_rock.delete_self()
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
    spawn_side = random.randint(1, 2)
    if spawn_side == 1:
        x = 1
        y = random.randint(1, 28)
    else:
        x = random.randint(1, 36)
        y = 27
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
        placement_valid = False
        while not placement_valid:
            new_enemy = area.add_entity(4, x, y, ['enemies/skeleton.png',str(random_enemy)])
            placement_valid = new_enemy.get(Body).is_position_valid()
            if not placement_valid:
                new_enemy.delete_self()
                x,y = rand_enemy_coords(x,y)
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

def rand_enemy_coords(x, y):
    if x == 1:
        new_x = 1
        new_y = random.randint(1,28)
    elif  y == 27:
        new_x = random.randint(1, 36)
        new_y = 27
    return new_x, new_y