# Memory Strategy

## Short version

For this specific friend and this specific managed-instance setup:

- **OpenClaw / Lossless Claw** should own the **current conversation**
- **Hindsight** should own **long-term factual recall**
- **Notion** should own **curated outputs and workflow state**

That is the cleanest boundary.

---

## Why this matters

His most important use cases are not generic “chat memory.”

They are things like:

- “Who is this person and what happened before?”
- “What did this client want?”
- “What open loop did I leave hanging?”
- “Cross this new lead with my old work and draft a proposal.”

That is **long-term factual/business memory**, not just session continuity.

---

## Layer 1 — OpenClaw memory / Lossless Claw

### What it should do

Use OpenClaw’s native conversation memory for the active chat.

If the managed instance allows it, enable `lossless-claw` because it is the right tool for:

- live session continuity
- exact recovery inside the conversation
- long chat handling without relying on fragile summary-only recall

### What it should not do alone

It should **not** be the only system carrying months of client, email, and project history.

That is not the job.

---

## Layer 2 — Hindsight for long-term business memory

### Why Hindsight fits this friend better than “just memory files”

Hindsight is a better fit here because the problem is:

- recalling people and prior interactions
- linking emails, notes, and project history
- retrieving old context accurately
- synthesizing next actions from real history

That is exactly the kind of work Hindsight is good at.

### Why Hindsight fits this friend better than our own stack 1:1

Our own stack evolved for **our** environment:

- local access
- more control
- more infrastructure freedom
- more experiments

His setup is different:

- managed instance
- no terminal access
- tiny resources on the instance itself
- non-technical user

So the right move is to keep memory **external** and keep OpenClaw lean.

---

## Why not just use Honcho here?

Honcho is real, useful, and has a native OpenClaw integration.

It is especially strong when the problem is:

- multi-participant identity modeling
- agent/user preference modeling
- cross-session user understanding
- multi-agent / multi-user memory

That was a strong fit for **our** setup and history.

But for **this friend’s v1**, the most important asks are closer to:

- factual recall
- email/client/project history
- old thread retrieval
- proposal/context synthesis

That leans more naturally toward **Hindsight**.

### Practical rule

- If the assistant is mainly a **solo operator’s business memory + drafting engine**, prefer **Hindsight**.
- If the assistant later becomes a **richer multi-user / multi-agent identity system**, revisit **Honcho**.

### Clean recommendation

For this roadmap:

- choose **Hindsight first**
- keep **Honcho as the main alternative** if the product later shifts toward relationship/identity modeling across more participants

---

## Why Notion should not be the memory backend

Notion is excellent for:

- proposals
- content drafts
- CRM-lite pages
- tasks
- review queues

Notion is bad as the raw memory layer for:

- every email body
- every thread artifact
- every transcript chunk
- every retrieval event

If you dump everything there, it becomes noisy and brittle.

Use Notion as the **human-facing operating surface**, not the raw archive.

---

## Hosting strategy

## Best option: Hindsight external / managed first

The cleanest path is:

- keep OpenClaw on the managed instance
- keep Hindsight outside it
- keep ingestion bridges outside it

This avoids trying to make a 1 vCPU / 3 GB managed box do too much.

## If self-hosting Hindsight later

Do it on **separate infrastructure**, not on the managed OpenClaw instance.

### Good database options from prior research

If a separate self-hosted Hindsight deployment is needed later, the best pgvector PostgreSQL options we researched were:

#### 1. Supabase
Best overall starting point.

Why:

- officially supported path in Hindsight docs
- connection pooling available
- Frankfurt region is good for Italy
- easy setup

Main tradeoff:

- storage is smaller than some alternatives

#### 2. Neon
Good fallback.

Why:

- also officially supported in Hindsight docs
- pooled connections available
- simple hosted PostgreSQL path

Main tradeoff:

- storage limits can become the constraint sooner

#### 3. Aiven
Useful if storage matters more and concurrency stays low.

Why:

- 1 GB free tier looked attractive in our research
- always-on behavior is nice

Main tradeoff:

- hard connection limits and no pooling on free tier make it less forgiving

### Important rule

Even if Hindsight is self-hosted later, it should still be **separate** from the managed OpenClaw runtime.

---

## Memory write strategy

Every ingested memory artifact should carry enough metadata to be useful later.

Minimum metadata:

- source type (`email`, `chat`, `meeting`, `notion`, `manual-note`, `research`)
- person/entity
- company/client
- topic/project
- timestamp
- source ID or canonical link
- privacy scope (`business`, `personal`, etc.)

This is what makes later retrieval actually useful.

---

## Guardrails

### 1. No duplicate truth systems without a reason

Do not let all of these become messy overlapping records of the same thing:

- OpenClaw thread memory
- Hindsight
- Notion
- external bridge cache

Each system needs one job.

### 2. Retrieve before answering history questions

When the user asks about a person, client, old thread, or past project:

- retrieve first
- summarize second

### 3. Use original sources when commitments matter

If the question is about:

- dates
- exact promises
- specific asks
- prior wording

prefer the original source artifact over summary-only recall.

### 4. Separate business and personal context clearly

If the assistant will later handle both, start tagging for that now.

---

## Decision

If we are building the friend’s v1 now, the memory decision should be:

### Recommended v1

- **Managed OpenClaw** for runtime
- **Lossless Claw if available** for active conversation continuity
- **Hindsight external** for long-term factual memory
- **Notion** for structured outputs and review

### Not recommended for v1

- self-hosting memory on the same managed OpenClaw box
- using Notion as the raw memory backend
- overcomplicating the first version with multiple overlapping memory systems

---

## Revisit later if the product grows

Revisit the memory choice if he later wants:

- more multi-user/team-aware memory
- richer agent/user identity modeling
- multiple assistants/personas sharing context
- more behavioral personalization than factual recall

That is where Honcho becomes more interesting again.

For now, Hindsight is the cleaner choice.