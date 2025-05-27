from lib.db.connection import get_connection

def run_schema():
    with open("lib/db/schema.sql") as f:
        sql = f.read()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.executescript(sql)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    run_schema()
    print("Database setup complete!")
