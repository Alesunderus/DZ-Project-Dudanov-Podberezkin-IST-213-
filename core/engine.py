import pygame

from core.camera import create_screen
from core.input import keys_down

pygame.init()

engine = None
default_width = 1280
default_height = 720


class Engine:
    def __init__(self, game_title):
        global engine
        engine = self

        self.active_objs = []

        self.background_drawables = []
        self.drawables = []
        self.ui_drawables = []

        self.clear_color = (50, 150, 200)
        self.screen = create_screen(default_width, default_height, game_title)
        self.stages = {}
        self.current_stage = None

    def register(self, stage_name, func):
        self.stages[stage_name] = func

    def switch_to(self, stage_name):
        self.reset()
        self.current_stage = stage_name
        func = self.stages[stage_name]
        print(f'switching to {self.current_stage}')
        func()

    def run(self):
        clock = pygame.time.Clock()
        self.running = True
        while self.running:
            dt = clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    keys_down.add(event.key)
                elif event.type == pygame.KEYUP:
                    keys_down.remove(event.key)

            # Update code
            for a in self.active_objs:
                a.update(dt)

            # Draw code
            self.screen.fill(self.clear_color)
            for b in self.background_drawables:
                b.draw(self.screen)
            for s in self.drawables:
                s.draw(self.screen)
            for u in self.ui_drawables:
                u.draw(self.screen)

            pygame.display.flip()

        pygame.quit()

    def reset(self):
        from components.physics import reset_physics
        reset_physics()
        self.active_objs.clear()
        self.drawables.clear()
        self.ui_drawables.clear()
        self.background_drawables.clear()