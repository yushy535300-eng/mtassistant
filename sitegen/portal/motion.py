"""Real, complete MT MATRIX recordings in one responsive media section."""
from html import escape
from ..common import asset_url, arrow

BASE = "/assets/mt-real"
VIDEOS = (
    ("mt-login-full", "01", "登入與程式介面", "原始登入流程", "00:04", 472, 960, "原始錄影無聲"),
    ("mt-gameplay-full", "02", "多桌牌路實際操作", "桌台、牌面與分析面板", "00:20", 440, 960, "原聲"),
    ("mt-model-full", "03", "實際牌局與模型", "牌局變化、模型與操作介面", "00:21", 472, 960, "原聲"),
)

def _video(item):
    name, number, title, detail, duration, width, height, audio = item
    source = asset_url(f"{BASE}/{name}.mp4")
    poster = asset_url(f"{BASE}/{name}.webp")
    return f'''<article class="mt-video-card">
      <div class="mt-video-frame">
        <video class="mt-full-video" controls playsinline preload="metadata" width="{width}" height="{height}" poster="{poster}" aria-label="{escape(title, quote=True)}">
          <source src="{source}" type="video/mp4">
          你的瀏覽器不支援影片播放。<a href="{source}">開啟原始影片</a>
        </video>
      </div>
      <div class="mt-video-caption">
        <div class="mt-video-meta"><span>MT MATRIX · {number}</span><span>{duration} · {audio}</span></div>
        <h3>{escape(title)}</h3>
        <p>{escape(detail)}</p>
      </div>
    </article>'''

def home_videos():
    cards = "".join(_video(item) for item in VIDEOS)
    return f'''<section class="portal-section mt-original-videos" id="mt-videos" aria-labelledby="mt-videos-title">
      <div class="section-top mt-videos-heading">
        <div><p class="kicker">MT MATRIX / 實際操作</p><h2 id="mt-videos-title">真實程式操作，一次看懂。</h2><p>完整保留原始錄影，點擊播放，可調整音量及全螢幕觀看。</p></div>
        <a class="text-link" href="/features">查看多桌輔助 {arrow()}</a>
      </div>
      <div class="mt-video-grid">{cards}</div>
    </section>'''
