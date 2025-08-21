from flask import Flask, jsonify
import socket
import time
import os
import random

app = Flask(__name__)

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'backend',
        'hostname': socket.gethostname(),
        'timestamp': time.time()
    })

@app.route('/api/data')
def get_data():
    # Simulate some data processing
    sample_data = [
        {'id': 1, 'name': 'ClusterIP Service', 'type': 'Internal', 'port': 80},
        {'id': 2, 'name': 'NodePort Service', 'type': 'External', 'port': 30080},
        {'id': 3, 'name': 'LoadBalancer Service', 'type': 'External', 'port': 80},
        {'id': 4, 'name': 'ExternalName Service', 'type': 'External', 'port': 443},
        {'id': 5, 'name': 'Headless Service', 'type': 'Internal', 'port': 5432}
    ]
    
    return jsonify({
        'status': 'success',
        'data': sample_data,
        'served_by': socket.gethostname(),
        'timestamp': time.time(),
        'random_id': random.randint(1000, 9999)
    })

@app.route('/api/services-info')
def services_info():
    """Provide information about different Kubernetes service types"""
    services_info = {
        'ClusterIP': {
            'description': 'Default service type, only accessible within cluster',
            'use_case': 'Internal microservice communication',
            'accessibility': 'Internal only',
            'ip_allocation': 'Cluster IP from service subnet'
        },
        'NodePort': {
            'description': 'Exposes service on each node IP at a static port',
            'use_case': 'Development, testing, or simple external access',
            'accessibility': 'External via NodeIP:NodePort',
            'port_range': '30000-32767'
        },
        'LoadBalancer': {
            'description': 'Cloud provider load balancer with external IP',
            'use_case': 'Production external access',
            'accessibility': 'External via cloud load balancer',
            'requirement': 'Cloud provider support'
        },
        'ExternalName': {
            'description': 'Maps service to external DNS name',
            'use_case': 'Access external services with consistent naming',
            'accessibility': 'DNS CNAME mapping',
            'no_proxy': 'Returns DNS record, no proxying'
        },
        'Headless': {
            'description': 'No cluster IP, returns pod IPs directly',
            'use_case': 'StatefulSets, direct pod communication',
            'accessibility': 'DNS returns pod IPs',
            'cluster_ip': 'None'
        }
    }
    
    return jsonify({
        'services': services_info,
        'served_by': socket.gethostname(),
        'timestamp': time.time()
    })

@app.route('/api/pod-info')
def pod_info():
    """Return information about this pod"""
    return jsonify({
        'pod_name': os.getenv('HOSTNAME', socket.gethostname()),
        'pod_ip': os.getenv('POD_IP', 'unknown'),
        'node_name': os.getenv('NODE_NAME', 'unknown'),
        'namespace': os.getenv('NAMESPACE', 'default'),
        'service_account': os.getenv('SERVICE_ACCOUNT', 'default'),
        'timestamp': time.time()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
