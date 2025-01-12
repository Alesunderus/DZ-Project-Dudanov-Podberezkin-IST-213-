from components.enemy import EnemyType

enemy_types = []

def initialize_enemy_types(rows):
    from stages.menu import writeTofile
    for i, row in enumerate(rows):
        filename = f'static/images/enemies/enemy{i}.png'
        fileref = f'enemies/enemy{i}.png'
        writeTofile(row[6], filename)
        enemy = EnemyType(row[1], row[2], row[3], row[4], row[5], fileref)
        enemy_types.append(enemy)