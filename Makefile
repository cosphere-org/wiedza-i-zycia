# Makefile

include .lily/lily_assistant.makefile

SHELL := /bin/bash

VERSION := $(shell python setup.py --version)


.PHONY: run
run:
	source .venv/bin/activate && \
	source env.sh && \
	which python && \
	python wiedza_i_zycie/scraper.py 

