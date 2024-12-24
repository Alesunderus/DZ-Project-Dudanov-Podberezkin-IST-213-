from core.map import Map
from gamedata.objects import create_entity

area = None
area_folder_location = 'static/maps'


class Area:
    def __init__(self, area_file, tiles_type):
        global area
        area = self
        self.tile_types = tiles_type
        self.load_file(area_file)

    def search_for_first(self, kind):
        for e in self.entities:
            c = e.get(kind)
            if c is not None:
                return e

    def remove_entity(self, e):
        print(e)
        self.entities.remove(e)
        for c in e.components:
            g = getattr(c, 'breakdown', None)
            if callable(g):
                c.breakdown()

    def load_file(self, area_file):
        # Read all data from file
        file = open(area_folder_location + '/' + area_file, 'r')
        data = file.read()
        file.close()

        from core.engine import engine
        engine.reset()

        # Split data between tiles and entities by minus
        chunks = data.split('-')
        tile_map_data = chunks[0]
        entity_data = chunks[1]

        # Load map
        self.map = Map(tile_map_data, self.tile_types)

        # Load the entites
        self.entities = []
        entity_lines = entity_data.split('\n')[1:]
        for line in entity_lines:
            try:
                items = line.split(',')
                id = int(items[0])
                x = int(items[1])
                y = int(items[2])
                self.entities.append(create_entity(id, x, y, items[3:]))
                print(self.entities)
            except Exception as e:
                print(f"Error parsing line: {line}. {e}")