import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    BITCOIN_TESTNET = True  # Set to False for mainnet
    PORT = int(os.environ.get('PORT', 5000))
    WALLET_DESCRIPTOR = os.environ.get('WALLET_DESCRIPTOR', 'tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx')
    DATABASE_PATH = os.environ.get('DATABASE_PATH', os.path.join(os.path.dirname(os.path.dirname(__file__)), 'wallet.db'))
