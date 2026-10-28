# Original website source

`original-site.tar.gz` contains the original theme, pages, assets, scripts and old workflows. Every archived file was compared byte-for-byte before the expanded copies were removed. The archive is excluded from Jekyll and hidden in the writing workspace. The original Git history and root LICENSE remain intact.

To inspect it without changing the current site:

```sh
mkdir -p .tools/original-site
tar -xzf .archive/original-site.tar.gz -C .tools/original-site
```

These originals contain outdated profiles and theme samples. Do not treat them as verified current content. See `maintenance/MIGRATION.md`.
