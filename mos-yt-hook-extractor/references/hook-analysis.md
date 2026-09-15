# Hook analysis method

How to turn `openings.md` into `HOOKS.md`. Read this before writing a word of the analysis.

The goal is a formula the user can copy, derived from what the ranking videos for *this* keyword actually do. The worked example at the bottom shows the bar, not the answer: a different keyword will produce a different formula, and that is the point.

---

## 1. Vocabulary

### Hook types (one primary type per video)

Classify by the job the **first one or two sentences** do. Everything after that shows up in the beats.

| Type | What the first sentences do | Sounds like |
|---|---|---|
| **Proof number** | State a result the creator got, with a figure | "I added $19,000 in monthly revenue to a client's site..." |
| **Shift / stakes stat** | Say the world changed, usually with an outside stat | "Last year, SEO fundamentally changed." / "60% of searches end without a click" |
| **Promise / course intro** | Say what the video will teach, often time-boxed | "In the next 60 minutes I'm going to teach you..." |
| **Contrarian / myth-bust** | Attack a belief or the common advice | "Most advice does not work." / "No, it is not just SEO." |
| **Pain question / "you" callout** | Describe the viewer's situation or ask about it | "Right now, you're probably..." / "Does your name come up?" |
| **Story / scene** | Drop the viewer into a first-person moment or a named case | "Every time I walk into a new gym..." / "Today we're looking at four real gyms..." |
| **No hook** | Livestream chatter, podcast pleasantries, sponsor first | "Hello, just doing a quick audio check." |

If a video honestly sits between two, pick the one the first sentence serves and mention the other in the beats.

### Beats (the moves inside a hook, in the order they happen)

Proof · Checkable proof (the viewer could verify it now) · Stakes stat · Tension (the problem, the myth, the status quo) · Reframe (the turn, often "but") · Villain (who's selling the wrong answer) · Numbered promise ("three agents", "five skills") · Safety net ("even if you're a beginner") · Time box ("in 14 minutes") · Credibility (name, years, agency, results) · Open loop (a payoff held for later) · Roadmap (the chapter list read out) · Retention ask ("stay till the end") · Self-promo (subscribe, community, agency pitch)

### Promise lands

The timestamp of the paragraph where the viewer is first told what they will get. The transcripts carry paragraph timestamps every ~20 seconds, so write `~0:20`, `~1:00`. When a general promise and a specific numbered promise land far apart, give both (`~0:40 general, ~3:30 numbered`). Earlier is not automatically better, but a promise after 60 seconds is worth flagging.

### Content starts

The timestamp where the video stops introducing itself and starts delivering (the first step, the first gym, the first screen). The gap between a strong hook (~0:20) and the pack (~2:00) is often the clearest difference in a niche, so record it for the top N.

---

## 2. Process

1. **Read all of `openings.md`.** Not a sample. The counts in the type table have to be real.
2. **Top N first, deeply.** For each of the top N videos (N is the `--deep` value, default 10), record: primary type, the opening line verbatim, the beats in order, when the promise lands, and a one-line verdict (strong / solid / weak, plus why).
3. **Everyone else, lightly.** For ranks N+1 onwards: primary type, opening line verbatim (trim with "..." if long), one-line note.
4. **Separate rank from hook quality.** Some videos rank on exact-match titles, big channels, long runtimes or recency, with a weak or missing hook. Call those out ("ranks on title match, not the hook") and leave them out of the formula so the user doesn't copy a livestream's audio check. Treat two more groups the same way: **off-topic** videos the search pulled in (still typed and counted, flagged "off-topic"), and strong hooks built for a **different format** (a news explainer or a reaction in a list of tutorials). A different-format hook is often the best source for the gap.
5. **Derive the formula from the strong top-N hooks.** Count which beats appear, and in what order. The formula is the most common order, named as 4 to 7 short steps, each step backed by a verbatim quote and its rank. State the evidence as counts ("8 of 10 put a number or claim in sentence one").
   - **When the top N is thin** (fewer than three strong hooks), back the steps with strong hooks from further down the list, label each with its rank, and say so in the formula section.
   - **When the whole niche is small** (the most-viewed video is in the low thousands, or most have a few hundred views), open the formula section with one sentence saying how much evidence it rests on.
6. **Write the fill-in template.** One line per step with square-bracket slots.
7. **Find the gap.** A beat or type that is rare in the top N but clearly strong where it does appear (or strong in the wider list). Present it as an observation with the evidence, not a guarantee. One main gap; add a second only if its evidence is as strong.
8. **Add the caveat.** Views reflect channel size and video age as much as the hook, so type-versus-views is not causal.

### Quoting rules

- Opening lines and step quotes are **verbatim from `openings.md`**, taken from inside one timestamped paragraph so they can be checked with a plain text search. You may cut with "...".
- Caption mishearings (of brands, products or people's names) stay as captioned, with the correction in square brackets straight after: "GPT rappers [wrappers]", "Alex Herozy [Hormozi]". The verification step strips the brackets and matches the rest exactly.
- Every number you state comes from the openings or the manifest (views, ranks, counts). Don't bring in outside stats.
- Quote marks are fine in HOOKS.md; attribute each quote to its channel and rank.

---

## 3. HOOKS.md template

```markdown
---
keyword: <keyword>
source: <vidIQ YouTube search | YouTube search via yt-dlp>, top <M> in ranking order, pulled <YYYY-MM-DD>
analysed: first ~450 spoken words (top <N>) and ~220 words (#<N+1>-<M>) of each transcript
---

# Hook analysis: "<keyword>" top <M>

## The formula (from what the top <N> actually do)

**<Step> → <Step> → <Step> → <Step> → <Step>**

1. **<Step name>.** <one sentence on the job>. "<verbatim quote>" (<channel>, #<rank>).
2. ...

### Fill-in template

> [slot] ...
> [slot] ...

### The gap nobody in the top <N> fills

<2 to 4 sentences, with the evidence>

---

## Top <N> breakdown

| # | Video (channel, views) | Hook type | Opening line (verbatim) | Beats in order | Promise lands | Content starts | Verdict |
|---|---|---|---|---|---|---|---|
| 1 | ... | ... | "..." | Proof → Reframe → ... | ~0:20 | ~0:40 | Strong. ... |

**Top <N> pattern:** <2 or 3 counted observations, and which videos rank on something other than the hook>

---

## All <M> by hook type

| Type | Count | What it sounds like | Videos (rank) |
|---|---|---|---|
| ... | ... | ... | ... |

### #<N+1>-<M> one-liners

| # | Opening line (verbatim, trimmed) | Type | Note |
|---|---|---|---|

---

*Caveat: view counts are shaped by channel size and video age as much as by the hook, so hook type vs views isn't causal. Transcripts are YouTube captions; quotes are lightly cleaned of caption errors.*
```

The type-table counts must add up to the number of videos with transcripts. Skipped videos (no captions) get one line under the table saying which ranks and why.

---

## 4. Worked example (excerpt, keyword "AI SEO", September 2026)

Three top-10 rows and the formula they fed, to show the depth expected:

| # | Video | Hook type | Opening line (verbatim) | Beats in order | Promise lands | Verdict |
|---|---|---|---|---|---|---|
| 2 | AI SEO for Beginners (Sabrina Ramonov, 32K) | Proof number | "My website got 1.4 million views in 2026." | Proof → Checkable proof → Promise → Credibility | ~0:12 | Strong. The only proof in the top 10 a viewer can verify themselves. |
| 4 | I Let AI Agents Run My SEO (Matt Diggity, 5K) | Proof number | "Earlier this year I added $19,000 in monthly revenue to a client's site just by getting a crack team of AI agents to find and fix what was broken." | Proof → Story → Open loop → Numbered promise → Credibility | ~0:40 | Strong. Every beat in order; low views are recency, not quality. |
| 6 | SEO in 2026: Get Customers From ChatGPT and Claude AI (Sabrina Ramonov, 14K) | No hook | "Hello. I'm just doing quick audio check." | Livestream setup | never | Ranks on relevance and channel. Don't model. |

Formula that came out of that top 10: **Proof → Stakes → Reframe → Numbered promise → Credibility → Open loop**, with the gap being checkable proof (1 of 10).
