import sqlite3
cursor=None
connection=None


def main():
    global cursor
    global connection
    connection=sqlite3.connect('data/discord_login.db', check_same_thread=False)
    connection.execute(
    '''CREATE TABLE IF NOT EXISTS USERS
    (HASHED_ID      CHAR(60)    PRIMARY KEY     NOT NULL,
    SALT            CHAR(29)    NOT NULL,
    ACCESS_TOKEN    CHAR(18),
    REFRESH_TOKEN   CHAR(18))
    ''')
    cursor=connection.cursor()

def get_access_token(hashed_id):
    cursor.execute("SELECT ACCESS_TOKEN FROM USERS WHERE HASHED_ID=?",(hashed_id, ))
    return cursor.fetchone()[0]


def get_refresh_token(hashed_id):
    cursor.execute("SELECT REFRESH_TOKEN FROM USERS WHERE HASHED_ID=?",(hashed_id, ))
    return cursor.fetchone()[0]

def is_registered(hashed_id):
    cursor.execute("SELECT * FROM USERS WHERE HASHED_ID=?",(hashed_id,))
    return cursor.fetchall()!=[]

def add_user(hashed_id, salt, access_token, refresh_token):
    cursor.execute("INSERT INTO USERS (HASHED_ID, SALT, ACCESS_TOKEN, REFRESH_TOKEN) VALUES(?,?,?,?)", (hashed_id, salt, access_token, refresh_token))
    connection.commit()

def delete_user(hashed_id):
    cursor.execute("DELETE FROM USERS WHERE HASHED_ID=?",(hashed_id,))
    connection.commit()

def update_tokens(hashed_id, access_token, refresh_token):
    if not is_registered(hashed_id):
        return None
    cursor.execute("UPDATE USERS SELECT ACCESS_TOKEN=?, REFRESH_TOKEN=? WHERE HASHED_ID=?", (access_token, refresh_token, hashed_id))
    cursor.fetchall()
def print_user(hashed_id):
    cursor.execute("SELECT * FROM USERS WHERE HASHED_ID=?", (hashed_id, ))
    print(cursor.fetchall())
def print_all_users():
    cursor.execute("SELECT * FROM USERS")
    print(len(cursor.fetchall()),cursor.fetchall())
main()
print_all_users()
