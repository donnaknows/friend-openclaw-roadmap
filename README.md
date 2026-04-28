# friend-openclaw-roadmap

Build guide for a business operator assistant on a managed OpenClaw instance.

## Start here

👉 **[ROADMAP.md](ROADMAP.md)** — the complete step-by-step build guide.

Written for the agent itself to follow. 10 steps, in order, with verification checklists and reference links.

## Architecture

- **Managed OpenClaw** (Kiloclaw) = runtime, chat, orchestration
- **Lossless Claw** = conversation recall (mandatory)
- **Gmail** via Kiloclaw built-in integration = email
- **Notion** = proposals, content drafts, CRM-lite, review surface
- **Hindsight** (later) = external long-term memory when session recall isn't enough

## Principles

1. Keep the instance lean. Heavy stuff goes outside.
2. Draft first, ask before external action.
3. Retrieve before summarizing when history matters.
4. Notion stores curated outputs, not raw memory dumps.
5. Do not skip steps. Do not guess.
