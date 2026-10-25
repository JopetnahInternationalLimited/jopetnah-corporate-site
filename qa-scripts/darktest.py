import os,mimetypes,sys,collections
from playwright.sync_api import sync_playwright
axe=open('/home/claude/axe/node_modules/axe-core/axe.min.js').read()
BASE='https://jopetnahinternationallimited.github.io/jopetnah-corporate-site/'; ROOT='/home/claude/site/'
def handler(route):
    rel=route.request.url[len(BASE):].split('?')[0].split('#')[0] or 'index.html'; path=ROOT+rel
    route.fulfill(path=path,content_type=mimetypes.guess_type(path)[0] or 'text/plain') if os.path.isfile(path) else route.abort()
detail=len(sys.argv)>1
with sync_playwright() as p:
    b=p.chromium.launch()
    for theme,files in (('dark',['index.html','about.html','projects.html','services.html','contact.html']),('light',['news.html'])):
        ctx=b.new_context(viewport={'width':375,'height':812}); ctx.route(BASE+'**',handler); pg=ctx.new_page()
        for f in files:
            pg.goto('file://'+ROOT+f,wait_until='domcontentloaded'); pg.wait_for_timeout(350)
            pg.evaluate(f"document.documentElement.setAttribute('data-theme','{theme}')"); pg.add_script_tag(content=axe)
            r=pg.evaluate("axe.run(document,{runOnly:['wcag2aa'],rules:{'color-contrast':{enabled:true}}}).then(r=>r.violations.filter(v=>v.id==='color-contrast').flatMap(v=>v.nodes.map(n=>({h:n.html.slice(0,70).replace(/\\s+/g,' '),m:((n.any[0]||{}).message||'').slice(0,95)}))))")
            print(f"{theme} {f}: {len(r)}")
            if detail and r:
                for x in r[:3]: print("    ",x['h'],"|",x['m'])
        ctx.close()
    b.close()
