class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../instance/wallet.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your-secret-key'  # Replace with a secure key