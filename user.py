class User(object):
    '''
ID: int
Name: string
Email Address: string
Password: string
Status: string
Preference/Search History: dict
IsAdmin: boolean
LastLogin: datetime
CreationDate: datetime
    '''
    def __init__(self, ID, Name, EmailAddress, Password, Status, CreationDate):
        self.ID = ID
        self.Name = Name
        self.EmailAddress = EmailAddress
        self.Password = Password
        self.Status = Status
        self.SearchHistory = {}
        self.IsAdmin = False
        self.LastLogin = CreationDate
        self.CreationDate = CreationDate

    def getSearchHistory(self, getLastN=5):
        # TODO
        pass

    def getName(self):
        return self.Name

    def getEmailAddress(self):
        return self.EmailAddress

    def getStatus(self):
        return self.Status

    def isAdmin(self):
        return self.IsAdmin

    def getLastLogin(self):
        return self.LastLogin

    def getCreationDate(self):
        return self.CreationDate
