image=lk-cr.artifactory.astralinux.ru/backend/app
tag=latest
image_tag=$(image):$(tag)
hadolint_version=2.12.0
# renovate: datasource=github-releases depName=aquasecurity/trivy extractVersion=true
trivy_version=0.53.0
ruff_version=0.7.4
uid=$(shell id -u)
gid=$(shell id -g)
pwd=$(shell pwd)

build:
	docker build --pull --no-cache -t $(image_tag) .

fmt:
	docker run --volume $(pwd)/src:/io/src --volume $(pwd)/tests:/io/tests --volume $(pwd)/pyproject.toml:/io/pyproject.toml --rm lika-ghcr.artifactory.astralinux.ru/astral-sh/ruff:$(ruff_version) format --no-cache

linter:
	docker run --volume $(pwd)/src:/io/src --volume $(pwd)/tests:/io/tests --volume $(pwd)/pyproject.toml:/io/pyproject.toml --rm lika-ghcr.artifactory.astralinux.ru/astral-sh/ruff:$(ruff_version) check --fix --no-cache

hadolint:
	docker run --rm -i hadolint/hadolint:$(hadolint_version) < project/Dockerfile