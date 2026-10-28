# Shared profile editing

The local `Ahmed.code-workspace` in the sibling private CV repository opens Website, GitHub profile and Private CV together. Use its **Watch shared profile (text only)** task for local automatic synchronization; use **Watch shared profile and PDFs** for optional PDF refresh.

Edit `shared-profile.json` here, or the marked `shared:bio`, `shared:skills`, `shared:education`, and `shared:links` sections in `_pages/cv.md`. Their public Markdown is shared with the profile README and private CV. Save, wait for sync/PDF completion, review and commit/push each relevant public repository. Different edits to one field stop for resolution; the watcher terminal identifies the private conflict report. No automatic commits or pushes occur.

Articles, talks, translations, project pages, contact badges and all unmarked content remain independent. The link field controls only the common link strip and PDF QR codes. Review repeated summaries and translations when shared facts change.

The website build does not need the private repository. Only public text and the PDF generated from this website's public CV page belong here. Never copy the private CV PDF, evidence directories or sync recovery journals into this repository. The shared JSON and this guide are excluded from the generated website.

Full setup, commands and conflict recovery are in the private repository's `profile-sync/README.md`. Existing article creation and push-to-publish instructions remain unchanged.

The workspace is portable: relative paths work under any parent directory. For different folder names, configure `profile-sync/repositories.json` and workspace folder paths in the private repository. Text synchronization needs only Python 3.9+; optional PDF builds require XeLaTeX and Poppler. No private repository is needed by public GitHub workflows.
