# friend-hermes-roadmap

Build guide for a business operator assistant on a Hermes deployment.

> Note: this repo started as an OpenClaw/Kiloclaw roadmap. The content is now being adapted for Hermes. I left the GitHub repo slug alone for the moment so existing links keep working; rename it later if you want a cleaner URL.

## Start here

👉 **[ROADMAP.md](ROADMAP.md)** — step-by-step build guide written for the agent to follow.

## Architecture

- **Hermes** = runtime, chat, orchestration
- **Remnic** = preferred memory layer
- **Email / Gmail path available in this Hermes deployment** = email context
- **Notion** = proposals, content drafts, CRM — adapts to the user's existing workspace
- **Example Notion skill** = a generic starting point that should be adapted to the user's real workflow

## Principles

1. Adapt to the user. Don't force a structure on them.
2. Draft first, ask before external action.
3. Retrieve before summarizing when history matters.
4. Keep the stack simple at first. Don't add more memory systems unless a real gap appears.
5. When Hermes-specific details vary by host, check the real deployment instead of assuming feature parity with the old OpenClaw/Kiloclaw setup.
