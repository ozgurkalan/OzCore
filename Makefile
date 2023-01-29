# automate pre-publish actions

help:
	@echo "Pre-publish actions"
	@echo "version: bump package version from latest tag"
	@echo "docs: prepare docs for publish"

version:
	@poetry version $(dunamai from any)

docs:
# create requirements.txt for Sphinx
	@echo "creating requirements.txt..."
	@poetry export -f requirements.txt -o docs/requirements.txt --with dev --without-hashes

