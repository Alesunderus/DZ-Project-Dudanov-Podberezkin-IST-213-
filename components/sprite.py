import pygame

from core.camera import camera

loaded = {}

image_folder_location = 'static/images'

class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, is_ui = False):
        super().__init__()
        self.is_ui = is_ui
        if image in loaded:
            self.image = loaded[image]
        else:
            self.image = pygame.image.load(image_folder_location + '/' + image)
            loaded[image] = self.image
        from core.engine import engine
        engine.drawables.append(self)

    def breakdown(self):
        from core.engine import engine
        engine.drawables.remove(self)

    def draw(self, screen):
        pos = (self.entity.x - camera.x, self.entity.y - camera.y) \
                if not self.is_ui else (self.entity.x, self.entity.y)
        screen.blit(self.image, pos)

    def set_image(self, image):
        if image in loaded:
            self.image = loaded[image]
        else:
            self.image = pygame.image.load(image_folder_location + '/' + image)
            loaded[image] = self.image
