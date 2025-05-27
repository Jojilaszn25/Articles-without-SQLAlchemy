from lib.models.author import Author
from lib.models.article import Article
from lib.models.magazine import Magazine
from lib.db.connection import get_connection

def setup_function():
    """Reset database before each test."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")
    conn.commit()

def test_create_author():
    author = Author.create("Nina Simone")
    assert isinstance(author, Author)
    assert author.name == "Nina Simone"
    assert author.id is not None

def test_get_all_authors():
    Author.create("Toni Morrison")
    Author.create("James Baldwin")
    authors = Author.get_all()
    names = [a.name for a in authors]
    assert "Toni Morrison" in names
    assert "James Baldwin" in names
    assert len(authors) == 2

def test_find_author_by_id():
    author = Author.create("Zora Neale Hurston")
    found = Author.find_by_id(author.id)
    assert found is not None
    assert found.id == author.id
    assert found.name == "Zora Neale Hurston"

def test_author_get_articles():
    author = Author.create("Langston Hughes")
    mag = Magazine.create("Poetry Digest", "Literature")
    Article.create("Dream Deferred", author.id, mag.id)
    Article.create("Harlem", author.id, mag.id)
    articles = author.get_articles()
    titles = [a.title for a in articles]
    assert "Dream Deferred" in titles
    assert "Harlem" in titles
    assert len(articles) == 2
