import sqlite3
import os
from tkinter import Tk, Frame, Button, Listbox, Scrollbar, Entry, Label, END, Toplevel, StringVar, OptionMenu, filedialog

db_path = 'db/game_database.db'

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data

# --- Создание базы данных и таблиц ---
def create_database():
    print(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()


    # Таблица аккаунтов игроков
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS player_account (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        login TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        progress_id INTEGER,
        FOREIGN KEY (progress_id) REFERENCES player_progress(ID)
    )
    """)


    # Таблица прогресса игроков
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS player_progress (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        current_wave INTEGER,
        tech_matrix TEXT,
        characteristics TEXT,
        area_file BLOB
    )
    """)


    # Таблица врагов
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS enemies (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        sprite TEXT NOT NULL,
        health INTEGER NOT NULL,
        speed REAL NOT NULL,
        damage INTEGER NOT NULL,
        first_wave INTEGER NOT NULL,
        spawn_cost INTEGER NOT NULL
    )
    """)


    # Таблица технологий
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS technologies (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        icon TEXT NOT NULL,
        resource_cost INTEGER NOT NULL,
        unlocks TEXT,
        required_tech TEXT
    )
    """)


    # Таблица построек
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS buildings (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        sprite_inactive TEXT NOT NULL,
        sprite_active TEXT NOT NULL,
        projectile_sprite TEXT NOT NULL,
        damage_type TEXT NOT NULL,
        damage INTEGER NOT NULL,
        health INTEGER NOT NULL,
        resource_cost INTEGER NOT NULL
    )
    """)

    conn.commit()
    conn.close()


# --- Заполнение таблиц тестовыми данными ---
def populate_tables():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        players = [("player1", "hashed_pass1", "player1@example.com", None),
                   ("player2", "hashed_pass2", "player2@example.com", None)]

        progress = [(1, '{"tech1": true}', '{"hp": 100}', '{"x": 0, "y": 0}'),
                    (2, '{"tech2": true}', '{"hp": 200}', '{"x": 10, "y": 10}')]

        enemies = [("enemy1.png", 100, 1.5, 10, 1, 50),
                   ("enemy2.png", 200, 2.0, 20, 2, 100)]

        technologies = [("tech1.png", 100, '{"unlocks": "tech2"}', '{"required": null}'),
                        ("tech2.png", 200, '{"unlocks": "tech3"}', '{"required": "tech1"}')]

        buildings = [("inactive1.png", "active1.png", "projectile1.png", "fire", 50, 100, 500),
                     ("inactive2.png", "active2.png", "projectile2.png", "ice", 70, 150, 700)]

        cursor.executemany("INSERT OR IGNORE INTO player_account (login, password, email, progress_id) VALUES (?, ?, ?, ?)", players)
        cursor.executemany("INSERT OR IGNORE INTO player_progress (current_wave, tech_matrix, characteristics, buildings_coordinates) VALUES (?, ?, ?, ?)", progress)
        cursor.executemany("INSERT OR IGNORE INTO enemies (sprite, health, speed, damage, first_wave, spawn_cost) VALUES (?, ?, ?, ?, ?, ?)", enemies)
        cursor.executemany("INSERT OR IGNORE INTO technologies (icon, resource_cost, unlocks, required_tech) VALUES (?, ?, ?, ?)", technologies)
        cursor.executemany("INSERT OR IGNORE INTO buildings (sprite_inactive, sprite_active, projectile_sprite, damage_type, damage, health, resource_cost) VALUES (?, ?, ?, ?, ?, ?, ?)", buildings)

    except sqlite3.IntegrityError:
        print("Данные уже существуют, пропускаем добавление.")

    conn.commit()
    conn.close()


# --- Добавление записи в таблицу ---
def add_record_to_table(table_name, values):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(f"PRAGMA table_info({table_name})")
    fields = [column[1] for column in cursor.fetchall() if column[1] != "ID"]
    placeholders = ", ".join(["?"] * len(fields))

    cursor.execute(f"INSERT INTO {table_name} ({', '.join(fields)}) VALUES ({placeholders})", values)
    conn.commit()
    conn.close()


# --- Интерфейс для добавления записи ---
def open_add_record_window(selected_table):
    def submit_record():
        values = [entry.get() for entry in entries]

        # Если это таблица с изображениями, обрабатываем путь спрайта
        if selected_table in ("enemies", "technologies", "buildings"):
            file_path = filedialog.askopenfilename(title="Выберите файл изображения")
            if file_path:
                sprite_name = os.path.basename(file_path)
                dest_dir = os.path.join(os.getcwd(), "sprites")
                os.makedirs(dest_dir, exist_ok=True)
                dest_path = os.path.join(dest_dir, sprite_name)
                os.rename(file_path, dest_path)
                values[0] = dest_path  # Сохраняем путь в базе

        add_record_to_table(selected_table, values)
        add_window.destroy()

    add_window = Toplevel()
    add_window.title(f"Добавление записи в {selected_table}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({selected_table})")
    fields = [column[1] for column in cursor.fetchall() if column[1] != "ID"]
    conn.close()

    entries = []
    for field in fields:
        Label(add_window, text=field).pack()
        entry = Entry(add_window, width=50)
        entry.pack()
        entries.append(entry)

    Button(add_window, text="Добавить запись", command=submit_record).pack(pady=10)


# --- Просмотр данных таблиц ---
def fetch_table_data(table_name):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    conn.close()
    return rows


def update_listbox(table_name, listbox):
    listbox.delete(0, END)
    rows = fetch_table_data(table_name)
    for row in rows:
        listbox.insert(END, row)


# --- Основной интерфейс ---
def create_interface():
    root = Tk()
    root.title("Управление базой данных")

    frame = Frame(root)
    frame.pack(pady=20)

    listbox = Listbox(frame, width=100, height=20)
    listbox.pack(side="left")

    scrollbar = Scrollbar(frame, command=listbox.yview)
    scrollbar.pack(side="right", fill="y")
    listbox.config(yscrollcommand=scrollbar.set)

    # Выбор таблицы
    selected_table = StringVar(root)
    selected_table.set("player_account")  # Значение по умолчанию

    tables = ["player_account", "player_progress", "enemies", "technologies", "buildings"]
    table_menu = OptionMenu(root, selected_table, *tables)
    table_menu.pack(pady=5)

    # Кнопка для добавления записи
    Button(root, text="Добавить запись", command=lambda: open_add_record_window(selected_table.get())).pack(pady=5)

    # Кнопка для обновления данных
    Button(root, text="Показать таблицу", command=lambda: update_listbox(selected_table.get(), listbox)).pack(pady=5)

    root.mainloop()

    from core.engine import engine
    engine.switch_to('Menu')

def find_account(typed_login):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM player_account WHERE login = '{typed_login}'")
    row = cursor.fetchone()
    conn.close()
    return row

def create_account(login, password, email):
    data = (login, password, email, None)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO player_account (login, password, email, progress_id) VALUES (?, ?, ?, ?)", data)
    conn.commit()
    cursor.close()

def find_progress(progress_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM player_progress WHERE ID = '{progress_id}'")
    row = cursor.fetchone()
    conn.close()
    return row

def create_assign_progress(player_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO player_progress (current_wave, tech_matrix, characteristics, area_file) VALUES (?, ?, ?, ?)", (1,None,None,None))
    progress_id = cursor.lastrowid
    cursor.execute(f"UPDATE player_account SET progress_id = '{progress_id}' WHERE ID = '{player_id}'")
    conn.commit()
    conn.close()

def import_area_file(progress_id):
    blob = convertToBinaryData('static/maps/load.map')
    print(blob)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = "UPDATE player_progress SET area_file =? WHERE ID =?"
    cursor.execute(query,(blob,progress_id))
    conn.commit()
    conn.close()

# --- Основной код ---
if __name__ == "__main__":
    create_database()
    create_interface()
