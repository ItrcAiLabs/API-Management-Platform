from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Wallet(db.Model):
    user_id = db.Column(db.String(50), primary_key=True)  # User ID from WSO2
    balance = db.Column(db.Float, default=0.0)

    def __repr__(self):
        return f'<Wallet user_id={self.user_id}, balance={self.balance}>'