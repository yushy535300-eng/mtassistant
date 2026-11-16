"""Decorative real-person scene layers, not a dealer roster or live stream."""
import re
from pathlib import Path
from ..common import asset_url

PUBLIC = Path(__file__).resolve().parents[2] / 'public'
PAGE_PERSON = {
    'home': 'live6',
    'features': 'live3',
    'auto': 'live4',
    'guide': 'live5',
    'faq': 'live1',
    'contact': 'live2',
}


def person(name, location='hero', eager=False):
    if name not in PAGE_PERSON.values():
        raise ValueError('Unknown scene asset')
    full = f'/assets/dealers/{name}-cutout.webp'
    mobile = f'/assets/dealers/{name}-cutout-mobile.webp'
    for path in (full, mobile):
        if not (PUBLIC / path.lstrip('/')).is_file():
            raise FileNotFoundError('Transparent scene asset is not ready: ' + path)
    return (
        f'<picture class="scene-person scene-person-{location}" aria-hidden="true">'
        f'<source media="(max-width:640px)" srcset="{asset_url(mobile)}">'
        f'<img src="{asset_url(full)}" width="626" height="626" alt="" '
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
        return head + foreground + body[end:]
    # The first div is the existing title/description, never the action group.
    intro_start = head.find('<div>')
    intro_end = head.find('</div>', intro_start)
    if intro_start < 0 or intro_end < 0:
        raise ValueError('Existing intro slot is missing: ' + page)
    head = head[:intro_end] + foreground + head[intro_end:]
    head = head[:intro_start] + head[intro_start:].replace('<div>', '<div class="scene-intro">', 1)
    return head + body[end:]
