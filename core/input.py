import pygame

keys_down = set()
keys_just_pressed = []
scroll_delta = 0

def is_key_pressed(key):
    return key in keys_down

def is_key_just_press(key):
    return key in keys_just_pressed

def is_mouse_pressed(button):
    return pygame.mouse.get_pressed()[button]

def is_mouse_just_pressed(button):
    return pygame.mouse.get_just_pressed()[button]

def add_scroll_delta(amount):
    global scroll_delta
    scroll_delta += amount

def reset_scroll():
    global scroll_delta
    scroll_delta = 0