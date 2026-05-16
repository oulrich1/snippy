# https://github.com/casey/just — run `just` to list recipes
set shell := ["bash", "-uc"]

# Default: show available recipes
default:
	@just --list

# Dev server (WASM + hot reload). Port is in client/Trunk.toml (default 8082).
serve:
	cd client && unset NO_COLOR FORCE_COLOR && trunk serve

# Production build (matches CI / GitHub Pages artifact)
build:
	cd client && unset NO_COLOR FORCE_COLOR && trunk build --release

# Quick compile check for the WASM target
check-client:
	cd client && cargo check --target wasm32-unknown-unknown

check-server:
	cd server && cargo check

check: check-client check-server

# Actix playground (127.0.0.1:8081 — not the public site)
server:
	cd server && cargo run

# Refresh scraped JSON + client/public-footprint.html (see README)
research:
	python3 scripts/research_scrape.py
