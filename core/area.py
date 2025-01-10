import os
import shutil
import struct
import traceback

from core.map import Map
from gamedata.objects import create_entity
from components.editor import EntityPlaceholder

area = None
area_folder_location = 'static/maps'
file_version = 2


class Area:
    def __init__(self, area_file, tiles_type):
        global area
        area = self
        self.entities = []
        self.area_file = area_file
        self.tile_types = tiles_type
        if not os.path.exists(area_folder_location + '/' + area_file):
            shutil.copyfile('static/maps/start.map', area_folder_location + '/' + area_file)
        self.load_file(area_file)

    def search_for_first(self, kind):
        for e in self.entities:
            c = e.get(kind)
            if c is not None:
                return e

    def add_entity(self, id, x, y, args):
        e = create_entity(id, x, y, args)
        e.add(EntityPlaceholder(id, args))
        self.entities.append(e)

    def remove_entity(self, e):
        print(e.get(EntityPlaceholder).id)
        self.entities.remove(e)
        for c in e.components:
            g = getattr(c, 'breakdown', None)
            if callable(g):
                c.breakdown()

    def save_file(self):
        path = area_folder_location + '/' + self.area_file
        file = open(path, 'wb')
        # File header
        file.write(struct.pack('c', bytes('\0', 'utf-8')))

        # Write the file version for future updates
        file.write(struct.pack('i', file_version))

        # Write the size of the tilemap
        # First Width, then height
        print(self.map.tiles)
        width = len(self.map.tiles[0])
        height = len(self.map.tiles)
        file.write(struct.pack('i', width))
        file.write(struct.pack('i', height))
        print("saving", width, height)

        # --- Body of the File ---

        # Save the Tile data
        self.map.save_to_file(file)

        for e in self.entities:
            from components.editor import EntityPlaceholder
            print(f'{e.x} {e.y}')
            if e.has(EntityPlaceholder):
                p = e.get(EntityPlaceholder)
                s = f"{p.id},{int(e.x / 32)},{int(e.y / 32)}"

                # If there are extra arguments for that kind of entity
                # then we save them.
                if p.args is not None and len(p.args) != 0:
                    s += ","
                    s += ",".join(p.args)
                b = bytes(s, 'utf-8')
                packed = struct.pack(f"{len(b)}s", b)
                file.write(packed)
                packed = struct.pack('c', bytes('\0', 'utf-8'))
                file.write(packed)
        file.close()


    def load_file(self, area_file):
        from core.engine import engine
        engine.reset()
        file = open(area_folder_location + "/" + area_file, "rb")

        # New file format has a null byte at the beginning
        b = struct.unpack('c', file.read(1))[0]
        b = str(b, 'utf-8')
        if b != '\0':
            # If it doesn't have this, its the old file format
            # We load with the previous method
            file.close()
            print("Loading Legacy file")
            self.load_file_legacy(area_file)
            return

        self.entities = []
        self.name = area_file.split(".")[0].title().replace("_", " ")
        # If we make it past this part, this is the new file format

        # For backwards compatibility,
        # Try to read the version number from the first 4 bytes
        version = struct.unpack('i', file.read(4))[0]
        tilemap_width = struct.unpack('i', file.read(4))[0]
        tilemap_height = struct.unpack('i', file.read(4))[0]
        tilemap_width = int(tilemap_width)
        tilemap_height = int(tilemap_height)

        print("loading", tilemap_width, tilemap_height)

        # Load tile data
        tiles = []
        for y in range(tilemap_height):
            row = []
            for x in range(tilemap_width):
                binary_data = file.read(2)
                tile_number = struct.unpack('H', binary_data)[0]
                row.append(tile_number)
            tiles.append(row)
        self.map = Map(tiles, self.tile_types, False)

        # Save each entity, delimited by a null terminated char
        # We read all the rest of the data from the file for this
        entity_data = file.read()

        # Convert it to a string
        entity_data = str(entity_data, encoding='utf-8')

        # Split the string to get each entity
        entities = entity_data.split('\0')

        # Throw away the last one, because there is a null character at the very end
        # of the file
        entities = entities[:len(entities) - 1]
        print(entities)
        for line in entities:
            try:
                print(line)
                items = line.split(',')
                id =  int(items[0])
                x = int(items[1])
                y = int(items[2])
                e = create_entity(id, x, y, items[3:])
                if not e.has(EntityPlaceholder):
                    e.add(EntityPlaceholder(id, items[3:]))
                self.entities.append(e)
            except Exception as e:
                print(f'Error parsing line {line}, {e}')
                traceback.print_exc()

    def load_file_legacy(self, area_file):
        # Read all data from file
        file = open(area_folder_location + '/' + area_file, 'r')
        data = file.read()
        file.close()

        from core.engine import engine
        engine.reset()

        # Split data between tiles and entities by minus
        chunks = data.split('\n-')
        tile_map_data = chunks[0]
        entity_data = chunks[1]

        # Load map
        self.map = Map(tile_map_data, self.tile_types, True)

        # Load the entites
        self.entities = []
        entity_lines = entity_data.split('\n')[1:]
        for line in entity_lines:
            try:
                items = line.split(',')
                id = int(items[0])
                x = int(items[1])
                y = int(items[2])
                e = create_entity(id, x, y, items[3:])
                if not e.has(EntityPlaceholder):
                    e.add(EntityPlaceholder(id, items[3:]))
                self.entities.append(e)
                print(self.entities)
            except Exception as e:
                print(f"Error parsing line: {line}. {e}")