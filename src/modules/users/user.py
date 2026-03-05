from abc import ABC, abstractmethod
class User :
    type = ""
    username = ""
    password = ""
    email = ""
    payinfo = 0

    def __init__(self, typ, user, passw, eml, pyfo):
        self.type = typ
        self.username = user
        self.password = passw
        self.email = eml
        self.payinfo = pyfo

    
   
    #Apparently we don't need to make any databases for this, so I'll be making a stock customer, driver, resturant and maybe admin

def getPassword(User):
    return User.password

customer = User("cust", "customer", "badPassword", "cus@gmail.com", 12345)
driver = User("drv", "driver", "123456", "drv@gmail.com", 98765)
resturant = User("rest", "resturant", "password", "rest@gmail.com", 34567)
stockuser = {
    "customer" ; customer;
    "driver" ; driver;
    "resturant" ; resturant
} 

class Login :
    

    usrnm = ""
    eml = ""
    passw = ""

    def signin():
        usr = str(input("Username"))
        pasw = str(input("Password"))
        if usr:
            if stockuser.get(usr):
                if stockuser.get(usr.getPassword()) == pasw:
                    print("Login Comfirmed")
                    #right now this just checks that they have an account and correct password
                else:
                    print("Password does not match with account")
            else:
                print("Account not found")
        else:
            print("A username must be entered")