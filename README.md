# Write → save → push

This is your personal website. Write ordinary Markdown in VS Code; GitHub builds and publishes it automatically when you push to `master`.

## Start a post in VS Code

1. Press **Cmd+Shift+P** → **Tasks: Run Task** → **New post**.
2. Enter the title, a short URL name such as `transformer-notes`, and choose `en`, `ar` or `ru`.
3. The new Markdown file opens. Write below the `---` header and save.
4. When finished, use **Source Control → Commit → Sync Changes** (or commit and `git push origin master`).

That is the normal publishing workflow. **No local build is required.** GitHub generates the article page, writing index, tags, RSS and sitemap. Wait for the Pages workflow to finish before checking the live site.

Or create `_posts/YYYY-MM-DD-your-topic.md` yourself:

```markdown
---
title: "Your title — عنوان المقال"
date: 2026-10-28
lang: ar
tags: [engineering]
---

Write here in Arabic, English or Russian.
```

Use today's date. A future date stays unpublished until a build runs after that date. Type `post` and select the **Article front matter** snippet to insert the header automatically.

## Posts with figures

Keep the Markdown file and a `figs` folder together inside a topic folder:

```text
_posts/my-topic/2026-10-31-my-topic.md
_posts/my-topic/figs/figure-1.svg
```

In the Markdown file, use a relative image path and put the paper credit underneath:

```markdown
![Description of the figure](figs/figure-1.svg)

*Figure 1. Reproduced from Figure X in Author et al. (year),
[Paper title](https://doi.org/DOI), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
State any cropping or other changes here.*
```

Use the actual paper, figure number and reuse licence. Commit and push the **whole topic folder**. GitHub automatically adds the article to the Writing page, tags, RSS and sitemap, and publishes its referenced figures. SVG, PNG, JPEG, GIF, WebP, AVIF, ICO, TIFF and linked PDFs are supported. Missing local figures stop the build with the article name and missing path.

The Markdown filename still needs `YYYY-MM-DD-` at the beginning. Remove `published: false` when the article is ready. Existing flat posts also work: `_posts/2026-10-31-my-topic.md` can link to `my-topic/figs/figure-1.svg`. No manual image copying or edits to the article index are needed.

## Your writing folders

| Folder | Use |
|---|---|
| `_posts/` | Finished articles, optionally grouped into topic folders with `figs/`; these publish when pushed |
| `_talks/` | Talks, presentation notes and slide links; use the **New talk** task |
| `_drafts/` | Unfinished writing; not published |
| `images/` | Shared images; article-specific figures can stay beside their Markdown |
| `docs/` | Markdown project documentation |
| `_pages/` | About/CV, projects, contact and other site pages |
| `files/` | Public CV and other intended downloads |
| `static-docs/` | Optional imported project documentation |

Use **New draft** for unfinished writing. When ready, move the dated file into `_posts/` and commit/push it. A post does not need translations. For real translations, give them the same optional `translation_key`.

The VS Code Explorer hides technical files so writing stays prominent. They remain on disk; change `files.exclude` in workspace settings whenever you want to work on the theme. No extension is required.

## Optional local preview

Run **Tasks: Run Task → Preview website**, then open http://127.0.0.1:4000. If the preview is already running, just open that address. **Check website** runs the production build and link checks.

Terminal equivalents:

```sh
bash scripts/site preview
bash scripts/site check
```

Fresh-machine setup and detailed Markdown examples: [Author guide](maintenance/AUTHOR_GUIDE.md).

## Google discovery

Every push updates the crawlable HTML, canonical URLs and [sitemap](https://ahmelkholy.github.io/sitemap.xml). Articles include author/date structured data. Complete [the one-time Google Search Console setup](maintenance/GOOGLE_INDEXING.md) after publishing; Google decides whether and when to index pages.

The phone number has been removed from the public CV page and PDF. Keep replacement CVs email-only.

[Rebuild report](SITE_REBUILD_REPORT.md) · [Migration map](maintenance/MIGRATION.md)

Original site sources are preserved in `.archive/original-site.tar.gz` and Git history, with the original LICENSE intact. These and maintenance files are not published.

## Shared profile

Use the local combined VS Code workspace to edit common biography, skills, education and links across the website, GitHub profile and private CV. See [shared profile editing](maintenance/SHARED_PROFILE.md). Ordinary articles still need only Markdown and a push.
