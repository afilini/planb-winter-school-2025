import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    BITCOIN_TESTNET = True  # Set to False for mainnet
    PORT = int(os.environ.get('PORT', 5000))
    WALLET_MNEMONIC = os.environ.get('WALLET_MNEMONIC', "illegal often ceiling century payment effort apology reduce tuition drip wasp work")
    DATABASE_PATH = os.environ.get('DATABASE_PATH', "wallet.sqlite")
