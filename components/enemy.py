import random

from components.physics import Body, get_bodies_within_circle
from components.sprite import Sprite
from gamedata.items_types import item_types
from core.math_ext import distance
from components.combat import Combat
from components.player import Player

def on_enemy_death(entity):
    from core.area import area
    area.remove_entity(entity)
    from stages.play import decrease_enemy_count
    decrease_enemy_count()
    print('Enemy died')


class EnemyType:
    def __init__(self, health, speed,weapon_item_id, first_wave, spawn_cost, sprite):
        self.health = health
        self.weapon = item_types[weapon_item_id]
        self.first_wave = first_wave
        self.spawn_cost = spawn_cost
        self.sprite = sprite
        self.speed = speed


class Enemy:
    def __init__(self, enemy_type) -> None:
        self.health = enemy_type.health
        self.weapon = enemy_type.weapon

        self.target = None
        self.targeted_entity = None
        self.stop_to_update = random.randint(0,30)
        self.vision_range = 2000
        self.walk_speed = enemy_type.speed
        self.sprite = enemy_type.sprite

        from core.engine import engine
        engine.active_objs.append(self)

    def setup(self):
        #sprite = self.entity.get(Sprite)
        #sprite.image = pygame.transform.scale(sprite.image, (32, 32))
        self.entity.add(Combat(self.health, on_enemy_death))
        self.combat = self.entity.get(Combat)
        self.combat.equip(self.weapon)
        del self.health
        self.entity.get(Sprite).set_image(self.sprite)

    def breakdown(self):
        from core.engine import engine
        engine.active_objs.remove(self)

    def update_ai(self):
        seen_objects = get_bodies_within_circle(self.entity.x, self.entity.y, self.vision_range)
        found_player = False
        for s in seen_objects:
            if s.entity.has(Player):
                self.target = (s.entity.x, s.entity.y)
                self.targeted_entity = s.entity
                found_player = True
        if not found_player:
            self.target = None
            self.targeted_entity = None

    def update(self, dt):
        from core.engine import engine
        if engine.step % 30 == self.stop_to_update:
            self.update_ai()
        if self.targeted_entity is not None:
            weapon_range = int(self.combat.equipped.stats['range'])
            dist = distance(self.entity.x, self.entity.y, self.targeted_entity.x, self.targeted_entity.y)
            if weapon_range > dist:
                self.combat.attack(self.targeted_entity.get(Combat))

        if self.target is not None:
            if self.entity.has(Body):
                body = self.entity.get(Body)
                prev_x = self.entity.x
                prev_y = self.entity.y
                if self.entity.x < self.target[0]:
                    self.entity.x += self.walk_speed
                if self.entity.x > self.target[0]:
                    self.entity.x -= self.walk_speed
                if not body.is_position_valid():
                    self.entity.x = prev_x
                if self.entity.y < self.target[1]:
                    self.entity.y += self.walk_speed
                if self.entity.y > self.target[1]:
                    self.entity.y -= self.walk_speed
                if not body.is_position_valid():
                    self.entity.y = prev_y