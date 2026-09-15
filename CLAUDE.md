# mos-yt-skills — Public Shared Repo

This repo is shared with The Vibe Marketing Lab community members. It is PUBLIC.

YouTube research skills: turn any channel into searchable text. This pack sits alongside the MarketingOS engine (`pipx install marketing-os`) and the other `mos-*-skills` packs.

---

## Security Rules (CRITICAL)

Every commit is visible to community members.

- **NEVER commit API keys, tokens, secrets, passwords, or credentials** — not in code, not in comments, not in examples
- **NEVER commit hardcoded file paths** containing usernames or machine-specific paths (e.g. `/mnt/c/Users/<name>/...`, `/Users/<name>/...`)
- **NEVER reference `.env` files with real values** — only env var NAMES as setup instructions (e.g. "set `GOOGLE_API_KEY` in your environment")
- **NEVER commit personal data** — emails, member lists, client info, business details
- **NEVER reference private repos** by path or content

**Before every commit, verify:**
1. `grep -r "API_KEY\|TOKEN\|SECRET\|PASSWORD\|sk-\|AIza" --include="*.md"` returns only env var name references, never values
2. `grep -r "/mnt/c/Users\|/Users/" --include="*.md"` returns zero results
3. No `.env`, `.env.*`, or credential files are staged

---

## What This Repo Contains

- `mos-yt-fast-scrape` — bulk transcript scraper: a whole channel, playlist or video into readable Markdown, 25 videos at a time, straight from YouTube's caption endpoint. No API key. Default output `~/Downloads/<channel-name>-yt/`
- `mos-yt-transcribe` — SRT subtitle downloader via yt-dlp (Apify for channel discovery). Use when per-line timestamps are needed
- `mos-yt-hook-extractor` — keyword in, hook formula out: top-ranking videos (vidIQ connector or yt-dlp search) → ranked transcripts → `openings.md` → `HOOKS.md` analysis. Default output `~/Downloads/<keyword>-hooks/`

`mos-yt-fast-scrape` is the default; `mos-yt-transcribe` is the SRT special case; `mos-yt-hook-extractor` starts from a keyword.

Each skill is a flat top-level folder with a `SKILL.md` (the skill prompt) and, where needed, `references/` (frameworks) or `scripts/` (deterministic tools). `setup.sh` links every top-level skill folder into `~/.claude/skills/`.

## Editing Rules

- Skills must work on any machine — relative paths and env var references only
- Skills sit at the top level of this repo; a nested skill folder is invisible to Claude Code
- Keep README.md current when adding or renaming a skill, then re-run `setup.sh`
- Test every skill without any private infrastructure before pushing

- `mos-yt-fast-scrape/scripts/fast_scrape.py` is standard-library Python. Keep it that way; members should not need to pip install anything for a single video
- `mos-yt-hook-extractor/scripts/hook_extractor.py` imports `fast_scrape` from the sibling folder. Changing `fetch`, `slug`, `fmt_dur`, `downloads_dir`, `ytdlp_cmd`, `ID_RE` or `PARAGRAPH_SECONDS` in fast_scrape.py means re-testing the hook extractor too
