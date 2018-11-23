# Book object
class Book:
    
    isbn = None
    title = None
    author = None
    year = None
    avgReview = None
    numReviews = None
    
    def __init__(self, isbn, title, author, year, avgReview, numReviews):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year
        self.avgReview = avgReview
        self.numReviews = numReviews
        