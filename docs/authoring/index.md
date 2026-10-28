---
title: Writing on this site
translation_key: authoring-example
math: true
---
This is author documentation and a working layout example. Ordinary articles are Markdown files in `_posts/` with a short YAML header. See the repository’s `maintenance/AUTHOR_GUIDE.md` for the complete local workflow.

## A small Markdown file

```yaml
title: A useful observation
date: 2026-10-28
lang: en
tags: [engineering]
```

Put `---` before and after this header. Then write the article below it. Use `lang: ar` for Arabic or `lang: ru` for Russian. A post does not need translations.

## Code and equations

Fenced code blocks use a language name for highlighting:

```python
voltage = 230
current = 5
power = voltage * current
print(power)
```

Set `math: true` in front matter only when a page needs equations. MathJax is served locally and loaded only on those pages. For example, apparent power:

$$S = V I^{*}$$

This equation is a typesetting example, not a project result.

## Images and captions

Use meaningful alt text. For a caption, use a small HTML figure in Markdown:

<figure>
<img src="/images/Transformer_donnection.png" alt="Transformer connection and phase-displacement symbols from the original article" loading="lazy">
<figcaption>Existing illustration from the transformer-connections article; retained during migration.</figcaption>
</figure>

## Links within documentation

Use relative directory links: [next: static imports](imports/). An imported bundle has [its own example page](/docs/static-example/) under `/docs/static-example/`.

## Translations

Give real counterparts the same `translation_key`. Each keeps its own URL and `lang`. The layout offers links only to published counterparts. The Arabic and Russian pages linked above are translated authoring examples.
