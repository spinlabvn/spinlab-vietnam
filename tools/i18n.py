"""Vietnamese -> English page translation by exact-match dictionary (data/en.json).

Units that get translated (keys are whitespace-normalised):
  - "rich" blocks: inner HTML of <p>/<li>/<td>/<dd>/<h1-6>/<summary>/<figcaption> that mixes text with inline tags
    (<strong>, <a>, <b>, <em>, <br>, <small>, <span>) — translated as a whole sentence, markup included;
  - plain text nodes;
  - attributes alt / aria-label / title / placeholder / data-alt and <meta name="description"> content;
  - string literals inside <script> (JSON data, UI messages).
Strings with Vietnamese letters are reported when missing; dictionary hits are used for any string. translate() returns (html, missing_keys).
"""
import html as H
import re

VI = re.compile('[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ'
                'ÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ]')
norm = lambda s: ' '.join(s.split())
INLINE = r'(?:strong|a|b|em|i|br|small|span|sup|sub|code)'
RICH = re.compile(r'(<(p|li|td|dd|dt|th|h[1-6]|summary|figcaption)\b[^>]*>)((?:(?!</?(?:p|li|ul|ol|div|section|table|h[1-6]|td|th|tr)\b).)*?<' + INLINE + r'\b(?:(?!</?(?:p|li|ul|ol|div|section|table|h[1-6]|td|th|tr)\b).)*?)(</\2>)', re.S)
ATTR = re.compile(r'(\b(?:alt|aria-label|title|placeholder|data-alt)=")([^"]*)(")')
META = re.compile(r'(<meta name="description" content=")([^"]*)(")')
SCRIPT = re.compile(r'(<script\b[^>]*>)(.*?)(</script>)', re.S)
STYLE = re.compile(r'<style\b[^>]*>.*?</style>', re.S)
JSSTR = re.compile(r'"((?:[^"\\\n]|\\.)*)"|\'((?:[^\'\\\n]|\\.)*)\'')
TEXT = re.compile(r'>([^<>]+)<')
# patterns whose numbers change with the data (prices, counts, dates)
RULES = [(re.compile(r'Từ ([\d.]+₫)'), r'From \1'),
         (re.compile(r'(\d+) sản phẩm'), r'\1 products'), (re.compile(r'(\d+) mẫu xe'), r'\1 models'),
         (re.compile(r'(\d+) điểm bán'), r'\1 stores'), (re.compile(r'(\d+) lựa chọn'), r'\1 options'),
         (re.compile(r'Đăng ngày (\d\d/\d\d/\d{4})'), r'Listed \1'),
         (re.compile(r'Các phiên bản trong dòng (<b>[^<]*</b>): ((?:(?![àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]).)*)', re.S),
          r'Versions in the \1 range: \2')]


def rule(key):
    for rx, rep in RULES:
        if rx.fullmatch(key):
            return rx.sub(rep, key)
    return None


def translate(page, d, collect_all=False):
    missing = []

    def look(raw, unescape=True):
        key = norm(H.unescape(raw) if unescape else raw)
        if collect_all:
            if re.search(r'[^\W\d_]', key):
                missing.append(key)
            return None
        if key in d:          # also Vietnamese without diacritics, e.g. "Xem ngay"
            return d[key]
        r = rule(key)
        if r is not None:
            return r
        if VI.search(raw):
            missing.append(key)
        return None

    # protect <style> and <script> while handling markup
    keep = []

    def stash(m):
        keep.append(m.group(0))
        return f'\x00{len(keep) - 1}\x00'
    s = STYLE.sub(stash, page)

    def script(m):
        body = JSSTR.sub(lambda q: _js(q, look), m.group(2))
        keep.append(m.group(1) + body + m.group(3))
        return f'\x00{len(keep) - 1}\x00'
    s = SCRIPT.sub(script, s)

    def rich(m):   # whole sentence with its inline markup; protected from the text-node pass either way
        t = look(m.group(3), unescape=False)
        keep.append(m.group(0) if t is None else m.group(1) + t + m.group(4))
        return f'\x00{len(keep) - 1}\x00'
    s = RICH.sub(rich, s)
    s = META.sub(lambda m: m.group(1) + H.escape(look(m.group(2)) or H.unescape(m.group(2)), quote=True) + m.group(3), s)
    s = ATTR.sub(lambda m: m.group(1) + H.escape(look(m.group(2)) or H.unescape(m.group(2)), quote=True) + m.group(3), s)

    def text(m):
        raw = m.group(1)
        t = look(raw)
        if t is None:
            return m.group(0)
        lead = raw[:len(raw) - len(raw.lstrip())]
        trail = raw[len(raw.rstrip()):]
        return '>' + lead + H.escape(t, quote=False) + trail + '<'
    s = TEXT.sub(text, s)
    s = re.sub('\x00(\\d+)\x00', lambda m: keep[int(m.group(1))], s)
    return s, missing


def _js(q, look):
    raw = q.group(1) if q.group(1) is not None else q.group(2)
    quote = '"' if q.group(1) is not None else "'"
    if not raw:
        return q.group(0)
    t = look(raw, unescape=False)
    if t is None:
        return q.group(0)
    esc = t.replace('\\', '\\\\').replace(quote, '\\' + quote)
    return quote + esc + quote


def units(fragment):
    """Translatable units of an HTML fragment, in document order (same segmentation as translate)."""
    return translate(fragment, {}, collect_all=True)[1]


def pairs(vi_html, en_html):
    """Dictionary entries from a Vietnamese fragment and its English version with the same structure."""
    a, b = units(vi_html), units(en_html)
    return dict(zip(a, b)) if len(a) == len(b) else {}
