from db_config import get_connection

def add_guide(name, country, experience, languages):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO guides (name, country, experience, languages) VALUES (%s, %s, %s, %s)",
        (name, country, experience, languages)
    )
    conn.commit()
    cursor.close()
    conn.close()

def get_all_guides():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM guides")
    guides = cursor.fetchall()
    cursor.close()
    conn.close()
    return guides

def delete_guide(guide_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM guides WHERE id = %s", (guide_id,))
    conn.commit()
    cursor.close()
    conn.close()
