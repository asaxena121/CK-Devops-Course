from flask import Flask, jsonify
import socket
import time
import os

app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'database',
        'hostname': socket.gethostname(),
        'timestamp': time.time(),
        'type': 'headless_service_demo'
    })

@app.route('/data')
def get_data():
    # Simulate database data
    return jsonify({
        'users': [
            {'id': 1, 'name': 'Alice', 'role': 'Admin'},
            {'id': 2, 'name': 'Bob', 'role': 'User'},
            {'id': 3, 'name': 'Charlie', 'role': 'User'}
        ],
        'served_by_pod': socket.gethostname(),
        'pod_ip': os.getenv('POD_IP', 'unknown'),
        'timestamp': time.time()
    })

@app.route('/stats')
def stats():
    return jsonify({
        'connections': 42,
        'uptime': '2h 30m',
        'database_size': '1.2GB',
        'served_by_pod': socket.gethostname(),
        'timestamp': time.time()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5432, debug=True)
