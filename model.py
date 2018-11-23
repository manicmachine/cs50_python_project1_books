import sqlalchemy

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Book(Base):
    
    __tablename__ = "books"
    
    isbn = Column(String, primary_key=True)
    title = Column(String)
    author = Column(String)
    year = Column(Integer)
    
    # reviews = relationship("Review", order_by=Review.id, back_populates="book")
    
    def __repr__(self):
        return "<Book(isbn='%s', title='%s', author='%s', year='%i')>" % (
            self.isbn, self.title, self.author, self.year)

class User(Base):
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    username = Column(String)
    password_hash = Column(String)
    member_since = Column(Date)
    
    # reviews = relationship("Review", order_by=Review.id, back_populates="user")
    
    def __repr__(self):
        return "<User(id='%i', first_name='%s', last_name='%s', email='%s', username='%s')>" % (
            self.id, self.first_name, self.last_name, self.email, self.username)
    
class Review(Base):
    
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True)
    review = Column(String)
    rating = Column(Integer)
    date = Column(Date)
    user_id = Column(Integer, ForeignKey('users.id'))
    book_id = Column(String, ForeignKey('books.isbn'))
    
    user = relationship("User", back_populates="reviews")
    book = relationship("Book", back_populates="reviews")
    
    def __repr__(self):
        return "<Review(id='%i', review='%s', rating='%i', date='%s', user_id='%i', book_id='%s')>" % (
            self.id, self.review, self.rating, self.date, self.user_id, self.book_id)
            

Book.reviews = relationship("Review", order_by=Review.id, back_populates="book")
User.reviews = relationship("Review", order_by=Review.id, back_populates="user")