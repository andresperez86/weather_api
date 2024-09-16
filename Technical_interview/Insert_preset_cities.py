from app import get_db_connection


conn = get_db_connection()
conn.execute('INSERT INTO cities (city_name, state, country) VALUES (?, ?, ?)', ('Los Angeles', 'CA', 'US'))
conn.execute('INSERT INTO cities (city_name, state, country) VALUES (?, ?, ?)', ('Los Angeles', 'CA', 'US'))
conn.execute('INSERT INTO cities (city_name, state, country) VALUES (?, ?, ?)', ('New York', 'NY', 'US'))
conn.execute('INSERT INTO cities (city_name, state, country) VALUES (?, ?, ?)', ('London', '', 'GB'))
conn.execute('INSERT INTO cities (city_name, state, country) VALUES (?, ?, ?)', ('Paris', '', 'FR'))
conn.commit()
conn.close()