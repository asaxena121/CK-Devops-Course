from flask import Flask, render_template, jsonify
import requests
import os
import socket

app = Flask(__name__)

# Configuration
BACKEND_SERVICE_URL = os.getenv('BACKEND_SERVICE_URL', 'http://backend-service:5000')
DATABASE_SERVICE_URL = os.getenv('DATABASE_SERVICE_URL', 'http://database-service:5432')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'frontend',
        'hostname': socket.gethostname(),
        'backend_url': BACKEND_SERVICE_URL
    })

@app.route('/api/backend-data')
def get_backend_data():
    try:
        response = requests.get(f'{BACKEND_SERVICE_URL}/api/data', timeout=5)
        return jsonify({
            'status': 'success',
            'backend_response': response.json(),
            'frontend_hostname': socket.gethostname()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'frontend_hostname': socket.gethostname()
        }), 500

@app.route('/api/service-discovery')
def service_discovery():
    """Demonstrate service discovery across different service types"""
    services = {}
    
    # Test ClusterIP service (backend)
    try:
        response = requests.get(f'{BACKEND_SERVICE_URL}/api/health', timeout=3)
        services['backend_clusterip'] = {
            'status': 'accessible',
            'response': response.json()
        }
    except Exception as e:
        services['backend_clusterip'] = {
            'status': 'error',
            'error': str(e)
        }
    
    # Test database connection (headless service)
    try:
        response = requests.get(f'{DATABASE_SERVICE_URL}/health', timeout=3)
        services['database_headless'] = {
            'status': 'accessible',
            'response': response.json()
        }
    except Exception as e:
        services['database_headless'] = {
            'status': 'error',
            'error': str(e)
        }
    
    return jsonify({
        'frontend_hostname': socket.gethostname(),
        'services': services
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
