import os,re,glob,json,collections
from bs4 import BeautifulSoup
BASE="https://jopetnahinternationallimited.github.io/jopetnah-corporate-site/"
files=sorted(glob.glob('*.html'))
ids={}
soups={}
for f in files:
    s=BeautifulSoup(open(f,encoding='utf-8',errors='replace').read(),'html.parser'); soups[f]=s
    ids[f]={t.get('id') for t in s.find_all(id=True)}
res=collections.defaultdict(list)
titles=collections.defaultdict(list); descs=collections.defaultdict(list)
for f,s in soups.items():
    if f.startswith('google'): continue
    t=s.title.string.strip() if s.title and s.title.string else None
    d=(s.find('meta',attrs={'name':'description'}) or {}).get('content')
    c=(s.find('link',rel='canonical') or {}).get('href')
    robots=(s.find('meta',attrs={'name':'robots'}) or {}).get('content')
    if not t: res['no_title'].append(f)
    else: titles[t].append(f)
    if not d: res['no_desc'].append(f)
    else:
        descs[d].append(f)
        if len(d)>165: res['desc_long'].append((f,len(d)))
    if not c: res['no_canonical'].append(f)
    elif c!=BASE+f and f!='index.html': res['canonical_mismatch'].append((f,c))
    if not s.html or not s.html.get('lang'): res['no_lang'].append(f)
    h1=s.find_all('h1')
    if len(h1)!=1: res['h1_count'].append((f,len(h1)))
    if not s.find('main'): res['no_main'].append(f)
    if not s.find('meta',attrs={'name':'viewport'}): res['no_viewport'].append(f)
    if not s.find('meta',property='og:image'): res['no_og_image'].append(f)
    if not s.find('script',type='application/ld+json'): res['no_jsonld'].append(f)
    # headings skipping
    lv=[int(h.name[1]) for h in s.find_all(re.compile('^h[1-6]$'))]
    for a,b in zip(lv,lv[1:]):
        if b-a>1: res['heading_skip'].append(f); break
    for img in s.find_all('img'):
        if img.get('alt') is None: res['img_no_alt'].append((f,img.get('src')))
        if not img.get('width') or not img.get('height'): res['img_no_dims'].append(f)
        if not img.get('loading') and not img.get('fetchpriority'): res['img_no_lazy'].append(f)
    for a in s.find_all('a',target='_blank'):
        rel=a.get('rel') or []
        if 'noopener' not in rel and 'noreferrer' not in rel: res['blank_no_noopener'].append((f,a.get('href')))
    for a in s.find_all('a',href=True):
        h=a['href'].strip()
        if h.startswith(('mailto:','tel:','javascript:')) : 
            if h=='#' or h.startswith('javascript:'): res['bad_href'].append((f,h))
            continue
        if h.startswith(('http://','https://')):
            if h.startswith('http://'): res['http_link'].append((f,h))
            if h.startswith(BASE):
                p=h[len(BASE):]; path,_,frag=p.partition('#')
                path=path or 'index.html'
                if not os.path.exists(path): res['broken_internal_abs'].append((f,h))
                elif frag and path.endswith('.html') and frag not in ids.get(path,set()): res['broken_anchor'].append((f,h))
            continue
        if h.startswith('#'):
            if len(h)>1 and h[1:] not in ids[f]: res['broken_anchor'].append((f,h))
            continue
        path,_,frag=h.partition('#'); path=path.split('?')[0]
        if not path: continue
        if not os.path.exists(path): res['broken_internal'].append((f,h))
        elif frag and path.endswith('.html') and frag not in ids.get(path,set()): res['broken_anchor'].append((f,h))
    for tag,attr in (('img','src'),('link','href'),('script','src'),('source','srcset')):
        for e in s.find_all(tag):
            v=e.get(attr)
            if v and not v.startswith(('http','data:','#','//')) and not os.path.exists(v.split('?')[0].split(' ')[0]): res['missing_asset'].append((f,v))
    # aria / form
    for inp in s.find_all(['input','textarea','select']):
        if inp.get('type') in ('hidden','submit'): continue
        i=inp.get('id'); 
        if not (inp.get('aria-label') or (i and s.find('label',attrs={'for':i}))): res['input_no_label'].append((f,inp.get('name')))
# sitemap compare
sm=set(re.findall(r'<loc>(.*?)</loc>',open('sitemap.xml').read()))
smf={u[len(BASE):] for u in sm}
pub={f for f in files if not f.startswith('google') and f not in('404.html',)}
res['sitemap_missing_files']=[u for u in smf if not os.path.exists(u)]
res['pages_not_in_sitemap']=sorted(pub-smf)
res['dup_titles']=[(t,fs) for t,fs in titles.items() if len(fs)>1]
res['dup_desc']=[(d[:50],fs) for d,fs in descs.items() if len(fs)>1]
res['noindex']=[f for f,s in soups.items() if (s.find('meta',attrs={'name':'robots'}) or {}).get('content','').find('noindex')>-1]
for k,v in res.items():
    if k in('img_no_dims','img_no_lazy'): v=sorted(set(v)) ; print(k,len(v),"pages", v[:6]); continue
    print(f"{k}: {len(v)}"); 
    for x in list(v)[:8]: print("   ",x)
