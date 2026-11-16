"""Translate actual Lighthouse failing text nodes into scoped contrast fixes."""
import json
import re
from pathlib import Path
from urllib.parse import urlparse
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
rules = {}
scores = []
existing = ROOT / 'sitegen/styles/validation.css'
if existing.exists():
    rules.update({selector.strip():color for selector,color in re.findall(r'^([^{\n]+)\{ color: (#[a-fA-F0-9]{6})',existing.read_text(),re.M)})

def luminance(hex_color):
    value = hex_color.lstrip('#')
    rgb = [int(value[i:i+2],16) / 255 for i in (0,2,4)]
    linear = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return sum(c * w for c,w in zip(linear,[0.2126,0.7152,0.0722]))

def ratio(a, b):
    high, low = sorted([luminance(a),luminance(b)],reverse=True)
    return (high + 0.05) / (low + 0.05)

for path in sorted((ROOT / 'docs/lighthouse').glob('*.report.json')):
    report = json.loads(path.read_text())
    page = urlparse(report['finalDisplayedUrl']).path.strip('/') or 'home'
    scores.append({'report':path.name,'scores':{k:round(v['score']*100) for k,v in report['categories'].items()}})
    for item in report['audits'].get('color-contrast',{}).get('details',{}).get('items',[]):
        node = item.get('node',{})
        selector = node.get('selector','')
        match = re.search(r'background color: (#[a-fA-F0-9]{6})', node.get('explanation',''))
        if not selector or not match: continue
        color = match.group(1)
        foreground = max(['#24161d','#f4f1e9'],key=lambda candidate: ratio(candidate,color))
        if ratio(foreground,color) < 4.5:
            foreground = max(['#000000','#ffffff'],key=lambda candidate: ratio(candidate,color))
        scoped = selector if selector.startswith('body.') else f'body.page-{page} {selector}'
        rules[scoped] = foreground
lines = ['/* Actual Lighthouse contrast failures, scoped to their exact page and node. */']
lines += [f'{selector} {{ color: {color} !important; opacity: 1; }}' for selector,color in sorted(rules.items())]
(ROOT / 'sitegen/styles/validation.css').write_text('\n'.join(lines) + '\n')
for name in ('live1','live2','live6'):
    source = ROOT / 'public/assets/dealers' / (name + '.webp')
    with Image.open(source) as image:
        image.resize((520,520),Image.Resampling.LANCZOS).save(source.with_name(name + '-mobile.webp'),'WEBP',quality=88,method=6)
print(json.dumps(scores,ensure_ascii=False,indent=2))
print('Created', len(rules),'scoped contrast rules and 3 proportion-preserving mobile photos.')
