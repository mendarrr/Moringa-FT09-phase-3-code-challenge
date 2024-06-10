# Import the database
from database.connection import get_db_connection

class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        self.id = id
        self.title = title if title else "Untitled"
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

    def __repr__(self):
        return f'<Article {self.title}>'
    

    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, title):
        if hasattr(self, '_title'):
            raise AttributeError("Cannot change title after it has been set")
        if isinstance(title, str) and len(title):
            self._title = title
        else:
            raise ValueError(
                "Title must be a non-empty string"
            )
        
    @property
    def content(self):
        return self._content
    
    @content.setter
    def content(self, content):
        if isinstance(content, str) and len(content):
            self._content = content
        else:
            raise ValueError(
                "Content must be a non-empty string"
            )
        
    @property
    def author_id(self):
        return self._author_id
    
    @author_id.setter
    def author_id(self, author_id):
        from models.author import Author
        if type(author_id) is int and Author.find_by_id(author_id):
            self._author_id = author_id
        else:
            raise ValueError(
                "Author ID must reference an author in the database")
        
    @property
    def magazine_id(self):
        return self._magazine_id
    
    @magazine_id.setter
    def magazine_id(self, magazine_id):
        from models.magazine import Magazine
        if type(magazine_id) is int and Magazine.find_by_id(magazine_id):
            self._magazine_id = magazine_id
        else:
            raise ValueError("Magazine ID must reference a magazine in the database")
    def author(self):
        from models.author import Author
        conn = get_db_connection()
        CURSOR = conn.cursor()
        """retrieves and returns the author who wrote this article"""
        sql = """
            SELECT a.*
            FROM authors a
            INNER JOIN articles ar ON ar.author = a.id
            WHERE ar.id = ?
        """
        CURSOR.execute(sql, (self.id))
        author_data = CURSOR.fetchone()

        if author_data:
            return Author(*author_data)
        else:
            return None

    def magazine(self):
        from models.magazine import Magazine
        conn = get_db_connection()
        CURSOR = conn.cursor()
        """retrieves and returns the magazine in which this article is published"""
        sql = """
            SELECT m.*
            FROM magazines m
            INNER JOIN articles ar ON ar.magazine = m.id
            WHERE ar.id = ?
        """
        CURSOR.execute(sql, (self.id))
        magazine_data = CURSOR.fetchone()

        if magazine_data:
            return Magazine(*magazine_data)
        else:
            return None