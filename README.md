# snippy

Personal site and experiments for **oriahulrich.com**, built with **Rust**, **Yew**, and **WebAssembly**. GitHub Pages deploys the `trunk` release build from `client/dist` (see `.github/workflows/rust.yml`). The `CNAME` file points Pages at `oriahulrich.com`.

The **Actix** app under `server/` is a small standalone HTTP playground (`127.0.0.1:8081`); production traffic for the domain is the static WASM site from CI.

## Client (site + boids demo)

```bash
rustup target add wasm32-unknown-unknown
cd client && trunk serve
```

Release build (matches CI):

```bash
cd client && trunk build --release
```

## Server

```bash
cd server && cargo run
```

## Research scrape (optional)

Maintainers: run this when you want to refresh **`client/public-footprint.html`** and a timestamped JSON dump of public API responses.

To snapshot public API responses for your own notes (output is **gitignored**):

```bash
python3 scripts/research_scrape.py
```

Files appear under `scraped/`. The same command also regenerates **`client/public-footprint.html`**, a standalone page of key points and outbound links (copied into `dist/` by Trunk for GitHub Pages).

## Git hooks

This repo can use Git hooks to run checks before you push (for example [actionlint](https://github.com/rhysd/actionlint) on workflows).

- **Enable hooks** (run once after clone): `./scripts/install-hooks`
- **List enabled hooks**: `./scripts/list-hooks`

Install actionlint (macOS):

```bash
brew install actionlint
```
