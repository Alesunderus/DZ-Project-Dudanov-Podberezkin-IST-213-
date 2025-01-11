import pygame

from components.entity import Entity
from components.sprite import Sprite
from core.effect import create_hit_text, Effect
from components.physics import get_bodies_within_circle


class Combat:
    def __init__(self, health, on_death):
        self.health = health
        self.max_health = health
        self.global_cooldown = 0
        self.equipped = None
        self.regen = 0.01
        self.on_death = on_death
        self.weapon_sprite = None
        self.can_attack = True
        from core.engine import engine
        engine.active_objs.append(self)

    def equip(self, item):
        self.equipped = item
        self.weapon_sprite = Entity(Sprite(self.equipped.icon_name)).get(Sprite)

    def unequip(self):
        self.equipped = None
        self.weapon_sprite.entity.delete_self()
        self.weapon_sprite = None

    def breakdown(self):
        from core.engine import engine
        engine.active_objs.remove(self)
        if self.weapon_sprite is not None:
            self.weapon_sprite.entity.delete_self()
        self.weapon_sprite = None

    def attack(self, other):
        if self.equipped == None:
            return

        if not self.can_attack:
            return

        damage = int(self.equipped.stats['damage'])
        other.health -= damage
        self.global_cooldown = self.equipped.stats['cooldown']*60
        self.can_attack = False
        print(self.global_cooldown)
        create_hit_text(other.entity.x, other.entity.y, str(damage), (255, 20, 20))
        from core.area import area

        if other.health <= 0 and other.entity in area.entities:
            other.on_death(other.entity)

    def perform_attack(self):
        if self.equipped == None:
            return

        nearby_objs = get_bodies_within_circle(self.entity.x, self.entity.y, self.equipped.stats['range'])

        for o in nearby_objs:
            if o.entity.has(Combat) and o.entity != self.entity:
                self.attack(o.entity.get(Combat))

    def update(self, dt):
        if self.global_cooldown > 0:
            self.global_cooldown -= 1
        if self.global_cooldown <= 0 and not self.can_attack:
            self.can_attack = True
        if self.health < self.max_health:
            self.health += self.regen
        if self.health > self.max_health:
            self.health = self.max_health

        if self.weapon_sprite is not None:
            self.weapon_sprite.entity.x = self.entity.x
            self.weapon_sprite.entity.y = self.entity.y