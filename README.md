# Kubernetes Minimal Lab

Minimal Kubernetes project demonstrating the flow: build → push → deploy → expose.

---

## Overview

A simple Kubernetes lab that runs a Dockerized Flask app using either plain YAML manifests or a Helm chart.

---

## Tech Stack

- Kubernetes
- Docker
- Helm
- Flask

---

## Quick Start

Build and push the image:

```bash
cd app
docker build -t <YOUR_DOCKERHUB_USERNAME>/k8s-minimal:1.0.0 .
docker login
docker push <YOUR_DOCKERHUB_USERNAME>/k8s-minimal:1.0.0

Deploy with plain YAML:

kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

Deploy with Helm:

helm upgrade --install k8s-minimal ./helm/helm-chart \
  --namespace k8s-minimal --create-namespace

---

## Usage

Before deploying, update the image name in:

k8s/deployment.yaml

helm/helm-chart/values.yaml

Test locally with port-forward:

kubectl -n k8s-minimal port-forward deploy/web 8080:8080
curl http://localhost:8080/

If port 8080 is already in use:

kubectl -n k8s-minimal port-forward deploy/web 8081:8080
curl http://localhost:8081/

Optional ingress with Helm:

helm upgrade --install k8s-minimal ./helm/helm-chart \
  --namespace k8s-minimal --create-namespace \
  --set ingress.enabled=true \
  --set ingress.host=k8s-minimal.local

---

## leanup

Delete YAML resources:

kubectl delete -f k8s --ignore-not-found=true

Remove Helm release:

helm uninstall k8s-minimal -n k8s-minimal || true
kubectl delete ns k8s-minimal --ignore-not-found=true

---

## Notes

Built for learning and demo purposes

Supports both plain manifests and Helm

Ingress and PVC are optional

Keep ArgoCD as a separate project to preserve scope
