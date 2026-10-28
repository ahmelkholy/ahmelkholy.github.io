# Website rebuild — local review

Initial local rebuild completed on 28 October 2026. The user subsequently authorized pushing; the successful deployment is recorded at the end of this report. No remote settings change was made. No other agent/session was started. Work was limited to this website repository; the named public profile sources were read only.

## Preview

The local preview is running at **http://127.0.0.1:4000/**.

To restart from this repository:

```sh
export PATH="$PWD/.tools/ruby/bin:$PATH"
JEKYLL_ENV=production bundle exec jekyll serve --host 127.0.0.1 --port 4000
```

For a production build and repeatable checks:

```sh
export PATH="$PWD/.tools/ruby/bin:$PATH"
JEKYLL_ENV=production bundle exec jekyll build
python3 scripts/check_site.py
python3 tests/authoring.py
```

Ruby 3.4.12 and its missing libyaml dependency were built inside `.tools/`, using the existing OpenSSL installation. Gems are isolated in `vendor/bundle/`. The interrupted original install was checked before restarting; a cached failed YAML extension required a fresh build directory. No system Ruby or shell settings were changed. A Linux platform is included in `Gemfile.lock` for CI.

## Delivered

- Kept Jekyll 4.4.1, with small custom layouts and plain CSS/JavaScript. No frontend build, CMS, database or runtime server is required for publishing.
- Revised the initially sparse design after user feedback: the existing profile photograph and author information now sit beside the content, with prominent page navigation, language links, public CV download and social links. Dark colors, readable typography, responsive layout and visible current-page tabs are included.
- Home, writing, projects, documentation, About/CV, publications, contact/community and privacy pages. PSCAD, NEPLAN, DIgSILENT PowerFactory, ETAP, stability/harmonic studies and YouTube are included. PhD remains in progress, expected December 2026; unresolved start year omitted.
- Eight original articles retained, with repaired language/tag/date metadata. Original prose and media were preserved. Twenty-six verified publications are listed; matching old publication pages retain their URLs with verified bibliographic content.
- English, Arabic and Russian Markdown support, localized writing indexes, Arabic RTL and isolated LTR code/math. Real translation links only. No invented Russian articles: the index has an explicit empty state, while a verified profile and authoring example demonstrate Russian rendering.
- Code highlighting, optional locally hosted MathJax, image captions/alt-text examples, heading anchors/TOC, tag index, title/tag filtering, RSS, canonical metadata and sitemap. Core reading/navigation work without JavaScript. Math requires JavaScript; TeX source remains otherwise.
- Native Markdown docs at `/docs/<project>/`, plus a working static import example. The post-write hook copies generated HTML unchanged, preserves underscore assets and rejects collisions, hidden files and symlinks. No workflow fetches another repository.
- Current public CV at `/files/Ahmed_M_Elkholy-cv.pdf`. The initial copy matched the authoritative PDF; the later email-only update permanently removed its phone text. The two emails, two-page layout and five Website/LinkedIn/Scholar/GitHub/YouTube QR labels remain intact.
- `maintenance/AUTHOR_GUIDE.md`, a safe UTF-8 new-post helper, repeatable validation scripts, and `maintenance/MIGRATION.md` with the source inventory and redirect map. Maintenance documents and archives are excluded from public output; `/docs/authoring/` is intentionally public.

## Validation actually run

| Check | Result |
|---|---|
| Production Jekyll build | Passed; 69 HTML pages, no build warnings/errors |
| Generated-output checker | Passed all local links, fragments, image alt text, accessible link labels, language/canonical metadata, RSS/sitemap XML, CV presence and maintenance exclusions |
| Public output privacy boundary | No local absolute evidence paths, private-source markers or draft/future sentinels found in generated HTML |
| Authoring regression fixtures | Passed English/Arabic/Russian helper output, translation routes and directions, draft/future/`published: false` exclusion |
| Static documentation | Byte-for-byte output comparison passed, including `_assets`; native/imported path collision correctly fails |
| Browser matrix | Chromium: 14 representative routes at 1440×900 and 390×900; all 28 returned 200, with no horizontal overflow or detected WCAG A/AA violations in axe-core 4.10.3 |
| Browser behavior | 20 assertions passed: Arabic search/filter, honest Russian empty state, original transformer image, article translation, TOC links, RTL/LTR code and rendered math, imported nested navigation, keyboard skip/focus, reduced-motion state, 320px layout, reading/navigation without JS |
| Localized indexes | Arabic navigation opens `/ar/articles/` with four Arabic articles; Arabic search works; `/ru/articles/` shows the Russian empty state |
| Console/network | Fresh final browser audit: no JavaScript/console errors or failed resource responses on the tested routes |
| Missing page | Unknown route returns HTTP 404 with the custom “Page not found” page |
| Diff whitespace | `git diff --check` passed |

Browser testing used the installed **webapp-testing** skill. Automated accessibility checks are evidence for the tested pages, not a full manual accessibility certification. Firefox, Safari and physical phones were not tested. External links and historical engineering claims were not comprehensively re-audited.

During validation, the initial empty navigation labels were fixed, filter labels were separated from select options for clear accessible names, and the static example received a favicon reference. The final clean browser audit has no errors. A test initially used strict viewport-width equality; it was corrected to allow a scrollbar reducing content width.

Screenshots and machine-readable audit are local, ignored and excluded from publishing:

- `review-artifacts/home-desktop.png`
- `review-artifacts/home-mobile.png`
- `review-artifacts/profile-ar-desktop.png`
- `review-artifacts/docs-ar-mobile.png`
- `review-artifacts/browser-audit.json`

`tests/browser.js` is a replayable function for the host Playwright tool, with the preview running and repository as its working directory. It does not add a browser dependency to the publishing pipeline.

## Migration and content limits

The old Academic Pages/Minimal Mistakes source, assets and conflicting workflows are retained in `.archive/original-site.tar.gz`, excluded from Jekyll. The original LICENSE and Git history remain; CHANGELOG and other legacy maintenance material are in the archive. Git status shows removed old source files and the new recoverable archive until staged; originals have not been destroyed.

The historical `/posts/2023/08/blog-post-4/` belonged to two articles. It now serves the 2023 website-generator article and its real Arabic counterpart. The transformer article has its own `/articles/2024/05/transformer-connections/` route. One old URL cannot identify both. Other practical old routes are retained or redirected; redirects are static HTML, not HTTP 301 responses. See `maintenance/MIGRATION.md`.

Generic teaching/talk/project samples and contradictory biographies were archived. Publication resources outside the verified paper list are retained in source; their old routes lead to the verified bibliography, without asserting uncertain authorship/publication status. The original green-hydrogen post still uses its external Bing image; that host remains an external dependency. No new engineering manuals or essays were invented.

Imported bundles must be configured for their actual `/docs/<project>/` prefix. They should supply their own sitemap if wanted; the Jekyll sitemap covers native pages, not the post-build copies. Restart preview after replacing an imported bundle. Future-dated articles require a build after their date to become public; there is no scheduled daily deploy.

## Publishing setup

Only `.github/workflows/pages.yml` is active. It builds and validates on pushes to the actual default branch **master** and manual dispatch, then uploads/deploys the Pages artifact. Dependencies are locked. Three old competing workflows were archived.

Read-only GitHub inspection confirmed **Pages source = GitHub Actions** (`build_type: workflow`) and enforced HTTPS. No one-time setting change appears necessary. If later disabled, select **Settings → Pages → Source → GitHub Actions** and ensure the `github-pages` environment allows `master`. Review and push only when ready. Remote CI/deployment was initially deferred; the later user-authorized deployment is recorded below.

Version-specific setup was checked against official [Jekyll installation](https://jekyllrb.com/docs/installation/macos/), [configuration](https://jekyllrb.com/docs/configuration/options/), [posts](https://jekyllrb.com/docs/posts/), [GitHub Pages custom workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages), [checkout](https://github.com/actions/checkout), [ruby/setup-ruby](https://github.com/ruby/setup-ruby), and [MathJax 3 self-hosting](https://docs.mathjax.org/en/v3.2/web/hosting.html) documentation. MathJax 3.2.2 is intentionally vendored for the optional Kramdown math path, with its licence; it is not described as the newest MathJax release.


## Follow-up: writing workflow, contact privacy, search and talks

Updated after the user’s subsequent requests:

- Removed the phone number from `_pages/cv.md` and permanently redacted its text from the public PDF (not a visual cover). Both emails, the two-page layout, all five QR labels and the remaining content are retained. The PDF was text-extracted and its first page visually inspected. The separate authoritative CV repository was not edited.
- Restored **Talks & presentations** at `/talks/` and the navigation tab, including Arabic/Russian tab labels. Added the `_talks` Markdown collection and a VS Code **New talk** task. No sample talks are presented as author accomplishments.
- Added VS Code tasks for **New post**, **New draft**, **New talk**, **Preview website** and **Check website**, plus article/figure snippets. The new-file task opens the file in VS Code when its CLI or macOS app is available. The same helper paths were exercised by isolated authoring tests; the VS Code UI itself was not automated.
- Rewrote README around the everyday workflow: write Markdown, save, commit and push. GitHub performs the build; a local build is optional. Explorer hides infrastructure while showing writing folders. Detailed guidance and migration notes now live in excluded `maintenance/`.
- Compressed original sources into `.archive/original-site.tar.gz`; compared every file byte-for-byte before removing the expanded archive. Removed obsolete Node dependencies, the abandoned Python environment, duplicate/unused legacy assets from active paths, downloads, build-source trees and temporary fixtures. Kept the Ruby/libyaml runtime and installed gems needed for preview. Source history and licences remain intact.
- Added WebSite, ProfilePage, WebPage and BlogPosting JSON-LD, article dates/authorship, representative images, search descriptions and explicit indexing rules. Existing canonical URLs, hreflang, RSS, sitemap and robots discovery remain. An optional real Search Console verification token can be set in `_config.yml`; no fake tag is emitted.
- Added `maintenance/GOOGLE_INDEXING.md` with URL-prefix verification and sitemap submission instructions. Google account verification/submission remains for the user after publishing; indexing and ranking cannot be guaranteed. No push or search-engine submission was made.

Follow-up validation: production build and all 69 generated-page checks passed; 44 normal pages passed JSON-LD, canonical, description and robots validation. New-talk authoring, existing en/ar/ru authoring, draft/future exclusion and static import tests passed. A supplied verification token was checked in an isolated fixture. Six affected routes at desktop/mobile sizes (12 checks) passed the Chromium/axe audit with eight visible navigation tabs, no overflow and no detected WCAG A/AA violations. The Talks tab was clicked and its target verified. The local CV page and PDF retain email-only direct contact details. Updated screenshots include `review-artifacts/talks-mobile.png` and `review-artifacts/cv-no-phone.png`.


## Authorized publication — 28 October 2026

The user explicitly requested “please push it”. The rebuild was committed as `00e0505d75af81eb6eb353253c1f053249f0e7db` and pushed normally to `origin/master`, without rewriting history. GitHub Actions run [40753483327](https://github.com/ahmelkholy/ahmelkholy.github.io/actions/runs/40753483327) completed both build/validation and deployment successfully.

Live checks returned HTTP 200 for the home page, `/talks/`, `/ar/`, `/cv/`, `/sitemap.xml` and `/robots.txt`. The live public PDF was downloaded and compared byte-for-byte with the phone-free local PDF. A Chromium check clicked the live Talks tab and verified its heading and all eight navigation links. The site is live at https://ahmelkholy.github.io/.

The workflow emitted non-blocking GitHub runner/Node migration notices; all jobs succeeded. Vendored MathJax contains upstream whitespace and the contact Markdown uses an intentional hard line break; a staged whitespace check reported these, rather than a build or runtime defect. The initial working-tree-only whitespace check did not include those then-untracked vendor files.

Search Console verification and sitemap submission remain an owner-account step; no Google indexing or ranking outcome is claimed. This report update changes excluded maintenance documentation only and does not require another site deployment.

## Scrolling navigation and link review

The existing top navigation now docks as a vertical reading rail on desktop after scrolling past the header. It retains the same focusable links, highlights the current page, shows the current content section, and offers Back to top. It mirrors naturally for Arabic RTL. On screens up to 760px it becomes a compact horizontally scrollable sticky bar. With JavaScript disabled the normal navigation remains available.

Added `/follow/` as a human-readable subscription page and changed the footer/contact links to point there. `/feed.xml` remains the standard Atom/RSS-compatible subscription feed, verified to return HTTP 200 with eight entries. Raw XML is expected for feed readers; it is not an empty page.

Validation: all 70 HTML pages pass internal-link/fragment/asset checks; 45 standard pages pass search-metadata checks. Chromium tested dock/undock at 1440, 800, 390 and 320px, Arabic RTL placement, active page, section tracking, clicking a docked link, Back to top and no-JavaScript navigation. No horizontal document overflow was detected. Screenshots are in `review-artifacts/navigation-desktop.png` and `navigation-mobile.png`.

External audit: 43 distinct links remain; 37 were reachable. Two DOI publisher links, LinkedIn, ResearchGate and SciProfiles restrict automated requests, while Scopus returned an unresolved redirect. Those six are unconfirmed by this automated audit, not represented as verified working. The old Bing-hosted green-hydrogen illustration returned a definite HTTP 404 and its broken reference was removed; the article prose and historical source remain. The read-only audit can be repeated with `python3 scripts/check_external_links.py`.


## Correction: recovered talks and conference entries

After the author pointed out missing conference history, the archived old CV was re-read in full. Its Talks section lists MEPCON 2017, 2018 and 2019; these were missed when reviewing the separate sample-only `_talks/` directory. All three have now been restored as Markdown conference entries and linked from Talks and the online CV. The earlier empty-state wording is superseded. The incorrectly repeated 2016 dates were corrected against official organizing-university records; see `maintenance/MIGRATION.md` for sources. No unsupported presentation title or speaking role is asserted.
