import sqlite3

def init_database():
    print("🛠️ Creating real SQLite Database 'neurolock_db.sqlite'...")
    conn = sqlite3.connect('neurolock_db.sqlite')
    cursor = conn.cursor()

    # 1. Create Tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            balance REAL DEFAULT 0.0,
            status TEXT DEFAULT 'active'
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount REAL,
            status TEXT DEFAULT 'PENDING'
        )
    ''')

    # 2. Insert Initial Dummy Data if empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO users (name, balance, status) VALUES ('Rahul', 1000.0, 'active')")
        cursor.execute("INSERT INTO users (name, balance, status) VALUES ('Priya', 2500.0, 'active')")
        cursor.execute("INSERT INTO orders (user_id, amount, status) VALUES (1, 150.0, 'PAID')")
        cursor.execute("INSERT INTO orders (user_id, amount, status) VALUES (2, 500.0, 'PENDING')")
        conn.commit()
        print("✅ Tables created & seeded with initial data!")
    else:
        print("ℹ️ Database already exists and contains data.")

    conn.close()

if __name__ == "__main__":
    init_database()