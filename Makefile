pwd=$(shell pwd)

lint:
	docker run --rm -v $(pwd)/manifests:/data stackrox/kube-linter:latest lint /data