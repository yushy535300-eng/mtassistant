"""Publish one pre-reviewed, due article per run; make no external model/API calls."""
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT=Path(__file__).resolve().parents[1]/"sitegen"/"portal"
queue=json.loads((ROOT/"editorial_queue.json").read_text(encoding="utf-8"))
published_path=ROOT/"editorial_published.json"
published=json.loads(published_path.read_text(encoding="utf-8"))
known={a["slug"] for a in published}
today=datetime.now(ZoneInfo("Asia/Taipei")).date().isoformat()
due=sorted((a for a in queue if a["publish_at"]<=today and a["slug"] not in known),key=lambda a:a["publish_at"])
if not due:
    print("No new approved article due for publication.")
else:
    post=due[0].copy()
    if len(post.get("sections",[]))<4 or not post.get("title") or not post.get("summary"):
        raise SystemExit("Editorial quality gate: incomplete article")
    post["published_at"]=today
    published.append(post)
    published_path.write_text(json.dumps(published,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("Published: "+post["slug"])
