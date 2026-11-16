"""Read-only audit of the isolated test service, never the product services."""
import json
import os
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse, urljoin
import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
BASE = os.environ.get('TEST_ORIGIN', 'http://127.0.0.1:3000').rstrip('/')
ROUTES = ['/', '/features', '/auto', '/guide?system=matrix', '/guide?system=auto', '/faq', '/contact']
LINE = 'https://line.me/ti/p/k2pkYGXGL3'
errors, results, visited = [], [], {}

def get(path):
    url = urljoin(BASE + '/', path)
    if url not in visited: visited[url] = requests.get(url, timeout=30, allow_redirects=False)
    return visited[url]

for route in ROUTES:
    response = get(route)
    soup: Any = BeautifulSoup(response.text, 'html.parser')
    failures = []
    def require(condition, message):
        if not condition: failures.append(message)
    require(response.status_code == 200, 'page status !=200')
    require(len(soup.find_all('h1')) == 1, 'must have exactly one H1')
    require(soup.find('meta', attrs={'name':'description'}) is not None, 'description missing')
    robots = soup.find('meta', attrs={'name':'robots'})
    require(robots is not None and 'noindex' in robots.get('content',''), 'staging noindex missing')
    require('noindex' in response.headers.get('X-Robots-Tag',''), 'X-Robots-Tag missing')
    require(soup.find('link', rel='canonical') is not None, 'explicit test canonical missing')
    require(soup.find('meta', property='og:image') is not None, 'OG image missing')
    require(soup.find('meta', attrs={'name':'twitter:card'}) is not None, 'Twitter Card missing')
    require(soup.find('main') is not None and len(soup.find('main').get_text()) > 300, 'initial body content missing')
    require('@116cfqfk' not in response.text and '%40116cfqfk' not in response.text, 'old LINE identity returned')
    require(all(a.get('href') == LINE for a in soup.find_all('a') if a.get('href','').startswith('https://line.me')), 'LINE mismatch')
    require(soup.find('a', href='https://mt-assistant-web-v3.onrender.com/') is not None, 'MATRIX entry missing')
    require(soup.find('a', href='https://autotable-o6a2.onrender.com/') is not None, 'AUTO entry missing')
    for script in soup.find_all('script', type='application/ld+json'):
        try: json.loads(script.string or script.get_text())
        except Exception: failures.append('Invalid JSON-LD')
    ids = [t['id'] for t in soup.find_all(attrs={'id':True})]
    require(len(ids) == len(set(ids)), 'duplicate HTML ids')
    for tag in soup.find_all(['a','img','source','script','link']):
        url = tag.get('href') if tag.name in ('a','link') else tag.get('srcset') if tag.name == 'source' else tag.get('src')
        if not url: continue
        if tag.name == 'source':
            candidates = [candidate.strip().split()[0] for candidate in url.split(',') if candidate.strip()]
            for candidate in candidates:
                if candidate.startswith('/'):
                    require(get(candidate).status_code == 200, 'missing responsive source: ' + candidate)
            continue
        parsed = urlparse(url)
        if parsed.scheme or parsed.netloc: continue
        if parsed.path:
            target = get(url)
            require(target.status_code in (200,301), 'missing internal resource: ' + url)
        if parsed.fragment:
            dest: Any = soup if not parsed.path or parsed.path == route.split('?')[0] else BeautifulSoup(get(parsed.path).text, 'html.parser')
            require(dest.find(id=parsed.fragment) is not None, 'missing anchor: ' + url)
        if tag.name == 'img' and tag.get('src'):
            decorative = tag.get('aria-hidden') == 'true' or tag.find_parent(attrs={'aria-hidden':'true'}) is not None
            require(tag.has_attr('alt') and (decorative or bool(tag.get('alt'))), 'missing visible image ALT')
            require(tag.get('width') and tag.get('height'), 'image dimensions missing')
    if route.startswith('/guide'):
        require(len(soup.select('[id^=matrix-step]')) == 5, 'MATRIX steps not5')
        require(len(soup.select('[id^=auto-step]')) == 6, 'AUTO steps not6')
    if route == '/features':
        require(all(soup.find(id=i) for i in ('radar','analysis','formulas','parity')), 'original feature anchors missing')
        require(not any('/interfaces/auto-' in i.get('src','') for i in soup.find_all('img')), 'AUTO screens mixed into MATRIX')
    if route == '/auto':
        require(not any('/interfaces/matrix' in i.get('src','') for i in soup.find_all('img')), 'MATRIX screen mixed into AUTO')
    if route == '/faq': require(len(soup.select('details.faq-item')) == 8, 'FAQ count not8')
    errors += [route + ': ' + f for f in failures]
    results.append({'route':route,'status':response.status_code,'title':soup.title.get_text() if soup.title else '', 'h1_count':len(soup.find_all('h1')),'html_bytes':len(response.content),'issues':failures})
for route in ('/index.html','/mt','/features/','/auto/','/guide/','/faq/','/contact/','/healthz','/manus-routes.json'):
    if get(route).status_code != 200: errors.append('legacy/manifest failed: ' + route)
for route, target in [('/guide/matrix','/guide?system=matrix'),('/guide/matrix/','/guide?system=matrix'),('/guide/auto','/guide?system=auto'),('/guide/auto/','/guide?system=auto')]:
    r = get(route)
    if r.status_code != 301 or r.headers.get('Location') != target: errors.append('redirect failed: ' + route)
for route in ('/does-not-exist','/assets/no-image.png','/.env','/%2e%2e/Cargo.toml'):
    if get(route).status_code != 404: errors.append('404/traversal failed: ' + route)
if requests.post(BASE + '/', timeout=30).status_code != 405: errors.append('POST should be405')
if 'Disallow: /' not in get('/robots.txt').text: errors.append('robots staging protection absent')
report = {'origin':BASE,'pages':results,'internal_urls_checked':len(visited),'errors':errors,'passed':not errors}
(ROOT / 'docs/http-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2) + '\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
sys.exit(1 if errors else 0)
