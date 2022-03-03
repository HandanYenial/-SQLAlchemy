from flask import Flask, request, render_template,  redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db,  connect_db, Pet   #imported Pet from models.py

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pet_shop_db'    #name of the database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']  =  False
app.config['SQLALCHEMY_ECHO'] =  True
app.config['SECRET_KEY'] = "cjktlrk21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)


@app.route('/')
def list_pets():
    """Shows list of all pets in db"""
    pets = Pet.query.all()                          #Pet.query.all() is the query I need,to show all pets name. then I created a variable
    return render_template('list.html', pets=pets)  #then made a html file in the templates and render it.


@app.route('/', methods=["POST"])
def create_pet():
    name = request.form["name"]
    species = request.form["species"]
    hunger = request.form["hunger"]
    hunger = int(hunger) if hunger else None  #making a form to add new pets

    new_pet  = Pet(name=name, species=species, hunger=hunger)
    db.session.add(new_pet)     
    db.session.commit()
    #adding the new pet to the database
    
    return redirect(f'/{new_pet.id}')

@app.route("/<int:pet_id>")         # we need a variable on the route as pet id so /4,/5
def show_pet(pet_id):
    """Show details about a single pet"""
    pet = Pet.query.get_or_404(pet_id)            #the query to get the pet id, if pet_id is not there, then instead of none it will return 404 page
    return render_template("details.html", pet=pet)

@app.route("/species/<species_id>")
def show_pets_by_species(species_id):
    pets = Pet.get_by_species(species_id)
    return render_template("species.html", pets=pets, species=species_id)
