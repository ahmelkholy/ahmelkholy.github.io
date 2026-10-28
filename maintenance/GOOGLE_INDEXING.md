# Google indexing — one-time setup

The site is ready to be crawled: server-generated HTML, public links, useful titles/descriptions, language metadata, canonical URLs, RSS and an automatically generated sitemap. `robots.txt` permits crawling and advertises the sitemap. Articles have BlogPosting structured data; profile pages identify their author. No account, tracking script or paid service is needed for normal publishing.

These changes are local until you commit and push them. We have not submitted the site to Google or claimed it is indexed.

## After your first push

1. Open [Google Search Console](https://search.google.com/search-console/) using your Google account.
2. Add a **URL prefix** property: `https://ahmelkholy.github.io/`. Use URL prefix because you do not control DNS for the `github.io` domain.
3. Choose **HTML tag** verification. Copy only the value inside `content="…"` from Google's tag.
4. Open `_config.yml` (Cmd+P works even when it is hidden in Explorer) and paste that value into `google_site_verification: ""`. Commit and push. The site inserts the actual verification tag automatically; it never publishes a fake placeholder.
5. Once the GitHub Pages workflow finishes, return to Search Console and click **Verify**. Keep the token in the configuration for ongoing ownership verification.
6. In **Sitemaps**, submit `sitemap.xml`.
7. Use **URL Inspection** for the home page and important articles, test the live URL, then request indexing.

This is normally a one-time setup. After that, write, save, commit and push. New articles are linked from the writing index and added to the sitemap automatically. Monitor the Page indexing report if a page is missing.

Google controls crawling, indexing and ranking. A sitemap or indexing request does not guarantee inclusion or a particular position. Useful original articles, clear titles and descriptive links make the site understandable to readers and search engines; there is no need to stuff titles or tags with keywords.

## Useful optional front matter

Ordinary posts need only `title`, `date`, `lang` and optional `tags`. A concise `description` can improve how a page is described; otherwise the opening paragraph is used. If the post has a representative image, set `image: /images/your-image.png` and `image_alt: A meaningful description`. Set `last_modified_at` only when you actually update the article. Do not use the author portrait as an article's representative illustration.

## Authoritative instructions

- [Verify ownership](https://support.google.com/webmasters/answer/9008080)
- [Create and submit a sitemap](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap)
- [Request crawling/indexing](https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl)
- [Article structured data](https://developers.google.com/search/docs/appearance/structured-data/article)

The downloadable PDF has been redacted locally. After publishing, existing Google copies or snippets may take time to refresh; use URL Inspection to request a recrawl of the updated CV page/PDF if needed.
