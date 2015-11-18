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

    user_id = session.get('user_id')
    # import pdb; pdb.set_trace()
    folders = Folder.query.filter_by(user_id=user_id).all()

    print attraction_results, hotel_results,location

    return render_template('main.html', folders=folders, attraction_results=attraction_results, hotel_results=hotel_results, restaurant_results=restaurant_results, museum_results=museum_results, festival_results=festival_results)




@app.route('/process-search-form', methods=["POST"])
def process_form():

    search = request.form.get("query")
    location = request.form.get("location")

    api_result = sample_query.search_places(search, location)
    print location, api_result

    return render_template('main.html', api_result=api_result) # the api_result will be included on the map.html



@app.route('/add-to-folder', methods=["POST"])
def add_to_folder():

    username = session['logged_in_user']
    folderName = request.form.get("folder_name")
    business_id = request.form.get("business_id")
    existing_place = Place.query.filter_by(business_id = business_id).first()
    print request.form

    #ask yelp to get data using business_id
    
    business = sample_query.yelp_api.business_query(id=business_id)
    if business['location']['address']:
        address = business['location']['address'][0]
    else:
        address = ""
    import pdb; pdb.set_trace()
    if business['categories'][0]:
        category_description, category = business['categories'][0]
    else:
        category = ""

    if business['name']:
        name = business['name']
    else:
        name = ""

    if business['location']['coordinate']['latitude']:
        latitude = business['location']['coordinate']['latitude']
    else:
        latitude = None

    if business['location']['coordinate']['longitude']:
        longitude = business['location']['coordinate']['longitude']
    else:
        longitude = None

    if business['location']['city']:
        city = business['location']['city']
    else:
        city = ""

    if business['location']['country_code']:
        country = business['location']['country_code']
    else:
        country = ""
    

    if not existing_place:
        
        new_place = Place(business_id=business_id, category=category, name=name, address=address, latitude=latitude, longitude=longitude, city=city, country=country)

        db.session.add(new_place)
        db.session.commit()
        place_id = new_place.place_id
    else:
        place_id = existing_place.place_id

    #Need to check if folder already exist in user's folders

    folder = Folder.query.filter_by(user = username, folder_name = folderName).first()

    if not folder:
        new_folder = Folder(user=username, folder_name=folderName)
        
        db.session.add(new_folder)
        db.session.commit()
        folder_id = new_folder.folder_id

        folder = new_folder

    # TODO: Find a way to add the place to the folder (and then save them)


#create place folder if it doesn't exist or if it does, use it.
# import pdb; pdb.set_trace()  n = next line c = continue until next break point  
   

    return render_template("add_folder.html")


@app.route('/folders')
def show_folders():
    
    user_id = session.get('user_id')
    import pdb; pdb.set_trace()
    folders = Folder.query.filter_by(user_id=user_id).all()

    # we're done - we just need to serialize these folders and return them
    folder_dicts = []
    for folder in folders:
        folder_dicts.append(folder.to_dict())

    return jsonify({'folders': folder_dicts})




@app.route('/create_folder', methods=["POST"])
def create_folder():

    user = request.form.get("username")
    folderName = request.form.get("FolderName")
    existing_user = User.query.filter(User.user_name == user).first()

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
        session['user_id'] = existing_user.user_id
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
        session['user_id'] = new_user.user_id
        #
    else:
        session['logged_in_user'] = existing_user.user_name
        session['firstname'] = existing_user.fname
        session['user_id'] = existing_user.user_id

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