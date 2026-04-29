# friend-openclaw-roadmap

Build guide for a business operator assistant on a managed OpenClaw instance (Kiloclaw).

## Start here

👉 **[ROADMAP.md](ROADMAP.md)** — step-by-step build guide written for the agent to follow.

## Architecture

- **Kiloclaw** (managed OpenClaw) = runtime, chat, orchestration
- **Remnic** = preferred memory layer
- **Gmail** via Kiloclaw built-in integration = email
- **Notion** = proposals, content drafts, CRM — adapts to the user's existing workspace
- **Example Notion skill** = a generic starting point that should be adapted to the user's real workflow

## Principles

1. Adapt to the user. Don't force a structure on them.
2. Draft first, ask before external action.
3. Retrieve before summarizing when history matters.
4. Keep the stack simple at first. Don't add more memory systems unless a real gap appears.
5. This is a starting point, not a rigid script — let the user steer.
