#!/bin/bash

# Kubernetes Services Demonstration Deployment Script
echo "🚀 Deploying Kubernetes Services Demo..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    print_error "kubectl is not installed or not in PATH"
    exit 1
fi

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed or not in PATH"
    exit 1
fi

# Build Docker images
print_status "Building Docker images..."

print_status "Building frontend image..."
cd frontend
docker build -t frontend-k8s-demo:latest .
if [ $? -eq 0 ]; then
    print_success "Frontend image built successfully"
else
    print_error "Failed to build frontend image"
    exit 1
fi
cd ..

print_status "Building backend image..."
cd backend
docker build -t backend-k8s-demo:latest .
if [ $? -eq 0 ]; then
    print_success "Backend image built successfully"
else
    print_error "Failed to build backend image"
    exit 1
fi
cd ..

print_status "Building database image..."
cd database
docker build -t database-k8s-demo:latest .
if [ $? -eq 0 ]; then
    print_success "Database image built successfully"
else
    print_error "Failed to build database image"
    exit 1
fi
cd ..

# Deploy to Kubernetes
print_status "Deploying to Kubernetes..."

# Apply manifests in order
kubectl apply -f k8s-manifests/00-namespace.yaml
sleep 2

kubectl apply -f k8s-manifests/03-configmap-secret.yaml
sleep 2

kubectl apply -f k8s-manifests/01-deployments.yaml
sleep 5

kubectl apply -f k8s-manifests/02-services.yaml
sleep 2

# Optional: Apply ingress and network policy
# kubectl apply -f k8s-manifests/04-ingress-networkpolicy.yaml

print_success "Kubernetes manifests applied successfully!"

# Wait for deployments to be ready
print_status "Waiting for deployments to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/frontend-deployment -n k8s-services-demo
kubectl wait --for=condition=available --timeout=300s deployment/backend-deployment -n k8s-services-demo

# Wait for StatefulSet to be ready
kubectl wait --for=condition=ready --timeout=300s pod -l app=database -n k8s-services-demo

print_success "All deployments are ready!"

# Display service information
print_status "Service Information:"
echo
kubectl get services -n k8s-services-demo -o wide

print_status "Pod Information:"
echo
kubectl get pods -n k8s-services-demo -o wide

# Get NodePort information
NODEPORT=$(kubectl get service frontend-nodeport -n k8s-services-demo -o jsonpath='{.spec.ports[0].nodePort}')
NODE_IP=$(kubectl get nodes -o jsonpath='{.items[0].status.addresses[?(@.type=="InternalIP")].address}')

echo
print_success "🎉 Deployment completed successfully!"
echo
echo "📋 Access Information:"
echo "  Frontend (NodePort): http://${NODE_IP}:${NODEPORT}"
echo "  Frontend (LoadBalancer): Check 'kubectl get svc frontend-loadbalancer -n k8s-services-demo' for external IP"
echo
echo "🔍 Service Discovery Commands:"
echo "  kubectl get svc -n k8s-services-demo"
echo "  kubectl get endpoints -n k8s-services-demo"
echo "  kubectl describe svc backend-service -n k8s-services-demo"
echo
echo "🧪 Testing Commands:"
echo "  # Test ClusterIP service"
echo "  kubectl exec -it deployment/frontend-deployment -n k8s-services-demo -- curl backend-service:5000/api/health"
echo
echo "  # Test Headless service DNS"
echo "  kubectl exec -it deployment/frontend-deployment -n k8s-services-demo -- nslookup database-headless"
echo
echo "  # Port forward for local testing"
echo "  kubectl port-forward svc/frontend-nodeport 8080:3000 -n k8s-services-demo"
echo

print_warning "Note: If using Minikube, you might need to run 'minikube tunnel' for LoadBalancer services"
