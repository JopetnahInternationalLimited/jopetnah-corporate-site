import sys,os
from playwright.sync_api import sync_playwright
out=sys.argv[1]
pages=['index','contact','impact','sustainability','news']
with sync_playwright() as p:
    b=p.chromium.launch()
    for theme in ('light','dark'):
        for w in (375,1366):
            pg=b.new_context(viewport={'width':w,'height':900}).new_page()
            for f in pages:
                pg.goto(f'http://localhost:8765/{f}.html',wait_until='domcontentloaded')
                pg.evaluate(f"document.documentElement.setAttribute('data-theme','{theme}')")
                pg.evaluate("document.querySelectorAll('img').forEach(i=>i.loading='eager')")
                el=pg.locator('footer.site-footer'); el.scroll_into_view_if_needed(); pg.wait_for_timeout(700)
                el.screenshot(path=f'{out}/{f}_{theme}_{w}.png')
            pg.context.close()
    b.close()
print("shots",len(os.listdir(out)))
