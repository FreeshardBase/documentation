---
name: generate-digest
description: Regenerate digest.md, the AI-optimized digest of the Freeshard developer docs. Run this manually as part of a docs release so downstream tools (e.g. the app-repository add-app skill) can fetch an authoritative digest instead of crawling the docs site.
---

# Generate the docs digest

`digest.md` (repo root) is the authoritative, AI-optimized summary of this
documentation site. Downstream skills — notably the `add-app` skill in the
app-repository — fetch it instead of crawling `docs.freeshard.net`. This skill
regenerates it from the current contents of `docs/`.

Run it **manually during a docs release** (or whenever the developer docs change
materially). It is not wired into CI.

## What the digest is for

The reader is an AI coding agent helping a developer build and submit a
Freeshard app. The digest must let that agent write a correct
`docker-compose.yml.template` and `app_meta.json` without reading the full site.
Optimize for information density, not prose:

- Keep every code block, table, variable name, path, and JSON/YAML example
  verbatim — these are the load-bearing facts.
- Drop marketing copy, screenshots, image references, and repeated narrative.
- Prefer terse bullets and tables over paragraphs.
- Resolve `markdown-include` directives (`{!developer_docs/includes/...!}`) by
  inlining the included snippet's content.

## Source material

Generate the digest primarily from the developer docs, with a short product
framing from the overview:

- `docs/developer_docs/*.md` (overview, docker_compose_template, app_meta_json,
  persisting, routing_and_ac, internal_services, peering, events, lifecycle,
  custom_apps, submitting, revenue_share, existing_apps) — the core.
- `docs/developer_docs/includes/*.md` — inline these where referenced.
- `docs/overview/index.md` and `docs/overview/concepts/*.md` — a brief
  "what Freeshard is" section only.

Note that some features are flagged `status: upcoming` / `status: disabled`
(events, peering, inter-app APIs, revenue-share manual adjustment) — keep the
flag so the reader does not build against unavailable features.

## Steps

1. Read the source files listed above.
2. Rewrite the existing `digest.md` from scratch following the structure of the
   current file (top metadata block, then sections mirroring the docs). Preserve
   the heading layout where possible so diffs stay reviewable.
3. Update the `Generated:` date at the top of `digest.md` to today's date and
   set `Source:` to this repository.
4. Keep it compact — aim for a single file that an agent can read in one pass
   (roughly a few hundred lines). If it grows much larger, you are including too
   much prose.
5. Review the diff before committing to confirm no developer-facing fact was
   dropped.
