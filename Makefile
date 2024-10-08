image=toolen/hw02
tag=latest
image_tag=$(image):$(tag)
hadolint_version=2.12.0
trivy_version=0.53.0
pwd=$(shell pwd)

build:
	make hadolint
	DOCKER_BUILDKIT=1 docker build --pull --no-cache -t $(image_tag) .
	make trivy

builder\:shell:
	DOCKER_BUILDKIT=1 docker build --pull --target builder -t $(image):builder .
	docker run -it -v $(pwd):/code $(image):builder /bin/bash

container:
	docker run -it -p 127.0.0.1:8000:8000 $(image_tag)

hadolint:
	docker run --rm -i hadolint/hadolint:$(hadolint_version) < Dockerfile

trivy:
	docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v ~/.cache/trivy:/root/.cache/ aquasec/trivy:$(trivy_version) image --ignore-unfixed $(image_tag)

push:
	docker push $(image_tag)

fmt:
	poetry run black .