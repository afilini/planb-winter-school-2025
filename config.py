import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    BITCOIN_TESTNET = True  # Set to False for mainnet
    PORT = int(os.environ.get('PORT', 5000))
    WALLET_DESCRIPTOR = os.environ.get('WALLET_DESCRIPTOR', "wpkh([c258d2e4/84h/1h/0h]tpubDDYkZojQFQjht8Tm4jsS3iuEmKjTiEGjG6KnuFNKKJb5A6ZUCUZKdvLdSDWofKi4ToRCwb9poe1XdqfUnP4jaJjCB2Zwv11ZLgSbnZSNecE/0/*)")
    DATABASE_PATH = os.environ.get('DATABASE_PATH', os.path.join(os.path.dirname(os.path.dirname(__file__)), 'wallet.db'))
