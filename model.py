from mycards.db import db
from datetime import datetime

class Deck(db.Model):
    __tablename__ = 'decks'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    numCards = db.Column(db.Integer, nullable=False)
    numSuits = db.Column(db.Integer, nullable=False)
    numRanks = db.Column(db.Integer, nullable=False)
    bgImage = db.Column(db.String(255), nullable=True)
    type = db.Column(db.String(80), nullable=False)
    orientation = db.Column(db.String(80), nullable=True) # portrait or landscape
    width = db.Column(db.Integer, nullable=True)
    height = db.Column(db.Integer, nullable=True)
    cards = db.relationship('Card', backref='deck', lazy=True)

    # init named parameters:
    # uid=data['uid'],
    #     name=data['name'],
    #     numCards=data['numCards'],
    #     numSuits=data['numSuits'],
    #     numRanks=data['numRanks'],
    #     bgImage=data['bgImage'],
    #     type=data['type'],
    #     orientation=data.get('orientation'),
    #     width=data.get('width'),
    #     height=data.get('height'),
    def __init__(self, name=None, uid=None, numCards=None, numSuits=None, numRanks=None, bgImage=None, type=None, orientation=None, width=None, height=None):
        self.name = name
        self.uid = uid
        self.bgImage = bgImage
        self.numCards = numCards
        self.numSuits = numSuits
        self.numRanks = numRanks
        self.type = type
        self.orientation = orientation if orientation is not None else "portrait"  # Default to portrait if not provided
        self.width = width if width is not None else 0.0635  # Default to standard playing card width in meters if not provided
        self.height = height if height is not None else 0.0889  # Default to standard playing card height in meters if not provided

    def __repr__(self):
        return f'<Deck {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'uid': self.uid,
            'name': self.name,
            'numCards': self.numCards,
            'numSuits': self.numSuits,
            'numRanks': self.numRanks,
            'bgImage': self.bgImage,
            'type': self.type,
            'cards': [card.to_dict() for card in self.cards]
        }

# Standard suit ranks mapping from int to values
def get_name_of_suit(suit):
    if suit is None:
        return "Invalid suit"
    suit = int(suit)
    # Return the suit name based on the integer value provided
    if suit == 0:
        return "spades"
    elif suit == 1:
        return "hearts"
    elif suit == 2:
        return "diamonds"
    elif suit == 3:
        return "clubs"
    else:
        return "Invalid suit"

# Method to convert rank index int to a string (A, 2 ... 10, J, Q, K)
def rank_index_to_string(rank_index):
    if rank_index is None:
        return 'Invalid rank'

    rank_index = int(rank_index)

    if rank_index == 0:
        return "A"
    elif 1 <= rank_index <= 9:
        return str(rank_index + 1)
    elif rank_index == 10:
        return "J"
    elif rank_index == 11:
        return "Q"
    elif rank_index == 12:
        return "K"
    else:
        return "Invalid rank"

class Card(db.Model):
    __tablename__ = 'cards'
    id = db.Column(db.Integer, primary_key=True)
    deck_id = db.Column(db.Integer, db.ForeignKey('decks.id'), nullable=False)
    rank = db.Column(db.String(80), nullable=True)
    suit = db.Column(db.String(80), nullable=True)
    orientation = db.Column(db.String(80), nullable=True)
    width = db.Column(db.Integer, nullable=True)
    height = db.Column(db.Integer, nullable=True)

    def __init__(self, deck_id, rank=None, suit=None, orientation=None, width=None, height=None):
        self.deck_id = deck_id
        self.rank = rank
        self.suit = suit
        self.orientation = orientation if orientation is not None else "portrait"
        # Set default width and height if not provided
        self.width = width if width is not None else 0.0635  # Standard playing card width in meters
        self.height = height if height is not None else 0.0889  # Standard playing card height in meters

    def __repr__(self):
        suit_name = get_name_of_suit(self.suit)
        rank_string = rank_index_to_string(self.rank)
        return f'<Card {rank_string} of {suit_name}>'

    def to_dict(self):
        suit_name = get_name_of_suit(self.suit)
        rank_string = rank_index_to_string(self.rank)
        return {
            'id': self.id,
            'deck_id': self.deck_id,
            'rank': self.rank,
            'suit': self.suit,
            'rank_string': rank_string,
            'suit_name': suit_name,
            'card_text': self.card_text.to_dict() if self.card_text else None,
            'orientation': self.orientation,
            'width': self.width,
            'height': self.height
        }

class CardText(db.Model):
    __tablename__ = 'card_texts'
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('cards.id'), nullable=False)
    deck_id = db.Column(db.Integer, db.ForeignKey('decks.id'), nullable=False)
    front_text = db.Column(db.Text, nullable=True)
    rear_text = db.Column(db.Text, nullable=True)

    card = db.relationship('Card', backref=db.backref('card_text', uselist=False), lazy=True)

    def __repr__(self):
        return f'<CardText {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'card_id': self.card_id,
            'deck_id': self.deck_id,
            'front_text': self.front_text,
            'rear_text': self.rear_text
        }

# GameType model
class GameType(db.Model):
    __tablename__ = 'game_types'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)

# Playfield model
# class Playfield(db.Model):
#     __tablename__ = 'playfields'
#     id = db.Column(db.Integer, primary_key=True)
#     uid = db.Column(db.String, nullable=False)
#     name = db.Column(db.String, nullable=False)
#     game_id = db.Column(db.Integer, db.ForeignKey('game_types.id'), nullable=False)

# MoveSet model
class MoveSet(db.Model):
    __tablename__ = 'movesets'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game_types.id'), nullable=False)

# TODO: Implement PlayfieldArea model
# class PlayfieldArea(db.Model):
#     pass

# TODO: Implement PlayfieldSpot model
# class PlayfieldSpot(db.Model):
#     pass

# TODO: Implement GameMoveType model
# class GameMoveType(db.Model):
#     pass

# TODO: Implement PlayerGameMove model
# class PlayerGameMove(db.Model):
#     pass

# Implement GameInstance model
class GameInstance(db.Model):
    __tablename__ = 'game_instances'
    id = db.Column(db.Integer, primary_key=True)
    game_table_id = db.Column(db.Integer, db.ForeignKey('game_tables.id'), nullable=False)
    game_type_id = db.Column(db.Integer, db.ForeignKey('game_types.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)

# Implement PlayerGame pivot record
class PlayerGame(db.Model):
    __tablename__ = 'player_games'
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    game_table_id = db.Column(db.Integer, db.ForeignKey('game_tables.id'), nullable=False)
    game_instance_id = db.Column(db.Integer, db.ForeignKey('game_instances.id'), nullable=False)

    player = db.relationship('Player', backref='player_games', lazy=True)
    game_table = db.relationship('GameTable', backref='player_games', lazy=True)
    game_instance = db.relationship('GameInstance', backref='player_games', lazy=True)

# Implement GameTable model
class GameTable(db.Model):
    __tablename__ = 'game_tables'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    gametype_id = db.Column(db.Integer, db.ForeignKey('game_types.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)

class Player(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    verified = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_logged_in_at = db.Column(db.DateTime, nullable=True)
    deleted_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<Player {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'uid': self.uid,
            'name': self.name,
            'email': self.email,
            'verified': self.verified,
            'created_at': self.created_at,
            'last_logged_in_at': self.last_logged_in_at,
            'deleted_at': self.deleted_at
        }
