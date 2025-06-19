from db_config import get_connection

def login(username, password):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user  # возвращается словарь с ключами: id, username, password, role, food_preferences, allergies

def register(username, password, food_pref, allergies):
    conn = get_connection()
    cursor = conn.cursor()

    # проверка на существующего пользователя
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    if cursor.fetchone():
        return False, "Пользователь уже существует"

    cursor.execute(
        "INSERT INTO users (username, password, role, food_preferences, allergies) VALUES (%s, %s, %s, %s, %s)",
        (username, password, 'user', food_pref, allergies)
    )

    conn.commit()
    cursor.close()
    conn.close()
    return True, "Регистрация успешна"
