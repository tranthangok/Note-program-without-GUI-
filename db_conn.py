from pathlib import Path
import sqlite3
import sys


DB_FILEPATH = Path.cwd() / './notes.db'
DB_CONN = sqlite3.connect(DB_FILEPATH) 


class DB:
    @staticmethod
    def loadSqlScript(filepath: str) -> str:
        content = ''
        try:
            with open(filepath,'r', encoding="UTF-8") as file:
                content = file.read()
        except:
            print(f"Failed to read '{filepath}'' file.")
            sys.exit(-1)
        return content

    @staticmethod
    def initializeDB() -> None:
        script = DB.loadSqlScript('setup.sql')
        cursor = DB_CONN.cursor()
        cursor.executescript(script)
        DB_CONN.commit()
        cursor.close()
        return None


