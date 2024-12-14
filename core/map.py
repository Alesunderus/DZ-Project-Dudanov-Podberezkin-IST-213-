from math import ceil

import pygame

map = None

map_folder_location = 'static/maps'
image_folder_location = 'static/images'
tile_size = 32


class TileKind:
    def __init__(self, name, image, is_solid):
        self.name = name
        self.image = pygame.image.load(image_folder_location + '/' + image)
        self.is_solid = is_solid


class Map:
    def __init__(self, data, tile_kinds):
        from core.engine import engine
        engine.background_drawables.append(self)
        self.tile_kinds = tile_kinds

        # set up the tiles
        self.tiles = []
        for line in data.split('\n'):
            row =[]
            for tile_number in line:
                row.append(int(tile_number))
            self.tiles.append(row)

        # tiles size
        self.tile_size = tile_size

    def is_point_solid(self, x, y):
        x_tile = int(x/self.tile_size)
        y_tile = int(y/self.tile_size)
        if x_tile <= 0 or y_tile <= 0 or \
            y_tile >= len(self.tiles) or \
            x_tile >= len(self.tiles[y_tile]):
            return True
        tile = self.tiles[y_tile][x_tile]
        return self.tile_kinds[tile].is_solid

    def is_rect_solid(self, x, y, width, height):
        x_checks = int(ceil(width/self.tile_size))
        y_checks = int(ceil(height/self.tile_size))
        for yi in range(y_checks):
            for xi in range(x_checks):
                x = xi * self.tile_size + x
                y = yi * self.tile_size + y
                if self.is_point_solid(x, y):
                    return True
        if self.is_point_solid(x + width, y):
            return True
        if self.is_point_solid(x, y + height):
            return True
        if self.is_point_solid(x + width, y + height):
            return True
        return False

    def draw (self, screen):
        from core.camera import camera
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                location = (x * self.tile_size - camera.x, y * self.tile_size - camera.y)
                image = self.tile_kinds[tile].image
                screen.blit(image, location)