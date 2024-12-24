from redact_db import create_database, populate_tables, create_interface, fetch_table_data

db_path = 'db/game_database.db'

def db_menu():
    create_database()
    create_interface()