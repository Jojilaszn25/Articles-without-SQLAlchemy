from lib.db.connection import get_connection

def seed_data():
    conn = get_connection()
    cursor = conn.cursor()

    authors = [('Alice'), ('Bob'), ('Charlie')]
    cursor.executemany("INSERT INTO authors (name) VALUES (?)", [(a,) for a in authors])

    magazines = [('Tech Times', 'Technology'), ('Foodies', 'Cooking'), ('Health First', 'Wellness')]
    cursor.executemany("INSERT INTO magazines (name, category) VALUES (?, ?)", magazines)

    articles = [
        ('AI in 2025', 1, 1),
        ('Python Recipes', 2, 2),
        ('Wellness Tips', 3, 3)
    ]
    cursor.executemany("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)", articles)

    conn.commit()
    conn.close()
    print("Seed data inserted!")

if __name__ == "__main__":
    seed_data()
