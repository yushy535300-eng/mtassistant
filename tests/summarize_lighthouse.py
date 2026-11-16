import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
reports = []
for path in sorted((ROOT / 'docs/lighthouse').glob('*.report.json')):
    report = json.loads(path.read_text())
    scores = {key:round(value['score'] * 100) for key,value in report['categories'].items()}
    audits = report['audits']
    metrics = {key:audits[key].get('numericValue') for key in ('first-contentful-paint','largest-contentful-paint','total-blocking-time','cumulative-layout-shift','speed-index')}
    issues = {key:{'title':value['title'],'score':value.get('score'),'details':value.get('details')} for key,value in audits.items() if value.get('score') is not None and value.get('score',1) < 1 and value.get('scoreDisplayMode') not in ('informative','notApplicable')}
    reports.append({'name':path.name.replace('.report.json',''),'url':report['finalDisplayedUrl'],'fetchTime':report['fetchTime'],'lighthouseVersion':report['lighthouseVersion'],'scores':scores,'metrics':metrics,'issues':issues,'report':str(path.relative_to(ROOT))})
(ROOT / 'docs/lighthouse-summary.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2) + '\n')
for report in reports:
    print(report['name'], report['scores'], report['metrics'])
    print('Issues:', ', '.join(report['issues']))
    for key in ['color-contrast','link-name','image-alt','aria-valid-attr-value','aria-hidden-focus','target-size']:
        if key in report['issues']:
            print(key, json.dumps(report['issues'][key],ensure_ascii=False)[:2500])
