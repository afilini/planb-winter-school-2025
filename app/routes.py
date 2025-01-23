from flask import render_template, request, flash, redirect, url_for
from app import app

# For demo purposes - in production you'd want to properly manage keys
WALLET_ADDRESS = "tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx"  # Example testnet address

@app.route('/')
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', 
                         balance=0.1,
                         address=WALLET_ADDRESS,
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