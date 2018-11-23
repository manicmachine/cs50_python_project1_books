class User:
    
    userId = None
    firstName = None
    lastName = None
    email = None
    username = None
    memberSince = None
    
    def __init__(self, userId, firstName, lastName, email, username, memberSince):
        self.userId = userId
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.username = username
        self.memberSince = memberSince