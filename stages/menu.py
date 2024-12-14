from components.entity import Entity
from components.button import Button
from components.label import Label
from components.sprite import Sprite
from core.camera import camera

def new_game():
    from core.engine import engine
    engine.switch_to('Play')

def edit_db():
    from core.engine import engine
    engine.switch_to('DB')

def quit_game():
    from core.engine import engine
    engine.running = False

def menu():
    menu_label = Entity(Label('Montserrat-Medium.ttf', 'Main Menu',
                                80, (255, 255, 0)))
    new_game_btn = Entity(Label('Montserrat-Medium.ttf', 'New Game',
                                80, (255,255,0)))
    db_btn = Entity(Label('Montserrat-Medium.ttf', 'Edit data base',
                                 80, (255, 255, 0)))
    quit_game_btn = Entity(Label('Montserrat-Medium.ttf', 'Quit Game',
                                80, (255, 255, 0)))

    menu_label_size = menu_label.get(Label).get_bounds()
    new_btn_size = new_game_btn.get(Label).get_bounds()
    quit_btn_size = quit_game_btn.get(Label).get_bounds()
    db_btn_size = db_btn.get(Label).get_bounds()
    menu_label.x = camera.width / 2 - menu_label_size.width / 2
    menu_label.y = camera.height - 700
    new_game_btn.x = camera.width / 2 - new_btn_size.width / 2
    new_game_btn.y = camera.height - 500
    db_btn.x = camera.width / 2 - db_btn_size.width / 2
    db_btn.y = camera.height - 350
    quit_game_btn.x = camera.width / 2 - quit_btn_size.width / 2
    quit_game_btn.y = camera.height - 200

    new_game_btn.add(Button(new_game, new_btn_size))
    db_btn.add(Button(edit_db, db_btn_size))
    quit_game_btn.add(Button(quit_game, quit_btn_size))
