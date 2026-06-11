# Repeatable Prospecting Runbook

Use this runbook when you want to run the same multistage prompt sequence for Project Triage or any similar offer. The process is intentionally prompt-driven rather than code-driven: each stage produces structured output that becomes the input to the next stage.

## Inputs to prepare

Before starting, fill in these fields:

- **Product name:** The offer you are prospecting for.
- **Product description:** One concise paragraph describing the problem solved and the outcome promised.
- **Target buyers:** Roles, company types, company sizes, or industries that can buy the offer.
- **Buying signals:** Observable public signals that imply pain, urgency, or fit.
- **Disqualifiers:** Any roles, company types, regions, industries, or weak signals to exclude.
- **Prospect count:** The maximum number of prospects to return.
- **Source requirements:** Whether sources must be public webpages, LinkedIn posts, podcasts, job posts, reviews, case studies, or other evidence.

## Stage 1 — Define the search brief

Prompt:

```text
I want to run a prospecting sequence for this offer:

PRODUCT NAME:
{{product_name}}

PRODUCT DESCRIPTION:
{{product_description}}

TARGET BUYERS:
{{target_buyers}}

BUYING SIGNALS:
{{buying_signals}}

DISQUALIFIERS:
{{disqualifiers}}

Create a search brief with:
1. the strongest ICP segments,
2. the best public buying signals to search for,
3. search query patterns,
4. source types to prioritize,
5. source types to avoid,
6. a scoring rubric out of 25 points.
Do not list prospects yet.
```

Expected output: a search strategy and scoring rubric. Review this before continuing so the rest of the run does not drift into weak-fit leads.

## Stage 2 — Find candidate prospects

Prompt:

```text
Using the search brief above, find up to {{prospect_count}} candidate prospects.

Rules:
- Prefer prospects with named people in buyer or influencer roles, not just company names.
- Each prospect must have at least one public source URL supporting the fit or buying signal.
- Prioritize recent or durable signals related to the stated pain.
- Do not infer that a prospect is actively buying; only say they are a plausible fit.
- Avoid duplicate companies unless there are different buyer personas worth testing.

Return a table with:
- prospect name,
- organization,
- role,
- source URL,
- evidence summary,
- matching buying signal,
- reason to keep or reject.
```

Expected output: a candidate pool. If the evidence is thin, rerun this stage with narrower search queries before scoring.

## Stage 3 — Score and rank

Prompt:

```text
Score the kept prospects using this rubric:
- Buyer fit: 1-5
- Signal strength: 1-5
- Urgency/timing: 1-5
- Ability to buy / authority: 1-5
- Personalization quality from public evidence: 1-5

Return the top {{prospect_count}} prospects ranked by total score.
For each prospect, include:
- rank,
- name,
- organization,
- buyer role fit,
- public buying signal,
- source URLs,
- score,
- one sentence explaining the score.
```

Expected output: a final shortlist that can be used by sales or founder-led outreach.

## Stage 4 — Draft initial outreach

Prompt:

```text
Create initial outreach drafts for the top {{draft_count}} prospects from the ranked shortlist.

Rules:
- Use the public buying signal as the first-sentence personalization hook.
- Do not overstate the signal or claim the prospect has the problem right now.
- Offer a lightweight diagnostic, checklist, template, or teardown before asking for a meeting.
- Keep each draft under 120 words.
- Include a subject line.
- Use a low-pressure CTA.
```

Expected output: ready-to-edit first-touch messages for the highest-priority prospects.

## Stage 5 — Create a reusable follow-up sequence

Prompt:

```text
Create a 3-step follow-up sequence for prospects not covered by the personalized drafts.

Rules:
- Email 1 should reference the prospect-specific public signal using a placeholder.
- Email 2 should clarify the value of the offer and distinguish it from common alternatives.
- Email 3 should be a polite close-the-loop note.
- Keep each message concise and easy to personalize.
```

Expected output: a generic but source-aware sequence that can be personalized from the shortlist table.

## Stage 6 — Quality check before sending

Prompt:

```text
Audit the shortlist and outreach for quality.

Check for:
- unsupported claims,
- stale or weak evidence,
- prospects outside the ICP,
- language that implies the prospect requested help,
- over-personalization that feels invasive,
- missing source URLs,
- outreach drafts over 120 words,
- unclear CTAs.

Return required edits first, then optional improvements.
```

Expected output: a cleanup list. Apply required edits before sending or storing the run.

## Recommended output format

Store each completed run as a Markdown file under `prospecting/` with these sections:

1. Product
2. ICP and scoring model
3. Prospect shortlist
4. Highest-priority outreach drafts
5. Sequence template for remaining prospects
6. Recommended next steps

The Project Triage run in this repository follows that format and can be used as the example output for future runs.
