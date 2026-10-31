# Author guide

For everyday writing, use **Cmd+Shift+P → Tasks: Run Task → New post** in VS Code. It prompts for title, URL slug and language, then opens the file. Write, save, commit and push. No local build is required. **New draft**, **New talk**, **Preview website** and **Check website** are also available. See the root README for the short workflow.

Technical files are hidden only in the VS Code Explorer through `.vscode/settings.json`; Cmd+P can still open them. Remove entries under `files.exclude` if you want the full tree.

## Local setup and preview

Use Ruby **3.4.12** (see `.ruby-version`) and Bundler. The Ruby installed during this rebuild is isolated in `.tools/ruby/`; no system Ruby or shell configuration was changed. On this machine:

```sh
cd /Users/ahmelkholy/Documents/ahmelkholy.github.io
export PATH="$PWD/.tools/ruby/bin:$PATH"
bundle config set --local path vendor/bundle
bundle install
bundle exec jekyll serve --host 127.0.0.1 --port 4000
```

Open http://127.0.0.1:4000. Markdown changes trigger rebuilds. Restart after changing `_config.yml`, plugins, or imported static docs. Stop with Ctrl-C.

On a fresh machine, install the Ruby version in `.ruby-version` with your Ruby version manager first. The repository-local Ruby and gems are ignored and never deployed. See [Jekyll’s macOS setup](https://jekyllrb.com/docs/installation/macos/) rather than using macOS system Ruby. No Node/npm install is needed to build or write.

Production build and generated-output checks:

```sh
JEKYLL_ENV=production bundle exec jekyll build --trace
python3 scripts/check_site.py
python3 tests/authoring.py
bundle exec ruby tests/post_assets.rb
```

## Write an article

Create `_posts/2026-10-28-my-topic.md` in UTF-8. Use an ASCII filename for a simple URL; the title and body can be in any supported language.

```markdown
---
title: A useful observation
date: 2026-10-28
lang: en
tags: [engineering, notes]
---

Write here. Use `##` for sections; the layout supplies the article title.
```

For Arabic, set `lang: ar` and write normally. The page uses RTL, while code and equations stay LTR. For Russian, set `lang: ru`. There is no requirement to translate a post. The Writing page provides language and title/tag filters; `/articles/?lang=ar` opens the Arabic filter. `/ar/articles/` and `/ru/articles/` provide localized writing indexes.

The optional helper creates files without overwriting existing work:

```sh
python3 scripts/new_post.py my-topic --title 'A useful observation' --lang en --tag engineering
python3 scripts/new_post.py arabic-note --title 'ملاحظة هندسية' --lang ar --draft
python3 scripts/new_post.py russian-note --title 'Инженерная заметка' --lang ru --draft
```

New routes use `/articles/YYYY/MM/slug/`. Existing articles keep their explicit `permalink`. Add an explicit `permalink` only when you need a stable custom address. Do not reuse a URL.

## Drafts, dates and translations

Drafts go in `_drafts/`; preview them with `bundle exec jekyll serve --drafts`. Move the final file into `_posts/` with a `YYYY-MM-DD-slug.md` filename to publish it. The draft folder starts empty. Regression fixtures live under `tests/fixtures/`.

Future-dated posts are excluded from normal builds. They appear on the next build after their date, not automatically at midnight: push or manually run the workflow to publish them. Use `--future` only for local preview. `published: false` also hides unfinished content.

For real translations, add the same `translation_key: my-topic` to each counterpart, with its own `lang`, filename and URL. Keep one counterpart per language. The translation menu links only published counterparts. The site does not generate translations or pretend every post exists in three languages.

## Articles with their own figures

For an article with figures, put these two items in one topic folder under `_posts/`:

| Item | Example |
|---|---|
| Dated Markdown file | `_posts/my-topic/2026-10-31-my-topic.md` |
| Figure folder | `_posts/my-topic/figs/` |

Keep the same front matter as an ordinary post. Write image paths relative to the Markdown file:

```markdown
![Describe the figure and what it shows](figs/figure-1.svg)

*Figure 1. Reproduced from Figure X in Author et al. (year),
[Paper title](https://doi.org/DOI). [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
Cropped to the original figure area; no data or labels changed.*
```

Replace the placeholders with the actual source, original figure number and applicable licence. Use the authors' original figure when reproducing a paper; identify any crop or modification. Check any separate credit attached to the figure as well as the paper's licence. A citation alone does not grant reuse permission.

Commit and push the whole folder. The existing Pages workflow builds it, adds the article to the Writing page, tags, RSS and sitemap, and publishes the figures. There is no manual asset-copying step. Remove `published: false` when ready; draft and future-date rules still apply.

The `_plugins/post_assets.rb` plugin resolves image paths from the Markdown file's source directory and publishes referenced assets under `/assets/posts/`. This also works with custom permalinks and a nonempty site `baseurl`, and in RSS content and article excerpts. The original Markdown and asset files are not modified. Only referenced files are copied, and obsolete copies are removed on a normal rebuild.

Supported files are SVG, PNG, JPEG, GIF, WebP, AVIF, ICO, TIFF and PDF. Standard Markdown images, HTML `<img>` / `<source>` image URLs and `srcset`, video posters, `<object data>` and links to these file types are resolved. For example, `[Paper](figs/paper.pdf#page=2)` publishes and links the adjacent PDF. External URLs, root-relative website URLs and in-page anchors keep their original behavior. Data-URI `srcset` values are left unchanged. Hidden files, symlinks, missing referenced figures and conflicting output paths stop the build with a message identifying the post and URL.

Flat posts remain supported. A file at `_posts/2026-10-31-my-topic.md` can reference `my-topic/figs/figure-1.svg` or `my-topic/figure-1.svg`. Use a separate topic folder to avoid mixing figures from different articles. Keep downloads intended for publication in one of the supported formats; source Markdown and maintenance notes are not copied as figures.

## Images, code, math, headings and tags

Shared images can still go in `images/` or `assets/images/`:

```markdown
![Describe what the reader needs to understand](/images/example.png)
```

For a caption:

```html
<figure>
  <img src="/images/example.png" alt="Meaningful description" loading="lazy">
  <figcaption>Caption and source credit.</figcaption>
</figure>
```

Use fenced code blocks with a language (`python`, `julia`, `matlab`, `bash`, etc.). Rouge highlights at build time. For equations add `math: true`, then write `$$S = V I^{*}$$`; local MathJax renders them. Pages without this flag load no math library. The vendored MathJax 3.2.2 bundle keeps the supported Jekyll/Kramdown TeX workflow self-contained; see [MathJax hosting documentation](https://docs.mathjax.org/en/v3.2/web/hosting.html).

In Arabic prose wrap a literal URL or an ambiguous English identifier with `<bdi dir="ltr">…</bdi>`. Code fences, inline code and equations are already direction-isolated. Use a descriptive link label instead of a long bare URL where possible.

Article `##` and `###` headings populate a collapsible contents list. Set `toc: false` to disable it. Headings also retain native anchor IDs when JavaScript is off. Tags in front matter appear in `/tags/`; keep spelling consistent. Filter/search is deliberately small: titles and tags, no backend or third-party search service.

## Project documentation

For native Markdown, create:

```text
docs/my-project/index.md
docs/my-project/setup/index.md
```

Each file needs only a `title` in front matter; `lang` defaults to English. Link from the first page with `[Setup](setup/)` and back with `[Overview](../)`. Add the project to `docs/index.md` and the projects page. `/docs/authoring/` is the working example, including Arabic and Russian variants. For your own project, set `doc_home: /docs/my-project/` and `doc_title: My project` on its pages to customize the breadcrumb.

For externally generated documentation:

1. Build Documenter.jl, MkDocs or another generator locally. Set its site/deployment URL to `https://ahmelkholy.github.io/docs/my-project/`. Configure relative links or that exact asset prefix; a root-relative `/assets/` from the external generator usually points at the wrong site directory.
2. Inspect the generated output to ensure it contains only public material.
3. Copy the output into `static-docs/my-project/` (including `index.html`), preserving directory structure. Remove an old bundle before replacing it so obsolete files do not linger.
4. Build and run the link checks. The `_plugins/static_docs.rb` post-write hook copies it unchanged to `_site/docs/my-project/`, including `_assets`. Liquid/front matter is not interpreted. Do not create a native Markdown directory at the same project path.
5. Add a link to `docs/index.md` and commit the public generated files with the rest of the site. No workflow fetches private repositories.

Only lowercase names with numbers/hyphens are accepted for imported project directories. Hidden files and symlinks fail the build; use plain public files. The sample `static-docs/static-example/` demonstrates nested relative navigation and literal Liquid text. Its name and content explicitly identify it as author documentation.

Imported generators should supply their own canonical metadata and sitemap if they need search indexing; Jekyll's sitemap covers native pages, not post-build copies. Link the imported sitemap from `robots.txt` if supplied.

## CV and bibliography

The public PDF is at `/files/Ahmed_M_Elkholy-cv.pdf`. Replace this file when the CV changes; keep the path. The public CV must contain only the two email addresses as direct contact details: remove any phone number from replacement PDFs before publishing. Update `_pages/cv.md`, localized profile pages and `_pages/publications.md` from verified public information. Do not copy audit files or private supporting documents into this repository. The PhD remains **in progress, expected December 2026**; its start year is deliberately omitted.

## Publish when ready

Review changes and run the production checks first. Then, when you choose to publish:

```sh
git status
git add <reviewed-files>
git commit -m "Update writing and website"
git push origin master
```

Do not literally type `<reviewed-files>`; select the files you intend to publish. There is no need to commit `_site`, `.tools`, `vendor` or screenshots. One workflow builds and deploys on `master` or manual dispatch. GitHub Pages is free for this public repository.

The default branch is `master`, and GitHub Actions builds and deploys the site through the `github-pages` environment. The workflow follows [GitHub’s custom Pages workflow](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages) using an uploaded static artifact. After pushing, wait for **Build and deploy Jekyll** to succeed before checking the public page. A failed build keeps the previously deployed site in place; open the failing step to find the post or asset that needs correction.

## What stays private to maintenance

`maintenance/AUTHOR_GUIDE.md`, `maintenance/MIGRATION.md`, `SITE_REBUILD_REPORT.md`, scripts, test results, `.archive`, tools and dependency directories are explicitly excluded. `/docs/authoring/` is intentionally public. The original source and licence are retained; see `maintenance/MIGRATION.md` for redirects and the one historical URL collision.

## Talks and presentations

Use the **New talk** task or `python3 scripts/new_post.py my-talk --title "My talk" --lang en --talk`. It creates Markdown in `_talks/`. Add a short description, event details, images and slide links in the body. Optional `venue` in front matter appears in the listing. Use `published: false` while preparing an unfinished talk. The `/talks/` index updates automatically on push. Old theme sample talks are archived; the public section starts without invented entries.

## Google indexing

Follow [Google Search Console setup](GOOGLE_INDEXING.md) once after publishing. The site maintains the sitemap and search metadata automatically. A real verification token can be added in `_config.yml`; no account settings were changed during this work.
