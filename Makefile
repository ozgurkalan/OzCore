# automate pre-publish actions

help:
	@echo "Pre-publish actions"
	@echo "ready: prepare docs for publish"
	@echo "switch: git switch branches"

ready:
# create requirements.txt for Sphinx
	@echo "creating requirements.txt..."
	@poetry export -f requirements.txt -o docs/requirements.txt --with dev --without-hashes

switch:
# switch between branches
	@git switch -