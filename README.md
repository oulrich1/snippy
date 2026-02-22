### Server

```bash
cargo run
```

### Client

```bash
trunk serve
```

### Git Hooks

This repo uses Git hooks to run checks before you push (e.g. lint GitHub Actions workflows).

- **Enable hooks** (run once after clone): `./scripts/install-hooks`  
  This sets `core.hooksPath` to `.githooks` so the project’s hooks run instead of your global/default ones.
- **List enabled hooks**: `./scripts/list-hooks`  
  Shows the hooks directory and which hook scripts are present (e.g. `pre-push`).

The **pre-push** hook runs [actionlint](https://github.com/rhysd/actionlint). Install actionlint with:

```bash
brew install actionlint
```