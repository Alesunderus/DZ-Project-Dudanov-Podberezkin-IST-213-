import pygame

from core.camera import create_screen
from core.input import keys_down, keys_just_pressed, add_scroll_delta, reset_scroll
from stages.play import night_event, start_night, day_event, start_day

pygame.init()

engine = None
default_width = 1280
default_height = 720


class Engine:
    def __init__(self, game_title):
        self.step = 0
        global engine
        engine = self
        self.account = None

        self.active_objs = []

        self.background_drawables = []
        self.drawables = []
        self.ui_drawables = []

        self.usables = []

        self.clear_color = (50, 150, 50)
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
            reset_scroll()
            self.step += 1
            keys_just_pressed.clear()
            dt = clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    keys_down.add(event.key)
                    keys_just_pressed.append(event.key)
                    keys_just_pressed.append(event.unicode)
                elif event.type == pygame.KEYUP:
                    keys_down.remove(event.key)
                elif event.type == pygame.MOUSEWHEEL:
                    add_scroll_delta(event.y)

                if self.current_stage == 'Play':
                    if event.type == night_event:
                        start_night()
                    if event.type == day_event:
                        start_day()

            # Update code
            for a in self.active_objs:
                a.update(dt)

            # Draw code
            self.screen.fill(self.clear_color)
            for b in self.background_drawables:
                b.draw(self.screen)
            for s in self.drawables:
                s.draw(self.screen)
            from core.effect import effects
            for e in effects:
                e.draw(self.screen)
            for u in self.ui_drawables:
                u.draw(self.screen)

            pygame.display.flip()

        pygame.quit()

    def reset(self):
        from core.area import area
        if area is not None:
            e = area.entities.copy()
            for a in e:
                a.delete_self()
        from components.physics import reset_physics
        reset_physics()
        self.active_objs.clear()
        self.drawables.clear()
        self.ui_drawables.clear()
        self.background_drawables.clear()
        self.usables.clear()
        from core.effect import effects
        effects.clear()