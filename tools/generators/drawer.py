import glob,sys,os
D=sys.argv[1]
CSS='''/* Mobile menu drawer */
.nav-head,.nav-backdrop{display:none}
@media (max-width:1023px){
  .nav{display:block;position:fixed;top:0;left:0;bottom:0;width:min(86vw,360px);z-index:60;background:#fff;border:0;overflow-y:auto;overscroll-behavior:contain;transform:translateX(-100%);visibility:hidden;transition:transform .25s ease,visibility 0s linear .25s;box-shadow:0 0 40px rgba(0,0,0,.2)}
  body.nav-open .nav{transform:none;visibility:visible;transition:transform .25s ease}
  body.nav-open{overflow:hidden}
  .nav-head{display:flex;align-items:center;justify-content:space-between;min-height:60px;padding:0 8px 0 20px;background:var(--brand-yellow);font-weight:800;text-transform:uppercase;letter-spacing:.04em}
  .nav-close{display:grid;place-items:center;width:44px;height:44px;border:0;background:none;border-radius:var(--radius);font-size:28px;line-height:1;color:var(--text)}
  .nav-backdrop{display:block;position:fixed;inset:0;z-index:55;background:rgba(0,0,0,.45);opacity:0;visibility:hidden;transition:opacity .25s,visibility 0s linear .25s}
  body.nav-open .nav-backdrop{opacity:1;visibility:visible;transition:opacity .25s}
  .nav .container{padding:0}
  .nav .container>ul{flex-direction:column;gap:0}
  .nav .container>ul>li{border-bottom:1px solid var(--line)}
  .nav .container>ul>li>a,.nav-top{width:100%;justify-content:space-between;min-height:54px;padding:0 20px;border:0}
  .nav a:hover{border-bottom-color:transparent}
  .nav .sub{position:static;display:none;opacity:1;visibility:visible;transform:none;min-width:0;border:0;border-radius:0;box-shadow:none;padding:0 0 10px;background:var(--surface)}
  .nav-top[aria-expanded="true"]+.sub{display:block}
  .has-sub:hover .nav-top{border-bottom-color:transparent;color:inherit}
  .nav-top[aria-expanded="true"]{color:var(--brand-red)}
  .has-sub:hover .nav-top svg{transform:none}
  .nav-top[aria-expanded="true"] svg{transform:rotate(180deg)}
  .nav .sub a{min-height:46px}
  .fly-top{min-height:46px;font-weight:600}
  .fly-top svg{display:none}
  .has-fly:hover>.fly-top,.fly-top[aria-expanded="true"]{background:none;color:inherit}
  .fly{position:static;opacity:1;visibility:visible;transform:none;min-width:0;border:0;border-radius:0;box-shadow:none;padding:0 0 6px 16px;background:none}
  .nav .fly a{min-height:42px;font-size:14px}
  .nav .sub-brands{min-width:0;padding:4px 16px 16px}
}
'''
JS='''// Mobile menu drawer: ☰ opens the menu as a side panel; Escape, the backdrop, ✕ or a link closes it
(() => {
  const btn=document.querySelector('.menu-btn'), nav=document.querySelector('.nav');
  if(!btn||!nav) return;
  nav.id=nav.id||'site-nav'; btn.setAttribute('aria-controls',nav.id);
  const head=document.createElement('div'); head.className='nav-head';
  head.innerHTML='<span>Menu</span><button class="nav-close" type="button" aria-label="Đóng menu">×</button>';
  nav.prepend(head);
  const bd=document.createElement('div'); bd.className='nav-backdrop'; nav.after(bd);
  const mq=matchMedia('(max-width:1023px)');
  const set=open=>{ document.body.classList.toggle('nav-open',open); btn.setAttribute('aria-expanded',String(open)); btn.setAttribute('aria-label',open?'Đóng menu':'Mở menu');
    if(mq.matches) nav.toggleAttribute('inert',!open);
    if(open) head.querySelector('.nav-close').focus(); };
  btn.addEventListener('click',()=>set(!document.body.classList.contains('nav-open')));
  head.querySelector('.nav-close').addEventListener('click',()=>{ set(false); btn.focus(); });
  bd.addEventListener('click',()=>set(false));
  nav.addEventListener('click',e=>{ if(e.target.closest('a')) set(false); });
  document.addEventListener('keydown',e=>{ if(e.key==='Escape'&&document.body.classList.contains('nav-open')){ set(false); btn.focus(); } });
  const sync=()=>{ if(mq.matches){ nav.toggleAttribute('inert',!document.body.classList.contains('nav-open')); } else { set(false); nav.removeAttribute('inert'); } };
  mq.addEventListener('change',sync); sync();
})();
'''
n=0;miss=[]
for f in glob.glob(os.path.join(D,'*.html')):
    if f.endswith('v1-premium.html'): continue
    s=open(f,encoding='utf-8').read()
    if '/* Mobile menu drawer */' in s: continue
    if '</script>\n</body>' not in s or '.menu-btn' not in s: miss.append(f); continue
    s=s.replace('</style>',CSS+'</style>',1)
    i=s.rindex('</script>\n</body>'); s=s[:i]+JS+s[i:]
    open(f,'w',encoding='utf-8').write(s); n+=1
print(n,miss)
