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


def translate(page, d):
    missing = []

    def look(raw, unescape=True):
        key = norm(H.unescape(raw) if unescape else raw)
        if key in d:          # also Vietnamese without diacritics, e.g. "Xem ngay"
            return d[key]
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
