import pytest
from lib.models.magazine import Magazine
from lib.models.author import Author
from lib.models.article import Article
from lib.db.connection import get_connection

@pytest.fixture(autouse=True)
def run_around_tests():
    conn = get_connection()
    conn.execute("DELETE FROM articles")
    conn.execute("DELETE FROM magazines")
    conn.execute("DELETE FROM authors")
    conn.commit()
    yield

def test_create_magazine():
    mag = Magazine.create("Gadget World", "Tech")
    assert isinstance(mag, Magazine)
    assert mag.name == "Gadget World"

def test_get_all_magazines():
    Magazine.create("Science Today", "Science")
    Magazine.create("Health Life", "Health")
    mags = Magazine.get_all()
    names = [m.name for m in mags]
    assert "Science Today" in names and "Health Life" in names

def test_find_magazine_by_id():
    mag = Magazine.create("Art Monthly", "Art")
    found = Magazine.find_by_id(mag.id)
    assert found.name == "Art Monthly"

def test_magazine_get_articles_and_authors():
    mag = Magazine.create("Music Vibes", "Music")
    author = Author.create("Elena")
    Article.create("Beats and Rhythms", author.id, mag.id)
    articles = mag.get_articles()
    authors = mag.get_authors()
    assert articles[0].title == "Beats and Rhythms"
    assert authors[0].name == "Elena"
