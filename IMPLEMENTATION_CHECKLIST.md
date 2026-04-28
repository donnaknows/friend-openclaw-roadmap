# Implementation Checklist

## Step-by-step build sequence

Follow these in order. Do not skip ahead.

### Step 1: Audit the managed instance
- [ ] Confirm plugin install capability
- [ ] Confirm `lossless-claw` availability
- [ ] Confirm image generation availability
- [ ] Confirm web research/fetch availability
- [ ] Confirm cron/reminders availability
- [ ] Confirm Notion integration path
- [ ] Confirm secrets/API key configuration method
- [ ] Write capability table (available / unavailable / uncertain / must-externalize)

### Step 2: Set up assistant persona
- [ ] Define assistant role and name
- [ ] Define tone and communication style
- [ ] Define approval policy for all external actions
- [ ] Define business-only vs mixed scope
- [ ] Define uncertainty behavior
- [ ] Write system prompt / operating rules

### Step 3: Run onboarding interview
- [ ] Interview user: identity and business
- [ ] Interview user: communication style preferences
- [ ] Interview user: client/relationship seed list
- [ ] Interview user: tools and workflow
- [ ] Interview user: boundaries and safety rules
- [ ] Interview user: aspirations and priorities
- [ ] Store profile in long-term memory
- [ ] Create Notion user profile page
- [ ] Confirm understanding with user

### Step 4: Set up long-term memory
- [ ] Choose Hindsight Cloud vs self-hosted
- [ ] Create memory bank / project
- [ ] Define metadata schema (source type, person, company, topic, date, privacy)
- [ ] Ingest 3-5 test artifacts
- [ ] Test retrieval on a real prompt

### Step 5: Set up Notion workspace
- [ ] Confirm existing workspace or create new
- [ ] Create Companies database
- [ ] Create Contacts database
- [ ] Create Opportunities database
- [ ] Create Proposals database
- [ ] Create Tasks/Follow-ups database
- [ ] Create Content Drafts database
- [ ] Define review statuses
- [ ] Create proposal template
- [ ] Create social content draft template

### Step 6: Set up email ingestion
- [ ] Choose email source (Gmail / AgentMail / other)
- [ ] Build or configure external ingestion bridge
- [ ] Normalize email content (subject, sender, thread, body, timestamps)
- [ ] Write ingested emails into memory with metadata
- [ ] Define proactive notification vs on-demand rules
- [ ] Test end-to-end: email arrives → retrievable later

### Step 7: Build research + proposal workflow
- [ ] Confirm research path (native web search or external)
- [ ] Define proposal template structure
- [ ] Test: “Research this prospect and draft a Notion proposal”
- [ ] Verify retrieval of relevant past work before drafting
- [ ] Verify output stays in review state, never auto-sent

### Step 8: Build social content workflow
- [ ] Define content brief structure
- [ ] Define post generation prompt pattern
- [ ] Confirm image generation provider
- [ ] Test: “Create a LinkedIn post about X for client Y”
- [ ] Verify: 2-3 angles, recommended draft, image concept, review state in Notion

### Step 9: Build ops assistant flows
- [ ] Define approval gates for each ops workflow
- [ ] Test one travel/support use case end-to-end
- [ ] Test: draft refund request → pause for approval
- [ ] Add follow-up reminder tracking

### Step 10: Acceptance testing
- [ ] Relationship recall: “Who is this person and what happened before?”
- [ ] Proposal: “Research and draft a proposal for new client X”
- [ ] Social: “Write a LinkedIn post about X”
- [ ] Ops: “Airline canceled my flight — help”
- [ ] Safety: assistant asks before all external actions
- [ ] Safety: assistant shows uncertainty when history is incomplete

---

## Goal

Build a **lean managed-instance business operator assistant** for a non-technical user.

The assistant should be good at:

- relationship/context recall
- email and lead recap
- proposal drafting
- social post drafting
- operational/admin assistance

The assistant should **not** try to be a fully autonomous operator in v1.

---

## V1 principles

- Keep the **managed OpenClaw instance lean**
- Push heavy integrations and long-term memory **outside** the instance
- Default to **draft first, ask before external action**
- Use **Notion as the review surface**, not as raw memory storage
- Prefer **retrieval before synthesis** when history matters
- Avoid building around terminal access that does not exist

---

## Phase 0 — Managed instance audit

### Objective

Confirm what the managed OpenClaw instance can actually do before designing around imaginary capabilities.

### Checklist

- [ ] Confirm whether plugin install/config is available at all
- [ ] Confirm whether `lossless-claw` can be enabled
- [ ] Confirm whether image generation is available
- [ ] Confirm whether web research / fetch is available
- [ ] Confirm whether reminders/cron are available
- [ ] Confirm whether subagents/session spawning are available
- [ ] Confirm whether any browser automation capability exists
- [ ] Confirm whether there is a native or practical Notion integration path
- [ ] Confirm how secrets/API keys are configured on the managed instance
- [ ] Confirm whether webhooks can target the instance directly, or only an external bridge

### Done when

You have a written table of:

- available capabilities
- unavailable capabilities
- uncertain capabilities
- what must be moved to external support

---

## Phase 0.5 — Onboarding interview

### Objective

The assistant interviews the user to learn who they are, what they do, and how they work.

This is the foundation for everything else. Without it, the assistant is generic.

### Checklist

#### A. Identity and business
- [ ] What do you do, in your own words?
- [ ] What is your business? Freelance, agency, product, consulting?
- [ ] What services or products do you sell?
- [ ] Who are your typical clients?
- [ ] What does a great client relationship look like?
- [ ] What does a bad one look like?

#### B. Communication style
- [ ] How do you normally talk to clients? Formal, casual, direct?
- [ ] What tone should the assistant use when drafting on your behalf?
- [ ] Language preferences? Italian, English, both?
- [ ] Any brands or people whose communication style you admire?

#### C. Clients and relationships
- [ ] Top 5-10 current or recent clients (name, company, what they need)
- [ ] Important past clients worth remembering
- [ ] People you want to reconnect with
- [ ] People or companies you want to avoid

#### D. Tools and workflow
- [ ] Where do you track tasks and projects today?
- [ ] Do you use Notion already? How?
- [ ] What email system do you use?
- [ ] What social platforms matter?
- [ ] Where do your leads come from?

#### E. Boundaries and safety
- [ ] What should the assistant never do without asking?
- [ ] What should the assistant never do at all?
- [ ] Anything private the assistant should not store or reference?
- [ ] How do you want to handle mistakes?

#### F. Aspirations and direction
- [ ] What does success look like in 3 months?
- [ ] Single most annoying thing you want the assistant to handle?
- [ ] Specific workflow where the assistant would save the most time?

### Interview behavior rules

1. **Conversational, not interrogative.** A few questions at a time, not all 30 at once.
2. **Write everything down.** Store answers in Hindsight and create a Notion user profile page.
3. **Confirm understanding.** Paraphrase back, let the user correct.
4. **Do not rush.** 2-3 short sessions are better than one exhausting one.
5. **Offer to skip.** If the user does not want to answer, note it and move on.

### Output of this phase

- [ ] User profile stored in long-term memory (identity, business, style, boundaries)
- [ ] Notion page with user profile summary
- [ ] Client/contact seed list (even partial)
- [ ] Tone/communication style guide
- [ ] Explicit approval policy tailored to this user
- [ ] List of "never do" actions
- [ ] Prioritized list of workflows to build first

### Done when

The assistant can answer "What does this user care about, how do they work, and what should I never do?" without guessing.

---

## Phase 1 — Foundation and persona

### Objective

Make the assistant coherent, safe, and pleasant before adding automation.

### Checklist

- [ ] Define the assistant role: business operator / chief-of-staff / Donna-style aide
- [ ] Define tone and communication style
- [ ] Define approval policy for outbound or irreversible actions
- [ ] Define business-only vs business+personal scope
- [ ] Define what counts as a “must ask first” action
- [ ] Define default output formats for common tasks (recaps, proposals, content drafts)
- [ ] Define uncertainty behavior: retrieve sources first when dates/commitments matter

### Deliverables

- [ ] Final agent brief
- [ ] Initial operating rules / system prompt
- [ ] Approval rules list

### Done when

The assistant can answer basic requests consistently and safely without any external automation yet.

---

## Phase 0.5 — Onboarding interview

### Objective

The assistant interviews the user to learn who they are, what they do, and how they work.

This is the foundation for everything else — memory, proposals, social content, relationship recall. Without it, the assistant is generic.

### Checklist

#### A. Identity and business
- [ ] What do you do, in your own words?
- [ ] What is your business? Freelance, agency, product, consulting?
- [ ] What services or products do you sell?
- [ ] Who are your typical clients?
- [ ] What does a great client relationship look like?
- [ ] What does a bad one look like?

#### B. Communication style
- [ ] How do you normally talk to clients? Formal, casual, direct?
- [ ] What tone should the assistant use when drafting on your behalf?
- [ ] Language preferences? Italian, English, both?
- [ ] Any brands or people whose communication style you admire?

#### C. Clients and relationships
- [ ] Top 5-10 current or recent clients (name, company, what they need)
- [ ] Important past clients worth remembering
- [ ] People you want to reconnect with
- [ ] People or companies you want to avoid

#### D. Tools and workflow
- [ ] Where do you track tasks and projects today?
- [ ] Do you use Notion already? How?
- [ ] What email system do you use?
- [ ] What social platforms matter?
- [ ] Where do your leads come from?

#### E. Boundaries and safety
- [ ] What should the assistant never do without asking?
- [ ] What should the assistant never do at all?
- [ ] Anything private the assistant should not store or reference?
- [ ] How do you want to handle mistakes?

#### F. Aspirations and direction
- [ ] What does success look like in 3 months?
- [ ] Single most annoying thing you want the assistant to handle?
- [ ] Specific workflow where the assistant would save the most time?

### Interview behavior rules

1. **Conversational, not interrogative.** A few questions at a time, not all 30 at once.
2. **Write everything down.** Store answers in Hindsight and create a Notion user profile page.
3. **Confirm understanding.** Paraphrase back, let the user correct.
4. **Do not rush.** 2-3 short sessions are better than one exhausting one.
5. **Offer to skip.** If the user does not want to answer, note it and move on.

### Output of this phase

- [ ] User profile stored in Hindsight (identity, business, style, boundaries)
- [ ] Notion page with user profile summary
- [ ] Client/contact seed list (even partial)
- [ ] Tone/communication style guide
- [ ] Explicit approval policy tailored to this user
- [ ] List of "never do" actions
- [ ] Prioritized list of workflows to build first

### Done when

The assistant can answer "What does this user care about, how do they work, and what should I never do?" without guessing.

---

## Phase 2 — Long-term memory setup

### Objective

Give the assistant durable recall across emails, people, projects, and historical context.

### Recommendation

Use **Hindsight externally** as the primary long-term factual memory.

### Checklist

- [ ] Decide between Hindsight Cloud vs self-hosted Hindsight on separate infrastructure
- [ ] Create one initial memory bank for the user
- [ ] Define metadata/tagging strategy
- [ ] Define source types: `email`, `chat`, `notion`, `meeting`, `manual-note`, `research`
- [ ] Define business/private tags if mixed scope is allowed
- [ ] Test ingestion of 3-5 sample artifacts
- [ ] Test retrieval on a real “who is this / what happened before?” prompt

### Minimum metadata to store

- source type
- person/entity
- company/client
- topic/project
- timestamp
- canonical source ID / URL
- privacy scope

### Done when

The assistant can answer a prompt like:

> “Who is this person, what happened before, and what should I do next?”

with a useful, source-aware answer.

---

## Phase 3 — Notion workspace

### Objective

Give the assistant a structured, human-reviewable output surface.

### Checklist

- [ ] Confirm whether the user already has a serious Notion workspace
- [ ] If not, create a simple starter workspace
- [ ] Create or confirm these databases:
  - [ ] Companies
  - [ ] Contacts
  - [ ] Opportunities
  - [ ] Proposals
  - [ ] Tasks / Follow-ups
  - [ ] Content Drafts
- [ ] Define review statuses
- [ ] Define one proposal template
- [ ] Define one social content draft template

### Design rule

Notion stores **curated outputs**, not every raw artifact.

### Done when

The assistant can create a usable proposal draft or content draft in Notion without manual cleanup.

---

## Phase 4 — Email ingestion

### Objective

Bring email context into the memory layer without creating a disconnected shadow assistant.

### Architecture rule

Use an **external bridge**, not the managed instance itself.

### Checklist

- [ ] Choose email source: Gmail, AgentMail, other
- [ ] Build or configure external ingestion bridge
- [ ] Normalize subject, sender, thread context, body, and timestamps
- [ ] Write ingested email artifacts into Hindsight with metadata
- [ ] Optionally update matching contact/company/opportunity records in Notion
- [ ] Define rules for when OpenClaw should be proactively notified vs retrieve on demand
- [ ] Mark or track ingestion state to avoid duplicates

### Important guardrail

- [ ] Do **not** let inbound email webhooks make autonomous decisions outside the main assistant context

### Done when

A new email thread is retrievable later in a prompt like:

> “This client resurfaced after two months. What do they want?”

---

## Phase 5 — Research + proposal workflow

### Objective

Turn memory + external research into commercial output.

### Checklist

- [ ] Confirm research path inside OpenClaw (native web fetch/search or external research support)
- [ ] Define proposal structure template
- [ ] Define retrieval step for relevant past work before drafting
- [ ] Define Notion page creation flow
- [ ] Keep final output in review state, never auto-send
- [ ] Test on one realistic prospect/client scenario

### Acceptance prompt

> “New client X came to me for Y. Research the market, cross it with my past work, and prepare a Notion proposal draft.”

### Done when

The assistant creates a real Notion draft with:

- context summary
- problem framing
- recommended offer
- assumptions
- risks
- next questions

---

## Phase 6 — Social content studio

### Objective

Help the user or client generate social content consistently.

### Checklist

- [ ] Define content brief structure
- [ ] Define post generation prompt pattern
- [ ] Define visual concept generation pattern
- [ ] Confirm image generation provider availability
- [ ] Create Notion content draft template
- [ ] Decide whether v1 is draft-only or includes scheduling support

### Recommendation

V1 should be **draft-only**.

### Acceptance prompt

> “For client X, create a post on topic Y.”

### Done when

The assistant outputs:

- 2-3 angles
- 1 final recommended draft
- image concept
- generated image or generation prompt
- CTA/platform notes
- review status in Notion

---

## Phase 7 — Operational assistant

### Objective

Reduce annoying repetitive work without giving the assistant reckless autonomy.

### First candidates

- [ ] lead follow-up reminders
- [ ] invoice/payment reminder drafting
- [ ] inbox triage
- [ ] travel disruption triage
- [ ] refund/support draft preparation
- [ ] post-meeting action extraction
- [ ] task/follow-up generation

### Checklist

- [ ] Define approval gates clearly
- [ ] Define which actions are draft-only
- [ ] Define which actions may submit after approval
- [ ] Add reminders/open-loop tracking
- [ ] Test one travel/support use case end to end

### Done when

The assistant can gather facts, prepare the action, and stop for approval before external submission.

---

## External services checklist

### Must-have external support

- [ ] Long-term memory service (preferred: Hindsight external)
- [ ] Notion
- [ ] Email bridge
- [ ] Search/research support
- [ ] Image generation provider

### Nice-to-have later

- [ ] Social scheduler/posting bridge
- [ ] Browser automation runner
- [ ] Meeting transcript ingestion

---

## Acceptance test pack

Use these prompts as the real test suite.

### Relationship recall
- [ ] “Who is this guy and what happened before?”
- [ ] “Summarize the last meaningful interactions with this client.”
- [ ] “What open loops do I still have with them?”

### Proposal drafting
- [ ] “Research this prospect and prepare a Notion proposal draft.”
- [ ] “Find related past work and use it in the proposal.”

### Social drafting
- [ ] “Write a LinkedIn post about X for client Y.”
- [ ] “Give me three hook options and an image concept.”

### Ops assistant
- [ ] “This airline canceled my flight — what should I do?”
- [ ] “Draft the refund/support request but don’t send it yet.”

### Safety/guardrails
- [ ] Assistant asks before sending any email/post/submission
- [ ] Assistant shows uncertainty when history is incomplete
- [ ] Assistant separates private and business information correctly

---

## Default build order

1. Managed instance audit
2. Persona + operating rules
3. Hindsight setup
4. Notion structure
5. Email ingestion
6. Research/proposal workflow
7. Social drafts
8. Operational assistant flows

---

## Suggested milestone definition

### Milestone A — useful assistant
- can answer coherently
- can research
- can draft
- can write to Notion

### Milestone B — remembers context
- durable recall works
- email ingestion works
- people/company recap works

### Milestone C — real business leverage
- proposal drafting works
- social drafts work
- follow-up tracking works

### Milestone D — semi-agentic ops
- support/admin workflows work with approval gates

---

## Things to explicitly avoid in v1

- full autonomous posting
- full autonomous customer support negotiation
- stuffing raw history into Notion
- trying to self-host memory on the managed OpenClaw instance
- building around terminal/systemd assumptions
- multi-agent sprawl before the first assistant is already good

---

## Final go/no-go check

Before you call v1 done, all of these should be true:

- [ ] The assistant is coherent
- [ ] The assistant remembers key context through Hindsight
- [ ] The assistant can create useful drafts in Notion
- [ ] The assistant can draft social content and image concepts
- [ ] The assistant asks before external action
- [ ] The assistant can help with at least one annoying ops workflow
- [ ] The architecture does not depend on terminal access on the managed instance
