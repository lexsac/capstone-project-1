from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    """Site user."""
    
    __tablename__ = 'users'
    
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )

    first_name = db.Column(
        db.Text,
        nullable=False,
    )

    last_name = db.Column(
        db.Text,
        nullable=False,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    profile_img = db.Column(
        db.Text,
        default="/static/images/default-pic.png",
    )

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow(),
    )
    
    location = db.Column(
        db.Text,
    )
    
    company = db.Column(
        db.Text,
    )
    
    experience_level = db.Column(
        db.Text,
    )
    
    category = db.Column(
        db.Text,
    )
    
    # def __repr__(self):
    #     return f"<User #{self.id}: {self.username}, {self.email}>"

    @classmethod
    def signup(cls, first_name, last_name, email, username, password, profile_img, location, experience_level, category, company):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(password)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode('UTF-8')
        
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            password=hashed_utf8,
            profile_img=profile_img,
            location=location,
            experience_level=experience_level,
            category=category,
            company=company
        )
    
        return new_user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.
    
        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.
    
        If can't find matching user (or if password is wrong), returns False.
        """
    
        user = cls.query.filter_by(username=username).first()
    
        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user
    
        return False

##############################################################################
# Data pulled from API

class Job(db.Model):
    """Job in the system."""

    __tablename__ = 'jobs'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )

    name = db.Column(
        db.Text,
        nullable=False,
    )

    description = db.Column(
        db.Text,
        nullable=False,
    )

    # location_id = db.Column(
    #     db.Integer,
    #     db.ForeignKey('locations.id', ondelete='CASCADE'),
    #     nullable=False,
    # )

    # category_id = db.Column(
    #     db.Integer,
    #     db.ForeignKey('categories.id', ondelete='CASCADE'),
    #     nullable=False,
    # )

    # experience_level_id = db.Column(
    #     db.Integer,
    #     db.ForeignKey('experience_levels.id', ondelete='CASCADE'),
    #     nullable=False,
    # )

    # company_id = db.Column(
    #     db.Integer,
    #     db.ForeignKey('companies.id', ondelete='CASCADE'),
    #     nullable=False,
    # )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow(),
    )

    landing_page = db.Column(
        db.Text,
    )
    
    
def connect_db(app):
    # Connect this database to provided Flask app. You should call this in your Flask app.
    
    db.app = app
    db.init_app(app)