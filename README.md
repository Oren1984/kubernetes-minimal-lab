# kubernetes-minimal-lab

A minimal Kubernetes project demonstrating the flow: **build → push → deploy → expose**.  
Includes plain Kubernetes YAML manifests and a simple Helm chart.  
(ArgoCD is recommended as a separate project to keep this one minimal.)

---

## 📂 Project Structure
kubernetes-minimal-lab/
├─ app/ # Flask "Hello, Kubernetes!" sample app
│ ├─ app.py
│ ├─ requirements.txt
│ └─ Dockerfile
├─ k8s/ # Plain Kubernetes manifests
│ ├─ namespace.yaml
│ ├─ deployment.yaml
│ ├─ service.yaml
│ ├─ ingress.yaml # optional (NGINX Ingress)
│ └─ pvc.yaml # optional (PersistentVolumeClaim)
└─ helm/
└─ helm-chart/ # Helm chart for the same app
├─ Chart.yaml
├─ values.yaml
└─ templates/
├─ _helpers.tpl
├─ deployment.yaml
├─ service.yaml
└─ ingress.yaml


---

## Prerequisites
- Docker
- kubectl connected to a running cluster (minikube / k3s / kind / EKS)
- (Optional) NGINX Ingress Controller for `ingress.yaml`
- Helm v3 if you want to deploy via Helm

---

## 1. Build & Push the Docker image
```bash
cd app
# Build
docker build -t <YOUR_DOCKERHUB_USERNAME>/k8s-minimal:1.0.0 .

# Login (first time)
docker login

# Push
docker push <YOUR_DOCKERHUB_USERNAME>/k8s-minimal:1.0.0
2A. Deploy using plain YAML

# Create namespace
kubectl apply -f k8s/namespace.yaml

# Update image name in k8s/deployment.yaml first
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# (Optional) Ingress / PVC
# kubectl apply -f k8s/ingress.yaml
# kubectl apply -f k8s/pvc.yaml


🔎 Test with port-forward
# Default
kubectl -n k8s-minimal port-forward deploy/web 8080:8080
curl http://localhost:8080/

# ⚠️ If port 8080 is already in use (e.g. Jenkins is running),
# use another local port:
kubectl -n k8s-minimal port-forward deploy/web 8081:8080
curl http://localhost:8081/
2B. Deploy using Helm


# Update your image in helm/helm-chart/values.yaml
helm upgrade --install k8s-minimal ./helm/helm-chart \
  --namespace k8s-minimal --create-namespace
Enable ingress via Helm:


helm upgrade --install k8s-minimal ./helm/helm-chart \
  --namespace k8s-minimal --create-namespace \
  --set ingress.enabled=true \
  --set ingress.host=k8s-minimal.local
3. Expose
With port-forward (local testing)

With Ingress (recommended in clusters with NGINX/Traefik)

Or change Service to NodePort (edit service.yaml)

4. Clean Up
# YAML
kubectl delete -f k8s --ignore-not-found=true

# Helm
helm uninstall k8s-minimal -n k8s-minimal || true
kubectl delete ns k8s-minimal --ignore-not-found=true


📌 Notes
Always update the image name in k8s/deployment.yaml or in helm/helm-chart/values.yaml.
