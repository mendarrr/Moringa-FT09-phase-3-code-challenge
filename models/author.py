#Import the database
from database.connection import get_db_connection

class Author:
    all = {}

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return f'<Author {self.id} {self.name}>'
    

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id):
        if isinstance(id, int):
            self._id = id


    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, new_name):
        if hasattr(self, '_name'):
            raise AttributeError("Name cannot be changed after initializING")
        else:
            if isinstance(new_name, str):
                if len(new_name) > 0:
                    self._name = new_name


    def save(self):
        conn = get_db_connection()
        CURSOR = conn.cursor()
        sql = """
            INSERT INTO authors (name)
            VALUES (?)
        """
        CURSOR.execute(sql, (self.name,))
        conn.commit()
        
        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    #creates a new entry in the authors table of the database
    def create(cls, name):
        author = cls(name)
        author.save()
        return author
    
    def get_author_id(self):
        return self.id

    def articles(self):
        from models.article import Article
        conn = get_db_connection()
        CURSOR = conn.cursor()
        """retrieves and returns a list of articles wriitten by this author"""
        sql = """
            SELECT ar.*
            FROM articles ar
            INNER JOIN authors a ON ar.author = a.id
            WHERE a.id = ?
        """

        CURSOR.execute(sql, (self.id,))
        article_data = CURSOR.fetchall()

        articles = []
        for row in article_data:
            articles.append(Article(*row))
        return articles
    

    def magazines(self):
        from models.magazine import Magazine
        conn = get_db_connection()
        CURSOR = conn.cursor()
        """Retrieves and returns a list of Magazine objects where this Author has written articles"""
        sql = """
            SELECT DISTINCT m.*
            FROM magazines m
            INNER JOIN articles ar ON ar.magazine = m.id
            INNER JOIN authors a ON ar.author = a.id
            WHERE a.id = ?
        """

        CURSOR.execute(sql, (self.id,))
        magazine_data = CURSOR.fetchall()

        magazines = []
        for row in magazine_data:
            magazines.append(Magazine(*row))
        return magazines
    
    def update(self):
        conn = get_db_connection()
        """Update the table row corresponding to the current Article instance."""
        sql = """
            UPDATE authors
            SET author_id = ?, name = ?
            WHERE id =?
        """
        cur = conn.cursor()
        cur.execute(sql, (self.author_id, self.name))
        conn.commit()

    def delete(self):
        conn = get_db_connection()
        """Delete the table row corresponding to the current Article instance,
        delete the dictionary entry, and reassign id attribute"""

        sql = """
            DELETE FROM authors
            WHERE id =?
        """

        cur = conn.cursor()
        cur.execute(sql, (self.author_id,))
        conn.commit()

        # Delete the dictionary entry using id as the key
        del type(self).all[self.author_id]

        # Set the id to None
        self.id = None

    @classmethod
    def find_by_id(cls, author_id):
        """Find an author by id"""
        conn = get_db_connection()
        CURSOR = conn.cursor()
        sql = """
            SELECT *
            FROM authors
            WHERE id = ?
        """
        CURSOR.execute(sql, (author_id,))
        author_data = CURSOR.fetchone()

        if author_data:
            return cls(*author_data)
        else:
            return None