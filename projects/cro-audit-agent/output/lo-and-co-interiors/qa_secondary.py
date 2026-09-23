"""Independent safe interaction QA for collection, full cart and policy."""
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from playwright.sync_api import sync_playwright
OUT = Path(__file__).resolve().parent
home = json.loads((OUT / 'qa-home-desktop.json').read_text(encoding='utf-8'))
product = next(x['url'] for x in home['links'] if '/products/' in x['url'])
collection = next(x['url'] for x in home['links'] if '/collections/new' in x['url'])
policy = next(x['url'] for x in home['links'] if x['text'] == 'Shipping & Returns')
with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={'width':1440,'height':1000})
    page.add_locator_handler(page.get_by_role('button', name='Close dialog', exact=True), lambda locator: locator.click())
    def capture(name):
        d = {'url':page.url,'captured_at':datetime.now(timezone.utc).isoformat(),'text':page.locator('body').inner_text(), 'controls':page.locator('button, input, select, [role=button]').evaluate_all('els=>els.filter(e=>e.checkVisibility()).map(e=>({tag:e.tagName,text:e.innerText,type:e.type,aria:e.getAttribute("aria-label"),html:e.outerHTML.slice(0,1500)}))')}
        (OUT / f'qa-{name}.json').write_text(json.dumps(d,indent=2),encoding='utf-8')
        page.screenshot(path=str(OUT / f'qa-{name}.png'), full_page=True)
        return d
    page.goto(collection,wait_until='domcontentloaded',timeout=60000)
    page.wait_for_timeout(6000)
    filter_control = page.get_by_text(re.compile('^filter$', re.I)).filter(visible=True)
    print('Visible FILTER controls',filter_control.count())
    if filter_control.count():
        filter_control.first.click()
        page.wait_for_timeout(1000)
    d=capture('filters-open')
    print('Filter controls',json.dumps(d['controls'],ensure_ascii=True)[:7000])
    page.goto(policy,wait_until='domcontentloaded',timeout=60000)
    page.wait_for_timeout(4000)
    for name in ['Returns', 'Shipping Costs']:
        control = page.get_by_role('button', name=name, exact=True)
        if control.count():
            control.first.click()
            page.wait_for_timeout(400)
            capture('policy-' + name.lower().replace(' ', '-'))
    d=capture('shipping-returns')
    print('Policy',d['text'][-7000:].encode('ascii',errors='backslashreplace').decode())
    page.goto(product,wait_until='domcontentloaded',timeout=60000)
    page.wait_for_timeout(4000)
    page.get_by_role('button',name='ADD TO BAG',exact=False).first.click()
    page.wait_for_timeout(2000)
    view_bag = page.get_by_role('link',name=re.compile('^view bag$', re.I))
    if not view_bag.count():
        page.get_by_role('button', name='Open the shopping cart summary modal', exact=True).filter(visible=True).first.click()
    view_bag.click()
    page.wait_for_timeout(3000)
    d=capture('full-cart')
    print('Full cart',d['text'][-5000:].encode('ascii',errors='backslashreplace').decode())
    b.close()
