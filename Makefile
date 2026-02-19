# flext-plugin - Plugin Framework
PROJECT_NAME := flext-plugin
include ../base.mk

# === PROJECT-SPECIFIC TARGETS ===
.PHONY: test-unit test-integration build shell

.DEFAULT_GOAL := help
