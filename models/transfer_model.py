from db_config import get_connection

def add_transfer(city, date, description):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO transfers (city, date, description) VALUES (%s, %s, %s)",
        (city, date, description)
    )
    conn.commit()
    cursor.close()
    conn.close()

def get_all_transfers():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM transfers")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def delete_transfer(transfer_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transfers WHERE id = %s", (transfer_id,))
    conn.commit()
    cursor.close()
    conn.close()
