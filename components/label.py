import pygame

from core.input import is_mouse_just_pressed, is_key_just_press, keys_just_pressed

fonts = []

anti_alias = True
font_folder_path = 'static/fonts'


class Label:
    def __init__(self, font, text, size = 32, color = (255,255,255)):
        from core.engine import engine
        global labels
        self.color = color
        if font in fonts:
            self.font = font
        else:
            self.font = pygame.font.Font(font_folder_path + '/' + font, size)

        self.set_text(text)
        engine.ui_drawables.append(self)

    def get_bounds(self):
        return pygame.Rect(0,0,self.surface.get_width(), self.surface.get_height())

    def breakdown(self):
        from core.engine import engine
        engine.ui_drawables.remove(self)

    def set_text(self, text):
        self.text = text
        self.surface = self.font.render(self.text, anti_alias, self.color)
        self.shadow_surface = self.font.render(self.text, anti_alias, (0,0,0))

    def draw(self, screen):
        screen.blit(self.shadow_surface, (self.entity.x+1, self.entity.y+1))
        screen.blit(self.surface, (self.entity.x, self.entity.y))


class InputText(Label):
    def __init__(self, font, text, size = 32, color = (255,255,255), click_area = pygame.Rect(0,0,32,32)):
        super().__init__(font, text, size, color)
        self.active = False
        self.background = pygame.Surface((click_area.width, click_area.height))
        self.background.fill(color = (5, 20, 50))
        from core.engine import engine
        engine.active_objs.append(self)
        self.click_area = click_area

    def update(self, dt):
        mouse_pos = pygame.mouse.get_pos()


        x = self.click_area.x + self.entity.x
        y = self.click_area.y + self.entity.y

        if is_mouse_just_pressed(0):
            print(self.active)
            if x <= mouse_pos[0] <= x + self.click_area.width and \
                y <= mouse_pos[1] <= y + self.click_area.height:
                self.active = True
            else:
                self.active = False

        if self.active:
            if is_key_just_press(pygame.K_BACKSPACE):
                self.text = self.text[:-1]
            else:
                if (len(keys_just_pressed) > 0):
                    key = keys_just_pressed[1]
                    print(key)
                    self.text += key
            super().set_text(self.text)

    def draw(self, screen):
        screen.blit(self.background, (self.entity.x, self.entity.y))
        screen.blit(self.shadow_surface, (self.entity.x+1, self.entity.y+1))
        screen.blit(self.surface, (self.entity.x, self.entity.y))