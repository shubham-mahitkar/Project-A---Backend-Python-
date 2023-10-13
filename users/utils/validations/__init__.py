"""Initialize Marshmallow."""
from users.app import app
from flask_marshmallow import Marshmallow

ma = Marshmallow(app)
