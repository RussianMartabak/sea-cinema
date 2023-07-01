import sqlite3

conn = sqlite3.connect('db.sqlite3')

c = conn.cursor()

for fk in range(1, 5):
    for no in range(1, 65):
        conn.execute(f"""
        INSERT INTO data_seating (seat_number, is_empty,movie_id_id)
        VALUES({no}, 1 , {fk})
        """)

conn.commit()