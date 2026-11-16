"""Check named section/control/description references in initial HTML."""
import json
import os
from pathlib import Path
import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
ORIGIN = os.environ.get('TEST_ORIGIN', 'http://127.0.0.1:3000')
rows = []
for path in ['/', '/features', '/auto', '/guide?system=matrix', '/guide?system=auto', '/faq', '/contact']:
    soup = BeautifulSoup(requests.get(ORIGIN + path, timeout=10).text, 'html.parser')
    ids = {str(element.get('id')) for element in soup.find_all(id=True)}
    missing = []
    for element in soup.select('[aria-labelledby],[aria-controls],[aria-describedby]'):
        for attribute in ['aria-labelledby','aria-controls','aria-describedby']:
            for target in str(element.get(attribute, '')).split():
                if target not in ids:
                    missing.append({'element':element.name,'attribute':attribute,'target':target})
    rows.append({'page':path,'missing':missing})
(ROOT / 'docs/aria-reference-audit.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
print(json.dumps(rows,ensure_ascii=False,indent=2))
assert not any(row['missing'] for row in rows)
