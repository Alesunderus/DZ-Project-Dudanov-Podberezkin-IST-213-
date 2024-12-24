from components.entity import Entity
from components.sprite import Sprite
from components.player import Player
from components.physics import Body
from components.inventory import Inventory, DroppedItem
from gamedata.items_types import item_types
from components.usables import Minable, Chopable

entity_factories = [
    # 0 - Makes a player
    lambda args: Entity(Player(), Sprite('player/down/0.png'), Body(8, 24, 12, 12), x = 0, y = 0),

    # 1 makes a tree
    lambda args: Entity(Sprite('assets/tree.png'), Chopable('tree', 'assets/tree_stump.png'), Body(16, 96, 32, 32),  x = 0, y = 0),

    # 2 makes a rock
    lambda args: Entity(Sprite('assets/rock.png'), Minable('rock'), Body(0,24, 32, 16),  x = 0, y = 0),

    # 3 makes a collectible
    lambda args: Entity(DroppedItem(item_types[int(args[0])], int(args[1])), Sprite(item_types[int(args[0])].icon_name))
]

def create_entity(id, x, y, data=None):
    factory = entity_factories[id]
    e = factory(data)
    e.x = x*32
    e.y = y*32
    return e