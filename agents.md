# Documentation

Developer and user documentation site for Freeshard, published at docs.freeshard.net. Built with MkDocs and the Material theme.

## Tech Stack

- **Generator**: MkDocs with Material theme
- **Plugins**: blog, glightbox (image lightbox)
- **Markdown extensions**: admonitions, details, syntax highlighting, Mermaid diagrams, emoji, markdown-include
- **Dependencies**: `requirements.txt` (mkdocs, mkdocs-material, markdown-include, mkdocs-glightbox)

## Commands

```bash
pip install -r requirements.txt   # Install dependencies
mkdocs serve                      # Dev server on localhost:8000
mkdocs build                      # Generate static site to public/
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
  blog/
    posts/                 Blog posts (date-prefixed directories)
      YYYY-MM-DD_slug/       Each post: main.md + images
    .authors.yml           Blog author metadata
  css/extra.css          Custom styles
  img/                   Shared images (logo)
mkdocs.yml               Site config, navigation, theme, plugins
```

## Conventions

### Navigation
Navigation is explicitly defined in `mkdocs.yml` under the `nav` key. Four top-level sections: Overview, Developer Docs, Blog, User Guides. Adding a new page requires adding it to `nav`.

### Blog Posts
Blog posts live in `docs/blog/posts/YYYY-MM-DD_slug/main.md`. Each post directory contains the markdown file and any associated images. Authors are defined in `docs/blog/.authors.yml`.

### Markdown Includes
Reusable snippets in `docs/developer_docs/includes/` can be included in other docs via the `markdown-include` extension: `{!developer_docs/includes/snippet.md!}`.

### Images
Store images alongside the content that uses them (in subdirectory `img/` or in blog post directories). Use relative paths. The glightbox plugin automatically adds lightbox behavior to images.

### Mermaid Diagrams
Supported via `pymdownx.superfences` custom fence. Use ` ```mermaid ` code blocks.

## Deployment

Built and deployed via GitLab Pages. The `site_dir` is `public/` (GitLab Pages convention). Site URL: `https://docs.freeshard.net`.
