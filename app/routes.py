from flask import render_template, request, flash, redirect, url_for
from app import app

import bdkpython as bdk

mnemonic = bdk.Mnemonic.from_string(app.config["WALLET_MNEMONIC"])
key = bdk.DescriptorSecretKey(bdk.Network.SIGNET, mnemonic, None)
descriptor = bdk.Descriptor.new_bip84(key, bdk.KeychainKind.EXTERNAL, bdk.Network.SIGNET)
sqlite_config = bdk.SqliteDbConfiguration(path=app.config["DATABASE_PATH"])
db_config = bdk.DatabaseConfig.SQLITE(sqlite_config)
blockchain_config = bdk.BlockchainConfig.ESPLORA(
    bdk.EsploraConfig(
        base_url = "https://mutinynet.com/api",
        proxy = None,
        concurrency = 8,
        stop_gap = 10,
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
    return render_template('transactions.html', transactions=wallet.list_transactions(include_raw=True))

@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        # Get form data
        recipient_address = request.form.get('recipient')
        amount = request.form.get('amount')

        # Basic validation
        if not recipient_address or not amount:
            flash('Please fill in all fields', 'error')
            return render_template('send.html')
            
        try:
            amount = int(float(amount) * 1e8)
        except ValueError:
            flash('Invalid amount', 'error')
            return render_template('send.html')
        
        addr = bdk.Address(recipient_address, network=bdk.Network.SIGNET)
        builder = bdk.TxBuilder().add_recipient(addr.script_pubkey(), amount)

        psbt = builder.finish(wallet).psbt
        wallet.sign(psbt, None)
        blockchain.broadcast(psbt.extract_tx())

        wallet.sync(blockchain, None)

        # We'll implement the actual sending logic later
        flash('Transaction sent successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('send.html')

@app.route('/receive')
def receive():
    return render_template('receive.html', address=wallet.get_address(bdk.AddressIndex.LAST_UNUSED()).address.as_string())

@app.route('/refresh', methods=['POST'])
def refresh_wallet():
    next_page = request.form.get('next', '/')
    
    try:
        wallet.sync(blockchain, None)
        # Refresh wallet logic will go here
        # For now just a placeholder
        flash('Wallet refreshed successfully', 'success')
    except Exception as e:
        flash(f'Error refreshing wallet: {str(e)}', 'error')
    
    return redirect(next_page)