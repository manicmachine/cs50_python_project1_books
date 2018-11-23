import datetime

from model import User, Book, Review
from user import User as LocalUser
from werkzeug.security import generate_password_hash, check_password_hash

class AccountManager:
    
    __engine = None
    __db = None
    
    def __init__(self, engine, db):
        self.__engine = engine
        self.__db = db
        
    def accountExists(self, username):
        """Determines if the username provided exists in the database or not.
        
        Returns True is the username is present, otherwise returns False."""
        
        if self.__db.query(User).filter(User.username == username).count():
            return True
        else:
            return False
        
    def createAccount(self, accountDetails):
        """Creates a new account with the account details.
        
        NOTE: Password will be hashed prior to being submitted to the database.
        
        Returns True if account creation is successful, otherwise returns False."""
        
        accountDetails['password_hash'] = generate_password_hash(accountDetails['password'])
        accountDetails['member_since'] = str(datetime.date.today())

        newUser = User(
            first_name = accountDetails['firstName'],
            last_name = accountDetails['lastName'],
            email = accountDetails['email'],
            username = accountDetails['username'],
            password_hash = accountDetails['password_hash'],
            member_since = accountDetails['member_since'])
            
        self.__db.add(newUser)
        self.__db.commit()
            
        return True

    def login(self, authRequest):
        """Checks if provided user credentials are valid. 
        
        Returns user object if credentials are valid, otherwise returns False."""
        
        if self.accountExists(authRequest['username']):
            userInfo = self.__db.query(User).filter(User.username == authRequest['username']).first()
                    
            if check_password_hash(userInfo.password_hash, authRequest['password']):
                user = LocalUser(
                    userInfo.id,
                    userInfo.first_name,
                    userInfo.last_name,
                    userInfo.email,
                    userInfo.username,
                    userInfo.member_since)
                    
                return user
            else:
                return False
                
        else:
            return False
    
    def logout(self, session):
        """Removes the current user from their session, effectively logging them out."""
        
        session["user"] = None