import sqlite3

def init_db():
    conn = sqlite3.connect('bichometria.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS pets
                 (codigo TEXT PRIMARY KEY, nome TEXT, tipo TEXT, tutor_nome TEXT, tutor_chat_id TEXT)''')
    conn.commit()
    conn.close()

def add_pet(codigo, nome, tipo, tutor_nome, tutor_chat_id):
    conn = sqlite3.connect('bichometria.db')
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO pets VALUES (?,?,?,?,?)",
              (codigo, nome, tipo, tutor_nome, tutor_chat_id))
    conn.commit()
    conn.close()

def get_pet(codigo):
    conn = sqlite3.connect('bichometria.db')
    c = conn.cursor()
    c.execute("SELECT * FROM pets WHERE codigo=?", (codigo,))
    pet = c.fetchone()
    conn.close()
    return pet

init_db()