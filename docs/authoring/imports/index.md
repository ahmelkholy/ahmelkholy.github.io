---
title: Importing static documentation
---
This website supports both native Markdown and prebuilt static documentation. This page explains the publishing mechanism; it does not imply that any engineering project already has a manual.

## Native Markdown

Create `docs/my-project/index.md` and write Markdown with a title in front matter. Add pages such as `docs/my-project/setup/index.md`. Link from the index with `[Setup](setup/)`, and back with `[Overview](../)`.

Add the project to the [documentation index](/docs/). Each project can have its own small navigation include or links in Markdown.

## Imported HTML

Build your public documentation locally with Documenter.jl, MkDocs or another static generator. Configure its public URL to `https://ahmelkholy.github.io/docs/my-project/` and verify that its assets use relative links or that exact prefix.

Copy only the generated public output into `static-docs/my-project/`. Commit it alongside the site. The Jekyll post-write hook copies that directory byte-for-byte to `_site/docs/my-project/` **after** Jekyll finishes. Liquid and front matter in imported files are not interpreted. Underscore-prefixed assets are preserved.

Do not also create a native `docs/my-project/` directory: the build rejects collisions. Symlinks and hidden files are rejected. Use another project name to keep the two forms separate.

The deployment workflow never fetches another repository. Private sources, notebooks with private data, credentials and local evidence must not be included in the generated output.

## Preview and verify

Run `bundle exec jekyll build`, then `python3 scripts/check_site.py`. For a live preview, run `bundle exec jekyll serve`; restart it after replacing an imported bundle because that input directory is excluded from Jekyll’s file watcher.

[Open the working static example](/docs/static-example/) or [return to authoring](../).
