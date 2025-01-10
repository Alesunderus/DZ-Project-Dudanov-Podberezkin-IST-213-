from components.enemy import Enemy
from components.entity import Entity
from components.sprite import Sprite
from components.player import Player
from components.physics import Body
from components.inventory import Inventory, DroppedItem
from gamedata.items_types import item_types
from components.usables import Minable, Chopable
from components.tower import Tower
from gamedata.buildings import tower_types

class EntityFactory:
    def __init__(self, name, icon, factory, arg_names = [], defaults = []):
        self.name = name
        self.icon = icon
        self.factory = factory
        self.arg_names = arg_names
        self.defaults = defaults

entity_factories = [
    # 0 - Makes a player
    EntityFactory('Player', 'player/down/0.png',
                  lambda args: Entity(Player(100), Sprite('player/down/0.png'), Body(8, 24, 12, 12), x = 0, y = 0)),

    # 1 makes a tree
    EntityFactory('Tree', 'assets/tree.png',
                  lambda args: Entity(Sprite('assets/tree.png'), Chopable('tree', 'assets/tree_stump.png', args[0]=='True'), Body(16, 96, 32, 32),  x = 0, y = 0),
                  ['Chopped'],['False']),

    # 2 makes a rock
    EntityFactory('Rock', 'assets/rock.png',
                  lambda args: Entity(Sprite('assets/rock.png'), Minable('rock'), Body(0,24, 32, 16),  x = 0, y = 0)),

    # 3 makes a collectible
    EntityFactory('Dropped item', 'items/axe.png',
                  lambda args: Entity(DroppedItem(item_types[int(args[0])], int(args[1])), Sprite(item_types[int(args[0])].icon_name)),
                  ['Item Type ID', 'Quantity'], ['0','1']),

    # 4 makes an enemy
    EntityFactory('Enemy', 'enemies/skeleton.png',
                  lambda args: Entity(Sprite(args[0]), Enemy(100, 3), Body(8,24,12,12)),
                  ['image'],['enemies/skeleton.png']),

    # 5 makes a tower
    EntityFactory('Tower', 'towers/archer.png',
                  lambda args: Entity(Sprite(tower_types[int(args[0])].icon), Tower(tower_types[int(args[0])]), Body(0,0,32,32)),['TowerID'], ['0'])
]

def create_entity(id, x, y, data=None):
    factory = entity_factories[id].factory
    e = factory(data)
    e.x = x*32
    e.y = y*32
    return e