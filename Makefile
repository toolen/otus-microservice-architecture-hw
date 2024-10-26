pwd=$(shell pwd)
kubernetes_version=v1.31.0
namespace=m

lint:
	docker run --rm -v $(pwd)/manifests:/data stackrox/kube-linter:latest lint /data

minikube\:start:
	minikube start --driver=virtualbox --kubernetes-version=$(kubernetes_version) --nodes=1
	kubectl config use-context minikube
	kubectl create namespace $(namespace) || exit 0

minikube\:loadimage:
	minikube image load toolen/hw02:0.0.1

minikube\:prepare:
	kubectl config use-context minikube
	helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx/
	helm repo update
	helm upgrade --install nginx ingress-nginx/ingress-nginx --namespace $(namespace) --set controller.service.externalIPs={$(shell minikube ip)}

minikube\:install:
	kubectl config use-context minikube
	kubectl apply --namespace $(namespace) -f $(pwd)/manifests/

minikube\:check:
    # minikube tunnel -c
	# curl http://$(shell minikube ip)/health
	curl --resolve "arch.homework:80:$(shell minikube ip)" -i http://arch.homework/health
