from flask import Flask, request, jsonify
from flask_cors import CORS
import hashlib
import time

app = Flask(__name__)
CORS(app)

# Simulated blacklist of known fraud addresses
BLACKLIST = {
    "0xdead35cc6634c0532925a3b8d4c9cf4a3f5e00",
    "0xbad1f109551bd432803012645ac136dde900",
    "0x1234badactor5678badactor9012badactor",
}

def get_address_reputation(address):
    """Check address against blacklist and return risk score 0-100"""
    addr_lower = address.lower()
    for blocked in BLACKLIST:
        if blocked[:10] in addr_lower:
            return 95
    return 5

def calculate_fraud_score(data):
    """
    Weighted fraud scoring across 6 risk dimensions.
    Returns score 0-100 where 100 = definite fraud.
    """
    scores = {}

    # 1. Velocity (transactions per hour)
    velocity = int(data.get('velocity', 1))
    scores['velocity'] = min(100, velocity * 2)

    # 2. Amount anomaly
    amount = float(data.get('amount', 0))
    if amount > 100:    scores['amount'] = 90
    elif amount > 10:   scores['amount'] = 60
    elif amount > 1:    scores['amount'] = 30
    else:               scores['amount'] = 10

    # 3. Account age
    age_map = {'new': 95, 'week': 60, 'month': 30, 'year': 5}
    scores['age'] = age_map.get(data.get('acct_age', 'year'), 5)

    # 4. Time pattern
    time_map = {'odd': 80, 'weekend': 30, 'normal': 5}
    scores['time'] = time_map.get(data.get('tx_time', 'normal'), 5)

    # 5. Gas fee anomaly
    gas = int(data.get('gas', 21))
    if gas > 300:   scores['gas'] = 85
    elif gas > 100: scores['gas'] = 50
    elif gas > 50:  scores['gas'] = 25
    else:           scores['gas'] = 5

    # 6. Address reputation
    scores['address'] = get_address_reputation(data.get('from_addr', ''))

    # Weighted average
    weights = {
        'velocity': 0.25,
        'amount':   0.20,
        'age':      0.20,
        'time':     0.10,
        'gas':      0.10,
        'address':  0.15,
    }

    overall = sum(scores[k] * weights[k] for k in scores)
    overall = max(1, min(99, round(overall)))

    return {
        'overall': overall,
        'factors': scores,
        'verdict': 'BLOCK' if overall > 70 else 'FLAG' if overall > 40 else 'APPROVE'
    }

def generate_tx_id(data):
    """Generate a deterministic transaction ID"""
    payload = str(data) + str(time.time())
    return '0x' + hashlib.sha256(payload.encode()).hexdigest()[:16].upper()

@app.route('/analyze', methods=['POST'])
def analyze():
    """Main fraud analysis endpoint"""
    data = request.json
    if not data:
        return jsonify({'error': 'No transaction data provided'}), 400

    required = ['from_addr', 'to_addr', 'amount']
    for field in required:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400

    result = calculate_fraud_score(data)
    result['tx_id'] = generate_tx_id(data)
    result['timestamp'] = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())
    result['from_addr'] = data['from_addr']
    result['to_addr'] = data['to_addr']
    result['amount'] = data['amount']

    return jsonify(result)

@app.route('/blacklist/add', methods=['POST'])
def add_to_blacklist():
    """Add address to fraud blacklist"""
    data = request.json
    if not data or 'address' not in data:
        return jsonify({'error': 'Address required'}), 400
    BLACKLIST.add(data['address'].lower())
    return jsonify({'success': True, 'blacklist_size': len(BLACKLIST)})

@app.route('/blacklist/check', methods=['GET'])
def check_blacklist():
    """Check if address is blacklisted"""
    address = request.args.get('address', '').lower()
    is_blocked = any(b[:10] in address for b in BLACKLIST)
    return jsonify({'address': address, 'blocked': is_blocked})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'online',
        'model': 'sentinel-v1.0',
        'blacklist_size': len(BLACKLIST)
    })

if __name__ == '__main__':
    print("SENTINEL Fraud Detection API running on http://localhost:5000")
    app.run(debug=True, port=5000)
