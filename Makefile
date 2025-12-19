# flext-plugin - Plugin Framework
PROJECT_NAME := flext-plugin
COV_DIR := flext_plugin
MIN_COVERAGE := 90

include ../base.mk

# === PROJECT-SPECIFIC TARGETS ===
.PHONY: test-unit test-integration build shell

.DEFAULT_GOAL := help
