from flask_sqlalchemy import SQLAlchemy
from mycards.app import app

import os

# Use the relative path to the decks.db file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'decks.db')
db = SQLAlchemy(app)