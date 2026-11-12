# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
<!-- e.g. "One of my questions is about a topic only two documents mention, so
     I expect that one to be hard." -->
For each question, I looked through the campus_life corpora and wrote a question based off a particular document. 
I expect the system to retrieve each of those documents. One of the questions is kind of vague and the retrieved
chunks may not include the answer

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
<!-- Why all five and not four? What about your setup makes that achievable —
     or what would have to go wrong for it not to be? -->
I want to make sure every answers is grounded in evidence and not made up. Because of this, if the system
produces an answer, there has to be a source document attached.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:**
<!-- What did your distances look like when you set the cutoff in Milestone 4?
     Was there a clean gap, or did the two groups overlap? -->
I want my system to have a certainty threshhold and to clearly communicate when it can't produce 
a confident answer. It should say there isn't enough information to respond confidently. This 
should happen almost every time an "OUT OF SCOPE" question arises. If something relevant is found, 
even if not correct, we can allow for this to pass (however, this should be rare).

---

## 4. Something about your chunks
Every sampled chunk should have about 317 characters. 

<!-- YOU WRITE THIS ONE.

     How would you know if your chunks were the right size? Name something
     countable or observable.

     Examples of the right shape — don't copy these, they should come from
     what you actually saw in Milestone 3:
       - "At least 4 of 5 sampled chunks read as a complete thought, with no
          sentence cut in half at either end."
       - "No chunk is shorter than 200 characters, since anything below that
          in my corpus turned out to be a heading with no content under it." -->

**Why this target:**
The README says that every document in `campus_life` is about 317 characters. I expect most, if not all, 
the chunks to be the same size as the documents since they are short and very specific on what they answer.

---

## 5. Your choice
Every answer the system generates should be within 2 seconds.
<!-- YOU WRITE THIS ONE TOO.

     Pick something you actually care about getting right. It could be about
     speed, about refusals, about a particular kind of question your corpus
     handles badly, about source attribution being correct rather than merely
     present — anything, as long as it names a number or an observable
     outcome. -->

**Why this target:**
I want to make sure the system is reliable and can answer questions confidently. Since there's only 88
documents in the corpus, I expect the system to search through relevant chunks quickly and either
give an answer or simply state there is no evidence.


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->

---

## Capstone

Five criteria for the Shape A extension (run path, logging, failure handling),
written before any capstone results exist.

### 1. Run Path Reproducibility

The application must successfully complete 3 out of 3 independent executions from a fresh checkout, following only the documented setup and execution steps in `RUNNING.md`. Each execution must complete without undocumented commands, source-code modifications, or manual fixes.

**Why this target:** My setup steps are fully pinned and deterministic — exact dependency versions, a documented fix for the port conflict — so nothing in the procedure is left to chance. The Gemini free-tier API hasn't been flaky in my testing, so a fresh checkout failing would point to a real environment problem, not bad luck. That's why I expect all 3 of 3 to hold.

---

### 2. Logging Accuracy

Across 10 execution attempts, 10 out of 10 records in `logs/runs.jsonl` must accurately reflect the execution outcome. Successful runs that invoke the model must contain non-null token usage values, failed runs must record `status: "error"`, and error records must not contain a successful response in the `output` field.

**Why this target:** `generate.py::_record_tokens` is deliberately forgiving — if a model response is missing `usage_metadata`, it silently does nothing rather than erroring, so my own counters would just stay at zero. An answered run with zero tokens wouldn't mean nothing happened; it would mean the model was genuinely called and probably cost something real, but my own instrumentation missed it with no signal that it did. That's worse than a visible error, since my `What It Costs` numbers would be silently wrong instead of obviously broken. I don't want any real usage going unmeasured.

---

### 3. Failure Record Accuracy

The application must correctly record 3 out of 3 distinct execution failures in `logs/runs.jsonl`. Each record must contain `status: "error"`, a nonempty error description identifying the actual failure, and no misleading successful output.

**Why this target:** This criterion's job is specifically that the record itself is correct — whether the exception also reaches the caller is Criterion 5's job, not this one's. A blank error description or the wrong exception type would mean I can't tell what actually broke from the log alone. When I diagnose a miss in Milestone 6, a bad record means re-running and guessing instead of reading the answer straight off the log — which costs real, avoidable API usage I'd rather not spend finding out what the log should have told me the first time.

---

### 4. Invalid Input Handling

The application must appropriately handle 3 out of 3 distinct invalid-input cases — a whitespace-only question, a nonexistent corpus, and a missing required argument to `retrieve` (e.g. `python app.py retrieve` with no question). Each case must produce an observable rejection or failure outcome consistent with the application's documented behavior, without generating a misleading successful answer.

**Why this target:** These three fail at three different layers rather than testing the same layer three times. A whitespace-only question passes argument parsing and reaches `ask_pipeline`, but fails at the embedding/gate stage (it gets a high distance and is refused). A nonexistent corpus also reaches `ask_pipeline`, but fails at the storage layer (no index found). A missing required argument to `retrieve` never gets that far — it's rejected by argument parsing itself, before `ask_pipeline` or any logging runs at all. I want to know bad input gets caught no matter which layer it would naturally break at, not just that one layer handles it well.

