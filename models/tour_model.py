from db_config import get_connection

def search_tours(country=None, max_price=None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = "SELECT * FROM tours WHERE 1=1"
    params = []

    if country:
        query += " AND country LIKE %s"
        params.append(f"%{country}%")
    if max_price:
        query += " AND price <= %s"
        params.append(max_price)

    cursor.execute(query, params)
    result = cursor.fetchall()

    cursor.close()
    conn.close()
    
    return result
def add_tour(title, country, start_date, end_date, price, description):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO tours (title, country, start_date, end_date, price, description)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (title, country, start_date, end_date, price, description))
    conn.commit()
    cursor.close()
    conn.close()

