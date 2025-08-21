# Testing Commands for Kubernetes Services Demo

## Service Discovery Tests

### 1. ClusterIP Service Testing
```bash
# Test backend service from frontend pod
kubectl exec -it deployment/frontend-deployment -n k8s-services-demo -- \
  curl -s backend-service:5000/api/health | jq

# Test backend service endpoints
kubectl exec -it deployment/frontend-deployment -n k8s-services-demo -- \
  curl -s backend-service:5000/api/services-info | jq

# Check DNS resolution
kubectl exec -it deployment/frontend-deployment -n k8s-services-demo -- \
  nslookup backend-service
```

### 2. Headless Service Testing
```bash
# Check headless DNS - returns multiple A records (pod IPs)
kubectl exec -it deployment/frontend-deployment -n k8s-services-demo -- \
  nslookup database-headless

# Compare with regular service DNS - returns single A record (cluster IP)
kubectl exec -it deployment/frontend-deployment -n k8s-services-demo -- \
  nslookup database-service

# Test direct pod communication via headless service
kubectl exec -it deployment/frontend-deployment -n k8s-services-demo -- \
  curl -s database-headless:5432/health | jq
```

### 3. ExternalName Service Testing
```bash
# Check external service DNS mapping
kubectl exec -it deployment/frontend-deployment -n k8s-services-demo -- \
  nslookup external-api-service

# Should resolve to api.github.com
kubectl exec -it deployment/frontend-deployment -n k8s-services-demo -- \
  dig external-api-service
```

## Service Endpoint Analysis

### View All Service Endpoints
```bash
# Show all services and their endpoints
kubectl get svc,endpoints -n k8s-services-demo

# Detailed endpoint information
kubectl describe endpoints -n k8s-services-demo

# Show service without selector (ExternalName)
kubectl describe svc external-api-service -n k8s-services-demo
```

### Compare Service Types
```bash
# ClusterIP - has cluster IP and endpoints
kubectl get svc backend-service -n k8s-services-demo -o yaml

# Headless - clusterIP: None, but has endpoints
kubectl get svc database-headless -n k8s-services-demo -o yaml

# ExternalName - no cluster IP, no endpoints
kubectl get svc external-api-service -n k8s-services-demo -o yaml
```

## Load Balancing Tests

### Test Backend Load Balancing
```bash
# Multiple requests to see load balancing across backend pods
for i in {1..10}; do
  kubectl exec -it deployment/frontend-deployment -n k8s-services-demo -- \
    curl -s backend-service:5000/api/pod-info | jq '.pod_name'
done
```

### Test Database Headless Service
```bash
# Direct pod access via headless service
kubectl get pods -l app=database -n k8s-services-demo -o jsonpath='{.items[*].metadata.name}'

# Test each pod directly
kubectl exec -it deployment/frontend-deployment -n k8s-services-demo -- \
  curl -s database-statefulset-0.database-headless:5432/health | jq

kubectl exec -it deployment/frontend-deployment -n k8s-services-demo -- \
  curl -s database-statefulset-1.database-headless:5432/health | jq
```

## External Access Tests

### NodePort Testing
```bash
# Get NodePort details
kubectl get svc frontend-nodeport -n k8s-services-demo

# Get node IP
NODE_IP=$(kubectl get nodes -o jsonpath='{.items[0].status.addresses[?(@.type=="InternalIP")].address}')
NODEPORT=$(kubectl get svc frontend-nodeport -n k8s-services-demo -o jsonpath='{.spec.ports[0].nodePort}')

echo "Frontend accessible at: http://$NODE_IP:$NODEPORT"

# Test NodePort access (if accessible)
curl -s http://$NODE_IP:$NODEPORT/api/health | jq
```

### LoadBalancer Testing
```bash
# Check LoadBalancer status
kubectl get svc frontend-loadbalancer -n k8s-services-demo

# Get external IP (may take time to provision)
kubectl get svc frontend-loadbalancer -n k8s-services-demo -o jsonpath='{.status.loadBalancer.ingress[0].ip}'

# For Minikube, you might need to run: minikube tunnel
```

## DNS Deep Dive

### Service DNS Patterns
```bash
# Full FQDN testing
kubectl exec -it deployment/frontend-deployment -n k8s-services-demo -- \
  nslookup backend-service.k8s-services-demo.svc.cluster.local

# Short name within same namespace
kubectl exec -it deployment/frontend-deployment -n k8s-services-demo -- \
  nslookup backend-service

# Cross-namespace access (if testing from different namespace)
kubectl exec -it deployment/frontend-deployment -n k8s-services-demo -- \
  nslookup backend-service.k8s-services-demo
```

### Headless Service DNS Records
```bash
# Get detailed DNS records for headless service
kubectl exec -it deployment/frontend-deployment -n k8s-services-demo -- \
  dig database-headless.k8s-services-demo.svc.cluster.local

# Individual pod DNS (StatefulSet pods have predictable DNS names)
kubectl exec -it deployment/frontend-deployment -n k8s-services-demo -- \
  nslookup database-statefulset-0.database-headless.k8s-services-demo.svc.cluster.local
```

## Network Policy Testing

### Test Pod Communication
```bash
# Test allowed communication (frontend to backend)
kubectl exec -it deployment/frontend-deployment -n k8s-services-demo -- \
  curl -s --connect-timeout 5 backend-service:5000/api/health

# Test blocked communication (if network policies are applied)
# This should work as backend to database is allowed
kubectl exec -it deployment/backend-deployment -n k8s-services-demo -- \
  curl -s --connect-timeout 5 database-service:5432/health
```

## Performance and Scaling Tests

### Scale Services and Test
```bash
# Scale backend deployment
kubectl scale deployment backend-deployment --replicas=5 -n k8s-services-demo

# Wait for scaling
kubectl wait --for=condition=available --timeout=120s deployment/backend-deployment -n k8s-services-demo

# Test load distribution
for i in {1..20}; do
  kubectl exec -it deployment/frontend-deployment -n k8s-services-demo -- \
    curl -s backend-service:5000/api/pod-info | jq -r '.pod_name'
done | sort | uniq -c
```

### Database StatefulSet Scaling
```bash
# Scale database StatefulSet
kubectl scale statefulset database-statefulset --replicas=3 -n k8s-services-demo

# Check headless service DNS with more pods
kubectl exec -it deployment/frontend-deployment -n k8s-services-demo -- \
  dig database-headless.k8s-services-demo.svc.cluster.local
```

## Monitoring and Debugging

### Service Troubleshooting
```bash
# Check service configuration
kubectl describe svc backend-service -n k8s-services-demo

# Check endpoints
kubectl get endpoints backend-service -n k8s-services-demo -o yaml

# Check pod labels and selectors
kubectl get pods -n k8s-services-demo --show-labels
```

### Network Troubleshooting
```bash
# Test network connectivity
kubectl exec -it deployment/frontend-deployment -n k8s-services-demo -- \
  nc -zv backend-service 5000

# Check iptables rules (on nodes)
# kubectl get nodes
# ssh to node and run: sudo iptables -t nat -L | grep backend-service
```

## Cleanup Tests
```bash
# Test service removal impact
kubectl delete svc backend-service -n k8s-services-demo

# Check what happens to DNS resolution
kubectl exec -it deployment/frontend-deployment -n k8s-services-demo -- \
  nslookup backend-service

# Recreate service
kubectl apply -f k8s-manifests/02-services.yaml
```

---

These commands provide comprehensive testing of all Kubernetes service types and their behaviors. Use them to understand how services work in different scenarios and troubleshoot networking issues.
