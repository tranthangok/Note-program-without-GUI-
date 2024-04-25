
from model_note import Note, NoteDAO, UserDAO
from kirje import Kirje, KirjeDetails

ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-0123456789"
RESTRICTED = "ÄäÖöÅå"

global login
global username
global records

class MenuNote:
    def showLogin(self) -> None:
        print("""Options:""")
        print("1 - Login")
        print("2 - Register")
        print("0 - Exit")
        return None
    def showOptions(self, username)-> None:
        print(f"""User '{username}' options:""")
        print("1 - List notes")
        print("2 - View note")
        print("3 - Add note")
        print("4 - Edit note")
        print("5 - Delete note")
        print("0 - Logout")
        return None
    def askChoice(self) -> int:
        choice = int(input("Your choice: "))
        return choice
    def askUsername(self) -> str:
        username = input("Insert username: ")
        return username
    def askPass(self) -> str:
        password = input("Insert password: ")
        return password
    
    def check_username(self, character): 
        checkcharacter = True
        lencharacter = True
        if len(character) < 4:
            print(f"Username must be minimum of '4' characters long.")
            lencharacter = False
        elif len(character) > 10:
            print(f"Username must be maximum of '10' characters long.")
            lencharacter = False
        for char in character:
            if char not in ALPHABET or char in RESTRICTED:
                checkcharacter = False
            else: pass
        if checkcharacter == False:
            print("Username can only contain:")
            print("1. Lower case characters 'a-z'")
            print("2. Upper case characters 'A-Z'")
            print("3. Special characters '_' and '-'")
        if lencharacter == True and checkcharacter == True:
            check_user = True
        else:
            check_user = False
        return check_user
    
    def check_pass(self, character): 
        checkcharacter = True
        lencharacter = True
        if len(character) < 4:
            print(f"Password must be minimum of '4' characters long.")
            lencharacter = False
        elif len(character) > 10:
            print(f"Password must be maximum of '10' characters long.")
            lencharacter = False
        for char in character:
            if char not in ALPHABET or char in RESTRICTED:
                checkcharacter = False
            else: pass
        if checkcharacter == False:
            print("Password can only contain:")
            print("1. Lower case characters 'a-z'")
            print("2. Upper case characters 'A-Z'")
            print("3. Special characters '_' and '-'")
        if lencharacter == True and checkcharacter == True:
            check_pass = True
        else:
            check_pass = False
        return check_pass

    def login(self) -> tuple[bool, str]:
        login = False
        print("Insert credentials below:")
        username = self.askUsername()
        password = self.askPass()
        (login,user_id) = UserDAO.checkUser(username, password)
        if login == True:
            print("Authenticated!")
        else:
            print("Failed to authenticate!")
        return login, username, user_id
    
    def register(self):
        username = self.askUsername()
        check_user = self.check_username(username)
        if check_user == True:
            password = self.askPass()
            check_pass = self.check_pass(password)
            if check_pass == True:
                re_password = input("Insert password again: ")
                if password == re_password:
                    UserDAO.addUser(username, password)
                    print("Registration completed!")
        return None

    def listNotes(self,user_id):
        memos = NoteDAO.getNotes(user_id)
        if len(memos) >= 1:
            rows = []
            for memo in memos:
                rows.append(f"{memo.id} - {memo.title}")
            row = '\n'.join(rows) 
            memo_details = KirjeDetails(
                content= row,
                header_separation=" - ",
                headers={
                    'ID': 'Title',
                    'Title': ' notes '
                }
            )
            memo_list = Kirje(memo_details)
            memo_list.display("streamlined")
        else:
            print("There are no notes.")
        return None
    

    def viewNote(self):
        title = input("Search note by title: ")
        note = NoteDAO.showNote(title)
        if note:
            details = KirjeDetails(
                content = note.content,
                header_separation=" - ",
                headers={
                    'ID' : note.id,
                    'Title': note.title
                }
            )
            current_memo = Kirje(details)
            current_memo.display('default')
        else:
            print("Not found.")
        return None
    

    def addNote(self, user_id):
        title = input("Insert title: ")
        num_rows = int(input("Insert the amount of rows: "))
        rows: list[str] = []
        i = 0
        while num_rows > i:
            i += 1
            row_content = input(f"Insert row {i}: ")
            rows.append(row_content)
        content = '\n'.join(rows)
        NoteDAO.addNote(title, content, user_id)
        del rows
        print("Note stored!")
        return None


    def editNote(self):
        title = input("Insert note title: ")
        note = NoteDAO.showNote(title)
        if note:
            rows = note.content.split('\n')
            user_input = int(input(f"Insert row number to edit 1-{len(rows)}, 0 to cancel: "))
            row_num = user_input - 1
            if row_num == -1:
                print("Cancelled.")
            else:
                replace_content = input("Insert replacement row: ")
                rows[row_num] = replace_content
                note.content = '\n'.join(rows)
                NoteDAO.editNote(note)
                print("Edit completed!")
        else:
            print(f"'{title}' not found.")
        return None
    

    def deleteNote(self):
        title = input("Delete note (insert title): ")
        deleted_num = NoteDAO.delNote(title)
        if deleted_num == 1:
            print("Note deleted.")
        else:
            print(f"'{title}' not found.")
        return None



    def activate(self):
        login = False
        while True:
            self.showLogin()
            choice = self.askChoice()
            if choice == 0:
                print()
                break
            elif choice == 1:
                login, username, user_id = self.login()
                while login == True:
                    print()
                    self.showOptions(username)
                    choice = self.askChoice()
                    if choice == 0:
                        break
                    elif choice == 1:
                        self.listNotes(user_id)
                    elif choice == 2:
                        self.viewNote()
                    elif choice == 3:
                        self.addNote(int(user_id))
                    elif choice == 4:
                        self.editNote() 
                    elif choice == 5:
                        self.deleteNote()
                    else: print('Unknown option, try again.')
            elif choice == 2:
                self.register()
            print()
        return None 