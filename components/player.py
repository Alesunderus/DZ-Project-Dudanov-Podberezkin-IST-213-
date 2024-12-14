import pygame

from components.sprite import Sprite
from core.camera import camera
from components.physics import Body, triggers
from components.label import Label
from components.entity import Entity
from components.ui.inventory_view import InventoryView
from components.inventory import Inventory

inventory = Inventory(3)

class Player:
    def __init__(self):
        self.loc_label = Entity(Label('Montserrat-Medium.ttf',
                                        'X: 0 - Y: 0')).get(Label)
        self.inventory_window = Entity(InventoryView(inventory))
        from core.engine import engine
        engine.active_objs.append(self)
        self.direction = pygame.math.Vector2()
        self.movement_speed = 200

    def update(self, dt):
        self.loc_label.set_text(f'X: {int(self.entity.x)} - Y: {int(self.entity.y)}')
        previous_x = self.entity.x
        previous_y = self.entity.y
        sprite = self.entity.get(Sprite)
        body = self.entity.get(Body)
        sprite.image = pygame.transform.scale(sprite.image, (32, 32))
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.entity.x += self.direction.x * dt * self.movement_speed
        if not body.is_position_valid():
            self.entity.x = previous_x
        self.entity.y += self.direction.y * dt * self.movement_speed
        if not body.is_position_valid():
            self.entity.y = previous_y
        camera.centerx = self.entity.x + sprite.image.get_width()/2
        camera.centery = self.entity.y + sprite.image.get_height()/2
        for t in triggers:
            if body.is_colliding_with(t):
                t.on(self.entity)

        recent_keys = pygame.key.get_just_pressed()
        if(recent_keys[pygame.K_SPACE]):
            print("Space")
        if (recent_keys[pygame.K_ESCAPE]):
            from core.engine import engine
            engine.switch_to('Menu')