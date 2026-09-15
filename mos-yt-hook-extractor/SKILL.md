---
name: mos-yt-hook-extractor
description: "Reverse-engineer the hooks of the top-ranking YouTube videos for any keyword: find the videos that rank (vidIQ if connected, free YouTube search otherwise), pull every transcript, then break down how each one opens and derive a copyable hook formula plus fill-in template, with a deep dive on the top 10. Outputs ranked transcripts, INDEX.md and HOOKS.md. Use this whenever the user wants to know how the videos ranking for a topic start: 'analyse the hooks for [keyword]', 'what hooks are the top videos using', 'give me the hook formula for [topic]', 'grab the top videos for X and transcribe them', 'how do the top YouTube videos on X open', 'reverse engineer the intros', 'hook research before I script', 'mos-yt-hook-extractor', or asks to search YouTube/vidIQ for a keyword and study the videos. Prefer it over mos-yt-fast-scrape when the input is a keyword rather than a channel, or when the point is the hooks rather than the full text."
---

# YouTube Hook Extractor

Type a keyword, get back the hook formula the videos ranking for it actually use. Three stages:

1. **Find** the top-ranking videos for the keyword (vidIQ's YouTube search when that connector is available, otherwise YouTube's own search through yt-dlp).
2. **Transcribe** every one of them into ranked Markdown files, using the same caption fetcher as `/mos-yt-fast-scrape` (25 at a time, no API key).
3. **Analyse** how each video opens: a type for every video, a beat-by-beat breakdown of the top 10, and a formula plus fill-in template derived from what's working.

Stages 1 and 2 are one script run (about a minute for 50 videos). Stage 3 is you reading the openings and writing `HOOKS.md` by the method in `references/hook-analysis.md`.

**What lands in the folder:**

| File | What it is |
|---|---|
| `01-<title>.md` ... `50-<title>.md` | One transcript per video, numbered by search rank, timestamped paragraphs, metadata at the top |
| `INDEX.md` | Ranked table: title, channel, views, length, date, link to each transcript |
| `openings.md` | The first ~450 words of the top 10 and ~220 of the rest, in rank order. The analysis input |
| `HOOKS.md` | The analysis: formula, template, gap, top-10 breakdown, every video typed |
| `_manifest.json` | All of it as data, plus skipped videos and why |

---

## Prerequisites

1. **Python 3.8+**: `python3 --version`
2. **yt-dlp**, for the free search path. Check both install styles before installing anything, because many people have the standalone binary rather than the Python module:
   ```bash
   yt-dlp --version || python3 -m yt_dlp --version || pip install yt-dlp
   ```
3. **The whole mos-yt-skills pack.** The script borrows the transcript fetcher from `mos-yt-fast-scrape`, so both folders must come from the same clone (`setup.sh` links them).
4. **Optional: the vidIQ connector.** If a `vidiq_youtube_search` tool is available, it can supply the ranking list instead of yt-dlp. Each search costs vidIQ credits (5 at the time of writing).

---

## Workflow

### Step 1: Ask what to extract

Ask these together in one message (AskUserQuestion if available), skipping anything the user already said:

1. **Keyword.** Usually in the request. Use it exactly as they typed it; ranking lists change a lot between "AI SEO" and "AI SEO tools".
2. **How many videos, and how many to study deeply.** Default **50 videos, top 10 deep**. Offer 20 / top 5 for a quick look. More than 50 rarely changes the formula.
3. **Search source**, only when the vidIQ tool is available: **vidIQ** (uses credits, the list vidIQ reports as ranking, includes views) or **free YouTube search** (yt-dlp). Without vidIQ, don't ask; use yt-dlp.
4. **Where to save.** Default `~/Downloads/<keyword>-hooks/` (the script works this out, including under WSL). If the project already keeps YouTube research in a numbered folder (for example `YouTube Research/01-...`), offer the next number there instead and follow that convention.

Confirm the keyword, counts and full folder path back in one line before running.

### Step 2 (vidIQ path only): Save the search results

Call `vidiq_youtube_search` with `query` = the keyword, `type` = `["video"]`, `limit` = the video count (max 50), `order` = `relevance`.

Fifty results are usually too large to return inline, so the harness saves them to a file and tells you the path. Pass that path to the script as `--from-vidiq`. If the results did come back inline, write the JSON exactly as returned to `<folder>/vidiq-search.json` and pass that.

### Step 3: Run the script

```bash
SKILL_DIR=$(dirname "$(readlink -f ~/.claude/skills/mos-yt-hook-extractor/SKILL.md)")
python3 "$SKILL_DIR/scripts/hook_extractor.py" "KEYWORD" --max 50 --deep 10 --out "FOLDER" [--from-vidiq FILE]
```

If the skill isn't linked into `~/.claude/skills` (for example you're running a copy straight from a clone), set `SKILL_DIR` to the folder this SKILL.md sits in instead.

| Flag | Effect |
|---|---|
| `--max N` | Videos to pull, in ranking order (default 50) |
| `--deep N` | How many top videos get the longer ~450-word opening (default 10) |
| `--out DIR` | Output folder (default `~/Downloads/<keyword>-hooks/`) |
| `--from-vidiq FILE` | Use saved vidIQ search results instead of searching with yt-dlp |
| `--workers N` | Parallel transcript downloads (default 25) |

The script prints a summary with the folder, counts and any skipped ranks. Trust it; don't recount by hand.

### Step 4: Read every opening

Read `openings.md` in full, in pages if it's long (50 videos is roughly 14,000 words). Read it yourself rather than skimming or sampling: the type counts and the formula are only as honest as the reading behind them. If context is genuinely tight, a subagent can classify ranks 11+ against the vocabulary in the reference, but read the top 10 yourself.

### Step 5: Write HOOKS.md

Read `references/hook-analysis.md`, then write `HOOKS.md` into the same folder using its template. The essentials:

- **Formula from the data.** Count the beats the strong top-10 hooks use and name the common order as 4 to 7 steps, each with a verbatim quote and its rank. The reference's AI SEO example shows the depth expected, not the answer; a different keyword gives a different formula.
- **Rank isn't hook quality.** Videos that rank on title match, channel size, length or recency with a weak hook (livestream chatter, a sponsor read) get called out and kept out of the formula. So do off-topic videos the search dragged in, and strong hooks built for a different format (a news explainer in a list of tutorials); those can feed the gap instead.
- **Thin data gets said out loud.** In a small niche the top 10 may hold only one or two strong hooks. Back the formula's steps with strong hooks from further down the list, label them with their rank, and state how much evidence the formula rests on (for example "one video in this niche has traction; treat this as what it did differently").
- **Verbatim quotes only**, taken from `openings.md`, each from inside a single timestamped paragraph. Leave caption mishearings as they are and put the correction in square brackets straight after: "Cloud Code [Claude Code]". No outside statistics.
- **Every transcribed video typed**, and the counts add up.
- **One main gap**: a move that's rare in the top 10 but strong where it appears. Add a second only when the evidence is as strong as the first.

`INDEX.md` already links to `HOOKS.md`, so the folder reads as one piece in Obsidian or any Markdown viewer.

### Step 6: Check it

- Type-table counts add up to the transcripts captured (INDEX.md's "Transcripts captured" line).
- The top-10 table has a row for each top-10 video that has a transcript.
- Spot-check three opening-line quotes against `openings.md` with `grep -F`, using the quote with any `[bracketed correction]` removed. Fix any that don't match exactly.

### Step 7: Report

Lead with the formula itself (one line), then the folder path, then:

```
Hook extraction complete
========================
Keyword  : AI SEO  (vidIQ YouTube search)
Saved to : ~/Downloads/ai-seo-hooks/
Videos   : 50 transcripts, 0 skipped, top 10 deep
Formula  : Proof → Stakes → Reframe → Numbered promise → Credibility → Open loop
Best-built hook : #4 Matt Diggity, "I Let AI Agents Run My SEO"
Gap      : checkable proof (1 of the top 10)
```

Natural next moves to offer:

- **Write hooks for their own video:** "give me 4 hook variations for my video titled X", using the template in HOOKS.md, plus their voice doc if the project has one. Only use stats they can source (from these transcripts or their own results), and never invent a result for them.
- **Study one video in full:** every transcript is in the folder.
- **Compound it:** run `/mos-wiki-ingest` on the folder.

---

## Troubleshooting

| Problem | What to do |
|---|---|
| "reuses the transcript fetcher from mos-yt-fast-scrape" | The pack is incomplete. Clone the whole `mos-yt-skills` repo and run `setup.sh` |
| "Searching YouTube needs yt-dlp" | `pip install yt-dlp`, or use the vidIQ path |
| "no videos found in FILE" on `--from-vidiq` | The file isn't vidIQ search JSON (for example it's an error message). Re-run the search with `type` set to `["video"]` |
| Several ranks skipped with "no captions on YouTube" | Normal for a few videos. They stay in INDEX.md with the reason and are left out of the type counts |
| The search list looks different from the user's browser | YouTube personalises and localises results. vidIQ and yt-dlp each give a clean, logged-out ranking; say which one was used |

## Key rules

- **Use the script for stages 1 and 2.** Don't loop yt-dlp per video or rebuild the fetcher inline.
- **Never download video files.** Captions only.
- **Ask before running**: keyword, counts, source (only if vidIQ exists), folder. One message, defaults offered.
- **The analysis is the product.** Transcripts without HOOKS.md are half the job; don't stop after the script.
