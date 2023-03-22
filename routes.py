from flask import send_from_directory, request, url_for, jsonify
from werkzeug.utils import secure_filename
import os

from mycards.app import app
from mycards.db import db
from mycards.model import Deck

with app.app_context():
    db.create_all()
    # List the SQLAlchemy model tables created
    tables = db.metadata.tables.keys()
    print(f"SQLAlchemy model tables created: {', '.join(tables)}")



@app.route('/')
def serve_static_html():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    # Ensure the 'images' folder exists
    images_folder = os.path.join(app.static_folder, 'uploads')
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)

    # Save the uploaded image
    image = request.files['image']
    filename = secure_filename(image.filename)
    image.save(os.path.join(images_folder, filename))

    # Print a debug message about the operation
    print(f"Debug: Uploaded image '{filename}' to the 'static/uploads' folder")
    

    # Return the URL to the image
    return jsonify({'url': url_for('static', filename=f'uploads/{filename}')})



@app.route('/decks', methods=['POST'])
def create_deck():
    data = request.get_json()

    new_deck = Deck(
        name=data['name'],
        numCards=data['numCards'],
        numSuits=data['numSuits'],
        numRanks=data['numRanks'],
        bgImage=data['bgImage'],
        type=data['type']
    )

    db.session.add(new_deck)
    db.session.commit()

    return jsonify({'message': 'Deck created successfully', 'deck_id': new_deck.id})

@app.route('/decks', methods=['GET'])
def get_decks():
    # Query all decks from the database
    decks = Deck.query.all()

    # Convert the decks to a JSON array
    decks_json = [deck.to_dict() for deck in decks]

    # Return the JSON array of decks
    return jsonify(decks_json)