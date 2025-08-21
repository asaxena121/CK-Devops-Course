# Makefile for Kubernetes Services Demo

.PHONY: help build deploy clean test local-up local-down

# Default target
help:
	@echo "Kubernetes Services Demo"
	@echo "========================"
	@echo ""
	@echo "Available targets:"
	@echo "  build       - Build Docker images"
	@echo "  deploy      - Deploy to Kubernetes"
	@echo "  clean       - Clean up Kubernetes resources"
	@echo "  test        - Run service discovery tests"
	@echo "  local-up    - Start with Docker Compose"
	@echo "  local-down  - Stop Docker Compose"
	@echo "  help        - Show this help"

# Build Docker images
build:
	@echo "Building Docker images..."
	docker build -t frontend-k8s-demo:latest ./frontend
	docker build -t backend-k8s-demo:latest ./backend
	docker build -t database-k8s-demo:latest ./database
	@echo "✅ Images built successfully!"

# Deploy to Kubernetes
deploy: build
	@echo "Deploying to Kubernetes..."
	./deploy.sh

# Clean up Kubernetes resources
clean:
	@echo "Cleaning up..."
	./cleanup.sh

# Run basic tests
test:
	@echo "Running service discovery tests..."
	@echo "Testing ClusterIP service..."
	kubectl exec -it deployment/frontend-deployment -n k8s-services-demo -- \
		curl -s backend-service:5000/api/health || echo "❌ Backend service test failed"
	
	@echo "Testing Headless service DNS..."
	kubectl exec -it deployment/frontend-deployment -n k8s-services-demo -- \
		nslookup database-headless || echo "❌ Headless DNS test failed"
	
	@echo "✅ Basic tests completed!"

# Local development with Docker Compose
local-up:
	@echo "Starting local development environment..."
	docker-compose up --build -d
	@echo "✅ Local environment started!"
	@echo "Frontend: http://localhost:3000"
	@echo "Backend: http://localhost:5000"

local-down:
	@echo "Stopping local environment..."
	docker-compose down
	@echo "✅ Local environment stopped!"

# Port forward for easy access
port-forward:
	@echo "Setting up port forwarding..."
	kubectl port-forward svc/frontend-nodeport 8080:3000 -n k8s-services-demo

# Get service information
info:
	@echo "Service Information:"
	@echo "==================="
	kubectl get svc -n k8s-services-demo
	@echo ""
	@echo "Pod Information:"
	@echo "==============="
	kubectl get pods -n k8s-services-demo -o wide
	@echo ""
	@echo "Endpoint Information:"
	@echo "===================="
	kubectl get endpoints -n k8s-services-demo
