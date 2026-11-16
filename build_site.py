"""Build all static pages offline. No database or secrets required."""
import gzip
import hashlib
import importlib
import json
import os
import re
from html import escape
from pathlib import Path
from sitegen.common import DATA, LINE, THREADS, asset_url, viewer
from sitegen.portal.articles import ARTICLES, BY_SLUG, PHOTO_ASSETS, render_article

portal_shell = importlib.import_module("sitegen.portal.shell")
scene_people = importlib.import_module("sitegen.portal.dealers")
scarab_ads = importlib.import_module("sitegen.portal.ads")



ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT / 'public'
ORIGIN = os.environ.get('SITE_ORIGIN', '').rstrip('/')
INDEXABLE = os.environ.get('ALLOW_INDEXING', 'false').lower() == 'true'
if INDEXABLE and not ORIGIN.startswith('https://'):
    raise SystemExit('ALLOW_INDEXING=true requires an explicit HTTPS SITE_ORIGIN')
PAGE_INFO = {
    'home': ('/', '御策百家輔助｜多桌牌路分析與自動下注工具介紹', '認識御策百家輔助的 MT MATRIX 多桌牌路分析與 MT AUTO 自動下注工具。查看真實產品介面、各自的操作教學與常見問題，了解工具用途與操作風險。', '首頁'),
    'features': ('/features', 'MT MATRIX 多桌百家輔助｜功能與牌路分析・御策百家', '了解 MT MATRIX 多桌雷達、平台連線、AI 綜合分析、V38 四式算牌與終值奇偶模型。查看真實操作介面及對應教學；分析資訊不保證下一局結果。', '多桌輔助'),
    'auto': ('/auto', 'MT AUTO 百家自動下注｜策略設定與執行紀錄・御策百家', '認識 MT AUTO 自動下注的推薦與配注、基本單注、停止時間、止損止盈和執行紀錄。依據真實介面了解設定流程，操作前請先閱讀說明並評估風險。', '自動下注'),
    'guide': ('/guide', '操作教學｜多桌輔助與自動下注使用流程・御策百家輔助', '分別閱讀 MT MATRIX 多桌輔助五步教學與 MT AUTO 自動下注六步教學。從帳號授權、平台連線到配注、停止條件與執行紀錄，逐項核對真實介面。', '操作教學'),
    'download': ('/download', '下載安裝教學｜多桌輔助・自動下注 iPhone／Android｜御策百家', '御策百家輔助手機下載安裝教學：選擇即時多桌牌路或百家樂自動下注，查看 iPhone Safari 與 Android Chrome 圖文步驟及對應程式入口。', '下載安裝'),
    'faq': ('/faq', '常見問題｜帳號授權、裝置與工具風險・御策百家輔助', '查詢御策百家輔助的帳號授權、瀏覽器與手機使用、兩套產品差異、自動下注設定及停止狀態。搜尋常見問題，了解牌路分析與策略無法保證獲利。', '常見問題'),
    'articles': ('/articles', '百家樂規則・路單教學・機率知識與御策程式指南｜御策百家', '認識百家樂莊閒和、點數與補牌規則、珠盤路與大路、機率觀念；同時閱讀 MT MATRIX 與 MT AUTO 真實程式的使用說明與操作教學。', '文章專區'),
    'contact': ('/contact', '客服中心｜LINE 操作支援與聯繫方式・御策百家輔助', '透過指定 LINE 客服聯繫御策百家輔助，取得帳號授權、連線及操作說明協助。聯繫前整理系統名稱、裝置、發生時間與錯誤截圖，請勿提供密碼。', '客服中心'),
}

def page(route, title, description, body, label, guide_system='matrix'):
    body = scene_people.integrate(body, route.strip('/') or 'home')
    if route not in ('/', '/404') and not route.startswith('/articles'):
        # Insert one compact ad after the existing first section, no new page or route.
        end = body.find('</section>')
        if end >= 0:
            body = body[:end+10] + scarab_ads.carousel('content', 1) + body[end+10:]
    body = '\n'.join(line.rstrip() for line in body.splitlines())
    absolute = ORIGIN + route if ORIGIN and route != '/404' else ''
    share_name = 'home'
    image = ORIGIN + '/assets/social/' + share_name + '.png' if ORIGIN else ''
    tags = ''
    if absolute:
        tags += f'<link rel="canonical" href="{escape(absolute)}"><meta property="og:url" content="{escape(absolute)}">'
    if image:
        tags += f'<meta property="og:image" content="{escape(image)}"><meta property="og:image:alt" content="御策百家輔助・{label}品牌分享圖"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:image" content="{escape(image)}">'
    schemas = [{'@context':'https://schema.org','@type':'WebPage','name':title,'description':description,'inLanguage':'zh-Hant'}]
    if ORIGIN:
        schemas[0]['url'] = absolute
        schemas.append({'@context':'https://schema.org','@type':'WebSite','@id':ORIGIN+'/#website','name':'御策百家輔助','url':ORIGIN + '/'})
        schemas.append({'@context':'https://schema.org','@type':'Organization','@id':ORIGIN+'/#organization','name':'御策百家輔助','url':ORIGIN+'/','logo':ORIGIN+'/assets/baccarat-logo.png','sameAs':[THREADS]})
        if route != '/':
            schemas.append({'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'首頁','item':ORIGIN + '/'},{'@type':'ListItem','position':2,'name':label,'item':absolute}]})
    if route == '/faq':
        schemas.append({'@context':'https://schema.org','@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for _,q,a in DATA['questions']]})
    if route in ('/features','/auto'):
        schemas.append({'@context':'https://schema.org','@type':'SoftwareApplication','name':'MT AUTO' if route == '/auto' else 'MT MATRIX','applicationCategory':'UtilitiesApplication','operatingSystem':'Web browser','description':description})
    if route == '/contact': schemas[0]['@type'] = 'ContactPage'
    if route == '/articles': schemas[0]['@type'] = 'CollectionPage'
    if route.startswith('/articles/'):
        a = BY_SLUG[route.rsplit('/',1)[1]]
        schemas.append({'@context':'https://schema.org','@type':'Article','headline':a['title'],'description':a['summary'],'inLanguage':'zh-Hant','mainEntityOfPage':absolute,'image':[ORIGIN+'/assets/social/home.png'] if ORIGIN else [],'datePublished':a.get('published_at','2026-11-17')+'T00:00:00+08:00','dateModified':a.get('published_at','2026-11-17')+'T00:00:00+08:00','author':{'@type':'Organization','name':'御策編輯團隊','url':ORIGIN+'/articles'},'publisher':{'@id':ORIGIN+'/#organization'}})
        for schema in schemas:
            if schema['@type']=='BreadcrumbList':
                schema['itemListElement']=[{'@type':'ListItem','position':1,'name':'首頁','item':ORIGIN+'/'},{'@type':'ListItem','position':2,'name':'文章專區','item':ORIGIN+'/articles'},{'@type':'ListItem','position':3,'name':a['title'],'item':absolute}]

    breadcrumb = '' if route == '/' else f'<nav class="wrap breadcrumb" aria-label="麵包屑"><a href="/">首頁</a><span aria-hidden="true">/</span><span aria-current="page">{label}</span></nav>'
    if route.startswith('/articles/'):
        breadcrumb = f'<nav class="wrap breadcrumb" aria-label="麵包屑"><a href="/">首頁</a><span aria-hidden="true">/</span><a href="/articles">文章專區</a><span aria-hidden="true">/</span><span aria-current="page">{escape(label)}</span></nav>'
    nojs = '''<noscript><style>.portal-topbar{position:static;height:auto;min-height:64px;flex-wrap:wrap;padding-block:8px}.portal-category{position:static}.header-inner{flex-wrap:wrap}.mobile-nav[hidden]{display:grid!important;position:static;flex-basis:100%;grid-template-columns:repeat(2,minmax(0,1fr));max-height:none;padding:9px 0;background:transparent;box-shadow:none;border:0}body.page-guide #guide-panel-matrix,body.page-guide #guide-panel-auto,body.page-guide #guide-preview-matrix,body.page-guide #guide-preview-auto,[role=tabpanel][hidden]{display:block!important}.menu-toggle,.header-motion,.focus-tabs{display:none!important}@media(min-width:981px){.mobile-nav[hidden]{display:none!important}}</style></noscript>'''
    robots = 'index,follow' if INDEXABLE and route != '/404' else 'noindex,nofollow,noarchive'
    preload = f'<link rel="preload" as="font" href="{asset_url("/assets/fonts/yuce-tc-regular.woff2")}" type="font/woff2" crossorigin>'
    schema_json = json.dumps(schemas,ensure_ascii=False).replace('</', '<\\/')
    page_footer = portal_shell.footer()
    body += portal_shell.welcome()
    document = f'''<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="theme-color" content="#0c0d0c"><title>{escape(title)}</title><meta name="description" content="{escape(description,quote=True)}"><meta name="robots" content="{robots}"><meta property="og:site_name" content="御策百家輔助"><meta property="og:title" content="{escape(title,quote=True)}"><meta property="og:description" content="{escape(description,quote=True)}"><meta property="og:type" content="{'article' if route.startswith('/articles/') else 'website'}"><meta property="og:locale" content="zh_TW"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{escape(title,quote=True)}"><meta name="twitter:description" content="{escape(description,quote=True)}">{tags}<link rel="icon" href="/favicon.png"><link rel="apple-touch-icon" href="/assets/baccarat-logo.png">{preload}<link rel="stylesheet" href="{asset_url('/site.css')}"><script src="{asset_url('/site.js')}" defer></script><script src="{asset_url('/portal.js')}" defer></script><script src="{asset_url('/refine.js')}" defer></script><script src="{asset_url('/v2.js')}" defer></script><script type="application/ld+json">{schema_json}</script>{nojs}</head><body class="page-{'article' if route.startswith('/articles/') else (route.strip('/') or 'home')}" data-guide-system="{guide_system}"><div class="portal-shell">{portal_shell.sidebar(route)}<div class="portal-main">{portal_shell.header(route)}<main id="main">{breadcrumb}{body}</main>{page_footer}</div></div>{portal_shell.bottomnav(route)}{scarab_ads.floating() if route != "/404" else ""}{viewer()}</body></html>
'''
    def contact_link(match):
        tag = match.group(0)
        if f'href="{LINE}"' in tag:
            marker = 'data-line-link'
        elif f'href="{THREADS}"' in tag:
            marker = 'data-threads-link'
        else:
            return tag
        tag = re.sub(r'\s+(?:target|rel|data-line-link|data-threads-link)="[^"]*"', '', tag)
        return tag[:-1] + f' {marker} target="_blank" rel="noopener noreferrer">'
    return re.sub(r'<a\b[^>]*>', contact_link, document)

def build():
    scarab_ads.ensure_assets()
    (PUBLIC / 'pages').mkdir(exist_ok=True)
    # Complete portal replacement: only the new source is rendered.
    css = [(ROOT / 'sitegen/portal/portal.css').read_text(), (ROOT / 'sitegen/portal/detail-polish.css').read_text(), (ROOT / 'sitegen/portal/dealers.css').read_text(), (ROOT / 'sitegen/portal/v2.css').read_text(), (ROOT / 'sitegen/portal/download.css').read_text(), (ROOT / 'sitegen/portal/motion.css').read_text(), (ROOT / 'sitegen/portal/ads.css').read_text(), (ROOT / 'sitegen/portal/atelier.css').read_text(), (ROOT / 'sitegen/portal/layout-fixes-20261117.css').read_text(), (ROOT / 'sitegen/portal/scarab-ad-layout.css').read_text(), (ROOT / 'sitegen/portal/mobile-corrections.css').read_text(), (ROOT / 'sitegen/portal/v5-finish.css').read_text()]
    minify = importlib.import_module('sitegen.css_build').minify
    # Preserve source readability; only the generated HTTP stylesheet is compressed.
    compiled_css = '\n'.join(css)
    for weight in ('regular', 'medium'):
        font = f'/assets/fonts/yuce-tc-{weight}.woff2'
        compiled_css = compiled_css.replace(f"url('{font}')", f"url('{asset_url(font)}')")
    for name in ('yuce-display-bold', 'yuce-ui-bold'):
        font = f'/assets/fonts/{name}.woff2'
        compiled_css = compiled_css.replace(f"url('{font}')", f"url('{asset_url(font)}')")
    (PUBLIC / 'site.css').write_text(minify(compiled_css))
    for module, (route, title, description, label) in PAGE_INFO.items():
        body = importlib.import_module('sitegen.portal.' + module).render()
        destination = PUBLIC / 'index.html' if route == '/' else PUBLIC / 'pages' / (module + '.html')
        destination.write_text(page(route, title, description, body, label), encoding='utf-8')
        if module == 'guide':
            auto_body = importlib.import_module('sitegen.portal.guide').render('auto')
            (PUBLIC / 'pages/guide-auto.html').write_text(page(route, title, description, auto_body, label, 'auto'), encoding='utf-8')
    for a in ARTICLES:
        route='/articles/'+a['slug']
        (PUBLIC/'pages'/('article-'+a['slug']+'.html')).write_text(page(route,a['title']+'｜御策百家知識專區',a['summary']+(' 本文介紹百家樂遊戲規則與知識，內容包含圖片、詳細說明與相關文章。' if a['slug'] in PHOTO_ASSETS else ' 依真實程式介面整理操作步驟，附相關圖文教學與客服入口。'),render_article(a['slug']),a['title']),encoding='utf-8')
    error_body = importlib.import_module('sitegen.portal.error').render()
    (PUBLIC / 'pages/404.html').write_text(page('/404', '找不到頁面｜御策百家輔助', '請確認網址，或返回御策百家輔助首頁繼續瀏覽。', error_body, '找不到頁面'), encoding='utf-8')
    urls = ''.join(f'<url><loc>{escape(ORIGIN + route)}</loc></url>' for route in [*[info[0] for info in PAGE_INFO.values()],*['/articles/'+a['slug'] for a in ARTICLES]]) if INDEXABLE else ''
    (PUBLIC / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + urls + '</urlset>\n')
    (PUBLIC / 'robots.txt').write_text('User-agent: *\n' + ('Allow: /\nSitemap: ' + ORIGIN + '/sitemap.xml\n' if INDEXABLE else 'Disallow: /\n'))
    routes = [{'path': info[0], 'title': info[3]} for info in PAGE_INFO.values()]
    routes += [{'path':'/articles/'+a['slug'],'title':a['title']} for a in ARTICLES]
    routes += [{'path':'/guide?system=matrix','title':'多桌輔助教學'},{'path':'/guide?system=auto','title':'自動下注教學'},{'path':'/mt','title':'多桌輔助舊入口'},{'path':'/index.html','title':'首頁舊入口'}]
    (PUBLIC / 'manus-routes.json').write_text(json.dumps({'routes':routes},ensure_ascii=False,indent=2) + '\n')
    assets = []
    gzip_assets = []
    for path in sorted(PUBLIC.rglob('*')):
        if path.is_file() and path.suffix != '.gz':
            relative = path.relative_to(PUBLIC).as_posix()
            assets.append(f'    ("/{relative}", include_bytes!("../public/{relative}")),')
            if path.suffix in ('.html', '.css', '.js', '.json', '.xml', '.txt'):
                path.with_name(path.name + '.gz').write_bytes(gzip.compress(path.read_bytes(), compresslevel=9, mtime=0))
                gzip_assets.append(f'    ("/{relative}", include_bytes!("../public/{relative}.gz")),')
    (ROOT / 'src/assets.rs').write_text('pub static ASSETS: &[(&str, &[u8])] = &[\n' + '\n'.join(assets) + '\n];\npub static GZIP_ASSETS: &[(&str, &[u8])] = &[\n' + '\n'.join(gzip_assets) + '\n];\n')
    manifest = {str(p.relative_to(PUBLIC)):hashlib.sha256(p.read_bytes()).hexdigest() for p in PUBLIC.rglob('*') if p.is_file()}
    (ROOT / 'docs/build-manifest.json').write_text(json.dumps(manifest,indent=2) + '\n')
    print('Built 14 indexable URLs, 2 tutorial states, sitemap and embedded Rust asset map.')

if __name__ == '__main__': build()
