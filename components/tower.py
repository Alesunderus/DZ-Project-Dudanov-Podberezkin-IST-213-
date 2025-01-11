import random

from core.effect import create_hit_text
from core.math_ext import distance
from components.physics import get_bodies_within_circle
from components.enemy import Enemy
from components.combat import Combat


class TowerType():
    def __init__(self, name, icon, projectile_sprite, damage, attack_speed, range, health):
        self.name = name
        self.icon = icon
        self.projectile_sprite = projectile_sprite
        self.damage = damage
        self.attack_speed = attack_speed
        self.range = range
        self.health = health


class Tower():
    def __init__(self, towertype):
        self.max_health = towertype.health
        self.health = self.max_health
        self.range = towertype.range
        self.damage = towertype.damage
        self.attack_speed = towertype.attack_speed
        self.projectile = towertype.projectile_sprite
        self.global_cooldown = 0
        self.can_attack = True
        self.target = None
        self.targeted_entity = None
        self.stop_to_update = random.randint(0, 30)
        from core.engine import engine
        engine.active_objs.append(self)

    def breakdown(self):
        from core.engine import engine
        engine.active_objs.remove(self)

    def update_ai(self):
        seen_objects = get_bodies_within_circle(self.entity.x, self.entity.y, self.range)
        found_enemy = False
        for s in seen_objects:
            if s.entity.has(Enemy):
                self.target = (s.entity.x, s.entity.y)
                self.targeted_entity = s.entity
                found_enemy = True
                return
        if not found_enemy:
            self.target = None
            self.targeted_entity = None

    def attack(self, other):
        other.health -= self.damage
        self.global_cooldown = self.attack_speed * 60
        self.can_attack = False
        print(self.global_cooldown)
        create_hit_text(other.entity.x, other.entity.y, str(self.damage), (255, 20, 20))
        from core.area import area
        if other.health <= 0 and other.entity in area.entities:
            other.on_death(other.entity)

    def update(self, dt):
        from core.engine import engine
        if engine.step % 30 == self.stop_to_update:
            self.update_ai()
        if self.targeted_entity is not None:
            dist = distance(self.entity.x, self.entity.y, self.targeted_entity.x, self.targeted_entity.y)
            if self.range > dist and self.can_attack:
                self.attack(self.targeted_entity.get(Combat))

        if self.global_cooldown > 0:
            self.global_cooldown -= 1
        if self.global_cooldown <= 0 and not self.can_attack:
            self.can_attack = True
        if self.health < self.max_health:
            self.health += self.regen
        if self.health > self.max_health:
            self.health = self.max_health