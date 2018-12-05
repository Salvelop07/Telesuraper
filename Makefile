.PHONY: help

.DEFAULT_GOAL := help
SHELL := /bin/bash

REPOSITORY := 'dreglad/telesur-scraper'
VERSION ?= latest

# If the first argument is "run"...
ifeq (run,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "run"
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(RUN_ARGS):;@:)
endif

help: # http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

release: ## tag a release from master and push to origin
	bash -c '[[ -z `git status -s` ]]'
	git tag -a -m release $(VERSION)
	git push --tags

build: ## build the Docker image
	docker build --tag $(REPOSITORY) --rm=false .

build-nc: ## build the Docker image without cache
	docker build --tag $(REPOSITORY) --rm=false .

login: ## Login to docker hub
	docker login -e $DOCKER_EMAIL -u $DOCKER_USER -p $DOCKER_PASSWORD

push: ## push the latest image to DockerHub
	docker push $(REPOSITORY)

run: ## run an interactive bash session
	docker run -it --env-file=.env $(REPOSITORY) $(RUN_ARGS)
