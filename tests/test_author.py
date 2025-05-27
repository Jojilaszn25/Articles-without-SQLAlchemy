import pytest
from lib.models.author import Author
from lib.models.article import Article
from lib.db.connection import get_connection

@pytest.fixture(autouse=True)
def run_around_tests():
    
    conn = get_connection()
    conn.execute("DELETE FROM articles")
    conn.execute("DELETE FROM authors")
    conn.commit()
    yield

def test_create_author():
    author = Author.create("Test Author")
    assert isinstance(author, Author)
    assert author.name == "Test Author"

def test_get_all_authors():
    Author.create("Alice")
    Author.create("Bob")
    authors = Author.get_all()
    names = [a.name for a in authors]
    assert "Alice" in names and "Bob" in names

def test_find_author_by_id():
    author = Author.create("Charlie")
    found = Author.find_by_id(author.id)
    assert found.name == "Charlie"

def test_author_get_articles():
    author = Author.create("Dana")
    Article.create("Article A", author.id, 1)  
    Article.create("Article B", author.id, 1)
    articles = author.get_articles()
    titles = [a.title for a in articles]
    assert "Article A" in titles and "Article B" in titles
