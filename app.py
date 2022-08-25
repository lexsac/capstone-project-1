from flask import Flask, request, redirect, render_template, session, g, flash, abort
from flask_debugtoolbar import DebugToolbarExtension
import requests

from models import db, connect_db, User, Job
from forms import UserAddForm
from sqlalchemy.exc import IntegrityError
from secrets import API_SECRET_KEY

CURR_USER_KEY = "curr_user"
API_BASE_URL = "https://www.themuse.com/api/public/jobs"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///capstone1"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisisasecret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

##############################################################################
# API request with user's info

def get_jobs(location, company, category, experience_level):
    
    res = requests.get(f"{API_BASE_URL}?page=1",
                            params={'api_key': API_SECRET_KEY, 
                                    'location': location,
                                    'experience_level': experience_level,
                                    'company': company,
                                    'category': category})
    
    data = res.json()
    
    job_title = data['results'][0]['name']
    description = data['results'][0]['contents']
    landing_page = data['results'][0]['refs']['landing_page']
    posted_date = data['results'][0]['publication_date']
    jobs = {'title': job_title, 'description': description, 'url': landing_page, 'date_posted': posted_date}
    
    return jobs


##############################################################################
# User signup/login/logout

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
       
       
@app.route('/signup', methods=["GET", "POST"])
def add_new_user():
    """Add a new user."""
    
    form = UserAddForm()
       
    if form.validate_on_submit():
        
        try: 
            new_user = User.signup( 
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                username=form.username.data,
                email=form.email.data,
                password=form.password.data,
                profile_img=form.profile_img.data,
                location=form.location.data,
                experience_level=form.experience_level.data,
                company=form.company.data,
                category=form.category.data)
                
            db.session.add(new_user)
            db.session.commit()

        except IntegrityError: 
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)
                
        do_login(new_user)
        
        user_id = new_user.id
        
        flash('Welcome! Successfully Created Your Account!', "success")
        return redirect('/')
    
    else: 
        return render_template('users/signup.html', form=form)
    

# @app.route('/login', methods=['GET', 'POST'])
# def login_user():
#     form = LoginForm()
#     if form.validate_on_submit():
#         username = form.username.data
#         password = form.password.data

#         user = User.authenticate(username, password)
#         if user:
#             do_login(user)
#             flash(f"Welcome Back, {user.username}!", "primary")
#             return redirect('/')
        
#         else:
#             flash("Invalid credentials.", 'danger')

#     return render_template('users/login.html', form=form)


# @app.route('/logout')
# def logout_user():
#     """Handle logout of user."""
   
#     session.pop('user.id')
#     flash("Goodbye!", "info")
#     return redirect('/login')


##############################################################################
# Homepage

@app.route('/', methods=['GET'])
def homepage():
    """Show homepage: 
    
    - anon users: random job listings sorted by date posted
    - logged in: job listings that match their preferences, 'No new jobs. Check back later' message if no jobs match criteria."""
    
    if g.user:     
        
        location = g.user.location 
        experience_level = g.user.experience_level
        company = g.user.company
        category = g.user.category
    
        jobs = get_jobs(location, company, category, experience_level)
        
        # import pdb 
        # pdb.set_trace()
        
        return render_template('home.html', jobs=jobs)
    
    else: 
        
        return render_template('home-anon.html')
    
    
