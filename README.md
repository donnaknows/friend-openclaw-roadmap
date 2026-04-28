# Managed OpenClaw Roadmap for a Non-Technical Founder/Operator

## Start here

This repo is now organized as a small implementation package, not just one long memo.

Read it in this order:

1. **`README.md`** - the main architecture and phased roadmap
2. **`MEMORY_STRATEGY.md`** - why this setup should use OpenClaw + Hindsight + Notion with clean boundaries
3. **`IMPLEMENTATION_CHECKLIST.md`** - the actual build checklist
4. **`OPEN_QUESTIONS.md`** - the decisions your friend still needs to answer
5. **`AGENT_BRIEF.md`** - the compact handoff brief for the future assistant

## Recommendation in one sentence

Build a **lean managed-instance assistant** where:

- **OpenClaw** handles runtime and orchestration
- **Lossless Claw** handles current-session recall, if available
- **Hindsight** handles long-term factual memory externally
- **Notion** handles structured outputs and human review
- **external bridges** handle email and other integrations

That is the shortest path to something genuinely useful without overloading a tiny managed instance.

## Executive summary

Do **not** clone our full Donna stack 1:1.

That would be the wrong move for a brand-new **managed** OpenClaw instance with **no terminal access** and only **1 vCPU / 3 GB RAM**.

The right v1 is this:

- **OpenClaw managed instance** = the agent runtime and chat surface
- **Lossless Claw (`lossless-claw`)** = live/session recall inside OpenClaw, **if the managed instance allows it**
- **Hindsight (external)** = durable factual memory across emails, clients, old threads, and project history
- **Notion** = structured system of record for proposals, content drafts, CRM-lite, and review queues
- **Small external bridge** = webhook/API glue for email ingestion, optional social posting, and other outbound automations

That gives him the outcomes he actually wants:

1. **"What does this person want and what happened before?"**
2. **"Draft me a social post + image concept."**
3. **"Research this lead/client and prepare a Notion proposal draft."**
4. **"Take annoying operational work off my plate."**

And it does it without trying to run half the internet inside a tiny managed OpenClaw box.

---

## What we are optimizing for

This roadmap is for a friend who is:

- non-technical
- using a managed OpenClaw instance
- constrained on local resources
- likely to need trust and usefulness fast
- more interested in business leverage than infrastructure purity

So the design goal is:

> **Keep OpenClaw lean. Push heavy memory, ingestion, and platform-specific integrations outside. Keep the agent smart, not overloaded.**

---

## The requested use cases, translated into product requirements

### 1) Conversation + email recap / relationship memory

Example ask:

> "Donna che cazzo vuole sto qua che si è rifatto vivo dopo 2 mesi? Puoi recuperarmi highlight del trascorso e farmi proposta di next actions?"

This requires:

- durable memory across sessions
- email ingestion and normalization
- entity-aware recall by person/company/topic
- source-aware summaries
- next-action suggestions

### 2) Social content generation

Example ask:

> "Donna vorrei per cliente X fare un post su questo argomento: mi fai proposta di testo e di immagine?"

This requires:

- project/client context
- past positioning and tone recall
- text generation
- image concept generation
- optionally image generation
- eventually scheduling/posting

### 3) Client/project brainstormer

Example ask:

> "Donna questo nuovo cliente X è venuto da me per Y. Trova info online e di mercato, incrociale con mie competenze e progetti vecchi, e fammi una bozza di proposta su pagina Notion, così che possa rivederlo e poi in caso mandarla."

This requires:

- web research
- retrieval from past projects / capabilities / notes
- synthesis into an offer/proposal structure
- Notion writing
- approval-first delivery

### 4) Time-saving agentic operations

Example ask:

> "Donna sta compagnia aerea mi ha cancellato il volo: parla tu con il loro servizio clienti e prova a ottenere rimborso o a capirci qualcosa."

This requires:

- browsing / form filling / email drafting / thread handling
- document collection
- approval gates before irreversible actions
- tracking open loops and reminders

---

## Constraints that should shape the build

### Hard constraints

- **No terminal access** on the OpenClaw instance
- **1 vCPU / 3 GB RAM** on the managed instance
- **Brand-new setup** with likely minimal plugins/tools enabled
- End user is **not technical**

### Practical implications

This means:

- no local daemons on the OpenClaw box
- no assuming we can run custom bridge services locally
- no assuming we can self-host extra databases/vector stores on the same machine
- no copying our local webhook/systemd-heavy setup
- no building v1 around shell access

So the architecture must be **API-first, provider-hosted, and externally bridged**.

---

## Recommendation: the right memory architecture

## Layer 1 - OpenClaw session memory

Use OpenClaw's own in-thread memory for the current conversation.

If the managed platform supports plugin installation/configuration, enable:

- **`lossless-claw`** for live conversation recall and exact recovery inside OpenClaw

This layer should own:

- current chat continuity
- session-level recall
- active thread context

It should **not** be the only source of truth for long-term business memory.

## Layer 2 - Hindsight as external long-term memory

Use **Hindsight externally** for durable recall across:

- emails
- clients
- partners
- past project notes
- proposals
- structured relationship history
- business facts and decisions

### Why Hindsight fits this case

Based on our prior research and this use case, Hindsight is the better first memory layer here because:

- it is strong at **factual recall**
- it is designed for **long-term memory and retrieval accuracy**
- it works well for **emails, transcripts, project notes, and decision history**
- it is easier to justify than a heavier multi-service self-hosted memory stack on a tiny managed instance
- the friend sounds closer to a **single operator with an assistant** than a multi-user collaborative memory graph product

### Recommended deployment choice

**Preferred v1:** use **Hindsight Cloud** or another externally hosted Hindsight deployment.

Do **not** host it on the OpenClaw managed instance.

### Fallback if cloud is not acceptable

If cost/privacy later pushes us away from managed Hindsight, run Hindsight on a **separate service** and keep OpenClaw unchanged.

Do not make the OpenClaw box carry both the agent runtime and the memory infrastructure.

## Layer 3 - Notion as structured operating system

Notion should be the place where the agent writes:

- proposal drafts
- content drafts
- CRM-lite records
- action lists
- follow-up queues
- curated summaries worth reviewing

Notion should **not** be treated as the raw memory dump for everything.

Use it as the **human-facing workspace** and **review surface**.

## The boundary rule

Keep the layers clean:

- **Lossless/OpenClaw memory** = live conversation
- **Hindsight** = durable factual recall
- **Notion** = curated outputs and operational structure

Do **not** make all three store the same thing in the same way.

That gets messy fast.

---

## Why not just copy our current stack?

Because our stack grew around local control.

What we should reuse from our history:

- clear persona and operating instructions
- explicit approval gates for external actions
- webhook/event-driven ingestion over clumsy polling when possible
- strong memory boundaries
- Notion as a review/workflow surface
- research delegation for non-trivial web work

What we should **not** copy blindly:

- local bridge daemons running on the same box
- systemd/service assumptions
- shell-heavy setup procedures
- too many custom plugins on day one
- multi-agent sprawl before the core assistant is useful

This should be a **stripped-down managed-instance architecture**, not a replica of Donna HQ.

---

## Recommended v1 architecture

```text
User
  ↓
Managed OpenClaw instance
  ├─ live chat / orchestration
  ├─ current-session memory (and lossless-claw if available)
  ├─ research + drafting
  └─ approval-gated actions

External services
  ├─ Hindsight → durable factual memory
  ├─ Notion → proposals / CRM-lite / content calendar / tasks
  ├─ Email bridge → inbox ingestion and normalization
  ├─ Search provider(s) → market/company research
  ├─ Image generation provider → post visuals
  └─ Optional posting bridge → social scheduling / publishing
```

### Key design principle

**OpenClaw is the brain and coordinator. External systems are the memory, pipes, and hands.**

---

## Core capability roadmap

## Phase 0 — Foundation and trust

### Goal

Make the assistant coherent, safe, and usable before adding automation.

### Deliverables

- Agent identity/persona configured
- Basic operating instructions written
- Approval policy defined
- Plugin/tool availability audited on the managed instance

### Must-have outcomes

The assistant can:

- answer normally in a consistent voice
- ask for approval before sending/posting/submitting anything external

### Notes

This phase matters more than people think.

If the assistant's voice, boundaries, and output structure are sloppy, everything built afterward feels unreliable.

---

## Phase 0.5 — Onboarding interview

### Goal

The assistant interviews the user to learn who they are, what they do, and how they work.

This is not optional. It is the foundation for everything the assistant will do later — memory, proposals, social content, relationship recall. Without this, the assistant is generic.

### Why this matters

A good assistant does not guess about:

- what the user's business actually is
- who their clients are
- what tone they want in communications
- what they consider a good vs bad outcome
- what they never want the assistant to do

The interview fills all of that.

### Recommended interview structure

The assistant should guide the user through these topics in a conversational way, not as a form.

#### A. Identity and business

- What do you do, in your own words?
- What is your business? Freelance, agency, product, consulting?
- What services or products do you sell?
- Who are your typical clients?
- What does a great client relationship look like for you?
- What does a bad one look like?

#### B. Communication style

- How do you normally talk to clients? Formal, casual, direct?
- What tone do you want the assistant to use when drafting things on your behalf?
- Any language preferences? Italian, English, both?
- Any brands or people whose communication style you admire?

#### C. Clients and relationships

- Who are your top 5-10 current or recent clients? (name, company, what they need from you)
- Any important past clients worth remembering?
- Are there people you want to reconnect with?
- Are there people or companies you want to avoid?

#### D. Tools and workflow

- Where do you keep track of tasks and projects today?
- Do you already use Notion? If yes, how?
- What email system do you use?
- What social platforms do you care about?
- Where do your leads come from? Referrals, inbound, cold outreach?

#### E. Boundaries and safety

- What should the assistant never do without asking?
- What should the assistant never do at all?
- Is there anything you consider private that the assistant should not store or reference?
- How do you want to handle mistakes? Fix silently, flag and ask, or something else?

#### F. Aspirations and direction

- What does success look like in 3 months with this assistant?
- What is the single most annoying thing you do today that you want the assistant to handle?
- Is there a specific workflow or client scenario where the assistant would save you the most time?

### How the assistant should conduct the interview

1. **Conversational, not interrogative.** Ask a few questions at a time, not all 30 at once.
2. **Write everything down.** After each interview segment, store the answers in Hindsight and create a Notion page with the user profile.
3. **Confirm understanding.** Paraphrase back what you heard. Let the user correct you.
4. **Do not rush.** It is better to do 2-3 short sessions than one exhausting one.
5. **Offer to skip.** If the user does not want to answer a section, note it and move on. Do not push.

### Output of this phase

After the interview, the assistant should have:

- [ ] A written user profile stored in Hindsight (identity, business, style, boundaries)
- [ ] A Notion page with the user profile summary
- [ ] A client/contact seed list (even partial)
- [ ] A tone/communication style guide
- [ ] An explicit approval policy tailored to this user
- [ ] A list of "never do" actions
- [ ] A prioritized list of workflows to build first

### Done when

The assistant can answer:

> "What does this user care about, how do they work, and what should I never do?"

without guessing.

---

## Phase 1 — Memory and intake

### Goal

Make the agent good at: "Who is this person, what happened before, and what should I do now?"

### Deliverables

- Hindsight connected externally
- Memory schema/tags decided
- Email ingestion pipeline in place
- Notion databases for people/companies/opportunities/tasks
- Source-linking strategy defined

### Recommended memory write strategy

Every ingested artifact should carry metadata such as:

- source type (`email`, `chat`, `notion`, `meeting`, `manual-note`)
- person/entity
- company/client
- topic/project
- date/time
- raw source ID or canonical URL

### Email ingestion architecture

Because the OpenClaw instance is managed and has no terminal, do this with an **external bridge**, not a local daemon.

#### Preferred pattern

1. Email arrives in Gmail / AgentMail / other provider
2. External bridge receives webhook or polls provider API
3. Bridge normalizes the content
4. Bridge writes the artifact into Hindsight with tags/metadata
5. Bridge optionally creates or updates the related Notion record
6. OpenClaw is notified only when useful, or the agent pulls on demand

### Critical lesson from our own history

Do **not** let inbound webhooks create a disconnected "shadow assistant" that acts without context.

We already learned that webhook-triggered flows can lose conversational continuity.

So for this system:

- treat inbound email as **memory ingestion first**
- treat agent interaction as **retrieval + synthesis second**
- do not let a separate orphan workflow make judgment calls without the main context

### Acceptance test

User asks:

> "This guy resurfaced after two months. What does he want?"

The assistant should return:

- who the person is
- last meaningful interactions
- relevant open loops
- likely intent
- suggested next actions
- confidence / uncertainty if the signal is weak

---

## Phase 2 - CRM-lite and proposal engine

### Goal

Turn memory + research into usable commercial output.

### Deliverables

- Notion databases for contacts, companies, opportunities, proposals
- Research workflow
- Old project retrieval workflow
- Proposal page template in Notion

### Minimal Notion schema

#### 1. Companies
- Name
- Industry
- Website
- Status
- Relationship summary
- Last contact date
- Linked opportunities

#### 2. Contacts
- Name
- Company
- Role
- Email
- Relationship notes
- Last contact date
- Next follow-up

#### 3. Opportunities
- Client/company
- Need/problem
- Stage
- Value estimate
- Relevant past work
- Proposed next step
- Proposal page

#### 4. Proposals
- Title
- Client
- Opportunity
- Scope draft
- Offer structure
- Risks / assumptions
- Review status

#### 5. Tasks / follow-ups
- Owner
- Due date
- Channel
- Linked entity
- Status

### Workflow target

User says:

> "New client X came to me for Y. Research the market, cross it with my past work, and prepare a Notion draft."

The assistant should:

1. research the company/market/problem
2. retrieve similar past projects and skills
3. identify angles / offer shapes
4. create a Notion proposal draft
5. leave it in review state, not auto-send

### Acceptance test

The output is not just a chat answer.

It creates a usable Notion page with:

- short context summary
- problem framing
- recommended offer
- rationale
- assumptions
- next questions to validate

---

## Phase 3 - Social content studio

### Goal

Help him consistently create social content for himself or clients.

### Deliverables

- Content brief template in Notion
- Prompt pattern for post generation
- Image concept generation flow
- Optional image generation integration
- Draft queue / approval queue

### v1 recommendation

Start with **drafts only**.

The assistant should generate:

- 2-3 text variants
- 1-3 hook options
- a visual concept
- optional generated image or image prompt
- CTA suggestion
- posting recommendation by platform

### v2 recommendation

If direct publishing is needed, integrate a **social scheduler API** rather than every social network directly.

That keeps the build cleaner.

### Acceptance test

User says:

> "For client X, make a post on topic Y."

The assistant returns or writes to Notion:

- angle options
- final draft
- image idea
- generated image or generation prompt
- platform-specific notes
- status = ready for review

---

## Phase 4 - Operational assistant / annoying work removal

### Goal

Take repetitive coordination and customer-service-like tasks off his plate.

### Best first targets

These are good v1/v2 agentic ops candidates:

- follow-up reminders on leads/partners/clients
- invoice/payment reminder drafting
- inbox triage
- travel disruption triage
- refund/claim draft preparation
- meeting prep packs
- post-meeting task extraction
- collecting documents/info needed for a request
- form-prefill / browser-assisted admin tasks

### What to automate first

Automate the tasks that are:

- annoying
- repetitive
- low creativity
- high context-switch cost
- approval-friendly

### What not to automate too early

Do **not** give full autonomy on day one for:

- social posting
- accepting refund/settlement terms
- sending emotionally sensitive emails
- legal/financial commitments
- anything involving irreversible purchases/submissions

### Safer pattern

For tasks like airline refunds, the assistant should initially:

1. gather facts
2. identify the correct policy/path
3. draft the message or prefill the form
4. ask for approval
5. submit only after approval
6. track the open loop until resolved

That is useful without being reckless.

---

## Extra high-value use cases worth adding later

These are the kinds of operations that usually pay off fast:

### Client relationship intelligence
- "Who have I ignored too long?"
- "Which warm contacts should I follow up with this week?"
- "Summarize every open promise I've made."

### Proposal leverage
- "Find three old projects relevant to this new lead."
- "Turn my old work into a case-study angle."
- "Draft a lighter paid discovery offer instead of a full build."

### Content consistency
- "Turn my last three meetings into post ideas."
- "Find strong opinions I've repeated often enough to become content pillars."
- "Reuse this client story without leaking anything sensitive."

### Admin reduction
- "Prepare the email I need to send to chase payment."
- "Summarize this contract in plain English and flag weird clauses."
- "What deadlines or follow-ups are silently rotting?"

### Personal operator support
- "Given my week, what should I actually focus on?"
- "What have I started but not closed?"
- "What recurring annoying tasks should we automate next?"

---

## Plugin/tool checklist for the managed OpenClaw instance

## Required or highly desirable inside OpenClaw

- **Lossless Claw** (`lossless-claw`) if the managed offering supports it
- **Cron/reminders**
- **Subagents or session spawning** for research/deep work
- **Web fetch / web research capability**
- **Image generation**
- **Notion integration** (native skill, API bridge, or external integration path)

## Optional but powerful

- browser automation
- webhook intake support
- external MCP/API bridge support
- speech/TTS (only if the user actually wants voice mode)

## If plugin install is limited

Then the fallback is:

- keep OpenClaw very simple
- let it call only stable built-in capabilities
- move custom integration logic into the external bridge layer

That is the cleanest managed-instance strategy.

---

## External services to plan for

## 1. Hindsight

**Recommendation:** managed/external first.

Role:

- durable factual memory
- retrieval over emails/projects/threads/history

## 2. Notion

Role:

- human review surface
- CRM-lite
- content calendar
- proposals and tasks

## 3. Email bridge

Role:

- receive/provider-sync emails
- normalize content
- push into Hindsight + Notion

## 4. Search/research layer

Role:

- company research
- market research
- competitor/context gathering

## 5. Image generation provider

Role:

- social image drafts
- rough creative mockups

## 6. Optional posting/scheduling bridge

Role:

- queue approved social posts
- avoid one-off custom posting code per platform

## 7. Optional browser automation runner

Role:

- claims, forms, admin portals, customer support flows
- only after approval patterns are solid

---

## Data design recommendation

## Hindsight: start simple

Start with **one main memory bank** plus disciplined tagging, unless privacy or business separation clearly requires more.

Suggested tag families:

- `email`
- `client`
- `partner`
- `lead`
- `proposal`
- `project`
- `social`
- `ops`
- `travel`
- `finance`
- `personal`
- `business`

Suggested metadata fields:

- entity/person
- company
- source system
- timestamp
- source URL / message ID / page ID
- confidence or ingestion mode

## Notion: store outputs, not every raw artifact

Notion should store:

- curated summaries
- generated drafts
- opportunity records
- action plans
- content pipeline entries

Notion should **not** be the dumping ground for every raw email body or transcript chunk unless there is a strong reason.

---

## Guardrails

These matter. A lot.

## 1. Approval-first external actions

The assistant should default to:

- **drafting first**
- **asking before sending/posting/submitting**

Especially for:

- emails
- social posts
- refund claims
- support conversations
- anything with money or reputation attached

## 2. Source-aware answers

When answering "what happened before?", the agent should preserve links to sources.

It should know whether a claim came from:

- email
- prior chat
- Notion note
- meeting summary
- external research

## 3. Exactness rule

When exact wording, dates, promises, or commitments matter, the assistant should retrieve the source artifact instead of bluffing from a summary.

## 4. Personal vs business separation

If this assistant will eventually handle both personal and client work, define separation rules early.

Minimum requirement:

- tag private vs business artifacts clearly
- avoid accidental cross-contamination in answers

## 5. No duplicate "truth systems" without a reason

Do not let:

- OpenClaw thread memory
- Hindsight
- Notion
- the external bridge cache

all become partial, conflicting records of the same thing.

Pick the purpose of each layer and stick to it.

---

## The recommended build order

If we are building this for him, I would do it in this order:

### Step 1 - Foundation
- define the persona/instructions
- confirm available plugins/tools on managed OpenClaw
- connect Notion
- confirm image generation/search availability

### Step 2 - External memory
- provision Hindsight externally
- define tag/metadata scheme
- test retrieval on a few sample histories

### Step 3 - Email ingestion
- build the external email bridge
- normalize messages into Hindsight
- sync key entities/opportunities into Notion

### Step 4 - Proposal workflow
- implement research → retrieval → Notion draft flow
- test on one real-ish lead

### Step 5 - Social drafts
- implement content brief → post draft → image concept → approval queue

### Step 6 - Semi-agentic ops
- implement approval-gated admin/support workflows
- add reminders/follow-up tracking

That order gets value early and avoids glamorous nonsense before the memory layer is trustworthy.

---

## Rough effort estimate

Assuming we are building a sane v1, not a science project:

- **Foundation + operating contract:** 0.5-1 day
- **Hindsight integration design + testing:** 1 day
- **Email bridge + memory ingestion:** 1-2 days
- **Notion schema + proposal generation flow:** 1 day
- **Social draft flow:** 0.5-1 day
- **Ops/browser-assisted workflows:** 1-2 days depending on scope

Total realistic first pass:

- **4-7 working days** for a solid v1

That assumes we stay disciplined and don't try to automate every edge case immediately.

---

## Recommended final product shape

By the end of v1, the friend's assistant should feel like this:

### It should be strong at

- recalling people, threads, and context
- writing usable drafts
- preparing proposals and next steps
- turning messy info into structured Notion outputs
- keeping track of follow-ups and open loops

### It should be careful about

- sending anything external
- posting publicly
- negotiating or submitting on the user's behalf without approval

### It should not try to be yet

- a fully autonomous operator
- a full CRM replacement
- a magical browser bot with no supervision
- a self-hosted infrastructure monument

---

## Why this roadmap is the right one

Because it matches the reality of the setup.

He does **not** need an impressive architecture diagram.
He needs an assistant that can:

- remember people and history
- prepare business outputs
- reduce daily drag
- stay trustworthy

The shortest path to that is:

- managed OpenClaw
- external Hindsight
- Notion as review surface
- small external bridge for ingress/egress
- approval-gated operations

That's the version I'd actually build.

---

## Agent handoff brief

If we want to hand one compact brief to his future agent, use this:

> You are a business operator assistant running on a managed OpenClaw instance.
>
> Your job is to help the user remember context, draft outputs, research opportunities, and reduce operational friction.
>
> Operating rules:
> 1. Use OpenClaw/lossless memory for the current conversation only.
> 2. Use Hindsight as the primary long-term factual memory across emails, projects, clients, and prior work.
> 3. Use Notion as the human-facing workspace for proposals, content drafts, CRM-lite records, tasks, and review queues.
> 4. When answering questions about a person/company/thread, retrieve relevant history first, then summarize: who they are, what happened before, open loops, and recommended next actions.
> 5. When exact promises, dates, or wording matter, prefer the original source over a summary.
> 6. For social content, generate drafts and image concepts first. Do not post without approval.
> 7. For proposals, combine external research with prior relevant work and write the result into Notion in review state.
> 8. For operational tasks (refunds, support, admin), gather facts, prepare the action, and ask before any irreversible or external submission.
> 9. Keep personal and business context clearly separated.
> 10. Be useful, structured, and fast - but not reckless.

---

## Open questions before implementation

Before building, we still need a few decisions:

1. Which email provider will he use?
2. Which social platforms matter first?
3. Does he already use Notion seriously, or are we also designing the workspace?
4. Is Hindsight Cloud acceptable, or does he want self-hosted later?
5. Does he want the assistant to handle only business, or mixed business + personal ops?
6. Which actions should always require approval, no exceptions?
7. Does the managed OpenClaw plan support plugin install/config for `lossless-claw`?

---

## Bottom line

**Build a lean managed-instance assistant, not a mini data center.**

If we keep the boundaries clean:

- OpenClaw = runtime
- Hindsight = long-term factual memory
- Notion = structured outputs
- external bridge = integrations

then this can become genuinely useful fast.

---

## Companion files in this repo

### `MEMORY_STRATEGY.md`
Use this when the conversation turns into "why this memory architecture?" or "why Hindsight here instead of something else?"

### `IMPLEMENTATION_CHECKLIST.md`
Use this as the build sequence. It turns the roadmap into a practical execution plan.

### `OPEN_QUESTIONS.md`
Use this with your friend to collect the missing decisions before implementation drifts.

### `AGENT_BRIEF.md`
Use this as the seed brief/system prompt draft for the assistant itself.
