#!/usr/bin/env python3
"""Read-only reachability audit. A blocked response is not proof of a broken link."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import Request,urlopen
from urllib.error import HTTPError
from concurrent.futures import ThreadPoolExecutor
import json
urls=set()
class Links(HTMLParser):
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag not in ('a','img'): return
  url=a.get('href',a.get('src',''))
  parsed=urlsplit(url)
  if parsed.scheme in ('http','https') and parsed.netloc not in ('ahmelkholy.github.io','localhost:4000','127.0.0.1:4000'): urls.add(url)
for p in Path('_site').rglob('*.html'):Links().feed(p.read_text())
def check(url):
 try:
  with urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0 (website link check)'}),timeout=18) as r:
   return {'url':url,'status':r.status,'final':r.url,'result':'reachable'}
 except HTTPError as e:
  return {'url':url,'status':e.code,'result':'blocked or rate-limited' if e.code in (401,403,429,999) else 'redirect could not be resolved' if e.code in (301,302,303,307,308) else 'needs review'}
 except Exception as e:return {'url':url,'result':'unconfirmed','error':str(e)}
with ThreadPoolExecutor(max_workers=8) as pool: results=list(pool.map(check,sorted(urls)))
Path('review-artifacts').mkdir(exist_ok=True)
Path('review-artifacts/external-links.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
for row in results:
 if row['result']!='reachable':print(json.dumps(row,ensure_ascii=False))
print(f"Checked {len(results)} external links: {sum(r['result']=='reachable' for r in results)} reachable; results in review-artifacts/external-links.json")
