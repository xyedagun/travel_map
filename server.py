from jinja2 import StrictUndefined
from flask import Flask, render_template, jsonify, request, session, redirect
from flask_debugtoolbar import DebugToolbarExtension
from model import User, Folder, Place, connect_to_db, db
import sample_query 


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Show homepage."""


    return render_template("base.html")


@app.route('/results', methods=['POST'])
def get_result():
    location = request.form.get("location")

    attraction_results = sample_query.search_attractions(location)
    hotel_results = sample_query.search_hotels(location)
    restaurant_results = sample_query.search_restaurants(location)
    museum_results = sample_query.search_museums(location)
    festival_results = sample_query.search_festivals(location)


    print attraction_results, hotel_results,location

    return render_template('main.html', attraction_results=attraction_results, hotel_results=hotel_results, restaurant_results=restaurant_results, museum_results=museum_results, festival_results=festival_results)




@app.route('/process-search-form', methods=["POST"])
def process_form():

    search = request.form.get("query")
    location = request.form.get("location")

    api_result = sample_query.search_places(search, location)
    print location, api_result

    return render_template('main.html', api_result=api_result) # the api_result will be included on the map.html


@app.route('/add-to-folder', methods=["POST"])
def add_to_folder():

    user = request.form.get("username")
    folderName = request.form.get("FolderName")
    

    return render_template("add_folder.html")


@app.route('/submit', methods=["POST"])
def submit():
    """Sign in page."""

    user = request.form.get("username")
    first_name = request.form.get("firstname")
    last_name = request.form.get("lastname")
    email = request.form.get("email")
    password = request.form.get("password")

    existing_user = User.query.filter(User.user_name == user).first()

    if not existing_user:
    	new_user = User(user_name=user, fname=first_name, lname=last_name, email=email, password=password)
    	#white is column name from route, orange is the variable from model.py
    	db.session.add(new_user)
    	db.session.commit()
    	session['logged_in_user'] = new_user.user_name
        session['firstname'] = new_user.fname
        #
    else:
    	session['logged_in_user'] = existing_user.user_name
        session['firstname'] = existing_user.fname

    return render_template("base.html")
    

@app.route('/logged-in', methods=["POST"])
def log_in():
    """Log in page. Need to make sure the user enter correct password."""

    user = request.form.get("username")
    password = request.form.get("password")

    existing_user = User.query.filter_by(user_name=user, password=password).first()


    if user == existing_user.user_name:
        session['logged_in_user'] = existing_user.user_name
        session['firstname'] = existing_user.fname
    else:
        print "Try again"

    return render_template("base.html")



@app.route('/modal-loggedIn', methods=["POST"])
def modalLoggedIn():
    """Log in in modal window"""

    user = request.form.get("username")
    password = request.form.get("password")

    existing_user = User.query.filter_by(user_name=user, password=password).first()

    if user == existing_user.user_name:
        session['logged_in_user'] = existing_user.user_name
        session['firstname'] = existing_user.fname
    else:
        print "Try again"

    return render_template("base.html")



@app.route('/signup', methods=["POST"])
def signUp():
    """Sign up page in modal window"""

    user = request.form.get("username")
    first_name = request.form.get("firstname")
    last_name = request.form.get("lastname")
    email = request.form.get("email")
    password = request.form.get("password")

    existing_user = User.query.filter(User.user_name == user).first()

    if not existing_user:
        new_user = User(user_name=user, fname=first_name, lname=last_name, email=email, password=password)
        #white is column name from route, orange is the variable from model.py
        db.session.add(new_user)
        db.session.commit()
        session['logged_in_user'] = new_user.user_name
        session['firstname'] = new_user.fname
        #
    else:
        session['logged_in_user'] = existing_user.user_name
        session['firstname'] = existing_user.fname

    return render_template("base.html")


@app.route('/log-out')
def log_out():
    """Log out page"""


    session.clear()

    # if not 'logged_in_user' in session:
    # 	message = "You're not logged in"
    # else:
    # 	message = "You've been logged out"
    # 	del session['logged_in_user']
    	#to delete user from session
    return redirect("/") 



@app.route('/map')
def map():
    return render_template("map_sample.html")

    

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()