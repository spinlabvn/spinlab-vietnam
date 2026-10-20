"""Vittoria retail prices and in-stock SKUs (from Spinlab's price list, data/vittoria-stock.json).
Only SKUs listed there are shown on the website; each SKU carries its own retail price."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_D = json.load(open(os.path.join(ROOT, 'data', 'vittoria-stock.json'), encoding='utf-8'))
STOCK = {i['sku']: i for i in _D['items']}


def ok(sku):
    return bool(sku) and sku in STOCK


def price(sku):
    return STOCK[sku]['price'] if ok(sku) else None


def fmt(n):
    return f'{n:,}'.replace(',', '.') + '₫'


def label(skus):
    """'1.400.000₫' for one price, 'Từ 1.345.000₫' when the SKUs have different prices."""
    ps = sorted({price(s) for s in skus if ok(s)})
    if not ps:
        return ''
    return fmt(ps[0]) if len(ps) == 1 else 'Từ ' + fmt(ps[0])
