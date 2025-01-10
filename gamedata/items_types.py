from components.inventory import ItemType

item_types = [
    ItemType('Wood', 'items/wood_2.png', 10000),
    ItemType('Axe', 'items/axe.png', 1),
    ItemType('Sword', 'items/sword.png', 1, damage=50, cooldown = 0.5, range=70),
    ItemType('Weak Sword', 'items/weak_sword.png',1, damage = 2, cooldown = 0.5, range = 50),
    ItemType('Stone', 'items/stone.png',10000)
]