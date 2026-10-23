"""Spinlab admin — local website editor (this Mac only).

    python3 tools/admin.py            -> http://127.0.0.1:8770/admin  (also serves the site for preview)

Edits the data files the build uses:
  data/articles.json      articles (Tin tức / Hướng dẫn), with their English version
  data/page-prices.json   prices of bikes and Emume products;  data/vittoria-stock.json  Vittoria prices per SKU
  data/hidden.json        hidden products;  data/overrides.json  product texts (VI + EN)
"Cập nhật bản xem trước" runs the build; "Đăng lên web" builds, commits and pushes to GitHub.
Only listens on 127.0.0.1; API calls must carry the X-Spinlab-Admin header (blocks requests from other web pages).
"""
import base64, datetime, glob, html, json, os, re, subprocess, sys, threading, webbrowser
from http.server import ThreadingHTTPServer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, 'tools')
sys.path.insert(0, TOOLS)
sys.path.insert(0, os.path.join(TOOLS, 'generators'))
import serve, apply_overrides, i18n  # noqa: E402

PORT = next((int(a) for a in sys.argv[1:] if a.isdigit()), 8770)
DATA = lambda f: os.path.join(ROOT, 'data', f)
LOCK = threading.Lock()
STEPS = ['build_articles.py', 'apply_overrides.py', 'apply_hidden.py', 'build_new_products.py', 'apply_prices.py',
         'build_compare.py', 'card_hover.py', 'brand_logos.py', 'build_hubs.py', 'clean_urls.py', 'build_en.py']
SLUG = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')


def jload(name, default):
    p = DATA(name)
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else default


def jsave(name, obj):
    with open(DATA(name), 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)


def text(s):
    return ' '.join(html.unescape(re.sub(r'<[^>]+>', '', s)).split())


def page_html(f):
    for p in (os.path.join(ROOT, f), os.path.join(TOOLS, 'hidden-pages', f)):
        if os.path.exists(p):
            return open(p, encoding='utf-8').read()
    return ''


def products():
    global EN
    EN = jload('en.json', {})
    prices = jload('page-prices.json', {'prices': {}})['prices']
    stock = {i['sku']: i for i in jload('vittoria-stock.json', {'items': []})['items']}
    hidden = set(jload('hidden.json', {'pages': []})['pages'])
    over = jload('overrides.json', {'pages': {}})['pages']
    files = set(apply_overrides.product_pages()) | {os.path.basename(f) for f in glob.glob(os.path.join(TOOLS, 'hidden-pages', '*.html'))}
    out = []
    for f in sorted(files):
        s = page_html(f)
        main = re.search(r'<main id="main".*?</main>', s, re.S)
        m = main.group(0) if main else s
        name = text(re.search(r'<h1>(.*?)</h1>', m, re.S).group(1)) if '<h1>' in m else f
        brand = re.search(r'<span class="p-brand">(.*?)</span>', m, re.S)
        if f in prices or f.startswith(('polygon-', 'story-')):
            price = {'kind': 'page', 'value': prices.get(f)}
        else:
            skus = sorted(set(re.findall(r'data-sku="([^"]+)"', m)) | set(re.findall(r'"sku": "([^"]+)"', s)))
            price = {'kind': 'sku', 'skus': [{'sku': k, 'name': stock[k]['name'], 'price': stock[k]['price']} for k in skus if k in stock]}
        cur = apply_overrides.extract(s)
        tr = lambda t: EN.get(i18n.norm(t), '')
        cur_en = {'tagline': tr(cur['tagline']), 'heading': tr(cur['heading']), 'intro': [tr(x) for x in cur['intro']],
                  'features': [[tr(a), tr(b)] for a, b in cur['features']]}
        o = over.get(f)
        out.append({'file': f, 'name': name, 'brand': text(brand.group(1)) if brand else '', 'hidden': f in hidden,
                    'price': price, 'texts': cur, 'texts_en': cur_en, 'override': o})
    return out


def state():
    arts = jload('articles.json', {'articles': []})['articles']
    for a in arts:
        en = a.get('en') or {}
        a['_en_body_ok'] = (not en.get('body')) or len(i18n.units(a['body'])) == len(i18n.units(en['body']))
    st = subprocess.run(['git', 'status', '--porcelain'], cwd=ROOT, capture_output=True, text=True).stdout
    ahead = subprocess.run(['git', 'rev-list', '--count', 'origin/main..main'], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    pages = sorted(p[:-5] for p in os.listdir(ROOT) if p.endswith('.html'))
    return {'articles': arts, 'products': products(), 'pages': pages, 'settings': jload('settings.json', {'show_prices': True}),
            'git': {'changed': len([l for l in st.splitlines() if l.strip()]), 'ahead': int(ahead or 0)}}


def save_articles(arts):
    pages = {p[:-5] for p in os.listdir(ROOT) if p.endswith('.html')}
    seen = set()
    clean = []
    for a in arts:
        slug = (a.get('slug') or '').strip()
        if not SLUG.match(slug):
            raise ValueError(f'Đường dẫn bài viết không hợp lệ: "{slug}" (chỉ dùng chữ thường không dấu, số và dấu gạch ngang)')
        if slug in seen:
            raise ValueError(f'Trùng đường dẫn bài viết: {slug}')
        existing_article = any(x.get('slug') == slug for x in jload('articles.json', {'articles': []})['articles'])
        if slug in pages and not existing_article:
            raise ValueError(f'Đường dẫn "{slug}" đang được một trang khác dùng')
        seen.add(slug)
        if a.get('cat') not in ('tin-tuc', 'huong-dan'):
            raise ValueError('Chuyên mục phải là Tin tức hoặc Hướng dẫn')
        for k in ('title', 'lead', 'body', 'date'):
            if not (a.get(k) or '').strip():
                raise ValueError(f'Bài "{a.get("title") or slug}" còn thiếu: {k}')
        datetime.date.fromisoformat(a['date'])
        en = {k: (a.get('en') or {}).get(k, '').strip() for k in ('tag', 'title', 'lead', 'body')}
        clean.append({'slug': slug, 'cat': a['cat'], 'tag': a.get('tag') or ('Tin tức' if a['cat'] == 'tin-tuc' else 'Hướng dẫn'),
                      'date': a['date'], 'title': a['title'].strip(), 'lead': a['lead'].strip(), 'image': a.get('image') or a.get('thumb') or '',
                      'thumb': a.get('thumb') or a.get('image') or '', 'body': a['body'].strip(),
                      'products': [[p[0], p[1] if len(p) > 1 else ''] for p in a.get('products', []) if p and p[0]],
                      'en': {k: v for k, v in en.items() if v}})
    d = jload('articles.json', {'articles': []})
    d['articles'] = clean
    jsave('articles.json', d)


def save_prices(page_prices, sku_prices):
    d = jload('page-prices.json', {'prices': {}})
    for f, v in page_prices.items():
        if v in (None, ''):
            d['prices'].pop(f, None)
        else:
            d['prices'][f] = int(v)
    jsave('page-prices.json', d)
    s = jload('vittoria-stock.json', {'items': []})
    for i in s['items']:
        if i['sku'] in sku_prices and sku_prices[i['sku']] not in (None, ''):
            i['price'] = int(sku_prices[i['sku']])
    jsave('vittoria-stock.json', s)


def save_texts(f, o):
    d = jload('overrides.json', {'note': 'Mô tả sản phẩm sửa từ trang quản lý (tools/apply_overrides.py).', 'pages': {}})
    if not o:
        d['pages'].pop(f, None)
    else:
        keep = {k: o[k] for k in ('tagline', 'heading', 'intro', 'features', 'en') if o.get(k)}
        d['pages'][f] = keep
    jsave('overrides.json', d)


def upload(name, data):
    raw = base64.b64decode(data.split(',', 1)[-1])
    base = re.sub(r'[^a-z0-9-]+', '-', os.path.splitext(name.lower())[0]).strip('-') or 'anh'
    os.makedirs(os.path.join(ROOT, 'img', 'articles'), exist_ok=True)
    tmp = os.path.join(ROOT, 'img', 'articles', base + '.upload')
    open(tmp, 'wb').write(raw)
    out = os.path.join(ROOT, 'img', 'articles', base + '.jpg')
    r = subprocess.run(['sips', '-s', 'format', 'jpeg', '-s', 'formatOptions', '82', '-Z', '1600', tmp, '--out', out], capture_output=True, text=True)
    os.remove(tmp)
    if r.returncode != 0:
        raise ValueError('Không đọc được ảnh (hãy dùng JPG, PNG, WEBP hoặc HEIC)')
    return 'img/articles/' + base + '.jpg'


def build():
    log = []
    for step in STEPS:
        r = subprocess.run([sys.executable, os.path.join(TOOLS, step)], cwd=ROOT, capture_output=True, text=True)
        log.append(f'$ {step}\n{(r.stdout + r.stderr).strip()}')
        if r.returncode != 0:
            raise RuntimeError('\n\n'.join(log))
    missing = open(os.path.join(TOOLS, 'en-missing.txt'), encoding='utf-8').read().strip()
    return '\n\n'.join(log), [l.split('\t', 1)[1] for l in missing.splitlines()] if missing else []


def publish(message):
    log, missing = build()
    run = lambda *a: subprocess.run(list(a), cwd=ROOT, capture_output=True, text=True)
    run('git', 'add', '-A')
    if run('git', 'diff', '--cached', '--quiet').returncode == 0 and int(state()['git']['ahead']) == 0:
        return log + '\n\nKhông có thay đổi nào để đăng.', missing
    msg = (message.strip() or 'Cập nhật nội dung từ trang quản lý') + '\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>'
    c = run('git', 'commit', '-q', '-m', msg)
    p = run('git', 'push', 'origin', 'main')
    if p.returncode != 0:
        raise RuntimeError(log + '\n\n' + c.stdout + c.stderr + '\n' + p.stdout + p.stderr)
    h = run('git', 'log', '--oneline', '-1').stdout.strip()
    return log + f'\n\nĐã đăng lên GitHub: {h}', missing


class Admin(serve.Handler):
    def _json(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = self.path.split('?')[0]
        if path in ('/admin', '/admin/'):
            body = open(os.path.join(TOOLS, 'admin', 'index.html'), 'rb').read()
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Cache-Control', 'no-store')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            return self.wfile.write(body)
        if path == '/api/state':
            if self.headers.get('X-Spinlab-Admin') != '1':
                return self._json(403, {'error': 'forbidden'})
            return self._json(200, state())
        return super().do_GET()

    def do_POST(self):
        if self.headers.get('X-Spinlab-Admin') != '1' or not self.path.startswith('/api/'):
            return self._json(403, {'error': 'forbidden'})
        n = int(self.headers.get('Content-Length') or 0)
        try:
            req = json.loads(self.rfile.read(n).decode('utf-8') or '{}')
            with LOCK:
                p = self.path
                if p == '/api/articles':
                    save_articles(req['articles'])
                    return self._json(200, {'ok': True})
                if p == '/api/prices':
                    save_prices(req.get('page_prices', {}), req.get('sku_prices', {}))
                    return self._json(200, {'ok': True})
                if p == '/api/hidden':
                    jsave('hidden.json', {'note': 'Sản phẩm đang ẩn (tools/apply_hidden.py).', 'pages': sorted(req['pages'])})
                    return self._json(200, {'ok': True})
                if p == '/api/texts':
                    save_texts(req['file'], req.get('override'))
                    return self._json(200, {'ok': True})
                if p == '/api/settings':
                    d = jload('settings.json', {'note': 'Cài đặt chung của website.'})
                    d['show_prices'] = bool(req['show_prices'])
                    jsave('settings.json', d)
                    return self._json(200, {'ok': True})
                if p == '/api/upload':
                    return self._json(200, {'path': upload(req['name'], req['data'])})
                if p == '/api/build':
                    log, missing = build()
                    return self._json(200, {'log': log, 'missing': missing})
                if p == '/api/publish':
                    log, missing = publish(req.get('message', ''))
                    return self._json(200, {'log': log, 'missing': missing})
            return self._json(404, {'error': 'not found'})
        except (ValueError, KeyError) as e:
            return self._json(400, {'error': str(e)})
        except Exception as e:  # build / git failures: show the log
            return self._json(500, {'error': str(e)})

    def log_message(self, *a):
        pass


if __name__ == '__main__':
    url = f'http://127.0.0.1:{PORT}/admin'
    srv = ThreadingHTTPServer(('127.0.0.1', PORT), Admin)
    print('Trang quản lý Spinlab:', url, '— đóng cửa sổ này để tắt.')
    if '--no-browser' not in sys.argv:
        threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    srv.serve_forever()
