from db_config import get_connection

def login(username, password):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def register(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    if cursor.fetchone():
        return False, "Пользователь уже существует"
    cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, 'user')", (username, password))
    conn.commit()
    cursor.close()
    conn.close()
    return True, "Регистрация прошла успешно"
