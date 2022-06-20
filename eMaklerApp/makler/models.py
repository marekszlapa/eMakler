from makler import db

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    items = db.relationship('Akcje', backref='owned_user', lazy=True)

class Akcje(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    nazwa = db.Column(db.String(length=50), nullable=False)
    cena = db.Column(db.Float(), nullable=False)
    ilosc = db.Column(db.Integer(), nullable=False)
    wlasciciel = db.Column(db.Integer(), db.ForeignKey('user.id'))
    def __repr__(self):
        return f'Akcje {self.nazwa}'