"""Extract Vittoria 'Technology explained', technical chart (size/ETRTO/color/weight) and numbered tech features
from saved product HTML pages -> vtech.json"""
import sys, os, re, json, html
SRC, OUT = sys.argv[1], sys.argv[2]


def lines_of(path):
    t = open(path, encoding='utf-8', errors='ignore').read()
    t = re.sub(r'<script.*?</script>|<style.*?</style>', '', t, flags=re.S)
    return [l.strip() for l in html.unescape(re.sub(r'<[^>]+>', '\n', t)).split('\n') if l.strip()]


def parse(path):
    L = lines_of(path)
    d = {'tech_intro': '', 'chart': [], 'features': [], 'wide_rim': ''}
    if 'Technology explained' in L:
        i = L.index('Technology explained')
        d['tagline'], d['summary'] = L[i - 2], L[i - 1]
        d['tech_intro'] = L[i + 1] if L[i + 1] not in ('Technical chart', 'Specifications chart') else ''
    hdr = next((x for x in ('Technical chart', 'Specifications chart') if x in L), None)
    if hdr:
        i = L.index(hdr) + 1
        head = []
        while i < len(L) and L[i] in ('Size', 'ETRTO', 'Color', 'Weight', 'TPI', 'Casing', 'Compound', 'Bead'):
            head.append(L[i]); i += 1
        n = len(head)
        while i + n <= len(L) and re.match(r'^\d{2,3}x|^\d{3}x|^\d+(\.\d+)?x\d', L[i]):
            d['chart'].append(dict(zip(head, L[i:i + n]))); i += n
    if 'Wide rim optimization' in L:
        d['wide_rim'] = L[L.index('Wide rim optimization') + 1]
    # numbered features: '01', title, text, '02', ... (stop when numbering restarts)
    seen = set()
    for k, l in enumerate(L):
        if l == '01' and k + 2 < len(L) and not d['features']:
            j = k
            while j + 2 < len(L) and re.fullmatch(r'0\d', L[j]):
                title, text = L[j + 1], L[j + 2]
                if title in seen:
                    break
                seen.add(title)
                d['features'].append({'title': title, 'text': text})
                j += 3
            break
    return d


res = {}
for f in sorted(os.listdir(SRC)):
    if f.endswith('.html'):
        res[f[:-5]] = parse(os.path.join(SRC, f))
json.dump(res, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for h, d in res.items():
    print(f"{h:42} chart={len(d['chart']):2} feats={len(d['features'])} wide={'y' if d['wide_rim'] else '-'} | {[x['title'] for x in d['features']]}")
