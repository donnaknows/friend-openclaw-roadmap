---
name: notion-skill
description: >
  Interact with a user's Notion workspace via the Notion REST API using the
  bundled notion-cli.py script. Use when querying, creating, or updating items
  in Notion databases, searching across the workspace, drafting proposals or
  content in Notion, or adapting an assistant to an existing Notion setup.
  Do not assume a fixed schema. Discover first, then write.
---

# Notion Workspace

Use this skill as a **starting point**, not as a final design.

Every Notion workspace is different. The assistant should adapt to the user's real structure instead of forcing a prebuilt system onto them.

## Golden rules

1. **Discover before write.** Run `discover` at the start of a Notion session and any time you're unsure of property names or allowed values.
2. **Don't hardcode schema.** Database names, select values, relations, and page structure vary by user.
3. **Search before create.** Check whether a page already exists before making a new one.
4. **Draft first.** Writing into Notion is usually safe, but external actions based on those notes still require approval.
5. **Prefer simple structure.** If the user already has a place for proposals, content, CRM notes, or research, use it.
6. **Create new databases only when needed.** Suggest structure; don't impose it.
7. **Never delete casually.** Archive or mark inactive unless the user explicitly wants deletion.

## CLI quick reference

Run the bundled script like this:

```bash
python3 <skill-dir>/scripts/notion-cli.py <command> [args]
```

Main commands:
- `discover` — list visible data sources and schemas
- `search <query>` — search pages or data sources
- `get-page <id>` — fetch a page
- `get-db <id>` — fetch database metadata
- `get-ds <id>` — fetch data-source metadata
- `query <data_source_id>` — query rows
- `create-page <data_source_id> --props JSON` — create a page
- `update-page <page_id> --props JSON` — update a page
- `archive-page <page_id>` — soft-delete/archive a page
- `get-blocks <id>` — get child blocks
- `append-blocks <page_id> --blocks JSON` — append structured content

## Practical workflow

### 1. Discover the workspace

Start by finding what already exists.

Questions to answer:
- Where should proposals go?
- Where should social drafts go?
- Where should client notes go?
- Is there already a CRM, project tracker, or content database?

### 2. Confirm output destination

Ask the user where things belong if it is not obvious.

Examples:
- "Where should I store client proposals?"
- "Do you want content drafts in a content calendar, a notes page, or a project database?"
- "Do you already track clients in Notion, or should I just append notes to an existing page?"

### 3. Write structured output

Use properties for metadata and blocks for longer content.

Typical pattern:
1. create/update the page record
2. append headings, bullets, checklists, or paragraphs as structured blocks

### 4. Keep this skill evolving

This example is intentionally generic.

As the assistant learns the user's workspace, update this skill or clone it into a user-specific version with:
- actual database names
- property mappings
- common output templates
- safer defaults for that workspace

Do not keep pretending the generic version knows the user's schema if it doesn't.

## Good fits for this skill

- proposal drafts
- client/company notes
- content drafts
- lightweight CRM updates
- research summaries
- meeting notes
- task or project updates

## References

- [Notion API Getting Started](https://developers.notion.com/docs/getting-started)
- [Notion API Reference](https://developers.notion.com/reference/intro)
- [Create a Notion integration](https://www.notion.so/my-integrations)
