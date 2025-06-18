from db_config import get_connection

def book_tour(client_id, tour_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO bookings (client_id, tour_id, booking_date)
        VALUES (%s, %s, CURDATE())
    """, (client_id, tour_id))
    conn.commit()
    cursor.close()
    conn.close()
    
def get_bookings_for_user(client_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT b.id, t.title, t.country, t.start_date, t.end_date, t.price
        FROM bookings b
        JOIN tours t ON b.tour_id = t.id
        WHERE b.client_id = %s
        ORDER BY b.booking_date DESC
    """, (client_id,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def delete_booking(booking_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM bookings WHERE id = %s", (booking_id,))
    conn.commit()
    cursor.close()
    conn.close()

