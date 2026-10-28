#!/usr/bin/env python3
"""Validate crawlability and structured metadata in the production artifact."""
from pathlib import Path
from html.parser import HTMLParser
import json
import re
import sys
import xml.etree.ElementTree as ET
root=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
origin='https://ahmelkholy.github.io'
class Head(HTMLParser):
    def __init__(self,text):
        super().__init__(); self.metadata={};self.canonical=None;self.blocks=[];self.in_json=False;self.buffer='';self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='meta': self.metadata[a.get('name',a.get('property',''))]=a.get('content','')
        if tag=='link' and a.get('rel')=='canonical': self.canonical=a['href']
        if tag=='script' and a.get('type')=='application/ld+json': self.in_json=True;self.buffer=''
    def handle_data(self,data):
        if self.in_json:self.buffer+=data
    def handle_endtag(self,tag):
        if tag=='script' and self.in_json:
            self.blocks.append(json.loads(self.buffer));self.in_json=False
count=0
for path in root.rglob('*.html'):
    text=path.read_text()
    assert not re.search(r'\+20[\s-]*\d{10}|href=[\"\']tel:',text),f'Phone contact published: {path}'
    if 'class="site-header shell"' not in text:continue
    head=Head(text);assert head.canonical.startswith(origin+'/'),path
    assert head.metadata.get('description'),path
    assert len(head.blocks)==1,path
    record=head.blocks[0]
    assert record['url']==head.canonical and record['inLanguage'] in ['en','ar','ru'],path
    if path.name=='404.html':assert head.metadata['robots'].startswith('noindex')
    else:assert head.metadata['robots'].startswith('index, follow'),path
    if 'google-site-verification' in head.metadata:
        assert head.metadata['google-site-verification'].strip(), 'Do not publish an empty verification token'
    count+=1
post=Head((root/'posts/2023/08/blog-post-5/index.html').read_text()).blocks[0]
assert post['@type']=='BlogPosting' and post['author']['name']=='Ahmed M. Elkholy'
assert post['datePublished'] and post['inLanguage']=='ar'
profile=Head((root/'cv/index.html').read_text()).blocks[0]
assert profile['@type']=='ProfilePage' and 'telephone' not in profile['mainEntity']
urls={x.text for x in ET.parse(root/'sitemap.xml').iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')}
for path in ['/','/articles/','/ar/articles/','/talks/','/cv/','/posts/2023/08/blog-post-5/']:
    assert origin+path in urls,path
assert all('/maintenance/' not in url and '/404.html' not in url for url in urls)
assert 'Sitemap: '+origin+'/sitemap.xml' in (root/'robots.txt').read_text()
print(f'PASS: {count} pages with valid JSON-LD, production canonicals, descriptions and robots rules; sitemap discovery and email-only contact.')
