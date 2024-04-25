from db_conn import DB_CONN
from dataclasses import dataclass
import hashlib


@dataclass
class Note:
    id: int
    title: str
    content: str
    user_id: int

@dataclass
class User:
    id: int
    username: str
    password: str

class NoteDAO:
    @staticmethod
    def addNote(title: str, content: str, user_id: str) -> None:
        try: 
            query = "INSERT INTO note (title, content, user_id) VALUES (?, ?, ?)"
            info = (title, content, user_id)
            cursor = DB_CONN.cursor()
            cursor.execute(query, info)
            DB_CONN.commit()
            cursor.close()
        except:
            print("Error while inserting note.")
        return None
    
    @staticmethod
    def getNotes(user_id:int, limit: int = -1) -> list[Note]: 
        list_notes = []
        cursor = DB_CONN.cursor()
        query = "SELECT * FROM note"
        cursor.execute(query)
        records = cursor.fetchall()
        cursor.close()
        for record in records:
            note = Note(*record)
            list_notes.append(note)
        return list_notes
    
    @staticmethod
    def showNote(title: str) -> Note | None:
        query = "SELECT * FROM note WHERE title = ?"
        cursor = DB_CONN.cursor()
        cursor.execute(query, title)
        record = cursor.fetchone()
        DB_CONN.commit()
        cursor.close()
        note: Note 
        if record:
            note = Note(id=record[0], title=record[1], content=record[2], user_id= record[3])
        return note
    
    @staticmethod
    def editNote(note: Note) -> None:
        query = "UPDATE note SET content = ? WHERE id = ?"
        info = (note.content, note.id)
        cursor = DB_CONN.cursor()
        cursor.execute(query, info)
        DB_CONN.commit()
        cursor.close()
        return None
    
    @staticmethod
    def delNote(title: str) -> int:
        query = "DELETE FROM note WHERE title = ?"
        cursor = DB_CONN.cursor()
        cursor.execute(query, title)
        DB_CONN.commit()
        deleted_num = cursor.rowcount
        cursor.close()
        return deleted_num

class UserDAO:
    @staticmethod
    def checkUser(username: str, password: str) -> tuple[bool,str]:
        query = "SELECT * FROM user"
        cursor = DB_CONN.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        DB_CONN.commit()
        cursor.close()

        login = False
        en_pass = hashlib.md5(password.encode()).hexdigest()
        global user_id
        user_id = ''
        en_pass = hashlib.md5(password.encode()).hexdigest()
        for record in records:
            if username == record[1] and en_pass == record[2]:
                login = True
                user_id = record[0]
        return login, user_id
    
    @staticmethod
    def addUser(username: str, password: str) -> None:
        try:    
            en_pass = hashlib.md5(password.encode()).hexdigest()            
            query = "INSERT INTO user (name, password) VALUES (?, ?)"
            info = (username, en_pass)
            cursor = DB_CONN.cursor()
            cursor.execute(query, info)
            DB_CONN.commit()
            cursor.close()
        except:
            print("Error while inserting user.")
        return None