# kubernetes-minimal

Minimal personal Kubernetes project: **build → push → deploy → expose**.
Includes plain YAML *and* a simple Helm chart. (ArgoCD recommended as a separate project.)

> מבנה בסיסי לפרויקט קוברנטיס קצר: build → push → deploy → expose. כולל קבצי YAML ו־Helm. ארגו־סי־די מומלץ כפרויקט נפרד כדי לשמור על פשטות.

## Project Tree
```
kubernetes-minimal/
├─ app/                  # Flask "Hello, Kubernetes!"
│  ├─ app.py
│  ├─ requirements.txt
│  └─ Dockerfile
├─ k8s/                  # Plain manifests
│  ├─ namespace.yaml
│  ├─ deployment.yaml
│  ├─ service.yaml
│  ├─ ingress.yaml       # optional (NGINX Ingress)
│  └─ pvc.yaml           # optional
└─ helm/
   └─ kubernetes-minimal/  # Helm chart
      ├─ Chart.yaml
      ├─ values.yaml
      └─ templates/
         ├─ _helpers.tpl
         ├─ deployment.yaml
         ├─ service.yaml
         └─ ingress.yaml
```

## 0) Prereqs / דרישות מקדימות
- Docker, kubectl, and a running cluster (minikube/k3s/kind/EKS)
- (Optional) NGINX Ingress Controller for `ingress.yaml`
- Helm v3 if you want to use the chart

## 1) Build & Push the image / בנייה ודחיפה
```bash
cd app
# build
docker build -t <YOUR_DOCKERHUB_USERNAME>/k8s-minimal:1.0.0 .
# login (first time)
docker login
# push
docker push <YOUR_DOCKERHUB_USERNAME>/k8s-minimal:1.0.0
```

## 2A) Deploy with plain YAML / דיפלוי עם YAML
```bash
# create namespace
kubectl apply -f k8s/namespace.yaml

# set your image in k8s/deployment.yaml first
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# (optional) ingress / pvc
# kubectl apply -f k8s/ingress.yaml
# kubectl apply -f k8s/pvc.yaml
```

### Test (port-forward)
```bash
kubectl -n k8s-minimal port-forward deploy/web 8080:8080
curl http://localhost:8080/
```

## 2B) Deploy with Helm / דיפלוי עם Helm
```bash
# set your image repo/tag in helm/kubernetes-minimal/values.yaml
helm upgrade --install k8s-minimal ./helm/kubernetes-minimal   --namespace k8s-minimal --create-namespace
```

Enable ingress via Helm:
```bash
helm upgrade --install k8s-minimal ./helm/kubernetes-minimal   --namespace k8s-minimal --create-namespace   --set ingress.enabled=true --set ingress.host=k8s-minimal.local
```

## 3) Expose / חשיפה
- With `port-forward` (above) for local testing, or
- With Ingress (recommended in clusters with NGINX Ingress), or
- Change Service to `NodePort` if you prefer (edit `service.yaml`).

## 4) Clean up / ניקוי
```bash
# YAML
kubectl delete -f k8s --ignore-not-found=true
# Helm
helm uninstall k8s-minimal -n k8s-minimal || true
kubectl delete ns k8s-minimal --ignore-not-found=true
```

---
**Notes / הערות**
- Update the image name in `k8s/deployment.yaml` *or* set via Helm `values.yaml`.
- Keep ArgoCD for a separate repo to stay "minimal".
