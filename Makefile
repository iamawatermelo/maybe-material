THEME ?= "Sunset"

.PHONY: help build

help:
	@echo "make help - this text"
	@echo "make build - build everything"
	@echo "make THEME=\"...\" preview - preview a theme with preview.sh"

build: extension/themes/maybe-material.json

preview:
	sh preview.sh "Maybe Material ${THEME}"

gen/harmonized.m.kdl: gen-palettes.py variations.json fixed-tokens.json
	python3 gen-palettes.py > $@

maybe-material.kdl: gen-root.py variations.json
	python3 gen-root.py > $@

extension/themes/maybe-material.json: maybe-material.kdl modules/*.m.kdl gen/harmonized.m.kdl
	zed-hct-theme-maker compile maybe-material.kdl > $@
