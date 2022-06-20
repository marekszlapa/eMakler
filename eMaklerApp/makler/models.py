from makler import db

class Akcje(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    nazwa = db.Column(db.String(length=50), nullable=False)
    cena = db.Column(db.Float(), nullable=False)
    ilosc = db.Column(db.Integer(), nullable=False)

    def __repr__(self):
        return f'Akcje {self.nazwa}'