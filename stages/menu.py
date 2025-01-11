import json
import shutil

from components.entity import Entity
from components.button import Button
from components.label import Label
from components.sprite import Sprite
from core.camera import camera
from redact_db import find_progress, create_assign_progress, find_account
from stages.play import set_wave_count
from gamedata.items_types import item_types

def writeTofile(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)
    print("Stored blob data into: ", filename, "\n")

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

    from core.engine import engine
    print(engine.account)
    if engine.account[4] is not None:
        row = find_progress(engine.account[4])
        if not engine.loaded_progress:
            if row[4] is not None:
                writeTofile(row[4], 'static/maps/load.map')
                set_wave_count(row[1])
                engine.loaded_progress = True
            else:
                shutil.copyfile('static/maps/start.map', 'static/maps/load.map')
                engine.loaded_progress = True
            if row[3] is not None:
                inventory_data = json.loads(row[3])
                from components.player import inventory
                inventory.add(item_types[0], inventory_data['Wood'])
                inventory.add(item_types[4], inventory_data['Stone'])
    else:
        create_assign_progress(engine.account[0])
        engine.account = find_account(engine.account[1])
        print(engine.account)
        shutil.copyfile('static/maps/start.map', 'static/maps/load.map')
        engine.loaded_progress = True
