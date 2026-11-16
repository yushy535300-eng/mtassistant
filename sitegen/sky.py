"""One shared scene. It never owns the functional content or navigation."""
from .common import asset_url

DESKTOP = '/manus-storage/aurora-clean-desktop_f6812f6f.webp'
MOBILE = '/manus-storage/aurora-clean-mobile_e47e6270.webp'


def render():
    return f'''<div id="skyStage" class="sky-stage" aria-hidden="true" data-desktop="{asset_url(DESKTOP)}" data-mobile="{asset_url(MOBILE)}"><picture class="sky-art"><source media="(max-width:640px)" srcset="{asset_url(MOBILE)}"><img src="{asset_url(DESKTOP)}" width="1920" height="823" alt="" fetchpriority="high" decoding="async"></picture><div class="sky-fallback-light"></div><canvas id="auroraCanvas"></canvas><canvas id="starCanvas"></canvas><div class="sky-readability"></div></div><button id="motionToggle" class="motion-toggle" type="button" aria-pressed="false" hidden>暫停背景動態</button>'''
