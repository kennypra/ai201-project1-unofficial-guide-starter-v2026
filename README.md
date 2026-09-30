# The Unofficial Guide

Kenneth Prado — campus_life corpus

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

This project is a **Question and Answer** system over the `campus_life` corpus, containing 88 short posts written by students about life on a college campus. You ask a question in plain English (natural language), such as "how much does laundry cost in Aldridge?" or "what's the workload like in BIO160?", and the system finds the most relevant posts and writes a short answer grounded in truth. If the question isn't covered by the corpus, the system abstains from making an inaccurate prediction and explicitly says so.
<!-- Three or four sentences. Which corpus you picked, and the kinds of
     questions your system answers. Write it for someone who has never seen
     this repo.

     Milestone 5. -->

## Chunking Strategy

**Chunk size:** 600

**Overlap:** 0

Initially, I tried a chunk size of 200 and overlap of 50. However, after retrieving some chunks, I realized that some texts were cut off from important contexts. I decided this chunk size was too small and had to increase it.

After running `python app.py index`, using chunk size 800 and overlap 120, I realized that every chunk was essentially a brand new document in the corpus. The longest chunk was 549 (suggesting the longest document was 549 characters long) and therefore telling us the current chunk size was too long. Further, the avearage chunk has 317 characters. I decided to make chunk size 600 in case we ever needed to extend our corpus and document larger than 549 was added. Since 600 is larger than any document, no overlap was needed either. The README.md in the `/corpora` folder also mentioned that most of the documents in `corpora/campus_life` had clear and concise statements that were within 1 sentence.

<!-- What about YOUR documents made you pick these numbers? Short posts and
     long sectioned guides don't want the same chunking, and "800 seemed
     reasonable" earns nothing. Point at something you noticed when you read
     the documents in Milestone 1.

     If you changed your mind partway through, say so and say why. That's worth
     more than pretending you got it right first time.

     Milestone 3. -->

## Sample Chunks

<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->

**Chunk 1** — source: `admin_add_drop_deadline.txt#0` — produced by: `chunker.py::split_documents`

```On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.
```

**Chunk 2** — source: `course_biol_160.txt#0` — produced by: `chunker.py::split_documents`

```BIOL 160 Cell Biology

I lived here my sophomore year. Format is lecture three times a week with a weekly lab. Assessment: four unit tests and a cumulative final. Not curved.

Expect 9 to 11 hours a week, the heaviest first-year course by reputation.

The one piece of advice: the unit tests come fast, roughly every three weeks; falling behind once is very hard to recover from.
```

**Chunk 3** — source: `course_hist_118_workload.txt#0` — produced by: `chunker.py::split_documents`

```Workload for HIST 118 Modern World History

People keep asking so: a lot of reading, about 120 pages a week, but no problem sets. That's real time, not optimistic time.

It's front-loaded — the first month is heavier than the rest, partly because you're learning the format.
```

**Chunk 4** — source: `dining_pellew_dining_hall_followup.txt#0` — produced by: `chunker.py::split_documents`

```Re: Pellew Dining Hall

Adding to what people have said about Pellew Dining Hall. The wait figure of 12 to 18 minutes at peak matches what I've seen. If you're trying to eat between classes, go before 11:45 and it's a different building entirely.

Also worth saying: the furthest hall from anywhere, next to the athletics centre. Nobody tells you this at orientation.
```

**Chunk 5** — source: `housing_innisfree_hall.txt#0` — produced by: `chunker.py::split_documents`

```Innisfree Hall — what it's actually like

Transferred in last year, so take this with a grain of salt. Built 1991, renovated 2022. Rooms are doubles arranged as pairs sharing one bathroom between two rooms.

The good: the shared-bathroom-between-two-rooms arrangement is the best compromise on campus.

The bad: no air conditioning, which matters for the first three weeks of September.

Laundry costs $1.75 wash, $1.75 dry, app-based. On noise: moderate; the building is L-shaped and the short wing is much quieter.
```

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question:** python app.py ask "what's the workload like in BIO160"

**Answer:**

```(best distance 0.443, cutoff 0.6)

The workload for BIOL 160 Cell Biology is 9 to 11 hours a week, and it is the heaviest first-year course by reputation. It is also front-loaded, meaning the first month is heavier than the rest. (Source: `course_biol_160_workload.txt` and `course_biol_160.txt`)

Sources retrieved: course_biol_160.txt, course_biol_160_workload.txt, course_econ_101_workload.txt, course_engl_205_workload.txt, course_phys_130_workload.txt
```

**My relevance cutoff:**

<!-- The number you set in config.py, and how you got there.

     You ran five questions your corpus covers and the five in OUT_OF_SCOPE
     that it clearly doesn't, and wrote down the best distance for each. What
     did those two groups look like? Where was the gap? Put the actual numbers
     here — the table below wants all ten rows.

     Milestone 4. -->

| Question | In corpus? | Best distance |
|---|---|---|
| "what's the workload like in BIO160" | YES | 0.443 |
| "when is the atrium open?" | YES | 0.423 |
| "how is campus orientation?" | YES | 0.529 |
| "how much does laundry cost in aldridge?" | YES | 0.264 |
| "when is it cold on campus?" | YES | 0.502 |
| "What is the capital of Mongolia?" | NO | 0.825 |
| "How do I change the oil in a diesel engine?" | NO | 0.934 |
| "Who won the 1994 World Cup?" | NO | 0.886 |
| "What is the recommended dosage of ibuprofen for a headache?" | NO | 0.884 |
| "How do I write a for loop in Rust?" | NO | 0.896 |

## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1.** I asked Claude to read the repo and explain what each file and folder does. It helped break the pipeline into five stages (loading, chunking, embedding, retrieval, generation), the three corpora, and the two assignments (criteria.md and README.md). That gave me my first working picture of what RAG is and what unit 1 asks for. I then read questions.py and wrote my own criteria in criteria.md, using the corpus README's numbers (88 documents, about 317 characters each). 

**2.** For Milestone 3, I asked Claude how to choose a chunk size and overlap. I first tried 200/50, which turned 88 documents into 224 chunks, including one that was a single character. After seeing the results, I decided to try something else. Claude then wrote split_documents and a helper which keeps a document whole if it fits (i.e., smaler than chunk_size) and otherwise splits on paragraph breaks and repeats the title on each chunk. I set CHUNK_SIZE to 600 and CHUNK_OVERLAP to 0 so nothing in campus_life gets split. I added my own comment in the code, and I learned that my chunker's splitting branch never runs on this corpus since all documents are smaller than 600 characters.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Every sampled chunk should have about 317 characters | 5 of 5 | 0/5| 0/5| 0/5 | MISSED |
| 5. Every answer the system generates should be within 2 seconds | 5 of 5 | 0/5 | 0/5 | 0/5 | MISSED |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

### how is campus orientation? — run 1

- Best distance: 0.5288 (passed the gate)
- Sources retrieved: admin_wifi_and_accounts.txt, dining_the_atrium_followup.txt, housing_tamsin_court.txt, money_jobs.txt, orientation_what_matters.txt

```
Students say that most of orientation week is optional even though it is framed as if it isn't, and that the only two sessions worth attending are the meeting with your academic adviser and the library walkthrough because they save time later. They also mention that the club fair is useful for the first forty minutes of its four-hour duration, and that orientation does not tell you that The Atrium dining hall is picked clean by 1:15 and not restocked until the next morning. 

Sources: `orientation_what_matters.txt` and `dining_the_atrium_followup.txt`
```

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunk contains the answer | MET | Through every run, an answer was contained in the chunk. This was a great success because we received results we were expecting. |
| 2 | Every answer names a source | MET | Every retrieved chunk also returned sources attached to the correct answer. This was expected with my questions since each was based on particular files. |
| 3 | Gate stops out-of-corpus questions | MET | Every out of scope question was rejected and no answer was retrieved. This is great because the system abstains from answering questions it cannot support. Thus, it was a pass |
| 4 | Original: Every sampled chunk should have about 317 characters | MISSED | After testing, I realized I chose a poor criterion. "about" is not specific and I can't confidently quantify what "about" means since different people could reach the same conclusion. For this reason, this criterion failed with every run and question. |
| 4b | Revised: Every sampled chunk is between 300 and 334 characters | MISSED | Revision of #4. "About" had no fixed meaning, so two people could score the same chunk differently. This version gives a range anyone can check. |
| 5 | Every answer the system generates should be within 2 seconds | MISSED | This was also a poor criterion since I wasn't able to accurately measure the length of duration per response. I didn't realize that I needed to add additional code to actually record this and return. For this reason, none of the trials or runs were able to count the time and this criterion failed. |
| 5b | Revision of #5: Each answer's response time is recorded in the run output and is 2 seconds or less. | MISSED | The original couldn't be measured because my harness never recorded durations, and I can't add code, so no response time exists to check. This revision only adds the requirement that the time be recorded, so it is also MISSED. |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## Diagnoses

**Criterion 4 (about 317 characters per chunk; 4b: 300 to 334).**
Stage: chunking. This was a real miss on the numbers, not a scoring problem. The five sampled chunks measured 300, 379, 274, 367 and 516 characters, so only one of the five landed in the 300 to 334 range of 4b. The mechanism is my own chunking setup. With CHUNK_SIZE at 600, no document is split (the longest is 549 characters), so every chunk is one whole document and its length is just the length of that document. The 317 I used came from the corpus README as the *average* document length, and I wrote it as if every chunk would be near that number. An average says nothing about each chunk, so a per-chunk target near 317 could never hold with documents this varied. I wrote 4b to remove the vagueness of "about," but it still expects every chunk to sit near the mean, so it fails for the same reason and stays MISSED.

**Criterion 5 (every answer within 2 seconds; 5b: recorded and 2 seconds or less).**
Stage: none that I can prove. My run harness never recorded how long each answer took, so there is no timing to compare against the target. If I had to guess, latency would come from generation (the model call), but I have no data, so that is a guess and not a finding. Nothing in retrieval, embedding, chunking or loading is shown to be slow or fast.

**Pattern.** Both misses come from the same mistake: I wrote the criteria before checking what my setup could measure or what my corpus actually looks like. Criterion 4 assumed uniform chunk lengths in a corpus where lengths vary, and criterion 5 assumed timing data my harness never collected. These are two symptoms of one problem in how I wrote the criteria, not two separate pipeline failures.

**Criteria 1 to 3.** No misses. All three hit 5/5 on every run against targets of 4 of 5, 5 of 5 and 4 of 5, respectively. Criteria 1 and 3 may have been set low, since I never saw a run below the target. For criterion 3 the gap is wide: my worst in-corpus question had a best distance of 0.529 and my closest out-of-scope question had 0.825, with the cutoff at 0.6. I could tighten criterion 3 to 5 of 5.


## The Improvement

**What I changed:** Lowered CHUNK_SIZE in config.py from 600 to 350 (overlap stays 0) and re-ran `python app.py index`. Nothing else changed.

**Why I picked it:** **Why I picked it:** My diagnosis of criterion 4 named the chunking stage: at size 600 no document splits, so chunk length equals document length (274 to 516 in my samples). A smaller size makes the paragraph-splitting branch run for the first time on this corpus, so I can see whether chunk lengths get closer to 317 and whether smaller chunks hurt retrieval.

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 3/5 | 1/5 | 1/5 | MISSED |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MISSED |
| 4. Every sampled chunk should have about 317 characters | 5 of 5 | 0/5 | 0/5 | 0/5 | MISSED |
| 4b. Every sampled chunk is between 300 and 334 characters | 5 of 5 | 1/5 | 2/5 | 1/5 | MISSED |
| 5. Every answer the system generates should be within 2 seconds | 5 of 5 | 0/5 | 0/5 | 0/5 | MISSED |
| 5b. Response time recorded and 2 seconds or less | 5 of 5 | 0/5 | 0/5 | 0/5 | MISSED |

**Did it help?**

No. The change made criterion 1 worse and did not fix anything else.

Before (chunk size 600), criterion 1 scored 5/5 on all three runs. After (chunk size 350), it scored 3/5, 1/5 and 2/5, so it missed its 4 of 5 target on every run and went from MET to MISSED. Criteria 2 and 3 did not change: every answer still named a source (5/5 on all three runs), and the gate still refused all five out-of-scope questions, with best distances between 0.825 and 0.923 against a cutoff of 0.6. 

Criteria 4 and 4b: are still MISSED. Criteria 5 and 5b are unchanged at 0/5 because nothing records response time.

How I know: I changed only CHUNK_SIZE (600 to 350), re-indexed, and ran the same five questions three times each. The out-of-scope pass and the retrieved sources were identical across runs, so the drop in criterion 1 comes from the change and not from randomness in retrieval. The sources that changed from before are visible in the logs: for example, the orientation question now retrieves housing_aldridge_hall.txt, transit_shuttle.txt and transit_walking.txt instead of admin_wifi_and_accounts.txt, dining_the_atrium_followup.txt and money_jobs.txt, and the best distance for the atrium question moved from 0.423 to 0.378.

Two questions failed on all three runs after the change: laundry in Aldridge and when it is cold on campus. The right source files were retrieved for both (housing_aldridge_hall_laundry.txt and winter_gear.txt).

This matches the risk I wrote down before running it: my earlier 200/50 attempt cut answers away from their context, and a smaller chunk size does the same thing. Criterion 1 varied from run to run even though the retrieved sources did not, which suggests the pass/fail depends on the generated answer, not only on the chunks. I'm reporting the change as it came out: a smaller chunk size did not help, and the honest conclusion is that chunk size 600, which keeps each post whole, worked better for this corpus of short posts.

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->


## What's Still Broken

**Criterion 1 (retrieved chunk contains the answer): missed after my change.**
It scored 3/5, 1/5 and 2/5 against a target of 4 of 5, down from 5/5 on every run before. What I'd do about it: put CHUNK_SIZE back to 600, which met the target on all three runs. I stopped there because the improvement was a single change, and it made criterion 1 worse, so undoing it is the fix. Before I trust it, I'd also open the laundry and cold-weather source files and check whether their answers were split across chunks at size 350.

**Criteria 4 and 4b (chunk length): still missed.**
Chunk lengths in this corpus follow document lengths (274 to 516 in my sampled chunks, longest document 549), so a target near the 317 average cannot hold for every chunk. I would not chase this with more chunking changes, because the number was never something retrieval quality depends on. I stopped because fixing it would mean forcing documents to one length, which would split posts for no benefit.

**Criteria 5 and 5b (response time): still missed.**
My run harness never recorded how long each answer took, so there is no measurement to compare with the 2 second target. What I'd do: add timing around the generation call in run_eval.py and record it per answer. I stopped because this assignment doesn't allow me to add more code.

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

**Criterion 4.** I took the corpus README's average document length (about 317) and wrote it as a per-chunk target. An average tells you nothing about each chunk. I'd write a criterion about something that affects answers, such as "no chunk is cut mid-sentence" or "the answer sentence and its title are in the same chunk."

**Criterion 5.** I'd have checked that my harness records response times before writing a time target. A target you can't measure can't be met or missed.

**Criterion 1.** I worded it as a retrieval check, but the pass/fail changed between runs while the retrieved sources stayed identical, so what I actually scored depended on the generated answer. I'd word it as a check on the retrieved chunk's text, such as "the retrieved chunks contain the expected answer," so a retrieval problem can't hide behind a generation one.

**Targets for criteria 1 and 3.** Both scored 5/5 on every run before my change against targets of 4 of 5, so they were set low. I'd make criterion 3 5 of 5, since my gap between the worst in-corpus question (0.529) and the closest out-of-scope one (0.825) is large.

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
