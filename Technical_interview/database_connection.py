import sqlite3

def create_tables():
    try:
        conn = sqlite3.connect('wheather.db')
        print("Connection established.")
        c = conn.cursor()
        #with conn:
        c.execute('SELECT * FROM sqlite_master')
        print(c.fetchone())
        conn.commit()
    except sqlite3.ProgrammingError as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()
            print("Connection closed.")

create_tables()