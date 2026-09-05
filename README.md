# mos-yt-skills

YouTube research skills for Claude Code: turn any channel into searchable text you can read, grep, feed to Claude, or compile into your knowledge library.

Built by [The Vibe Marketing Lab](https://www.skool.com/the-vibe-marketing-lab) for the MarketingOS engine (`pipx install marketing-os`).

## What's in here

| # | Skill | What it does | Time |
|---|-------|--------------|------|
| 1 | `/mos-yt-fast-scrape` | A whole channel, playlist or video into clean Markdown transcripts, 25 videos at a time, straight from YouTube's own caption endpoint. No API key, no video download | ~40s per 500 videos |
| 2 | `/mos-yt-transcribe` | SRT subtitle files with per-line timestamps, via yt-dlp (plus a free Apify account for full-channel discovery) | ~10s per video |

Use `/mos-yt-fast-scrape` by default. Reach for `/mos-yt-transcribe` only when you specifically need SRT files, for example for video editing or caption work.

## Prerequisites

1. **Claude Code** with a Claude Pro or Max subscription.
2. **Python 3.8+** (already on macOS and most Linux; Windows usually has it from installing Claude Code).
3. **yt-dlp**, only for channels and playlists: `pip install yt-dlp`. Single videos need nothing else.

## Install

Skills live in `~/.claude/skills/`. This repo keeps them under version control and links them into place, so a `git pull` is all an update takes.

```bash
git clone https://github.com/the-vibe-marketing-lab/mos-yt-skills.git ~/Desktop/mos-yt-skills
cd ~/Desktop/mos-yt-skills
bash setup.sh
```

`setup.sh` links every skill folder in this repo into `~/.claude/skills/` (a symlink on macOS and Linux, a directory junction on Windows via Git Bash). Restart any open Claude Code session, then type `/mos-yt-fast-scrape` to confirm it loads.

**Updating:** `cd ~/Desktop/mos-yt-skills && git pull`. The links point at the clone, so that's it. Updates are announced in the Skool community.

**Other packs:** this is one of the `mos-*-skills` packs that accompany the [MarketingOS engine](https://github.com/the-vibe-marketing-lab/marketing-os). The full list is in the [marketing-os-skills](https://github.com/the-vibe-marketing-lab/marketing-os-skills) README.

## How to use

### `/mos-yt-fast-scrape`

Paste a channel, playlist or video URL. The skill asks two questions (how many videos, and where to save; the default is a new `[channel-name]-yt` folder in your Downloads), then pulls every English transcript as readable Markdown. Each file carries the title, URL, publish date, duration and word count, and the transcript is broken into paragraphs, with a new paragraph at every speaker change. Skips (no captions, non-English, private) are listed with reasons in `_manifest.json`.

A 500-video channel takes about 40 seconds. Then:

```bash
grep -ril "grand slam offer" ~/Downloads/alex-hormozi-yt/
```

or point Claude at the folder, or run `/mos-wiki-ingest` on it so the knowledge compounds instead of being re-read every time.

### `/mos-yt-transcribe`

Paste a YouTube URL and get SRT files in `outputs/transcripts/[Channel Name]/YYYY-MM-DD-[slug].en.srt`. Single videos and playlists need only yt-dlp. Full channels need a free Apify account and `APIFY_TOKEN` in your environment; the one-time setup is walked through inside the skill.

## Troubleshooting

- **"Listing a channel or playlist needs yt-dlp":** `pip install yt-dlp`, then rerun.
- **Every video fails with the same error:** YouTube changed its endpoint or your network blocks youtube.com. Try one video with `/mos-yt-transcribe`; if that works, report it in the community so the script can be updated.
- **Lots of skips on a channel that plays fine in a browser:** members-only or region-locked videos. Nothing to fix.
- **Skills don't show up:** the folders must be direct children of `~/.claude/skills/`. Re-run `setup.sh` and restart Claude Code.
