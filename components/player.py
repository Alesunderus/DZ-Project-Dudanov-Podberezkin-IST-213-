import pygame

from components.sprite import Sprite
from core.camera import camera
from core.input import is_mouse_just_pressed
from components.physics import Body, triggers
from components.label import Label
from components.entity import Entity
from components.ui.inventory_view import InventoryView
from components.inventory import Inventory
from components.ui.bar import Bar
from components.ui.scroll_view import ScrollView, create_scroll_sprite_generic, print_on_choose
from components.combat import Combat
from core.math_ext import distance
from gamedata.items_types import item_types
from redact_db import game_over, find_account

inventory = Inventory(3)
message_time_seconds = 3

def on_player_death(entity):
    from stages.play import quit_game
    quit_game()
    from core.engine import engine
    inventory.reset_resources()
    game_over(engine.account[0], engine.progress[0])
    engine.account = find_account(engine.account[1])
    engine.loaded_progress = False
    engine.switch_to('Menu')

class Player:
    def __init__(self, health):
        self.health = health
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
        self.weapon = item_types[2]

    def show_message(self, message):
        self.message_label.set_text(message)
        self.message_countdown = message_time_seconds * 60

    def setup(self):
        inventory.add(item_types[0], 0)
        inventory.add(item_types[4], 0)
        combat = Combat(self.health, on_player_death)
        self.entity.add(combat)
        self.combat = combat
        self.combat.equip(self.weapon)
        del self.health

        self.health_bar = Entity(Bar(self.combat.max_health, (255, 20, 20), (20, 255, 20))).get(Bar)
        self.health_bar.entity.x = camera.width/2 - self.health_bar.width/2
        self.health_bar.entity.y = camera.height - self.health_bar.height - 15
        from gamedata.buildings import tower_types
        self.buildings_scroll_view = Entity(ScrollView(tower_types, create_scroll_sprite_generic, print_on_choose,
                                                       48, 150, 100)).get(ScrollView)
        self.buildings_scroll_view.entity.x = 15
        self.buildings_scroll_view.entity.y = camera.height - self.buildings_scroll_view.height - 15

    def breakdown(self):
        self.loc_label.entity.delete_self()
        self.message_label.entity.delete_self()
        self.inventory_window.delete_self()
        self.health_bar.entity.delete_self()
        from core.engine import engine
        engine.active_objs.remove(self)

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
        self.health_bar.amount = self.combat.health
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
            if self.combat.equipped is not None:
                self.combat.unequip()
        if is_mouse_just_pressed(0):
            if self.buildings_scroll_view.selected_item is None:
                if self.combat.equipped is None:
                    self.combat.equip(self.weapon)
                self.combat.perform_attack()
            else:
                mouse_pos = pygame.mouse.get_pos()
                from gamedata.buildings import tower_types
                can_be_placed = False
                if inventory.has(item_types[0], tower_types[self.buildings_scroll_view.selected_item].price[0]) and \
                        inventory.has(item_types[4], tower_types[self.buildings_scroll_view.selected_item].price[1]):
                    can_be_placed = True
                from core.area import area
                if can_be_placed:
                    building = area.add_entity(5, (int(mouse_pos[0]+camera.x)/32), (int(mouse_pos[1]+camera.y)/32), [str(self.buildings_scroll_view.selected_item)])
                    if building.get(Body).is_position_valid():
                        self.show_message('Tower placed')
                        inventory.remove(item_types[0], tower_types[self.buildings_scroll_view.selected_item].price[0])
                        inventory.remove(item_types[4], tower_types[self.buildings_scroll_view.selected_item].price[1])
                    else:
                        building.delete_self()
                        self.show_message('Wrong position')
                else:
                    self.show_message('Not enough resources')

        if (recent_keys[pygame.K_ESCAPE]):
            from stages.play import quit_game
            quit_game()
            from core.engine import engine
            engine.switch_to('Menu')
