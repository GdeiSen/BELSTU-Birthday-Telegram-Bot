#create class to export database
import sqlite3 as sl
class Database:
    def create(self):
        con = sl.connect('data.db')
        with con:
            con.execute("""
                CREATE TABLE USER (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    telegram_id INTEGER,
                    block INTEGER,
                    name TEXT,
                    admin INTEGER,
                    ended INTEGER
                );
            """)
            con.execute("""
                CREATE TABLE TASK (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    description TEXT,
                    points INTEGER,
                    fullDescription TEXT,
                    photo TEXT,
                    hint TEXT
                );
            """)
            con.execute("""
                CREATE TABLE USER_TASK (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    task_id INTEGER,
                    status TEXT,
                    FOREIGN KEY (user_id) REFERENCES USER (id),
                    FOREIGN KEY (task_id) REFERENCES TASK (id)
                );
            """)

    def drop(self):
        con = sl.connect('data.db')
        with con:
            con.execute("""
                DROP TABLE USER
            """)
            con.execute("""
                DROP TABLE TASK
            """)
            con.execute("""
                DROP TABLE USER_TASK
            """)

    async def add_user(self, telegram_id, block, name, admin = 0, ended = 0):
        con = sl.connect('data.db')
        with con:
            con.execute("""
                INSERT INTO USER (telegram_id, block, name, admin, ended) VALUES (?, ?, ?, ?, ?)
            """, (telegram_id, block, name, admin, ended))
    
    def add_task(self, name, description, points, fullDescription, photo, hint):
        con = sl.connect('data.db')
        with con:
            con.execute("""
                INSERT INTO TASK (name, description, points, fullDescription, photo, hint) VALUES (?, ?, ?, ?, ?, ?)
            """, (name, description, points, fullDescription, photo, hint))

    async def add_user_task(self, user_id, task_id, status):
        con = sl.connect('data.db')
        with con:
            con.execute("""
                INSERT INTO USER_TASK (user_id, task_id, status) VALUES (?, ?, ?)
            """, (user_id, task_id, status))
    
    async def get_user(self, telegram_id):
        con = sl.connect('data.db')
        with con:
            data = con.execute("""
                SELECT * FROM USER WHERE telegram_id = ?
            """, (telegram_id,)).fetchone()
            return data
        
    async def get_user_by_id(self, id):
        con = sl.connect('data.db')
        with con:
            data = con.execute("""
                SELECT * FROM USER WHERE id = ?
            """, (id,)).fetchone()
            return data
        
    async def get_task(self, id):
        con = sl.connect('data.db')
        with con:
            data = con.execute("""
                SELECT * FROM TASK WHERE id = ?
            """, (id,)).fetchone()
            return data
        
    async def get_user_task(self, user_id, task_id):
        con = sl.connect('data.db')
        with con:
            data = con.execute("""
                SELECT * FROM USER_TASK WHERE user_id = ? AND task_id = ?
            """, (user_id, task_id)).fetchone()
            return data
        
    async def get_user_tasks(self, user_id):
        con = sl.connect('data.db')
        with con:
            data = con.execute("""
                SELECT * FROM USER_TASK WHERE user_id = ?
            """, (user_id,)).fetchall()
            return data
        
    async def get_all_tasks(self):
        con = sl.connect('data.db')
        with con:
            data = con.execute("""
                SELECT * FROM TASK
            """).fetchall()
            return data
        
    async def get_all_users(self):
        con = sl.connect('data.db')
        with con:
            data = con.execute("""
                SELECT * FROM USER
            """).fetchall()
            return data
        
    async def delete_user(self, telegram_id):
        con = sl.connect('data.db')
        with con:
            con.execute("""
                DELETE FROM USER WHERE telegram_id = ?
            """, (telegram_id,))

    async def delete_task(self, id):
        con = sl.connect('data.db')
        with con:
            con.execute("""
                DELETE FROM TASK WHERE id = ?
            """, (id,))

    async def delete_user_task(self, user_id, task_id):
        con = sl.connect('data.db')
        with con:
            con.execute("""
                DELETE FROM USER_TASK WHERE user_id = ? AND task_id = ?
            """, (user_id, task_id))

    async def update_user_task(self, user_id, task_id, status):
        con = sl.connect('data.db')
        with con:
            con.execute("""
                UPDATE USER_TASK SET status = ? WHERE user_id = ? AND task_id = ?
            """, (status, user_id, task_id))

    async def block_user(self, id):
        con = sl.connect('data.db')
        with con:
            con.execute("""
                UPDATE USER SET block = 1 WHERE id = ?
            """, (id,))

    async def unblock_user(self, id):
        con = sl.connect('data.db')
        with con:
            con.execute("""
                UPDATE USER SET block = 0 WHERE id = ?
            """, (id,))

    async def end_user(self, id):
        con = sl.connect('data.db')
        with con:
            con.execute("""
                UPDATE USER SET ended = 1 WHERE id = ?
            """, (id,))

    async def unend_user(self, id):
        con = sl.connect('data.db')
        with con:
            con.execute("""
                UPDATE USER SET ended = 0 WHERE id = ?
            """, (id,))

    async def update_task(self, id, name, description, points, fullDescription, photo):
        con = sl.connect('data.db')
        with con:
            con.execute("""
                UPDATE TASK SET name = ?, description = ?, points = ?, fullDescription = ?, photo = ? WHERE id = ?
            """, (name, description, points, fullDescription, photo, id))