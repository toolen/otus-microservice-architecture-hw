image=toolen/hw02
tag=latest
image_tag=$(image):$(tag)
hadolint_version=2.12.0
trivy_version=0.53.0

build:
	make hadolint
	DOCKER_BUILDKIT=1 docker build --pull --no-cache -t $(image_tag) .
	make trivy

hadolint:
	docker run --rm -i hadolint/hadolint:$(hadolint_version) < Dockerfile

trivy:
	docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v ~/.cache/trivy:/root/.cache/ aquasec/trivy:$(trivy_version) image --ignore-unfixed $(image_tag)
