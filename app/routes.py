from flask import Blueprint, request, redirect, url_for, jsonify, render_template_string
from .models import Wallet, db
from zarinpal.api import ZarinPalPayment  # Assumed available

bp = Blueprint('main', __name__)

# Cost per API call (fixed for simplicity)
API_CALL_COST = 10.0

# ZarinPal merchant ID
MERCHANT_ID = "your_merchant_id"  # Replace with your actual merchant ID

@bp.route('/topup', methods=['GET', 'POST'])
def topup():
    """Initiate wallet top-up with ZarinPal."""
    user_id = 'sample_user'  # Replace with actual user_id from WSO2 authentication
    if request.method == 'POST':
        amount = float(request.form['amount'])
        payment_handler = ZarinPalPayment(MERCHANT_ID, amount)
        callback_url = url_for('main.callback', _external=True)
        description = "Wallet top-up"
        mobile = "1234567890"  # Replace with user's mobile
        email = "user@example.com"  # Replace with user's email
        
        result = payment_handler.request_payment(callback_url, description, mobile, email)
        # Assuming result contains a 'payment_url' key; adjust based on actual response
        payment_url = result.get('payment_url')
        if payment_url:
            return redirect(payment_url)
        return "Payment initiation failed", 500
    
    # Simple form for GET request
    return render_template_string('''
        <form method="post">
            <label for="amount">Amount:</label>
            <input type="number" id="amount" name="amount" step="0.01" required>
            <input type="submit" value="Top Up">
        </form>
    ''')

@bp.route('/callback')
def callback():
    """Handle ZarinPal payment callback."""
    authority = request.args.get('Authority')
    status = request.args.get('Status')
    user_id = 'sample_user'  # Replace with actual user_id (stored or retrieved)
    amount = 1000  # Should be stored temporarily before payment initiation
    
    if status == 'OK':
        payment_handler = ZarinPalPayment(MERCHANT_ID, amount)
        result = payment_handler.verify_payment(authority)
        # Assuming result has a 'status' key; adjust based on actual response
        if result.get('status') == 'success':
            wallet = Wallet.query.get(user_id)
            if wallet:
                wallet.balance += amount
            else:
                wallet = Wallet(user_id=user_id, balance=amount)
                db.session.add(wallet)
            db.session.commit()
            return "Payment successful, wallet updated."
        return "Payment verification failed.", 400
    return "Payment cancelled or failed.", 400

@bp.route('/deduct', methods=['POST'])
def deduct():
    """Endpoint for WSO2 to deduct wallet balance per API call."""
    data = request.get_json()
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({"error": "user_id required"}), 400
    
    wallet = Wallet.query.get(user_id)
    if wallet and wallet.balance >= API_CALL_COST:
        wallet.balance -= API_CALL_COST
        db.session.commit()
        return jsonify({"status": "success", "balance": wallet.balance})
    return jsonify({"status": "insufficient_funds"}), 403

@bp.route('/balance')
def balance():
    """Check wallet balance."""
    user_id = 'sample_user'  # Replace with actual user_id
    wallet = Wallet.query.get(user_id)
    balance = wallet.balance if wallet else 0.0
    return jsonify({"balance": balance})