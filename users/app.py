'''CRUD operation using mysql'''
from flask import Flask
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, support_credentials=True)

import users.handlers as handlers