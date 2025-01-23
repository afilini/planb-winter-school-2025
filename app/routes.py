from flask import render_template, request, flash, redirect, url_for
from app import app

import bdkpython as bdk
import threading
import time

SIGNET_ESPLORA_URL = "http://signet.bitcoindevkit.net"

descriptor = bdk.Descriptor(app.config["WALLET_DESCRIPTOR"], bdk.Network.SIGNET)
sqlite_config = bdk.SqliteDbConfiguration(path=app.config["DATABASE_PATH"])
db_config = bdk.DatabaseConfig.SQLITE(sqlite_config)
blockchain_config = bdk.BlockchainConfig.ESPLORA(
    bdk.EsploraConfig(
        base_url = "http://mutinynet.com/api",
        proxy = None,
        concurrency = None,
        stop_gap = 100,
        timeout = None,
    )
)
blockchain = bdk.Blockchain(blockchain_config)

wallet = bdk.Wallet(
    descriptor=descriptor,
    change_descriptor=None,
    network=bdk.Network.SIGNET,
    database_config=db_config,
)

class BackgroundTasks(threading.Thread):
    def run(self,*args,**kwargs):
        while True:
            wallet.sync(blockchain, None)
            time.sleep(10)

# t = BackgroundTasks()
# t.start()

# For demo purposes - in production you'd want to properly manage keys
WALLET_ADDRESS = "tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx"  # Example testnet address

@app.route('/')
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', 
                         balance=wallet.get_balance().total / 1e8,
                         transactions=[])

@app.route('/transactions')
def transactions():
    # Placeholder for transaction data
    transactions = []  # We'll implement the logic later
    return render_template('transactions.html', transactions=transactions)

@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        # We'll implement the sending logic later
        flash('Transaction sent successfully!', 'success')
        return redirect(url_for('transactions'))
    return render_template('send.html')

@app.route('/receive')
def receive():
    return render_template('receive.html', address=WALLET_ADDRESS)

@app.route('/refresh', methods=['POST'])
def refresh_wallet():
    next_page = request.form.get('next', '/')
    
    try:
        # Refresh wallet logic will go here
        # For now just a placeholder
        flash('Wallet refreshed successfully', 'success')
    except Exception as e:
        flash(f'Error refreshing wallet: {str(e)}', 'error')
    
    return redirect(next_page)