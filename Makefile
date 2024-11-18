package_name = hw
repository = toolen/hw-04
version = $(shell poetry version -s)
image_tag = ghcr.io/$(repository):$(version)
hadolint_version=2.12.0
trivy_version=0.43.1
pwd=$(shell pwd)

test:
	poetry run pytest -vv --cov=$(package_name) hw/tests/

fmt:
	poetry run black .
	poetry run isort .
