# automate pre-publish actions

help:
	@echo "Pre-publish actions"
	@echo "ready: preparing to publish"
	@echo "switch: git switch branches"

ready:
# create requirements.txt for Sphinx
	@python config.py create

switch:
# switch between branches
	@git switch -