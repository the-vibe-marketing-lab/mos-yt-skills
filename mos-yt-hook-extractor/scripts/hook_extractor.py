#!/usr/bin/env python3
"""
hook_extractor.py — find the top-ranking YouTube videos for a keyword, pull their
transcripts, and cut every video's opening into one file ready for hook analysis.
Standard library only. Free YouTube search needs yt-dlp (`pip install yt-dlp`).

    python3 hook_extractor.py "KEYWORD" [--max 50] [--deep 10] [--out DIR]
    python3 hook_extractor.py "KEYWORD" --from-vidiq results.json [--max 50] ...

Writes into the output folder (default ~/Downloads/<keyword>-hooks):
  NN-<title>.md    one transcript per video, NN = search rank, timestamped paragraphs
  INDEX.md         ranked table: title, channel, views, length, date, transcript link
  openings.md      the opening of every transcript in rank order (~450 words for the
                   top --deep videos, ~220 for the rest): the input for HOOKS.md
  _manifest.json   all of the above as data, plus skipped videos with reasons

Transcripts come from the fetcher in the sibling mos-yt-fast-scrape skill, so both
skills must sit in the same mos-yt-skills clone.
"""
import argparse, json, re, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
SIBLING = HERE.parents[1] / "mos-yt-fast-scrape" / "scripts"
sys.path.insert(0, str(SIBLING))
try:
    import fast_scrape as fs
except ImportError:
    sys.exit("mos-yt-hook-extractor reuses the transcript fetcher from mos-yt-fast-scrape,\n"
             f"expected at {SIBLING}\nClone the whole mos-yt-skills repo and run setup.sh.")

DEEP_WORDS, SHALLOW_WORDS = 450, 220
HOOK_PARAGRAPH_SECONDS = 20        # finer than the scraper's 45s, so "the promise lands at 0:40" is readable
STAMP_RE = re.compile(r"^\[(?:\d+:)?\d+:\d{2}\] ")


# ----------------------------------------------------------------------------- search
def iso_seconds(iso):
    """vidIQ returns ISO-8601 durations like PT1H8M16S."""
    m = re.match(r"^P(?:\d+D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?$", iso or "")
    if not m:
        return 0
    h, mi, s = (int(x) if x else 0 for x in m.groups())
    return h * 3600 + mi * 60 + s


def search_youtube(keyword, n):
    cmd = fs.ytdlp_cmd()
    if not cmd:
        sys.exit("Searching YouTube needs yt-dlp. Install it with:  pip install yt-dlp\n"
                 "(Or run the search through vidIQ and pass --from-vidiq.)")
    print(f'searching YouTube for "{keyword}" (top {n}) ...', flush=True)
    r = subprocess.run(cmd + ["--flat-playlist", "--dump-json", "--no-warnings", "--quiet",
                              f"ytsearch{n}:{keyword}"], capture_output=True, text=True, timeout=300)
    rows = []
    for line in r.stdout.splitlines():
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue
        vid = d.get("id") or ""
        if fs.ID_RE.match(vid):
            rows.append({"id": vid, "title": d.get("title") or "",
                         "channel": d.get("channel") or d.get("uploader") or "",
                         "views": d.get("view_count"), "duration": int(d.get("duration") or 0),
                         "published": ""})
    if not rows:
        sys.exit(f"yt-dlp returned no search results for {keyword!r}\n{r.stderr.strip()[-500:]}")
    return rows


def from_vidiq(path):
    """Accepts the saved output of vidIQ's vidiq_youtube_search tool: {"results": [...]} or a bare list."""
    data = json.load(open(path, encoding="utf-8"))
    items = data.get("results", []) if isinstance(data, dict) else data
    rows = []
    for d in items:
        if d.get("kind", "video") != "video":
            continue
        vid = str(d.get("id") or d.get("videoId") or "")
        if not fs.ID_RE.match(vid):
            continue
        dur = d.get("duration")
        rows.append({"id": vid, "title": d.get("title") or "",
                     "channel": d.get("channelTitle") or d.get("channel") or "",
                     "views": d.get("viewCount"),
                     "duration": iso_seconds(dur) if isinstance(dur, str) else int(dur or 0),
                     "published": (d.get("publishedAt") or "")[:10]})
    if not rows:
        sys.exit(f"no videos found in {path} (expected vidIQ search results with an 'id' per video)")
    return rows


# ----------------------------------------------------------------------------- output
def opening(text, limit):
    """First `limit` spoken words, keeping the paragraph timestamps."""
    out, count = [], 0
    for para in text.split("\n\n"):
        m = STAMP_RE.match(para)
        stamp = m.group(0) if m else ""
        take = para[len(stamp):].split()[: max(0, limit - count)]
        if not take:
            break
        out.append(stamp + " ".join(take))
        count += len(take)
        if count >= limit:
            break
    return "\n\n".join(out), count


def views_str(v):
    return f"{v:,}" if isinstance(v, int) else "unknown"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("keyword", help="the search term, e.g. \"AI SEO\"")
    ap.add_argument("--max", type=int, default=50, help="how many ranking videos to pull (default 50)")
    ap.add_argument("--deep", type=int, default=10, help="how many top videos get a longer opening (default 10)")
    ap.add_argument("--out", help="output folder (default: ~/Downloads/<keyword>-hooks)")
    ap.add_argument("--from-vidiq", metavar="FILE", help="use saved vidIQ search results instead of yt-dlp search")
    ap.add_argument("--workers", type=int, default=25, help="parallel transcript downloads (default 25)")
    args = ap.parse_args()

    source = "vidIQ YouTube search" if args.from_vidiq else "YouTube search via yt-dlp"
    rows = (from_vidiq(args.from_vidiq) if args.from_vidiq else search_youtube(args.keyword, args.max))[: args.max]
    out = Path(args.out) if args.out else Path(fs.downloads_dir()) / f"{fs.slug(args.keyword, 60)}-hooks"

    fs.PARAGRAPH_SECONDS = HOOK_PARAGRAPH_SECONDS
    print(f"fetching {len(rows)} transcripts, {args.workers} at a time ...", flush=True)
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as ex:
        results = list(ex.map(lambda r: fs.fetch(r["id"], True), rows))
    elapsed = time.time() - t0

    out.mkdir(parents=True, exist_ok=True)
    width = max(2, len(str(len(rows))))
    today = time.strftime("%Y-%m-%d")
    items, openings = [], []
    for rank, (row, (vid, meta, err)) in enumerate(zip(rows, results), 1):
        meta_or = meta or {}
        item = {
            "rank": rank, "id": vid, "url": f"https://www.youtube.com/watch?v={vid}",
            "title": row["title"] or meta_or.get("title") or "untitled",
            "channel": row["channel"] or meta_or.get("author", ""),
            "views": row["views"] if isinstance(row["views"], int) else meta_or.get("views"),
            "duration": row["duration"] or meta_or.get("duration", 0),
            "published": row["published"] or meta_or.get("published", ""),
        }
        if not meta:
            item["skipped"] = err
            items.append(item)
            continue
        fn = f"{rank:0{width}d}-{fs.slug(item['title'], 60)}.md"
        q = lambda s: json.dumps(s, ensure_ascii=False)
        (out / fn).write_text(
            f"---\nrank: {rank}\nkeyword: {q(args.keyword)}\ntitle: {q(item['title'])}\n"
            f"channel: {q(item['channel'])}\nurl: {item['url']}\nviews: {item['views'] if item['views'] is not None else ''}\n"
            f"duration: {fs.fmt_dur(item['duration'])}\npublished: {item['published']}\n"
            f"captions: {meta['caption_kind']}\nwords: {meta['words']}\n---\n\n"
            f"# {item['title']}\n\n{meta['text']}\n", encoding="utf-8")
        item.update(file=fn, words=meta["words"], captions=meta["caption_kind"])
        items.append(item)
        deep = rank <= args.deep
        text, n = opening(meta["text"], DEEP_WORDS if deep else SHALLOW_WORDS)
        openings.append(
            f"## #{rank} {item['title']}\n\n"
            f"- Channel: {item['channel']} | Views: {views_str(item['views'])} | Length: {fs.fmt_dur(item['duration'])}"
            f" | Published: {item['published'] or 'unknown'} | Captions: {meta['caption_kind']}\n"
            f"- {'Deep' if deep else 'Short'} opening: first {n} words | Transcript: {fn}\n\n{text}\n")

    ok = [i for i in items if "file" in i]
    skipped = [i for i in items if "skipped" in i]
    (out / "openings.md").write_text(
        f"# Openings: \"{args.keyword}\"\n\n"
        f"Source: {source}, {len(rows)} videos in ranking order, pulled {today}. "
        f"Top {args.deep} carry ~{DEEP_WORDS} words, the rest ~{SHALLOW_WORDS}. "
        f"Timestamps mark where each paragraph starts.\n\n" + "\n".join(openings), encoding="utf-8")

    lines = [f"# YouTube: \"{args.keyword}\" top {len(rows)} ranking videos", "",
             f"Source: {source} (ranking order), pulled {today}. Transcripts: YouTube captions.",
             "Hook analysis: [HOOKS.md](HOOKS.md)", "",
             f"Transcripts captured: {len(ok)}/{len(rows)}.", "",
             "| # | Title | Channel | Views | Length | Published | Transcript |",
             "|---|---|---|---|---|---|---|"]
    for i in items:
        t = i["title"].replace("|", "/")
        cell = f"[{i['words']:,} words]({i['file']})" if "file" in i else f"skipped: {i['skipped']}"
        lines.append(f"| {i['rank']} | [{t}]({i['url']}) | {i['channel'].replace('|', '/')} | {views_str(i['views'])} "
                     f"| {fs.fmt_dur(i['duration'])} | {i['published'] or '-'} | {cell} |")
    (out / "INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    manifest = {"keyword": args.keyword, "source": source, "pulled": today, "deep": args.deep,
                "ok": len(ok), "skipped": len(skipped), "total_words": sum(i["words"] for i in ok),
                "items": items}
    (out / "_manifest.json").write_text(json.dumps(manifest, indent=1, ensure_ascii=False), encoding="utf-8")

    print()
    print("Hook extraction ready for analysis")
    print("==================================")
    print(f"Keyword  : {args.keyword}  ({source})")
    print(f"Saved to : {out}/")
    print(f"Videos   : {len(ok)} transcripts, {len(skipped)} skipped, top {args.deep} deep")
    print(f"Words    : {manifest['total_words']:,} transcribed")
    print(f"Time     : {elapsed:.1f}s")
    for i in skipped:
        print(f"  - #{i['rank']} {i['url']}  {i['skipped']}")
    print(f"Next     : read {out / 'openings.md'} and write HOOKS.md")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
