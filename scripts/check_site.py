#!/usr/bin/env python3
"""Check local links, assets, fragments, metadata and publication boundaries."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit, urljoin
import re
import sys
import xml.etree.ElementTree as ET

root = Path(sys.argv[1] if len(sys.argv) > 1 else '_site').resolve()
errors = []
class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.links, self.ids, self.images = [], set(), []
        self.lang = self.direction = None
        self.canonical = False
        self.anchor = None
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'a': self.anchor = a.get('aria-label', '')
        if tag == 'img' and self.anchor is not None: self.anchor += a.get('alt', '')
        if 'id' in a: self.ids.add(a['id'])
        if tag == 'html': self.lang, self.direction = a.get('lang'), a.get('dir')
        if tag == 'link' and a.get('rel') == 'canonical': self.canonical = True
        if tag == 'img' and not a.get('alt'): errors.append('Image lacks alt text: ' + str(a))
        for key in ('href', 'src', 'poster'):
            if key in a: self.links.append(a[key])

    def handle_data(self, data):
        if self.anchor is not None: self.anchor += data
    def handle_endtag(self, tag):
        if tag == 'a':
            if self.anchor is not None and not self.anchor.strip(): errors.append('Link has no accessible label')
            self.anchor = None

def resolve(url):
    p = root / unquote(url).lstrip('/')
    if p.is_dir(): p /= 'index.html'
    if not p.exists() and not p.suffix and p.with_suffix('.html').exists(): p = p.with_suffix('.html')
    return p

pages = {}
for path in root.rglob('*.html'):
    text = path.read_text(encoding='utf-8')
    pages[path] = Page(text)
    if re.search(r'/Users/|\.cv-private|DRAFT_EXCLUSION_SENTINEL|FUTURE_EXCLUSION_SENTINEL', text):
        errors.append(f'Private/local/draft content leaked: {path.relative_to(root)}')
    if not pages[path].lang: errors.append(f'Missing lang: {path.relative_to(root)}')
    if not pages[path].canonical: errors.append(f'Missing canonical: {path.relative_to(root)}')
    if pages[path].lang == 'ar' and pages[path].direction != 'rtl': errors.append(f'Arabic is not RTL: {path}')
for path, page in pages.items():
    relative = '/' + str(path.relative_to(root))
    base = 'https://ahmelkholy.github.io' + relative
    for link in page.links:
        url = urlsplit(urljoin(base, link))
        if url.scheme not in ('http', 'https') or url.netloc != 'ahmelkholy.github.io': continue
        dest = resolve(url.path)
        if not dest.exists(): errors.append(f'{relative}: missing {link}')
        elif url.fragment and dest in pages and unquote(url.fragment) not in pages[dest].ids:
            errors.append(f'{relative}: missing fragment {link}')
for name in ('feed.xml', 'sitemap.xml'):
    try: ET.parse(root / name)
    except (OSError, ET.ParseError) as error: errors.append(f'{name}: {error}')
for forbidden in ('shared-profile.json','profile-sync','.profile-sync','Ahmed.code-workspace','AUTHOR_GUIDE.md','MIGRATION.md','SITE_REBUILD_REPORT.md','scripts','tests','static-docs','maintenance','.archive','.tools','Gemfile','node_modules'):
    if (root / forbidden).exists(): errors.append(f'Maintenance path published: {forbidden}')
for path in Path('static-docs').rglob('*'):
    if path.is_file():
        target = root / 'docs' / path.relative_to('static-docs')
        if not target.exists() or target.read_bytes() != path.read_bytes(): errors.append(f'Imported file changed: {path}')
if not (root / 'files/Ahmed_M_Elkholy-cv.pdf').exists(): errors.append('Public CV is missing')
if errors:
    print('\n'.join(errors)); sys.exit(1)
print(f'PASS: {len(pages)} HTML pages; local links, fragments, images, canonical/language metadata, feeds, exclusions and static imports.')
