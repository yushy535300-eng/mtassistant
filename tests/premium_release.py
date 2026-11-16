"""Build-time link graph and SEO contracts for the complete published site."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,re,xml.etree.ElementTree as ET,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from sitegen.portal.articles import ARTICLES
PUBLIC=ROOT/'public'
ROUTES={'/':'index.html',**{'/'+p:'pages/'+p+'.html' for p in ('features','auto','guide','download','faq','contact','articles')},**{'/articles/'+a['slug']:'pages/article-'+a['slug']+'.html' for a in ARTICLES}}
ORIGIN='https://mtassistant-oozm.onrender.com'
class Document(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.h1=0;self.attrs=[];self.links=[];self.refs=[];self.schemas=[];self.script=False;self.buf=''
 def handle_starttag(self,t,attrs):
  a=dict(attrs);self.attrs.append((t,a))
  if a.get('id'):self.ids.append(a['id'])
  if t=='h1':self.h1+=1
  if t=='a' and a.get('href'):self.links.append(a['href'])
  if a.get('aria-controls'):self.refs+=a['aria-controls'].split()
  if t=='script' and a.get('type')=='application/ld+json':self.script=True;self.buf=''
 def handle_endtag(self,t):
  if t=='script' and self.script:self.schemas+=json.loads(self.buf);self.script=False
 def handle_data(self,d):
  if self.script:self.buf+=d
 def meta(self,name):return [a['content'] for t,a in self.attrs if t=='meta' and a.get('name')==name]
 def canonical(self):return [a['href'] for t,a in self.attrs if t=='link' and a.get('rel')=='canonical']
docs={}
for route,path in ROUTES.items():
 s=(PUBLIC/path).read_text();d=Document();d.feed(s);docs[route]=d
 assert d.h1==1,(route,'h1',d.h1)
 assert len(d.ids)==len(set(d.ids)),(route,'duplicate IDs')
 assert set(d.refs)<=set(d.ids),(route,'broken ARIA',set(d.refs)-set(d.ids))
 assert d.canonical()==[ORIGIN+route],(route,'canonical',d.canonical())
 assert d.meta('robots')==['index,follow'],(route,'indexing',d.meta('robots'))
 assert len(d.meta('description'))==1 and len(d.meta('description')[0])>=35,(route,'description')
 for tag,a in d.attrs:
  if tag in ('img','source','script','link'):
   src=a.get('src') or (a.get('href') if a.get('rel') in ('stylesheet','icon','apple-touch-icon','preload') else None)
   if src and src.startswith('/') and src!='/favicon.png':assert (PUBLIC/src.split('?')[0].lstrip('/')).is_file(),(route,'missing asset',src)
 for schema in d.schemas:
  if schema['@type']=='Article':
   assert schema['mainEntityOfPage']==ORIGIN+route
   assert schema['headline'] in s and schema['author']['name'] in s
   assert len(schema['headline'])>10
 for src in re.findall(r"url\(['\"]?([^)'\"]+)",s):
  if src.startswith('/'):assert (PUBLIC/src.lstrip('/').split('?')[0]).exists(),src
for route,d in docs.items():
 for href in d.links:
  u=urlsplit(href)
  if u.scheme or u.netloc:continue
  path=u.path or route
  if path not in ROUTES:
   assert (PUBLIC/path.lstrip('/')).is_file() or path in ('/mt','/index.html'),(route,'unresolved link',href)
  elif u.fragment:
   assert unquote(u.fragment) in docs[path].ids,(route,'unresolved anchor',href)
locs=[x.text for x in ET.parse(PUBLIC/'sitemap.xml').findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
assert set(locs)=={ORIGIN+r for r in ROUTES},('sitemap',locs)
assert len(locs)==len(set(locs))
for a in ARTICLES:
 schema=next(x for x in docs['/articles/'+a['slug']].schemas if x['@type']=='Article')
 assert len(a['sections'])>=4
css=(PUBLIC/'site.css').read_text()
assert 'yc-letter-glint' not in css and 'yc-metal-sweep' not in css and 'yc-button-sweep' not in css,'obsolete sweep stylesheet compiled'
assert 'animation:none;transform:none;opacity:1' in css,'hero beam not disabled'
assert 'premium-enter' in css and 'prefers-reduced-motion' in css
err=Document();err.feed((PUBLIC/'pages/404.html').read_text());assert 'noindex' in err.meta('robots')[0]
print(f'Premium release passed: {len(ROUTES)} indexable URLs, link graph, assets, heading/ARIA uniqueness, metadata, six Article schemas and sitemap.')
