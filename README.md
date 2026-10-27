# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Your community, and what your classifier sorts posts into. Three or four
     sentences. -->
     This project uses posts from the Wizard101 community on Reddit to explore how
people express opinions, make strong claims, and suggest improvements to the
game. The classifier sorts posts into three categories: Constructive_Criticism,
Opinion, and Hot_Take. Constructive_Criticism covers posts that identify a
problem and suggest a solution, Opinion covers personal preferences or
judgments, and Hot_Take covers strong claims that challenge or reject a
position. The goal is to train a model to recognize these differences in
community discussions.



---

## Label Taxonomy

<!-- Each label: a one-sentence definition and two real examples from your
     reading. Then your decision rule for the hardest boundary.

     The decision rule is worth a point on its own and it's the thing most
     people leave out. Every taxonomy has a hardest boundary. Name yours. -->

### `Constructive_Criticism`

**Definition:** A post that identifies something that could be improved and proposes a specific change or solution.

**Example 1:**

> TAKE: when using AOE, damage should be even to all enemies

Source: https://www.reddit.com/r/Wizard101/comments/1dg7s2k/

**Example 2:**

> KI really should actually keep restarting the servers at least every week with maintenance like they say they will on Twitter to help with server performance.

Source: https://www.reddit.com/r/Wizard101/comments/1dg7s2k/
>

### `Opinion`

**Definition:** A post that expresses a personal preference, belief, or judgment without explicitly challenging or rejecting a position or proposing a specific improvement.

**Example 1:**

> personally, i like that the game is still childlike or centric towards kids. if i wanted to play a more serious or mature themed mmorpg, i could play something else.

Source: https://www.reddit.com/r/Wizard101/comments/zycz9w/

**Example 2:**

> For that reason, I’m sort of inclined not to choose Death.

Source: https://www.reddit.com/r/Wizard101/comments/1tnu97b/

### `Hot_Take`

**Definition:** A post that makes a strong claim challenging or rejecting a position without proposing a specific change or solution.

**Example 1:**

> BASIC HOT TAKE: there are so many clueless high leveled wizards, when pve is a pretty basic structure.

Source: https://www.reddit.com/r/Wizard101/comments/1dg7s2k/

**Example 2:**

> Unpopular opinion: Wizard 101 is a better game than wow

Source: https://www.reddit.com/r/Wizard101/comments/1w2xaxo/unpopular_opinion_wizard_101_is_a_better_game/

### The hardest boundary

**Which two labels:** `Opinion` vs. `Hot_Take`

**The decision rule I used every time:** When a personal judgment explicitly challenges or rejects a position, I classify it as `Hot_Take` rather than `Opinion`.



---

## The Dataset

<!-- Where you collected from, how you labelled, your counts, and three hard
     cases. -->

**Where the posts came from:** The r/Wizard101 subreddit. I searched it by keyword, using terms like "trash," "overrated," and "they need to fix this." AI helped me come up with the keywords and find posts faster (see How I Used AI).

**How I labelled them:** AI pre-labelled the posts, and then I checked every one and corrected the labels I disagreed with. Of the 154 rows, 134 are AI-assisted and 20 are cold (labelled by me without AI, marked `cold` in `labels.csv`).

**Counts per label:**

| Label | Count | Share |
|---|---|---|
| `Opinion` | 95 | 61.7% |
| `Constructive_Criticism` | 40 | 26.0% |
| `Hot_Take` | 19 | 12.3% |
| **Total** | 154 | 100% |

**Three hard cases**

<!-- Any post that made you pause: what it was, which two labels it could have
     been, and what you chose. These are worth more than the easy 190. -->

**1.**
> *The post:* "If Wizard101 went fully free to play with optional purchases, would it be more successful?"
>
> *Could have been:* `Constructive_Criticism` or `Hot_Take`
>
> *I chose, because:* `Constructive_Criticism`. The post discusses changing the game's payment model to attract more players and possibly increase revenue. The idea is debatable, but the main purpose is to suggest a change that could improve the game.

**2.**
> *The post:* "Unpopular opinion: Wizard 101 is a better game than WoW."
>
> *Could have been:* `Opinion` or `Hot_Take`
>
> *I chose, because:* `Hot_Take`. The post makes a provocative comparison between two games that players are likely to disagree about. I chose `Hot_Take` because the claim is deliberately controversial rather than an ordinary personal preference.

**3.**
> *The post:* "First arc should be free." The author argues that making the early game free would help new players get invested before reaching the membership paywall.
>
> *Could have been:* `Constructive_Criticism` or `Hot_Take`
>
> *I chose, because:* `Constructive_Criticism`. The author identifies a specific problem (the early paywall) and explains how changing it could improve player retention. The post offers a concrete solution rather than only making a controversial statement.

---

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Base model:** distilbert-base-uncased

**Settings:** 3 epochs, learning rate 2e-5, batch size 16, max length 128, seed 42, trained on CPU (no GPU detected)

**Anything I changed from the defaults, and why:** None of the training settings. I changed `LABELS` in the notebook so it matches my three labels.

**Split sizes:** train 107 / val 23 / test 24 (stratified, seed 42). Test counts per label: `Opinion` 15, `Constructive_Criticism` 6, `Hot_Take` 3. `Constructive_Criticism` and `Hot_Take` are both under 8 in the test split, so their F1 scores will be unstable across seeds.



---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

**Moment 1**

- *What I asked for:* Keyword ideas for searching r/Wizard101 for posts that fit my criteria.
- *What came back:* A set of search keywords to try.
- *What I changed:* I used the keywords myself in the subreddit search. The subreddit has a lot of media and off-topic posts, so the keywords were how I narrowed it down.

**Moment 2**

- *What I asked for:* Posts from the subreddit that fit my criteria, found faster than I could browse.
- *What came back:* A list of posts. The first list included posts that went outside my criteria.
- *What I changed:* I asked for a different mix of post types so the dataset would have more variety, and I kept only posts that fit my criteria.

**Pre-labelling disclosure:** 134 of the 154 labels were AI pre-labels that I checked, and I corrected the ones I disagreed with. For example, some posts the AI called `Hot_Take` were really `Opinion` under my reading of the definitions. The other 20 I labelled myself, marked `cold` in `labels.csv`.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy |  |  |  |
| Macro F1 |  |  |  |
| F1 — `label_one` |  |  |  |
| F1 — `label_two` |  |  |  |

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted |  |  |  |
|---|---|---|---|
| **** |  |  |  |
| **** |  |  |  |
| **** |  |  |  |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** ___ / 30 = ___%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
