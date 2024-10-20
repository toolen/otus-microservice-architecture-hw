pwd=$(shell pwd)
kubernetes_version = v1.31.1
namespace=m

lint:
	docker run --rm -v $(pwd)/manifests:/data stackrox/kube-linter:latest lint /data

minikube\:start:
	minikube start --driver=virtualbox --kubernetes-version=$(kubernetes_version) --nodes=3
	kubectl config use-context minikube
	kubectl create namespace $(namespace) || exit 0

minikube\:loadimage:
	minikube image load toolen/hw02:0.0.1

minikube\:prepare:
	kubectl config use-context minikube
	helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx/
	helm repo update
	helm install nginx ingress-nginx/ingress-nginx --namespace m -f nginx-ingress.yaml

minikube\:install:
	kubectl config use-context minikube
	make minikube:install:backend
	make minikube:install:frontend
	make minikube:install:nlb
