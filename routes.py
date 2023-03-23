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
        uid=data['uid'],
        name=data['name'],
        numCards=data['numCards'],
        numSuits=data['numSuits'],
        numRanks=data['numRanks'],
        bgImage=data['bgImage'],
        type=data['type'],
        orientation=data.get('orientation'),
        width=data.get('width'),
        height=data.get('height'),
    )

    # Check if a deck with the given uid already exists
    existing_deck = Deck.query.filter_by(uid=data['uid']).first()

    num_cards_before_update = existing_deck.numCards if existing_deck else -1
    
    if existing_deck:
        # Update the existing deck with the new data
        existing_deck.name = data['name']
        existing_deck.numCards = data['numCards']
        existing_deck.numSuits = data['numSuits']
        existing_deck.numRanks = data['numRanks']
        existing_deck.bgImage = data['bgImage']
        existing_deck.type = data['type']
        existing_deck.orientation = data.get('orientation')
        existing_deck.width = data.get('width')
        existing_deck.height = data.get('height')

        new_deck.id = existing_deck.id

        # Commit the changes to the database
        db.session.commit()
    else:
        # Add the new deck to the session
        db.session.add(new_deck)
        db.session.commit()

    # Create Card models for the number of suits and ranks
    from mycards.model import Card

    should_create_cards = False
    if not existing_deck:
        should_create_cards = True
    elif num_cards_before_update != data['numCards']:
        should_create_cards = True

    if should_create_cards:
        # Delete all cards for the deck
        Card.query.filter_by(deck_id=new_deck.id).delete()
        # Commit
        db.session.commit()
        
        if data['numSuits'] <= 1 and data['numRanks'] <= 1:
            for _ in range(data['numCards']):
                new_card = Card(deck_id=new_deck.id, orientation=new_deck.orientation, width=new_deck.width, height=new_deck.height)
                db.session.add(new_card)
        else:
            for suit in range(data['numSuits']):
                for rank in range(data['numRanks']):
                    new_card = Card(deck_id=new_deck.id, suit=suit, rank=rank, orientation=new_deck.orientation, width=new_deck.width, height=new_deck.height)
                    db.session.add(new_card)

        # Commit the cards to the database
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

@app.route('/decks/<uid>', methods=['DELETE'])
def delete_deck(uid):
    # Find the deck with the given uid
    deck = Deck.query.filter_by(uid=uid).first()

    # If the deck is not found, return an error message
    if not deck:
        return jsonify({'message': 'Deck not found'}), 404

    # Delete related CardText models
    from mycards.model import CardText
    CardText.query.filter_by(deck_id=deck.id).delete()

    # Delete related card records
    from mycards.model import Card
    cards = Card.query.filter_by(deck_id=deck.id).all()
    for card in cards:
        db.session.delete(card)

    # Delete the deck
    db.session.delete(deck)
    db.session.commit()

    # Return a success message
    return jsonify({'message': 'Deck deleted successfully'})

@app.route('/card', methods=['POST'])
def upsert_card():
    from mycards.model import Card, CardText
    data = request.get_json()

    # strip the data.card_text object off the data into a separate variable
    card_text = data['card_text']
    data.pop('card_text', None)

    # Create a new Card model
    new_card = Card(
        deck_id=data['deck_id'],
        suit=data.get('suit'),
        rank=data.get('rank'),
        orientation=data.get('orientation'),
        width=data.get('width'),
        height=data.get('height')
    )

    # Add the new card to the session
    db.session.add(new_card)
    db.session.commit()

    # Check if card_text is provided in the request data
    if card_text:
        # Create a new CardText model
        new_card_text = CardText(
            deck_id=data['deck_id'],
            card_id=new_card.id, 
            front_text=card_text['front_text'], 
            rear_text=card_text['rear_text'])

        # Add the new card text to the session
        db.session.add(new_card_text)
        db.session.commit()

    return jsonify({'message': 'Card created successfully', 'card_id': new_card.id})

@app.route('/cards/<uid>', methods=['DELETE'])
def delete_card(uid):
    # Find the card with the given uid
    from mycards.model import Card, CardText
    card = Card.query.filter_by(uid=uid).first()

    # If the card is not found, return an error message
    if not card:
        return jsonify({'message': 'Card not found'}), 404

    # Delete related CardText models
    CardText.query.filter_by(card_id=card.id).delete()

    # Delete the card
    db.session.delete(card)
    db.session.commit()

    # Return a success message
    return jsonify({'message': 'Card deleted successfully'})