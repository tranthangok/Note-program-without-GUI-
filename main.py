from model_note import NoteDAO
from db_conn import DB_CONN,DB
from menu_note import MenuNote
import sqlite3

class Main:
    def __init__(self) -> None:
        print('Program starting.')
        try:
            DB.initializeDB()
        except: pass    
        obj = MenuNote()
        obj.activate()
        DB_CONN.close()
        print('Program ending.')
        return None

if __name__ == '__main__':
    app = Main()