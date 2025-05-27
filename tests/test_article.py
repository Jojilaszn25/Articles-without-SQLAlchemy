import pytest
from lib.models.article import Article
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.db.connection import get_connection

@pytest.fixture(scope='function', autouse=True)
def setup_and_teardown_db():

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")

    cursor.execute("INSERT INTO authors (name) VALUES ('Test Author')")
    cursor.execute("INSERT INTO magazines (name, category) VALUES ('Test Magazine', 'Test Category')")
    conn.commit()
    yield
    conn.close()

def get_test_author_id():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM authors WHERE name = 'Test Author'")
    author_id = cursor.fetchone()[0]
    conn.close()
    return author_id

def get_test_magazine_id():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM magazines WHERE name = 'Test Magazine'")
    magazine_id = cursor.fetchone()[0]
    conn.close()
    return magazine_id

def test_article_title_validation():
    author_id = get_test_author_id()
    magazine_id = get_test_magazine_id()
    with pytest.raises(ValueError):
        Article("", author_id, magazine_id)
    with pytest.raises(ValueError):
        Article("   ", author_id, magazine_id)

def test_article_save_and_find():
    author_id = get_test_author_id()
    magazine_id = get_test_magazine_id()
    article = Article("My Test Article", author_id, magazine_id)
    article.save()
    assert article.id is not None

    fetched = Article.find_by_id(article.id)
    assert fetched is not None
    assert fetched.title == "My Test Article"
    assert fetched.author_id == author_id
    assert fetched.magazine_id == magazine_id

    article.title = "Updated Title"
    article.save()
    updated = Article.find_by_id(article.id)
    assert updated.title == "Updated Title"

def test_article_author_and_magazine_relationship():
    author_id = get_test_author_id()
    magazine_id = get_test_magazine_id()
    article = Article("Relationship Test", author_id, magazine_id)
    article.save()

    author = article.author()
    magazine = article.magazine()
    assert author is not None
    assert author.id == author_id
    assert magazine is not None
    assert magazine.id == magazine_id

def test_find_by_title_and_by_author_and_magazine():
    author_id = get_test_author_id()
    magazine_id = get_test_magazine_id()

    article1 = Article("Common Title", author_id, magazine_id)
    article1.save()
    article2 = Article("Common Title", author_id, magazine_id)
    article2.save()

    found_by_title = Article.find_by_title("Common Title")
    assert len(found_by_title) >= 2

    found_by_author = Article.find_by_author(author_id)
    assert any(a.id == article1.id for a in found_by_author)

    found_by_magazine = Article.find_by_magazine(magazine_id)
    assert any(a.id == article2.id for a in found_by_magazine)
