from math import ceil

from components.ui.window import create_window, Window
from components.entity import Entity
from components.sprite import Sprite
from components.label import Label

items_per_row = 1
padding_size = 10
gap_size = 0
items_size = 128

class InventoryView:
    def __init__(self, inventory, slot_image = 'items/inventory_slot.png'):
        from core.engine import engine
        self.inventory = inventory
        self.slot_image = slot_image
        width = padding_size + (items_per_row * items_size) + ((items_per_row - 1) * gap_size) + padding_size
        rows = ceil(inventory.capacity / items_per_row)
        height = padding_size + (rows * items_size/4) + ((rows - 1) * gap_size) + padding_size

        from core.camera import camera
        x = camera.width - width
        y = camera.height - height

        self.window = create_window(x, y, width, height)
        self.slot_container_sprites = []
        self.slot_sprites = []

        inventory.listener = self
        self.render()
        engine.active_objs.append(self)

    def render(self):
        row = 0
        column = 0
        for slot in self.inventory.slots:
            x = column * (items_size + gap_size) + self.window.x + padding_size
            y = row * (items_size/4 + gap_size) + self.window.y + padding_size
            container_sprite = Entity(Sprite(self.slot_image, True), x = x, y = y)
            self.window.get(Window).items.append(container_sprite)
            if slot.type is not None:
                print(slot.type.name)
                item_sprite = Entity(Sprite(slot.type.icon_name, True), x = x, y = y)
                if slot.type.stack_size > 1:
                    label = Entity(Label('Montserrat-Medium.ttf', str(slot.amount), color = (255, 255, 0), size = 30), x = x + 37, y = y)
                    self.window.get(Window).items.append(label)
                self.window.get(Window).items.append(item_sprite)
            column += 1
            if column >= items_per_row:
                column = 0
                row += 1

    def clear(self):
        for i in self.window.get(Window).items:
            print(i.has(Sprite))
            if i.has(Sprite):
                i.get(Sprite).breakdown()
            elif i.has(Label):
                i.get(Label).breakdown()
        self.window.get(Window).items.clear()

    def refresh(self):
        self.clear()
        self.render()

    def breakdown(self):
        from core.engine import engine
        engine.active_objs.remove(self)
        self.clear()

    def update(self, dt):
        pass