import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from playwright.sync_api import sync_playwright
import browser


def test_snapshot_records_visible_context_locations_and_scroll(tmp_path):
    with sync_playwright() as p:
        b = p.chromium.launch()
        page = b.new_page(viewport={'width':390,'height':844})
        page.set_content('<main><h1>Product</h1><button>Add to cart</button><a href="/products/test">Test</a><span hidden>Hidden</span></main>')
        data = browser.snapshot(page, 'mobile-product', tmp_path)
        assert data['viewport']['width'] == 390
        assert any(x['text'] == 'Add to cart' and x['rect']['width'] > 0 for x in data['elements'])
        assert not any(x['text'] == 'Hidden' for x in data['elements'])
        assert Path(data['screenshot']).exists()
        assert data['url'] == 'about:blank'
        b.close()


def test_interaction_captures_before_after_and_verifies_outcome(tmp_path):
    with sync_playwright() as p:
        b = p.chromium.launch()
        page = b.new_page()
        page.set_content('<button onclick="this.innerText=\'Opened\'">Open</button>')
        result = browser.interact(page, 'open', page.get_by_text('Open', exact=True), tmp_path,
                                  lambda: page.get_by_text('Opened', exact=True).count() == 1)
        assert result['clicked'] and result['success']
        assert 'Open' in result['target']['text']
        assert Path(result['after']['screenshot']).exists()
        b.close()


def test_collect_discovers_links_and_stops_after_block(tmp_path):
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context()
        ctx.route('https://example.test/**', lambda route: route.fulfill(status=403, body='Access denied'))
        result = browser.collect('https://example.test/', tmp_path, context=ctx)
        assert result['status'] == 'could not audit'
        assert result['blocked'] is True
        assert len(result['visits']) == 1
        b.close()


def test_collect_visits_rendered_links_both_viewports_and_cart(tmp_path):
    html = '''<main><a href="/products/test">Test</a><a href="/collections/new">New</a>
    <h1>Test product</h1><img class="w-100" style="width:100px;height:100px" alt="product image" onclick="document.getElementById('zoom').hidden=false"><div id="zoom" class="image-zoom" hidden>Zoomed image</div>
    <button class="action" onclick="document.getElementById('results').hidden=false">MARBLE</button>
    <button aria-label="Open search" onclick="document.getElementById('s').hidden=false">Search</button>
    <input id="s" type="search" hidden oninput="document.getElementById('results').hidden=false">
    <div id="results" hidden><a href="/products/test">Test result</a></div>
    <button onclick="document.getElementById('bag').hidden=false">Add to bag</button>
    <div id="bag" hidden><p>Shopping bag Test product</p><p>Subtotal</p><p>$44</p><a href="/cart">View Bag</a></div></main>'''
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context()
        ctx.route('https://example.test/**', lambda route: route.fulfill(body=html, content_type='text/html'))
        result = browser.collect('https://example.test/', tmp_path, context=ctx)
        assert result['status'] == 'ok'
        for device in ('desktop', 'mobile'):
            assert result['snapshots'][device+'-product']['url'] == 'https://example.test/products/test'
            assert result['snapshots'][device+'-collection']['url'] == 'https://example.test/collections/new'
            assert result['interactions'][device+'-add-cart']['success']
            assert result['interactions'][device+'-zoom']['success']
            assert result['interactions'][device+'-filter']['success']
            assert result['snapshots'][device+'-cart-full']['url'] == 'https://example.test/cart'
        b.close()


def test_visit_broken_url_is_graceful(tmp_path):
    with sync_playwright() as p:
        b = p.chromium.launch()
        page = b.new_page()
        result = browser.visit(page, 'http://127.0.0.1:1/', 'broken', tmp_path)
        assert result['status'] == 'could not audit'
        assert result['reason']
        b.close()


def test_visit_detects_active_block(tmp_path):
    with sync_playwright() as p:
        b = p.chromium.launch()
        page = b.new_page()
        page.route('https://example.test/', lambda route: route.fulfill(status=403, body='<h1>Access denied</h1>'))
        result = browser.visit(page, 'https://example.test/', 'blocked', tmp_path)
        assert result['blocked'] is True
        b.close()
