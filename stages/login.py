import pygame

from components.entity import Entity
from components.button import Button
from components.label import Label, InputText
from components.sprite import Sprite
from core.camera import camera
from redact_db import find_account

login = ''
password = ''

def login():
    menu_label = Entity(Label('Montserrat-Medium.ttf', 'Enter account',
                              80, (255, 255, 0)))
    login_btn = Entity(Label('Montserrat-Medium.ttf', 'Log in',
                                 80, (255, 255, 0)))
    register_btn = Entity(Label('Montserrat-Medium.ttf', 'Create account',
                            40, (255, 255, 0)))
    login_label = Entity(Label('Montserrat-Medium.ttf', 'Login',
                                40, (255, 255, 0)))
    password_label = Entity(Label('Montserrat-Medium.ttf', 'Password',
                                40, (255, 255, 0)))
    login_input = Entity(InputText('Montserrat-Medium.ttf', 'login',
                                   60, (255, 255, 0), click_area=pygame.Rect(0, 0, 600, 90)))
    password_input = Entity(InputText('Montserrat-Medium.ttf', 'password',
                                      60, (255, 255, 0), click_area=pygame.Rect(0, 0, 600, 90)))
    global login
    login = login_input
    global password
    password = password_input

    menu_label_size = menu_label.get(Label).get_bounds()
    login_btn_size = login_btn.get(Label).get_bounds()
    register_btn_size = register_btn.get(Label).get_bounds()

    menu_label.x = camera.width / 2 - menu_label_size.width / 2
    menu_label.y = camera.height - 700
    login_btn.x = camera.width / 2 - login_btn_size.width/2
    login_btn.y = camera.height - 200
    register_btn.x = camera.width / 2 - register_btn_size.width / 2
    register_btn.y = camera.height - 100
    login_label.x = camera.width / 2 - 300
    login_label.y = camera.height - 550
    password_label.x = camera.width / 2 - 300
    password_label.y = camera.height - 375
    login_input.x = camera.width / 2 - 300
    login_input.y = camera.height - 500
    password_input.x = camera.width / 2 - 300
    password_input.y = camera.height - 325

    login_btn.add(Button(enter_account, login_btn_size))
    register_btn.add(Button(switch_to_register, register_btn_size))

def enter_account():
    value = find_account(login.get(InputText).text)
    print(value)
    if value is not None:
        if value[2] == password.get(InputText).text:
            print('Entered account')
            from core.engine import engine
            engine.account = value
            engine.switch_to('Menu')
        else:
            print('Wrong password')
    else:
        print('Account doesnt exist')

def switch_to_register():
    from core.engine import engine
    engine.switch_to('Register')