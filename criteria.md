# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. *"The model is accurate"* is an
opinion. *"Every label has an F1 of at least 0.60 on the held-out set"* is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — *"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"*. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in — a criterion that fits none of them is fine if it names a
number.

| Area | A question it could answer |
|---|---|
| Overall accuracy | How often does it need to be right to be worth using? |
| Per-label performance | Is one label allowed to be much worse than the others? |
| Balance | How lopsided can your label counts get before it's a problem? |
| Consistency | If someone else labelled the same posts, how often should you agree? |
| Confidence | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind — it is stricter than it first sounds.

---

# Acceptance Criteria

## 1. Overall Accuracy
**Target:** The model must achieve at least 0.65 (65%) overall accuracy on the held-out test set.

**Reason:** There are three labels, so random guessing would achieve roughly 33% accuracy if guesses were equally likely. I chose 65% as a target that would indicate the model is learning meaningful distinctions between the labels without assuming perfect classification.

## 2. Per-Label Performance
**Target:** Each of the three labels must achieve an F1 score of at least 0.50 on the held-out test set.

**Reason:** I want the model to recognize all three categories reasonably well rather than performing well overall while consistently misclassifying one label. I chose 0.50 as a challenging but attainable initial target because the labels have overlapping boundaries.

## 3. Label Balance
**Target:** No individual label may account for more than 50% of the labeled dataset.

**Reason:** If one label dominates the dataset, a model could achieve deceptively good accuracy by predicting that label too often. Keeping every label below 50% should encourage the model to learn distinctions across all three categories.

## 4. Labeling Consistency
**Target:** I must agree with an independent labeling of at least 70% of a sample of 20 posts.

**Reason:** The categories can overlap, particularly when distinguishing an Opinion from a Hot_Take. I chose 70% because I want my definitions and decision rules to produce reasonably consistent labels, while allowing for genuinely ambiguous posts.

## 5. Confidence
**Target:** Predictions with confidence scores of at least 0.80 must be correct at least 80% of the time on the held-out test set.

**Reason:** A high-confidence prediction should generally be more trustworthy than an uncertain one. I chose 80% as a useful threshold, although I recognize that the model's confidence scores may not accurately reflect its actual probability of being correct.

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
