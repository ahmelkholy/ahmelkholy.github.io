#!/usr/bin/env python3
"""Exercise authoring in an isolated copy; never add sample posts to the real site."""
from pathlib import Path
import shutil
import subprocess
import json
import re
root = Path(__file__).resolve().parents[1]
source = root / '.tools/fixture-source'
output = root / '.tools/fixture-output'
if source.exists(): shutil.rmtree(source)
shutil.copytree(root, source, ignore=shutil.ignore_patterns('.git','.tools','.archive','.site','.bundle','.codex-local','vendor','node_modules','_site','review-artifacts','__pycache__'))
(source/'_drafts').mkdir(exist_ok=True)
shutil.copyfile(source/'tests/fixtures/draft.md', source/'_drafts/exclusion-fixture.md')
for lang, title in [('en','English authoring fixture'),('ar','مثال اختبار الكتابة'),('ru','Проверка публикации')]:
    subprocess.run(['python3', str(source/'scripts/new_post.py'), 'fixture-'+lang, '--title', title, '--lang', lang, '--date','2020-01-02','--translation-key','test-fixture'], check=True, cwd=source)
config=source/'_config.yml'
config.write_text(config.read_text().replace('google_site_verification: ""', 'google_site_verification: "test-verification-token"'))
(source/'_posts/2099-01-01-future-test.md').write_text('---\ntitle: Future fixture\ndate: 2099-01-01\n---\nFUTURE_EXCLUSION_SENTINEL')
(source/'_posts/2020-01-01-hidden-test.md').write_text('---\ntitle: Hidden fixture\npublished: false\n---\nHIDDEN_EXCLUSION_SENTINEL')
subprocess.run(['bundle','exec','jekyll','build','--source',str(source),'--destination',str(output)],check=True,cwd=root)
assert 'name="google-site-verification" content="test-verification-token"' in (output/'index.html').read_text()
for lang in ['en','ar','ru']:
    html=(output/f'articles/2020/01/fixture-{lang}/index.html').read_text()
    assert f'<html lang="{lang}"' in html
    assert f'dir="{"rtl" if lang == "ar" else "ltr"}"' in html
    for other in ['en','ar','ru']:
        if other != lang: assert f'href="/articles/2020/01/fixture-{other}/"' in html
text=''.join(p.read_text() for p in output.rglob('*.html'))
for sentinel in ['FUTURE_EXCLUSION_SENTINEL','DRAFT_EXCLUSION_SENTINEL','HIDDEN_EXCLUSION_SENTINEL']:
    assert sentinel not in text, sentinel
# New-talk authoring uses a dedicated collection without fake public examples.
subprocess.run(['python3', str(source/'scripts/new_post.py'), 'fixture-talk', '--title', 'Talk fixture', '--lang', 'en', '--date', '2020-01-02', '--talk'], check=True, cwd=source)
subprocess.run(['bundle','exec','jekyll','build','--source',str(source),'--destination',str(output)],check=True,cwd=root)
assert 'Talk fixture' in (output/'talks/index.html').read_text()
assert (output/'talks/2020-01-02-fixture-talk/index.html').is_file()
# Imported docs must remain byte-for-byte identical, including underscore assets.
for p in (source/'static-docs').rglob('*'):
    if p.is_file(): assert p.read_bytes()==(output/'docs'/p.relative_to(source/'static-docs')).read_bytes()
# A native/generated path collision should fail rather than silently overwrite content.
collision=source/'docs/static-example';collision.mkdir()
(collision/'index.md').write_text('---\ntitle: Collision fixture\n---\n')
result=subprocess.run(['bundle','exec','jekyll','build','--source',str(source),'--destination',str(output)],cwd=root,capture_output=True,text=True)
assert result.returncode != 0 and 'Native/imported docs collision' in result.stderr
print('PASS: en/ar/ru authoring, translation links, directions, future/hidden/draft exclusion, new-talk creation, exact static copy, collision rejection.')

shutil.rmtree(source)
shutil.rmtree(output)
