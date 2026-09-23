"""Rendered evidence collection. Screenshots are saved, never interpreted."""
import json
from datetime import datetime, timezone
from pathlib import Path

EXTRACT = r"""() => [...document.querySelectorAll('h1,h2,h3,a,button,input,select,option,label,summary,video,iframe,img,p,li,dt,dd,table,[role],form,section,article,header,footer,nav,[class*="price"],[class*="review"],[class*="badge"],[class*="shipping"],[class*="payment"],[class*="product-info"],[class*="description"]')].filter(e => {const r=e.getBoundingClientRect();return r.width>0&&r.height>0&&getComputedStyle(e).visibility!=='hidden'}).map(e=>{const r=e.getBoundingClientRect();const s=getComputedStyle(e);return {tag:e.tagName.toLowerCase(),id:e.id,classes:String(e.className||''),role:e.getAttribute('role'),text:(e.innerText||e.getAttribute('alt')||'').trim().slice(0,2500),label:e.getAttribute('aria-label'),href:e.getAttribute('href'),src:e.getAttribute('src'),type:e.getAttribute('type'),name:e.getAttribute('name'),action:e.getAttribute('action'),position:s.position,rect:{x:r.x,y:r.y,width:r.width,height:r.height,documentY:r.y+scrollY},context:(e.parentElement?.innerText||'').trim().slice(0,1200),outer:e.outerHTML.slice(0,1500)}})"""


def snapshot(page, name, folder):
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    screenshot = folder / f'{name}.png'
    page.screenshot(path=str(screenshot), full_page=True, timeout=30000)
    data = {'name':name, 'url':page.url, 'captured_at':datetime.now(timezone.utc).isoformat(),
            'viewport':page.viewport_size, 'scrollY':page.evaluate('scrollY'),
            'document_height':page.evaluate('document.documentElement.scrollHeight'),
            'title':page.title(), 'screenshot':str(screenshot.resolve()),
            'elements':page.evaluate(EXTRACT)}
    (folder / f'{name}.json').write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
    return data


def interact(page, name, locator, folder, verify, fill=None):
    from playwright.sync_api import Error
    record = {'name':name, 'url':page.url, 'clicked':False, 'success':False}
    try:
        target = locator.first
        if not target.count() or not target.is_visible():
            record['reason'] = 'No visible unambiguous interaction target'
        else:
            record['target'] = {'text':target.inner_text(), 'outer':target.evaluate('(e)=>e.outerHTML'), 'rect':target.bounding_box()}
            if fill is None:
                target.click(timeout=7000)
            else:
                target.fill(fill, timeout=7000)
            record['clicked'] = True
            page.wait_for_timeout(1800)
            record['success'] = bool(verify())
            record['after'] = snapshot(page, name, folder)
            if not record['success']:
                record['reason'] = 'Action completed but expected outcome not verified'
    except Error:
        record['reason'] = 'Interaction failed or timed out; no absence inferred'
    (Path(folder) / f'{name}-interaction.json').write_text(json.dumps(record,indent=2,ensure_ascii=False),encoding='utf-8')
    return record


def collect(url, folder, context=None):
    from playwright.sync_api import sync_playwright
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    result = {'status':'ok', 'blocked':False, 'visits':[], 'snapshots':{}, 'interactions':{}}
    if context is None:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            ctx = browser.new_context()
            result = collect(url, folder, ctx)
            browser.close()
            return result
    import re
    from urllib.parse import urljoin, urlparse
    page = context.new_page()

    def save():
        (folder / 'manifest.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')

    def load(target, name):
        data = visit(page,target,name,folder)
        result['visits'].append({'url':target,'name':name,'status':data['status'],'blocked':data['blocked']})
        if data['blocked']:
            result.update(status='could not audit',blocked=True)
            save()
            raise RuntimeError('Active site restriction; audit stopped')
        if data['status'] == 'ok':
            result['snapshots'][name] = data
        return data

    def action(name, locator, verify, fill=None):
        item = interact(page,name,locator,folder,verify,fill)
        result['interactions'][name] = item
        if item.get('after'):
            result['snapshots'][name] = item['after']
        save()
        return item

    def dismiss():
        close = page.get_by_role('button',name='Close dialog',exact=True)
        if close.count() and close.first.is_visible():
            close.first.click()

    def links(data, path):
        return list(dict.fromkeys(urljoin(url,e['href']) for e in data.get('elements',[]) if e.get('href') and path in e['href'] and urlparse(urljoin(url,e['href'])).netloc == urlparse(url).netloc))

    try:
        for device, viewport in [('desktop',{'width':1440,'height':1000}),('mobile',{'width':390,'height':844})]:
            page.set_viewport_size(viewport)
            home = load(url,device+'-home')
            if home['status'] != 'ok':
                result['status'] = 'could not audit'
                break
            products = links(home,'/products/')[:3]
            collections = links(home,'/collections/')[:1]
            result.setdefault('discovered',{})[device] = {'products':products,'collections':collections}
            dismiss()
            search = page.get_by_role('button',name=re.compile('open search',re.I))
            action(device+'-search-open',search,lambda:page.locator('input[type="search"]:visible,input[placeholder*="Search"]:visible').count()>0)
            search_input = page.locator('input[type="search"]:visible,input[placeholder*="Search"]:visible')
            before = page.locator('a[href*="/products/"]:visible').count()
            action(device+'-search-type',search_input,lambda:page.locator('a[href*="/products/"]:visible').count()!=before,fill='Hubble')
            page.keyboard.press('Escape')
            for target in collections:
                collection = load(target,device+'-collection')
                dismiss()
                before_urls = page.locator('a[href*="/products/"]:visible').evaluate_all('(es)=>es.map(e=>e.href).join()')
                filters = page.locator('button.action:visible').filter(has_text=re.compile('^MARBLE$',re.I))
                if not filters.count():
                    filters = page.get_by_role('button',name=re.compile('filter',re.I))
                action(device+'-filter',filters,lambda:page.locator('a[href*="/products/"]:visible').evaluate_all('(es)=>es.map(e=>e.href).join()')!=before_urls)
                if not products:
                    products = links(collection,'/products/')[:3]
            for index, target in enumerate(products):
                name = device+'-product'+('' if index==0 else f'-{index+1}')
                data = load(target,name)
                if data['status'] != 'ok':
                    continue
                dismiss()
                if index:
                    continue
                for section in ('Specifications','Shipping & Returns','Warranty'):
                    control = page.get_by_role('button',name=section,exact=True)
                    action(device+'-'+section.split()[0].lower(),control,lambda c=control:c.get_attribute('aria-expanded')=='true')
                result['snapshots'][device+'-product-details'] = snapshot(page,device+'-product-details',folder)
                page.evaluate('scrollTo(0,0)')
                image = page.locator('img.w-100:visible').first
                action(device+'-zoom',image,lambda:page.locator('[class*="lightbox"]:visible,[class*="zoom"]:visible,[role="dialog"]:visible').count()>0)
                page.keyboard.press('Escape')
                load(target,device+'-product')
                dismiss()
                page.evaluate('scrollTo(0,innerHeight*2)')
                page.wait_for_timeout(500)
                result['snapshots'][device+'-product-scroll'] = snapshot(page,device+'-product-scroll',folder)
                add = page.get_by_role('button',name=re.compile(r'add to (bag|cart)',re.I))
                action(device+'-add-cart',add,lambda:page.get_by_text('Subtotal',exact=True).is_visible() and page.get_by_role('link',name='View Bag',exact=True).is_visible())
                bag = page.get_by_role('button',name=re.compile('open the shopping cart',re.I))
                if not result['interactions'][device+'-add-cart']['success']:
                    action(device+'-cart-open',bag,lambda:page.get_by_text('Subtotal',exact=True).is_visible() and page.get_by_role('link',name='View Bag',exact=True).is_visible())
                result['snapshots'][device+'-cart'] = snapshot(page,device+'-cart',folder)
                cart_link = page.get_by_role('link',name='View Bag',exact=True)
                if cart_link.count() and cart_link.is_visible():
                    load(urljoin(url,cart_link.get_attribute('href')),device+'-cart-full')
    except RuntimeError:
        pass
    finally:
        save()
        page.close()
    return result


def visit(page, url, name, folder):
    from playwright.sync_api import Error
    try:
        response = page.goto(url, wait_until='domcontentloaded', timeout=45000)
        page.wait_for_timeout(2000)
        status = response.status if response else 0
        title = page.title().lower()
        blocked = status in (401,403,429) or any(x in title for x in ('just a moment', 'access denied', 'robot verification'))
        if blocked:
            return {'status':'could not audit', 'blocked':True, 'reason':f'Active access restriction: HTTP {status}; stopped', 'url':url}
        if status >= 400:
            return {'status':'could not audit', 'blocked':False, 'reason':f'HTTP {status}', 'url':url}
        for y in range(0, min(page.evaluate('document.documentElement.scrollHeight'), 18000), 700):
            page.evaluate('(y) => scrollTo(0,y)', y)
            page.wait_for_timeout(120)
        page.evaluate('scrollTo(0,0)')
        page.wait_for_timeout(500)
        data = snapshot(page, name, folder)
        data.update(status='ok', blocked=False, http_status=status)
        return data
    except Error as exc:
        return {'status':'could not audit', 'blocked':False, 'reason':type(exc).__name__ + ': navigation/render failed', 'url':url}
