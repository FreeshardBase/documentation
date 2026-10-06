# Documentation

Developer and user documentation site for Freeshard, published at docs.freeshard.net. Built with MkDocs and the Material theme.

## Tech Stack

- **Generator**: MkDocs with Material theme
- **Plugins**: glightbox (image lightbox)
- **Markdown extensions**: admonitions, details, syntax highlighting, Mermaid diagrams, emoji, markdown-include
- **Dependencies**: `requirements.txt` (mkdocs, mkdocs-material, markdown-include, mkdocs-glightbox), pinned to exact versions — MkDocs 1.x is unmaintained and MkDocs 2.0 is not a viable upgrade (no plugin system, no Material support). Do not bump these; the migration target is Zensical, tracked in [issue #10](https://github.com/FreeshardBase/documentation/issues/10). That was blocked on the Material `blog` plugin, which Zensical does not implement; the blog has since moved to freeshard.net ([issue #4](https://github.com/FreeshardBase/documentation/issues/4)) and the plugin is gone, so #10 is unblocked.

## Commands

Environment is managed with **uv** (no `pyproject.toml`; deps live in `requirements.txt`).

```bash
uv venv                            # Create .venv (once)
uv pip install -r requirements.txt # Install dependencies
uv run mkdocs serve                # Dev server on localhost:8000
uv run mkdocs build                # Generate static site to public/
```

## Structure

```
docs/
  overview/              Product overview and concepts
    concepts/              Single-user isolation, devices, apps
  developer_docs/        Developer documentation for app creators
    includes/              Reusable markdown snippets (template vars, portal name info)
    img/                   Developer docs images
  user_guides/           End-user guides (password management, smart home)
  blog/                  Only redirect stubs now — see Retired Blog below
  css/extra.css          Custom styles
  img/                   Shared images (logo)
mkdocs.yml               Site config, navigation, theme, plugins
```

## Conventions

### Navigation
Navigation is explicitly defined in `mkdocs.yml` under the `nav` key. Three top-level sections: Overview, Developer Docs, User Guides. Adding a new page requires adding it to `nav`.

### Retired Blog
The blog no longer lives here. It moved to `freeshard.net/<lang>/blog/`, as an Astro content collection in the `landing-page` repo — write new posts there, not here.

What remains under `docs/blog/` is 20 hand-written `index.html` redirect stubs, one per URL the Material `blog` plugin used to publish (13 posts, 5 archive years, `page/2/`, and the index). MkDocs copies non-markdown files through verbatim, so they land at exactly the old paths. Each stub is an instant `meta refresh` plus a `rel=canonical` and a visible link.

They are static HTML rather than a server-side 301 because `docs.freeshard.net` is served by GitHub Pages, which cannot issue arbitrary redirects. Google [documents](https://developers.google.com/search/docs/crawling-indexing/301-redirects) that it reads an instant `meta refresh` as a permanent redirect, while still recommending a server-side redirect where one is possible. Putting the site behind a proxy that can answer 301s is the upgrade path if the link equity ever proves to matter.

Do not delete these stubs, and do not let a generator swap drop them — they are the only thing standing between the old URLs and a 404.

### Markdown Includes
Reusable snippets in `docs/developer_docs/includes/` can be included in other docs via the `markdown-include` extension: `{!developer_docs/includes/snippet.md!}`.

### Images
Store images alongside the content that uses them (in a subdirectory `img/`). Use relative paths. The glightbox plugin automatically adds lightbox behavior to images.

### Mermaid Diagrams
Supported via `pymdownx.superfences` custom fence. Use ` ```mermaid ` code blocks.

## Deployment

Built and deployed via GitHub Pages (`.github/workflows/ci.yml`). Every push builds with `mkdocs build --strict`; pushes to `main` also deploy. The `site_dir` is `public/`. Site URL: `https://docs.freeshard.net`.

## Commits

[Scoped Commits](https://scopedcommits.com/): `<scope>: <description>`. The scope is the area of the tree the change touches, never a change type — write `user_guides: document the backup restore flow`, not `fix(user_guides): ...`. Body and trailers are optional; a change's reasoning belongs in the body, not in a code comment.

Scopes for this repo: `blog` `developer_docs` `user_guides` `overview` `theme` `ci` `meta`

`meta` covers repo-level files (agents.md, README, justfile). For a change spanning several scopes, use a broader one, list two comma-separated, or use `treewide`. Merges and reverts keep their own format. Don't generate a changelog from the commit log — release notes come from merged PRs.
