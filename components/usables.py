from components.sprite import Sprite
from components.player import Player
from gamedata.items_types import item_types
from core.effect import Effect
from components.editor import EntityPlaceholder

image_folder = 'static/images'


class Usable:
    def __init__(self, obj_name):
        self.obj_name = obj_name
        from core.engine import engine
        engine.usables.append(self)

    def breakdown(self):
        from core.engine import engine
        engine.usables.remove(self)

    def on(self, other, distance):
        print('Base on function called')


class Minable(Usable):
    def __init__(self, obj_name):
        super().__init__(obj_name)

    def on(self, other, distance):
        from components.player import inventory
        player = other.get(Player)

        Effect(other.x - 10, other.y, 0,1,10, item_types[1].icon)

        if distance < 60:
            player.show_message('Harvesting ' + self.obj_name)
            inventory.add(item_types[4], 20)
            from core.area import area
            area.remove_entity(self.entity)
        else:
            player.show_message('Need to get closer')


class Chopable(Usable):
    def __init__(self, obj_name, chopped_image, is_chopped):
        super().__init__(obj_name)
        self.chopped_image = chopped_image
        print(is_chopped)
        self.is_chopped = is_chopped

    def setup(self):
        self.tree_image = self.entity.get(Sprite).image_location
        if self.is_chopped:
            self.entity.get(Sprite).set_image(self.chopped_image)

    def regen(self):
        self.entity.get(Sprite).set_image(self.tree_image)
        self.is_chopped = False
        self.entity.get(EntityPlaceholder).args[0] = 'False'

    def on(self, other, distance):
        from components.player import inventory
        player = other.get(Player)

        if self.is_chopped:
            player.show_message('Tree already chopped, wait for next day')
            return

        Effect(other.x - 10, other.y, 0, 1, 10, item_types[1].icon)

        if distance < 60:
            player.show_message('Harvesting ' + self.obj_name)
            inventory.add(item_types[0], 100)
            self.entity.get(Sprite).set_image(self.chopped_image)
            self.is_chopped = True
            self.entity.get(EntityPlaceholder).args[0] = 'True'
        else:
            player.show_message('Need to get closer')

