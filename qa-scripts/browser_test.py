import glob,json,os
from playwright.sync_api import sync_playwright
root='/home/claude/site'
pages=sorted(os.path.basename(f) for f in glob.glob(root+'/*.html') if 'google' not in f)
axe=open('/home/claude/axe/node_modules/axe-core/axe.min.js').read()
R={'overflow':[],'console':[],'failed_local':[],'axe':{}}
key=['index.html','about.html','services.html','contact.html','projects.html','impact.html','governance.html','404.html']
with sync_playwright() as p:
    b=p.chromium.launch()
    for name,w,h in [('mobile',375,812),('tablet',820,1180),('desktop',1366,900)]:
        ctx=b.new_context(viewport={'width':w,'height':h}); pg=ctx.new_page()
        errs=[];fails=[]
        pg.on('console',lambda m:errs.append((pg.url.split('/')[-1],m.text[:120])) if m.type=='error' else None)
        pg.on('pageerror',lambda e:errs.append((pg.url.split('/')[-1],'pageerror '+str(e)[:100])))
        pg.on('requestfailed',lambda r:fails.append((pg.url.split('/')[-1],r.url[:90])) if 'localhost' in r.url else None)
        for f in pages:
            try:
                pg.goto(f'http://localhost:8765/{f}',wait_until='domcontentloaded',timeout=15000); pg.wait_for_timeout(250)
                ov=pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
                if ov>1: R['overflow'].append((name,f,ov))
                if name=='mobile' and f in key:
                    pg.add_script_tag(content=axe)
                    r=pg.evaluate("axe.run(document,{runOnly:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}).then(r=>r.violations.map(v=>({id:v.id,impact:v.impact,n:v.nodes.length})))")
                    R['axe'][f]=r
            except Exception as e: R['console'].append((name,f,'NAV '+str(e)[:80]))
        R['console']+= [(name,)+e for e in errs]; R['failed_local']+=[(name,)+e for e in fails]
        ctx.close()
    # small-target check on index mobile
    ctx=b.new_context(viewport={'width':375,'height':812}); pg=ctx.new_page(); pg.goto('http://localhost:8765/index.html'); pg.wait_for_timeout(300)
    R['small_targets']=pg.evaluate("""[...document.querySelectorAll('a,button,input,select,textarea')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&r.height>0&&(r.width<24||r.height<24)&&getComputedStyle(e).display!=='none'}).map(e=>(e.tagName+' '+(e.textContent||e.getAttribute('aria-label')||'').trim().slice(0,25)+' '+Math.round(e.getBoundingClientRect().width)+'x'+Math.round(e.getBoundingClientRect().height))).slice(0,12)""")
    R['menu_toggle']=pg.evaluate("(()=>{const t=document.querySelector('[aria-controls],.nav-toggle,.menu-toggle,button[aria-expanded]');return t?{tag:t.outerHTML.slice(0,160)}:null})()")
    b.close()
R["console"]=[c for c in R["console"] if "NAME_NOT_RESOLVED" not in str(c)]
print(json.dumps({k:R[k] for k in R},indent=0)[:6000])
