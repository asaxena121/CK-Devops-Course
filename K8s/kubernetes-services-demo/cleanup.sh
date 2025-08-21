#!/bin/bash

# Cleanup script for Kubernetes Services Demo
echo "🧹 Cleaning up Kubernetes Services Demo..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# Delete Kubernetes resources
print_status "Deleting Kubernetes resources..."

kubectl delete namespace k8s-services-demo

print_success "Namespace and all resources deleted!"

# Remove Docker images
print_status "Removing Docker images..."
docker rmi frontend-k8s-demo:latest backend-k8s-demo:latest database-k8s-demo:latest 2>/dev/null

print_success "🎉 Cleanup completed!"
