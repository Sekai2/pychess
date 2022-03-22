import sqlite3

conn = sqlite3.connect(r'user.db')
cursor = conn.cursor()
create_users = """CREATE TABLE IF NOT EXISTS users(
id VARCHAR(15) username PRIMARY KEY,
hash INT(5000000000)
);"""