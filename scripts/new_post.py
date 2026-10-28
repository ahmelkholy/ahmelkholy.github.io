#!/usr/bin/env python3
"""Create a UTF-8 Markdown article without overwriting existing work."""
import argparse
from datetime import date
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('slug', help='URL-friendly slug, e.g. transformer-notes')
parser.add_argument('--title', required=True)
parser.add_argument('--lang', choices=['en', 'ar', 'ru'], default='en')
parser.add_argument('--date', default=date.today().isoformat())
parser.add_argument('--tag', action='append', default=[])
parser.add_argument('--translation-key')
parser.add_argument('--draft', action='store_true')
parser.add_argument('--talk', action='store_true', help='Create a talk or presentation')
parser.add_argument('--open', action='store_true', help='Open the new file in VS Code')
args = parser.parse_args()
if not args.title.strip():
    parser.error("Please enter an article title.")
if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', args.slug):
    parser.error('Use lowercase ASCII letters, numbers and hyphens for the slug.')
try:
    date.fromisoformat(args.date)
except ValueError:
    parser.error('Date must be YYYY-MM-DD.')
if args.talk and args.draft:
    parser.error('For an unfinished talk, use published: false in its header.')
folder = Path(__file__).resolve().parents[1] / ('_talks' if args.talk else '_drafts' if args.draft else '_posts')
folder.mkdir(exist_ok=True)
path = folder / f'{args.date}-{args.slug}.md'
fields = {'title': args.title, 'date': args.date, 'lang': args.lang, 'tags': args.tag}
if args.translation_key:
    fields['translation_key'] = args.translation_key
with path.open('x', encoding='utf-8') as stream:
    stream.write('---\n' + ''.join(f'{k}: {json.dumps(v, ensure_ascii=False)}\n' for k, v in fields.items()) + '---\n\n')
print(path.relative_to(folder.parent))

if args.open:
    if shutil.which('code'):
        subprocess.run(['code', '--reuse-window', str(path)], check=False)
    elif sys.platform == 'darwin':
        subprocess.run(['open', '-a', 'Visual Studio Code', str(path)], check=False)
    else:
        print('Open this file in VS Code: ' + str(path))
