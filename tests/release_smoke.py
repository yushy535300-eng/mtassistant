"""Verify the Rust release binary serves embedded assets without a public directory."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parent.parent
BINARY = ROOT / 'target/release/mtassistant-official'
PORT = int(os.environ.get('SMOKE_PORT', '3101'))
paths = ['/healthz', '/', '/guide?system=auto', '/site.css', '/assets/baccarat-logo.png', '/manus-storage/async-images/QIFZssPyOpL8IvxDiTwerQ/image-1.webp']
rows = []
with tempfile.TemporaryDirectory(prefix='yuce-embedded-smoke-') as directory:
    env = dict(os.environ, PORT=str(PORT), DEV_FILES='false', ALLOW_INDEXING='false')
    process = subprocess.Popen([str(BINARY)], cwd=directory, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for attempt in range(30):
            try:
                with urllib.request.urlopen(f'http://127.0.0.1:{PORT}/healthz', timeout=1) as response:
                    if response.status == 200:
                        break
            except (OSError, urllib.error.URLError):
                time.sleep(0.1)
        for path in paths:
            with urllib.request.urlopen(f'http://127.0.0.1:{PORT}{path}', timeout=5) as response:
                content = response.read()
                rows.append({'path':path,'status':response.status,'bytes':len(content),'noindex':'noindex' in response.headers.get('X-Robots-Tag','')})
        result = {'mode':'embedded release','public_directory_present':False,'checks':rows,'passed':all(row['status']==200 and row['bytes']>0 and (row['path']=='/healthz' or row['noindex']) for row in rows)}
        (ROOT / 'docs/release-smoke.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
        print(json.dumps(result,ensure_ascii=False,indent=2))
        assert result['passed']
    finally:
        process.terminate()
        try:
            process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
