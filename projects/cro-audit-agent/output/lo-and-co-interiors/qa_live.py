"""Independent live DOM QA capture; no model calls or personal-data submission."""
import json
from datetime import datetime, timezone
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent
HOME = json.loads((OUT / 'qa-home-desktop.json').read_text(encoding='utf-8'))
PRODUCT = next(x['url'] for x in HOME['links'] if '/products/' in x['url'])
COLLECTION = next(x['url'] for x in HOME['links'] if '/collections/new' in x['url'])


def dismiss(page):
    close = page.get_by_role('button', name='Close dialog', exact=True)
    if close.count() and close.first.is_visible():
        close.first.click()


def snapshot(page, label):
    dismiss(page)
    data = {'url': page.url, 'title': page.title(), 'captured_at': datetime.now(timezone.utc).isoformat(),
            'viewport': page.viewport_size, 'text': page.locator('body').inner_text(),
            'visible_controls': page.locator('button, a, select').evaluate_all('''els => els.filter(e => e.checkVisibility()).map(e => ({text:e.innerText, aria:e.getAttribute('aria-label'), href:e.href, tag:e.tagName}))''')}
    (OUT / f'qa-{label}.json').write_text(json.dumps(data, indent=2), encoding='utf-8')
    page.screenshot(path=str(OUT / f'qa-{label}.png'), full_page=True)
    return data


with sync_playwright() as p:
    browser = p.chromium.launch()
    for device, viewport in [('desktop', {'width': 1440, 'height': 1000}), ('mobile', {'width': 390, 'height': 844})]:
        context = browser.new_context(viewport=viewport, is_mobile=device == 'mobile', has_touch=device == 'mobile')
        page = context.new_page()
        page.add_locator_handler(page.get_by_role('button', name='Close dialog', exact=True), lambda locator: locator.click())
        page.goto(HOME['url'], wait_until='domcontentloaded', timeout=60000)
        page.wait_for_timeout(5000)
        dismiss(page)
        snapshot(page, f'home-{device}-verified')
        search = page.get_by_role('button', name='Open search', exact=True).filter(visible=True)
        if search.count():
            search.first.click()
            page.wait_for_timeout(700)
            inputs = page.locator('input').filter(visible=True)
            candidates = inputs.evaluate_all('els => els.map(e=>({type:e.type, placeholder:e.placeholder, html:e.outerHTML}))')
            (OUT / f'qa-search-inputs-{device}.json').write_text(json.dumps(candidates, indent=2), encoding='utf-8')
            search_input = page.locator('input[type=search], input[placeholder*="earch"]').filter(visible=True)
            if search_input.count():
                search_input.first.fill('Hubble')
                page.wait_for_timeout(2500)
                snapshot(page, f'search-{device}')
        page.goto(COLLECTION, wait_until='domcontentloaded', timeout=60000)
        page.wait_for_timeout(4000)
        dismiss(page)
        page.evaluate('window.scrollTo(0, 650)')
        snapshot(page, f'collection-{device}')
        page.goto(PRODUCT, wait_until='domcontentloaded', timeout=60000)
        page.wait_for_timeout(4000)
        dismiss(page)
        add = page.get_by_role('button', name='ADD TO BAG', exact=False).first
        top = add.bounding_box()
        page.evaluate('window.scrollTo(0, 1400)')
        page.wait_for_timeout(1000)
        after = add.bounding_box()
        (OUT / f'qa-atc-position-{device}.json').write_text(json.dumps({'viewport': viewport, 'initial': top, 'after_scroll': after, 'scroll_y': page.evaluate('window.scrollY')}), encoding='utf-8')
        for name in ['Specifications', 'Shipping & Returns', 'Warranty']:
            button = page.get_by_role('button', name=name, exact=True)
            if button.count():
                button.first.click()
                page.wait_for_timeout(400)
        snapshot(page, f'product-expanded-{device}')
        add.click()
        page.wait_for_timeout(2500)
        cart_button = page.get_by_role('button', name='Open the shopping cart summary modal', exact=True).filter(visible=True)
        # Only open if the add action did not already open the cart.
        cart_text = page.locator('body').inner_text()
        if 'Subtotal' not in cart_text and 'SUBTOTAL' not in cart_text and cart_button.count():
            cart_button.first.click()
            page.wait_for_timeout(1000)
        cart = snapshot(page, f'cart-{device}')
        print(device, 'captured; cart text ending:', cart['text'][-2500:].encode('ascii', errors='backslashreplace').decode())
        context.close()
    browser.close()
