"""Decorative real-person scene layers, not a dealer roster or live stream."""
import re
from pathlib import Path
from ..common import asset_url

PUBLIC = Path(__file__).resolve().parents[2] / 'public'
PAGE_PERSON = {
    'home': 'mt-real-01',
    'features': 'mt-real-02',
    'auto': 'mt-real-01',
    'guide': 'live5',
    'faq': 'live1',
    'contact': 'live2',
}


HOME_DEALERS = ('mt-real-01', 'mt-real-02', 'live1', 'live2', 'live3', 'live4', 'live5', 'live6')


def person(name, location='hero', eager=False):
    if name not in HOME_DEALERS:
        raise ValueError('Unknown scene asset')
    full = f'/assets/dealers/{name}-cutout.webp'
    mobile = f'/assets/dealers/{name}-cutout-mobile.webp'
    for path in (full, mobile):
        if not (PUBLIC / path.lstrip('/')).is_file():
            raise FileNotFoundError('Transparent scene asset is not ready: ' + path)
    sizes = {'mt-real-01': (415, 575), 'mt-real-02': (510, 545)}
    width, height = sizes.get(name, (626, 626))
    klass = 'brand-person' if location == 'brand' else f'scene-person scene-person-{location}'
    if name in sizes:
        klass += ' mt-original-dealer'
    return (
        f'<picture class="{klass}" aria-hidden="true">'
        f'<source media="(max-width:640px)" srcset="{asset_url(mobile)}">'
        f'<img src="{asset_url(full)}" width="{width}" height="{height}" alt="" '
        f'aria-hidden="true" loading="{"eager" if eager else "lazy"}" '
        f'decoding="async" fetchpriority="low"></picture>'
    )


def integrate(body, page):
    """Insert a noninteractive foreground into an existing first-section scene."""
    if page not in PAGE_PERSON:
        return body
    end = body.find('</section>')
    if end < 0:
        raise ValueError('Existing hero is missing: ' + page)
    head = body[:end]
    expected = 'portal-banner' if page == 'home' else 'portal-pagehead'
    if expected not in head:
        raise ValueError('Existing scene class is missing: ' + page)
    head, count = re.subn(
        r'(<section\b[^>]*class=")([^"]*)(")',
        lambda m: m.group(1) + m.group(2) + ' has-scene-person person-scene-' + page + m.group(3),
        head,
        count=1,
    )
    if count != 1:
        raise ValueError('Existing scene cannot be decorated: ' + page)
    foreground = person(PAGE_PERSON[page], page, eager=True)
    if page == 'home':
        slides = ''.join(person(name, page, eager=True) for name in HOME_DEALERS)
        foreground = '<div class="scene-person scene-person-home mt-dealer-rotation" aria-hidden="true" data-dealer-rotation>' + slides + '</div>'
        return head + foreground + body[end:]
    # The first div is the existing title/description, never the action group.
    intro_start = head.find('<div>')
    intro_end = head.find('</div>', intro_start)
    if intro_start < 0 or intro_end < 0:
        raise ValueError('Existing intro slot is missing: ' + page)
    head = head[:intro_end] + foreground + head[intro_end:]
    head = head[:intro_start] + head[intro_start:].replace('<div>', '<div class="scene-intro">', 1)
    return head + body[end:]
