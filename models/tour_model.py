from db_config import get_connection

def search_tours(country=None, max_price=None, allergy_exclude=None, food_preference=None):
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
    if allergy_exclude:
        for allergen in allergy_exclude:
            query += " AND description NOT LIKE %s"
            params.append(f"%{allergen}%")
    if food_preference:
        query += " AND description LIKE %s"
        params.append(f"%{food_preference.lower()}%")

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

def get_all_tours():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tours ORDER BY start_date")
    tours = cursor.fetchall()
    cursor.close()
    conn.close()
    return tours

def delete_tour(tour_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tours WHERE id = %s", (tour_id,))
    conn.commit()
    cursor.close()
    conn.close()

def update_tour_price(tour_id, new_price):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tours SET price = %s WHERE id = %s", (new_price, tour_id))
    conn.commit()
    cursor.close()
    conn.close()

def search_tours_admin(country=None, max_price=None):
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
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results
