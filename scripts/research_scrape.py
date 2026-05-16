#!/usr/bin/env python3
"""
Fetch public metadata for portfolio research and write JSON under scraped/.

Also writes client/public-footprint.html — a readable summary with links to
primary sources (committed; regenerate with this script).

The scraped/ directory is gitignored. Requires: Python 3.9+ (stdlib only).
"""

from __future__ import annotations

import html
import json
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "scraped"
CLIENT_DIR = ROOT / "client"
HTML_OUT = CLIENT_DIR / "public-footprint.html"
USER_AGENT = "snippy-research-scrape/1.0 (+https://oriahulrich.com; local research)"

# Curated external pages (not returned by GitHub API); update if URLs change.
OTHER_PUBLIC_PAGES: list[tuple[str, str, str]] = [
    (
        "https://www.linkedin.com/in/oriaheu/",
        "LinkedIn",
        "Professional history and education (login may be required for full profile).",
    ),
    (
        "https://devpost.com/oulrich",
        "Devpost portfolio",
        "Hackathon / project submissions under this account.",
    ),
    (
        "https://devpost.com/software/perusewithspritz",
        "Devpost — PeruseWithSpritz",
        "RSVP-style reading tool built around Spritz.",
    ),
    (
        "https://devpost.com/software/fallng",
        "Devpost — Fallng",
        "Game-style submission on Devpost.",
    ),
    (
        "https://substack.com/profile/30376376-oriah",
        "Substack profile",
        "Public writer profile on Substack.",
    ),
]


def get_json(url: str) -> object:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=45, context=ctx) as resp:
        charset = resp.headers.get_content_charset() or "utf-8"
        return json.loads(resp.read().decode(charset))


def esc(x: object) -> str:
    if x is None:
        return ""
    return html.escape(str(x), quote=True)


def format_utc_stamp(stamp: str) -> str:
    """Turn 20260516T023433Z into a friendlier UTC label."""
    if len(stamp) >= 16 and stamp.endswith("Z") and "T" in stamp:
        d, _, t = stamp.partition("T")
        if len(d) == 8 and len(t) >= 6:
            return f"{d[:4]}-{d[4:6]}-{d[6:8]} {t[:2]}:{t[2:4]}:{t[4:6]} UTC"
    return stamp


def render_public_footprint_html(bundle: dict[str, object]) -> str:
    stamp = str(bundle.get("generated_at_utc", ""))
    stamp_h = esc(format_utc_stamp(stamp) if stamp else "unknown")

    gh = bundle.get("github_user")
    repos_raw = bundle.get("github_repos_recent")

    parts: list[str] = [
        "<!doctype html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="utf-8" />',
        '<meta name="viewport" content="width=device-width, initial-scale=1" />',
        "<title>Public footprint — Oriah Ulrich</title>",
        "<style>",
        ":root { color-scheme: dark; --bg: #0b0d12; --card: #161a24; --text: #e8ecf4; --muted: #9aa3b5; --accent: #5eead4; --border: rgba(255,255,255,.1); }",
        "body { font-family: system-ui, sans-serif; margin: 0; padding: 1.5rem clamp(1rem, 4vw, 2.5rem) 3rem; background: var(--bg); color: var(--text); line-height: 1.55; }",
        "a { color: var(--accent); }",
        "h1 { font-size: 1.5rem; margin-top: 0; }",
        "h2 { font-size: 1.1rem; margin-top: 2rem; border-bottom: 1px solid var(--border); padding-bottom: 0.35rem; }",
        ".meta { color: var(--muted); font-size: 0.9rem; }",
        "table { width: 100%; border-collapse: collapse; font-size: 0.88rem; margin-top: 0.75rem; }",
        "th, td { text-align: left; padding: 0.45rem 0.5rem; border-bottom: 1px solid var(--border); vertical-align: top; }",
        "th { color: var(--muted); font-weight: 600; }",
        ".card { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 1rem 1.25rem; margin-top: 1rem; }",
        "ul { margin: 0.5rem 0 0; padding-left: 1.2rem; color: var(--muted); }",
        "code { font-size: 0.85em; background: #12151d; padding: 0.15rem 0.35rem; border-radius: 6px; }",
        "</style>",
        "</head>",
        "<body>",
        "<p class=\"meta\"><a href=\"./\">← Back to site</a></p>",
        "<h1>Public footprint (research summary)</h1>",
        f"<p class=\"meta\">Snapshot generated <strong>{stamp_h}</strong>.</p>",
        "<h2>Key points from GitHub (API)</h2>",
    ]

    if isinstance(gh, dict) and "error" in gh:
        parts.append(f"<p>GitHub user API error: {esc(gh.get('error'))}</p>")
    elif isinstance(gh, dict):
        login = esc(gh.get("login"))
        name = esc(gh.get("name") or login)
        profile_url = esc(gh.get("html_url") or "https://github.com/oulrich1")
        parts.append("<div class=\"card\">")
        parts.append(f"<p><strong>Display name:</strong> {name}</p>")
        parts.append(f"<p><strong>Login:</strong> <a href=\"{profile_url}\">{login}</a></p>")
        parts.append(
            "<p><strong>Public activity (as returned by the API):</strong> "
            f"{esc(gh.get('public_repos'))} repositories, "
            f"{esc(gh.get('public_gists'))} gists, "
            f"{esc(gh.get('followers'))} followers, "
            f"{esc(gh.get('following'))} following.</p>"
        )
        hireable = gh.get("hireable")
        parts.append(f"<p><strong>Hireable flag:</strong> {esc(hireable)}</p>")
        parts.append(
            "<p><strong>Account created:</strong> "
            f"{esc(gh.get('created_at'))} · "
            "<strong>Profile last updated (API field):</strong> "
            f"{esc(gh.get('updated_at'))}</p>"
        )
        parts.append(
            "<p class=\"meta\">Source: "
            f"<a href=\"{profile_url}\">GitHub profile</a> · "
            "<a href=\"https://api.github.com/users/oulrich1\">GitHub REST: GET /users/oulrich1</a></p>"
        )
        parts.append("</div>")
    else:
        parts.append("<p>GitHub user data missing.</p>")

    parts.append("<h2>Recently touched public repositories (API)</h2>")
    parts.append(
        "<p class=\"meta\">Up to 15 repositories by <code>updated</code> sort. "
        "<a href=\"https://docs.github.com/en/rest/repos/repos#list-repositories-for-a-user\">GitHub API</a>.</p>"
    )

    if isinstance(repos_raw, dict) and "error" in repos_raw:
        parts.append(f"<p>Repos API error: {esc(repos_raw.get('error'))}</p>")
    elif isinstance(repos_raw, list):
        parts.append("<table><thead><tr><th>Repository</th><th>Description</th><th>Language</th><th>Updated (UTC)</th></tr></thead><tbody>")
        for r in repos_raw:
            if not isinstance(r, dict):
                continue
            url = esc(r.get("html_url") or "#")
            full_name = esc(r.get("full_name") or r.get("name") or "?")
            fork_badge = ' <span class="meta">(fork)</span>' if r.get("fork") else ""
            desc = esc(r.get("description")) if r.get("description") else "—"
            lang = esc(r.get("language")) if r.get("language") else "—"
            upd = esc(r.get("updated_at") or "—")
            parts.append(
                f"<tr><td><a href=\"{url}\">{full_name}</a>{fork_badge}</td>"
                f"<td>{desc}</td><td>{lang}</td><td>{upd}</td></tr>"
            )
        parts.append("</tbody></table>")
    else:
        parts.append("<p>Repository list unavailable.</p>")

    parts.append("<h2>DuckDuckGo instant-answer API (this run)</h2>")
    parts.append(
        "<p class=\"meta\">The script queries the public JSON API for broad web-search-style "
        "queries. For many people-centric queries the payload is empty or a known placeholder; "
        "do <em>not</em> rely on it for facts.</p>"
    )
    sources = bundle.get("sources")
    if isinstance(sources, list):
        for item in sources:
            if not isinstance(item, dict):
                continue
            q = esc(item.get("query"))
            parts.append(f"<div class=\"card\"><p><strong>Query:</strong> {q}</p>")
            if "error" in item:
                parts.append(f"<p>Error: {esc(item.get('error'))}</p>")
            if "duckduckgo_note" in item:
                parts.append(f"<p>{esc(item.get('duckduckgo_note'))}</p>")
            ddg = item.get("duckduckgo")
            if isinstance(ddg, dict):
                abst = ddg.get("AbstractText") or ddg.get("Abstract")
                if abst:
                    parts.append(f"<p><strong>Instant answer:</strong> {esc(abst)}</p>")
                if ddg.get("AbstractURL"):
                    parts.append(
                        f"<p><a href=\"{esc(ddg.get('AbstractURL'))}\">"
                        f"{esc(ddg.get('AbstractSource') or 'Source link')}</a></p>"
                    )
                if not abst and not ddg.get("AbstractURL"):
                    parts.append("<p class=\"meta\">No usable abstract or URL in this response.</p>")
            parts.append("</div>")

    parts.append("<h2>Other public pages (curated links)</h2>")
    parts.append("<p class=\"meta\">Hand-picked outbound links; not produced by the DuckDuckGo calls above.</p><ul>")
    for url, title, note in OTHER_PUBLIC_PAGES:
        parts.append(
            f"<li><a href=\"{esc(url)}\">{esc(title)}</a> — {esc(note)}</li>"
        )
    parts.append("</ul>")
    parts.append("</body></html>")

    return "\n".join(parts)


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    CLIENT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    bundle: dict[str, object] = {
        "generated_at_utc": stamp,
        "sources": [],
    }

    queries = [
        "Oriah Ulrich software engineer",
        "Oriah Ulrich GitHub",
    ]

    for q in queries:
        ddg_url = "https://api.duckduckgo.com/?" + urllib.parse.urlencode(
            {"q": q, "format": "json", "no_html": "1", "t": "oriahulrich.com"}
        )
        try:
            ddg = get_json(ddg_url)
            entry: dict[str, object] = {"query": q, "duckduckgo": ddg}
            if isinstance(ddg, dict):
                meta = ddg.get("meta")
                if isinstance(meta, dict) and meta.get("id") == "just_another_test":
                    entry["duckduckgo_note"] = (
                        "Placeholder instant-answer payload from DuckDuckGo; treat as unusable."
                    )
            bundle["sources"].append(entry)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError) as e:
            bundle["sources"].append({"query": q, "error": repr(e)})

    try:
        bundle["github_user"] = get_json("https://api.github.com/users/oulrich1")
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError) as e:
        bundle["github_user"] = {"error": repr(e)}

    try:
        bundle["github_repos_recent"] = get_json(
            "https://api.github.com/users/oulrich1/repos?"
            + urllib.parse.urlencode({"per_page": "15", "sort": "updated"})
        )
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError) as e:
        bundle["github_repos_recent"] = {"error": repr(e)}

    out_path = OUT_DIR / f"research-{stamp}.json"
    out_path.write_text(json.dumps(bundle, indent=2), encoding="utf-8")
    print(f"Wrote {out_path}")

    html_doc = render_public_footprint_html(bundle)
    HTML_OUT.write_text(html_doc, encoding="utf-8")
    print(f"Wrote {HTML_OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
