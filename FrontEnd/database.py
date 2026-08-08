import sqlite3

def get_connection():
    return sqlite3.connect('users.db', check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)')
    
    # Safely migrate database to support profile photos
    try:
        c.execute("ALTER TABLE users ADD COLUMN profile_photo BLOB")
    except sqlite3.OperationalError:
        pass # Column already exists
        
    c.execute('CREATE TABLE IF NOT EXISTS documents (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, doc_name TEXT, original_text TEXT, simplified_text TEXT)')
    conn.commit()
    conn.close()

def verify_user(username, password):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    result = c.fetchone()
    conn.close()
    return result is not None

def create_user(username, password):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()
    conn.close()

def update_profile_photo(username, photo_bytes):
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE users SET profile_photo=? WHERE username=?', (photo_bytes, username))
    conn.commit()
    conn.close()

def get_profile_photo(username):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT profile_photo FROM users WHERE username=?', (username,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def insert_document(username, doc_name, original_text, simplified_text):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO documents (username, doc_name, original_text, simplified_text) VALUES (?, ?, ?, ?)", 
              (username, doc_name, original_text, simplified_text))
    doc_id = c.lastrowid
    conn.commit()
    conn.close()
    return doc_id

def update_document_simplified(doc_id, simplified_text):
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE documents SET simplified_text = ? WHERE id = ?", (simplified_text, doc_id))
    conn.commit()
    conn.close()

def get_user_documents(username):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, doc_name, original_text, simplified_text FROM documents WHERE username=? ORDER BY id DESC", (username,))
    result = c.fetchall()
    conn.close()
    return result