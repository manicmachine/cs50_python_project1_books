import requests
import json

# GoodReads API controller
class GoodReadsController:
    
    key = None
    secret = None
        
    def __init__(self, key, secret):
        self.key = key
        self.secret = secret
        
    def getReviewCounts(self, isbn):
        request = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": self.key, "isbns": isbn})
        loadedJson = json.loads(json.dumps(request.json()))

        return loadedJson["books"][0]
