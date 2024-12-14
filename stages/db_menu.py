from redact_db import create_database, populate_tables, create_interface

db_path = 'db/game_database.db'

def db_menu():
    create_database()
    populate_tables()
    create_interface()