.PHONY: all
# automate pre-publish actions

help:
	@echo "Pre-publish actions"
	@echo "all: make all pre-publish actions":
	@echo "version: bump package version from latest tag"
	@echo "docs: prepare docs for publish"

all: version docs

version:
	@poetry version $(shell dunamai from any)

docs:
# create requirements.txt for Sphinx
	@echo "creating requirements.txt..."
	@poetry export -f requirements.txt -o docs/requirements.txt --with dev --without-hashes

