import pygame

from components.entity import Entity
from components.button import Button
from components.label import Label, InputText
from components.sprite import Sprite
from core.camera import camera
from redact_db import find_account, create_account

login = ''
password = ''
email = ''

def register():
    menu_label = Entity(Label('Montserrat-Medium.ttf', 'Enter account',
                              80, (255, 255, 0)))
    register_btn = Entity(Label('Montserrat-Medium.ttf', 'Register',
                                 80, (255, 255, 0)))
    login_btn = Entity(Label('Montserrat-Medium.ttf', 'Log in',
                            40, (255, 255, 0)))
    email_label = Entity(Label('Montserrat-Medium.ttf', 'Email',
                               40, (255, 255, 0)))
    login_label = Entity(Label('Montserrat-Medium.ttf', 'Login',
                                40, (255, 255, 0)))
    password_label = Entity(Label('Montserrat-Medium.ttf', 'Password',
                                40, (255, 255, 0)))
    email_input = Entity(InputText('Montserrat-Medium.ttf', 'Email',
                                   60, (255, 255, 0), click_area=pygame.Rect(0, 0, 600, 90)))
    login_input = Entity(InputText('Montserrat-Medium.ttf', 'login',
                                   60, (255, 255, 0), click_area=pygame.Rect(0, 0, 600, 90)))
    password_input = Entity(InputText('Montserrat-Medium.ttf', 'password',
                                      60, (255, 255, 0), click_area=pygame.Rect(0, 0, 600, 90)))
    global login
    login = login_input
    global password
    password = password_input
    global email
    email = email_input

    menu_label_size = menu_label.get(Label).get_bounds()
    login_btn_size = login_btn.get(Label).get_bounds()
    register_btn_size = register_btn.get(Label).get_bounds()

    menu_label.x = camera.width / 2 - menu_label_size.width / 2
    menu_label.y = camera.height - 700
    register_btn.x = camera.width / 2 - register_btn_size.width/2
    register_btn.y = camera.height - 150
    login_btn.x = camera.width / 2 - login_btn_size.width / 2
    login_btn.y = camera.height - 50
    email_label.x = camera.width / 2 - 300
    email_label.y = camera.height - 600
    email_input.x = camera.width / 2 - 300
    email_input.y = camera.height - 550
    login_label.x = camera.width / 2 - 300
    login_label.y = camera.height - 450
    password_label.x = camera.width / 2 - 300
    password_label.y = camera.height - 300
    login_input.x = camera.width / 2 - 300
    login_input.y = camera.height - 400
    password_input.x = camera.width / 2 - 300
    password_input.y = camera.height - 250

    register_btn.add(Button(create_new_account, register_btn_size))
    login_btn.add(Button(switch_to_login, login_btn_size))

def create_new_account():
    value = find_account(login.get(InputText).text)
    print(value)
    if value is not None:
        print('Account with this login already exists')
    else:
        if len(login.get(InputText).text) > 0 and len(password.get(InputText).text) and len(email.get(InputText).text):
            create_account(login.get(InputText).text, password.get(InputText).text, email.get(InputText).text)
            value = find_account(login.get(InputText).text)
            print(value)
            if value is not None:
                from core.engine import engine
                engine.account = value
                engine.switch_to('Menu')
            else:
                print('Error saving data')
        else:
            print('Fill all fields')

def switch_to_login():
    from core.engine import engine
    engine.switch_to('Login')