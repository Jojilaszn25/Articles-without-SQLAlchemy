import pytest
from lib.models.magazine import Magazine

def test_create_magazine():
    mag = Magazine.create("Nature Explorer", "Science")
    assert mag.id is not None
    assert mag.name == "Nature Explorer"
    assert mag.category == "Science"

def test_get_all_magazines():
    Magazine.create("Global Politics", "Politics")
    magazines = Magazine.get_all()
    assert len(magazines) >= 1
    assert all(isinstance(m, Magazine) for m in magazines)

def test_find_by_id():
    mag = Magazine.create("History Today", "History")
    found = Magazine.find_by_id(mag.id)
    assert found is not None
    assert found.id == mag.id
    assert found.name == "History Today"

def test_find_by_id_not_found():
    found = Magazine.find_by_id(-1)  
    assert found is None
