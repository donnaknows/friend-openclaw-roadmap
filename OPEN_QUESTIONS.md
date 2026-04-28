# Open Questions

These are the decisions we still need from your friend before implementation gets too far.

---

## Must answer before build starts

### 1. What email system does he actually use?

Why it matters:

- decides the ingestion bridge
- decides webhook vs polling
- decides how easy threading/context will be

Answer options:

- Gmail
- Google Workspace
- AgentMail
- Outlook / Microsoft 365
- Other

### 2. Is Notion already part of his daily workflow?

Why it matters:

- changes whether we are integrating into an existing system or designing one from scratch
- affects how much of the project is “assistant setup” vs “workspace design”

Answer options:

- yes, serious existing workspace
- yes, but messy/light use
- no, build it from scratch

### 3. Which social platforms matter first?

Why it matters:

- changes draft format
- changes image sizes/angles/CTAs
- changes whether a scheduler bridge is worth building later

Answer options:

- LinkedIn
- X / Twitter
- Instagram
- Threads
- Facebook
- Other

### 4. Is the assistant business-only, or mixed business + personal ops?

Why it matters:

- changes privacy boundaries
- changes tagging rules
- changes how cautious the memory system should be

Answer options:

- business only
- business first, some personal ops
- mixed personal + business from day one

### 5. What actions must always require approval?

Why it matters:

- this is the real safety contract

Minimum suggested “always ask first” list:

- sending emails
- posting on social
- submitting support/refund requests
- agreeing to terms/settlements
- purchases/bookings
- anything financial or reputational

### 6. Can the managed OpenClaw plan install/configure plugins?

Why it matters:

- decides whether `lossless-claw` is available
- decides whether any native integrations are realistic
- changes how much must live in the external bridge layer

---

## Should answer before Phase 2

### 7. Is Hindsight Cloud acceptable, or does he want self-hosted later?

Why it matters:

- changes external support design
- changes operational complexity
- changes how fast we can get to value

Recommendation:

- start with managed/external first
- self-host only later if there is a clear privacy/cost/control reason

### 8. Does he want proactive reminders/follow-up nudges?

Why it matters:

- affects whether we build reminder/follow-up flows early
- affects cron/reminder tooling needs

Examples:

- “follow up with this lead in 5 days”
- “nudge me if this invoice is still unpaid next week”

### 9. Does he want the assistant to write directly into Notion, or draft in chat first?

Why it matters:

- some users want immediate structured output
- others want a preview before any write

Recommendation:

- write proposals/content drafts directly to Notion in review state
- still ask before anything external gets sent/published

### 10. What tone should the assistant have?

Why it matters:

- affects adoption more than people think
- especially important for social drafts and follow-up copy

Possible choices:

- direct / sharp
- warm / polished
- concise / businesslike
- more playful / founder energy

---

## Nice to answer later

### 11. Does he want meeting transcript ingestion?

If yes, this can become a strong source of:

- content ideas
- follow-up tasks
- proposal context
- memory enrichment

### 12. Does he want direct social posting later, or only drafting?

Recommendation:

- draft-only in v1
- revisit direct posting later

### 13. Does he want browser-assisted admin/support workflows?

Examples:

- refunds
- form prefills
- claim tracking
- support tickets

Recommendation:

- yes later, not day one

---

## Good defaults if he does not answer quickly

If we need to unblock the build, these are sensible defaults:

- Email: **use whatever inbox he already lives in**; don’t force a new one unless necessary
- Notion: **starter workspace if current one is messy/nonexistent**
- Social: **LinkedIn first**
- Scope: **business-first, light personal ops later**
- Safety: **all outbound actions require approval**
- Memory: **Hindsight external first**
- Posting: **draft-only v1**
- Browser automation: **defer to later**

---

## The real decision bottlenecks

If you only chase a few answers now, chase these first:

1. email provider
2. Notion existing vs greenfield
3. business-only vs mixed scope
4. approval rules
5. plugin availability on the managed OpenClaw plan

Those five decide most of the architecture.