import json

from components.tower import TowerType

tower_types = []

def initialize_tower_types(rows):
    from stages.menu import writeTofile
    for i, row in enumerate(rows):
        filename = f'static/images/towers/tower{i}.png'
        fileref = f'towers/tower{i}.png'
        writeTofile(row[2], filename)
        price_data = json.loads(row[8])
        tower = TowerType(row[1], fileref, fileref, row[4], row[5], row[6], row[7], [price_data['Wood'], price_data['Stone'],0])
        tower_types.append(tower)