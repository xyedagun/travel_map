from jinja2 import StrictUndefined
from flask import Flask, render_template, jsonify, request, session
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

@app.route('/sign-up')
def sign_up():
    """Sign up page"""

    return render_template("sign_up.html")



@app.route('/search-city-form')
def search_city():

    return render_template('search_form.html')




@app.route('/process-search-form', methods=["POST"])
def process_form():

    search = request.form.get("query")
    location = request.form.get("location")

    api_result = sample_query.search_places(search, location)
    print location, api_result
    return render_template('main.html', api_result=api_result) # the api_result will be included on the map.html


@app.route('/add-to-folder', methods=["POST"])
def add_to_folder():
    return "OK"


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



@app.route('/log-out')
def log_out():
    """Log out page"""
    if not 'logged_in_user' in session:
    	message = "You're not logged in"
    else:
    	message = "You've been logged out"
    	del session['logged_in_user']
    	#to delete user from session
    return render_template("logout.html", message = message) 





    

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()