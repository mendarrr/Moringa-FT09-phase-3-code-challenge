import unittest
from database.connection import get_db_connection
from models.author import Author
from models.article import Article
from models.magazine import Magazine

class TestModels(unittest.TestCase):
    # Tests for Author Class
    def test_author_creation(self):
        author = Author(1, "John Doe")
        self.assertEqual(author.name, "John Doe")

    def test_init(self):
        author = Author(1, "John Doe")
        self.assertEqual(author.id, 1)
        self.assertEqual(author.name, "John Doe")

    def test_save(self):
        author = Author(None, "Jane Doe")
        author.save()
        self.assertIsNotNone(author.id)
        self.assertIn(author.id, Author.all)

    def test_get_author_id(self):
        author = Author(1, "John Doe")
        self.assertEqual(author.get_author_id(), 1)

    def test_name_immutable(self):
        author = Author(1, "John Doe")
        with self.assertRaises(AttributeError):
            author.name = "Jane Doe"

    def test_author_repr(self):
        author = Author(1, "John Doe")
        self.assertEqual(repr(author), "<Author 1 John Doe>")

    def test_author_attributes(self):
        author = Author(2, "Jane Smith")
        self.assertEqual(author.id, 2)
        self.assertEqual(author.name, "Jane Smith")

    def test_id_setter(self):
        obj = Author(123, "John Doe")
        obj.id = 123
        self.assertEqual(obj.id, 123)

    def test_name_setter(self):
        obj = Author(123, "John Doe")
        self.assertEqual(obj.name, "John Doe")

        

# Tests for the Article Class
    def test_article_creation(self):
        article = Article(1, "Test Title", "Test Content", 1, 1)
        self.assertEqual(article.title, "Test Title")

    def test_magazine_creation(self):
        magazine = Magazine(1, "Tech Weekly", "Technology")
        self.assertEqual(magazine.name, "Tech Weekly")

if __name__ == "__main__":
    unittest.main()
