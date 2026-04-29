# friend-openclaw-roadmap

Build guide for a business operator assistant on a managed OpenClaw instance (Kiloclaw).

## Start here

👉 **[ROADMAP.md](ROADMAP.md)** — step-by-step build guide written for the agent to follow.

## Architecture

- **Kiloclaw** (managed OpenClaw) = runtime, chat, orchestration
- **Lossless Claw** = conversation recall (mandatory)
- **Gmail** via Kiloclaw built-in integration = email
- **Notion** = proposals, content drafts, CRM — adapts to user's existing workspace
- **Hindsight** (later) = external long-term memory when session recall isn't enough

## Principles

1. Adapt to the user. Don't force a structure on them.
2. Draft first, ask before external action.
3. Retrieve before summarizing when history matters.
4. This is a starting point, not a rigid script — let the user steer.
