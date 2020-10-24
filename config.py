# Statement for enabling the development environment
DEBUG = False

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://cl_payment:123456@localhost:5432/clooper_payment'

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"
