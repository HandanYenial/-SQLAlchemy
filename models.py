# database related commands will be here
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

# columns,values,schema... after this point


class Pet(db.Model): # class name should be singular like Pet, but the table name should be plural like pets.
    __tablename__ = 'pets'    #write the name of the table you'll be using in postgres
    
    # adding a class method for queries.
    
    @classmethod
    def get_by_species(cls,species): 
        cls.query.filter_by(species=species).all()  
        
    #so we will write a query here, and instead of writing Pet(the classname) I can now write cls
    # so in python normally when we write a query it looks like:
    # Pet.query.filter_by(species='cat').all()
    #since we have a classmethod now,
    #Pet.get_by_species('cat')

    @classmethod
    def get_all_hungry(cls):
        return cls.query.filter(Pet.hunger>20).all()
        
    # we are adding an instance method dunder r as repr for a better representation
    
    def __repr__(self):
        #return f ""<Pet id-self.id> writing self could be annoying and long for so many times,so instead we'll make a reference for self.
        #can be s=self or p=self(as like pet)
        
        p = self
        return f"<Pet id={p.id} name={p.name} species={p.species} hunger={p.hunger}"

    id = db.Column(db.Integer, # writing the data types as String, Integer...
                   primary_key=True,#since it is id there needs to be primary key
                   autoincrement=True) #

    name = db.Column(db.String(50), #database.datatype- at most 50 characters
                     nullable=False, # if you don't write that it will be null
                     unique=True)# all pets names will be uniqu

    species = db.Column(db.String(30), nullable=True)#Columns can contain NULL unless nullable=False

    hunger = db.Column(db.Integer, nullable=False, default=20)

    # we will add some custom methods.Methods is a representation of a row in a table in the database.
    #by mapping these rows, the entries we get back from the database into an object, it is not just about making the data accessible
    #it also allows us to include custom functuality.
    # can write methods to do simple or really complex operations.
    #could add a login method to my user method, or add a feed method to our pet,
    #which will actually change the hunger level.

    #ex;start with a greet method. This will be an istance method, which will return a simple f string.

    def greet(self):
        return f"Hi, I'm {self.name} the {self.species}"
    

    # now we will make feed, which will actually update a row in the pets table in the database
    
    def feed(self,amount=20):       # we gave it a default amount, how much we will feed them
        self.hunger -= amount       # to find the hunger we will subtract the given feed amount from hunger
        self.hunger = max(self.hunger , 0)  
        
        
    #we don't want hunger level to be a negative number. if the hunger is 13, and feed amount is 20 then
    #it will be 13-20=-7. so in the max(-7,0) it will take the maximum of -7 and 0 which is 0.
    # so in ipyhton
    # In [2]: newbe = Pet.query.get(5)
    # In [3]: newbe
    # Out[3]: <Pet id=5 name=Scout species=turtle hunger=20
    # In [4]: newbe.feed()
    # In [6]: newbe
    # Out[6]: <Pet id=5 name=Scout species=turtle hunger=0
    # But it didn't add this to the database so,
    # In [8]: db.session.add(newbe)
    # In [9]: db.session.commit()
    # updated in the database as  5 | Scout           | turtle  |      0




