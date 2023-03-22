from mycards.db import db

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
            'type': self.type
        }
