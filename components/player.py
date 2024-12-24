import pygame

from components.sprite import Sprite
from core.camera import camera
from components.physics import Body, triggers
from components.label import Label
from components.entity import Entity
from components.ui.inventory_view import InventoryView
from components.inventory import Inventory
from core.math_ext import distance

inventory = Inventory(3)
message_time_seconds = 3

class Player:
    def __init__(self):
        self.loc_label = Entity(Label('Montserrat-Medium.ttf',
                                        'X: 0 - Y: 0')).get(Label)
        self.message_label = Entity(Label('Montserrat-Medium.ttf', '')).get(Label)
        self.inventory_window = Entity(InventoryView(inventory))
        from core.engine import engine
        engine.active_objs.append(self)
        self.direction = pygame.math.Vector2()
        self.movement_speed = 200
        self.loc_label.entity.x = 10
        self.message_label.entity.x = 10
        self.message_label.entity.y = 32
        self.message_countdown = 0

    def show_message(self, message):
        self.message_label.set_text(message)
        self.message_countdown = message_time_seconds * 60

    def interact(self, mouse_pos):
        from core.engine import engine
        for usable in engine.usables:
            if usable.entity.has(Sprite):
                usable_sprite = usable.entity.get(Sprite)
                x_sprite = usable.entity.x - camera.x
                y_sprite = usable.entity.y - camera.y
                width_sprite = usable_sprite.image.get_width()
                height_sprite = usable_sprite.image.get_height()

                if x_sprite < mouse_pos[0] < x_sprite + width_sprite and \
                    y_sprite < mouse_pos[1] < y_sprite + height_sprite:
                        my_sprite = self.entity.get(Sprite)
                        d = distance(x_sprite + width_sprite/2, y_sprite + height_sprite,
                                     self.entity.x - camera.x + my_sprite.image.get_width()/2, self.entity.y - camera.y + my_sprite.image.get_height())
                        usable.on(self.entity, d)


    def update(self, dt):
        if self.message_countdown > 0:
            self.message_countdown -= 1
            if self.message_countdown <= 0:
                self.message_label.set_text('')
        self.loc_label.set_text(f'X: {int(self.entity.x/32)} - Y: {int(self.entity.y/32)}')
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
            mouse_pos = pygame.mouse.get_pos()
            self.interact(mouse_pos)
        if (recent_keys[pygame.K_ESCAPE]):
            from core.engine import engine
            engine.switch_to('Menu')