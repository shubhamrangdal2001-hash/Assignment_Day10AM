# Part A - E-Commerce Product Catalog System
# Uses nested dicts, defaultdict, dict comprehensions

from collections import defaultdict

# ─────────────────────────────────────────────
# Product catalog with 15+ products, 4 categories
# ─────────────────────────────────────────────
catalog = {
    'SKU001': {'name': 'Laptop',          'price': 65000, 'category': 'electronics', 'stock': 15, 'rating': 4.5, 'tags': ['computer', 'work', 'portable']},
    'SKU002': {'name': 'Wireless Mouse',  'price': 1200,  'category': 'electronics', 'stock': 0,  'rating': 4.1, 'tags': ['computer', 'accessories']},
    'SKU003': {'name': 'Mechanical Keyboard','price': 3500,'category': 'electronics','stock': 8,  'rating': 4.7, 'tags': ['computer', 'work', 'accessories']},
    'SKU004': {'name': 'Noise Cancel Headphones','price':8500,'category':'electronics','stock':5, 'rating': 4.6, 'tags': ['audio', 'portable', 'work']},
    'SKU005': {'name': 'USB-C Hub',        'price': 1800,  'category': 'electronics', 'stock': 20, 'rating': 3.9, 'tags': ['computer', 'accessories', 'portable']},
    'SKU006': {'name': 'Men T-Shirt',      'price': 499,   'category': 'clothing',    'stock': 50, 'rating': 3.8, 'tags': ['casual', 'summer', 'cotton']},
    'SKU007': {'name': 'Denim Jeans',      'price': 1799,  'category': 'clothing',    'stock': 30, 'rating': 4.2, 'tags': ['casual', 'denim']},
    'SKU008': {'name': 'Winter Jacket',    'price': 3999,  'category': 'clothing',    'stock': 0,  'rating': 4.4, 'tags': ['winter', 'warm', 'outdoor']},
    'SKU009': {'name': 'Sports Shoes',     'price': 2500,  'category': 'clothing',    'stock': 12, 'rating': 4.0, 'tags': ['sports', 'outdoor', 'summer']},
    'SKU010': {'name': 'Python Programming','price': 599,  'category': 'books',       'stock': 25, 'rating': 4.8, 'tags': ['programming', 'education', 'tech']},
    'SKU011': {'name': 'Data Structures',  'price': 450,   'category': 'books',       'stock': 10, 'rating': 4.6, 'tags': ['programming', 'education', 'tech']},
    'SKU012': {'name': 'The Alchemist',    'price': 299,   'category': 'books',       'stock': 0,  'rating': 4.9, 'tags': ['fiction', 'bestseller']},
    'SKU013': {'name': 'Atomic Habits',    'price': 350,   'category': 'books',       'stock': 18, 'rating': 4.7, 'tags': ['self-help', 'bestseller', 'education']},
    'SKU014': {'name': 'Basmati Rice 5kg', 'price': 420,   'category': 'food',        'stock': 100,'rating': 4.3, 'tags': ['staple', 'grains', 'organic']},
    'SKU015': {'name': 'Olive Oil 1L',     'price': 750,   'category': 'food',        'stock': 45, 'rating': 4.5, 'tags': ['cooking', 'organic', 'healthy']},
    'SKU016': {'name': 'Green Tea Pack',   'price': 280,   'category': 'food',        'stock': 0,  'rating': 4.2, 'tags': ['beverages', 'healthy', 'organic']},
    'SKU017': {'name': 'Almonds 500g',     'price': 650,   'category': 'food',        'stock': 60, 'rating': 4.6, 'tags': ['snacks', 'healthy', 'organic']},
}


def search_by_tag(tag):
    """Returns all products that contain the given tag, grouped using defaultdict."""
    tag_map = defaultdict(list)
    for sku, details in catalog.items():
        for t in details.get('tags', []):
            tag_map[t].append({'sku': sku, 'name': details.get('name')})
    return tag_map.get(tag, [])


def out_of_stock():
    """Returns products where stock == 0 using dict comprehension."""
    return {
        sku: details
        for sku, details in catalog.items()
        if details.get('stock', 1) == 0
    }


def price_range(min_price, max_price):
    """Filters products within the given price range."""
    return {
        sku: details
        for sku, details in catalog.items()
        if min_price <= details.get('price', 0) <= max_price
    }


def category_summary():
    """Returns count, avg price, avg rating per category using defaultdict(list)."""
    groups = defaultdict(list)
    for details in catalog.values():
        cat = details.get('category', 'unknown')
        groups[cat].append(details)

    summary = {}
    for cat, items in groups.items():
        prices = [p.get('price', 0) for p in items]
        ratings = [r.get('rating', 0) for r in items]
        summary[cat] = {
            'count':      len(items),
            'avg_price':  round(sum(prices) / len(prices), 2),
            'avg_rating': round(sum(ratings) / len(ratings), 2),
        }
    return summary


def apply_discount(category, percent):
    """Reduces prices for all products in a category by the given percent."""
    multiplier = 1 - (percent / 100)
    return {
        sku: {**details, 'price': round(details.get('price', 0) * multiplier, 2)}
        if details.get('category') == category else {**details}
        for sku, details in catalog.items()
    }


def merge_catalogs(catalog1, catalog2):
    """Merges two catalogs. catalog2 values overwrite catalog1 on duplicate SKUs."""
    return {**catalog1, **catalog2}


# ─────────────────────────────────────────────
# Demo / Sample Output
# ─────────────────────────────────────────────
if __name__ == '__main__':
    print("=" * 55)
    print("  E-COMMERCE PRODUCT CATALOG SYSTEM")
    print("=" * 55)

    print("\n[1] search_by_tag('organic')")
    for item in search_by_tag('organic'):
        print(f"    {item}")

    print("\n[2] out_of_stock()")
    for sku, d in out_of_stock().items():
        print(f"    {sku}: {d['name']}")

    print("\n[3] price_range(300, 1000)")
    for sku, d in price_range(300, 1000).items():
        print(f"    {sku}: {d['name']} - Rs.{d['price']}")

    print("\n[4] category_summary()")
    for cat, stats in category_summary().items():
        print(f"    {cat}: {stats}")

    print("\n[5] apply_discount('books', 10)  — showing books only")
    discounted = apply_discount('books', 10)
    for sku, d in discounted.items():
        if d['category'] == 'books':
            print(f"    {sku}: {d['name']} → Rs.{d['price']}")

    print("\n[6] merge_catalogs — adding 2 new products")
    extra = {
        'SKU018': {'name': 'Smart Watch', 'price': 12000, 'category': 'electronics',
                   'stock': 7, 'rating': 4.3, 'tags': ['wearable', 'portable']},
        'SKU001': {'name': 'Laptop Pro (updated)', 'price': 72000, 'category': 'electronics',
                   'stock': 10, 'rating': 4.7, 'tags': ['computer', 'work']},
    }
    merged = merge_catalogs(catalog, extra)
    print(f"    Original catalog size : {len(catalog)}")
    print(f"    Merged catalog size   : {len(merged)}")
    print(f"    SKU001 after merge    : {merged['SKU001']['name']} @ Rs.{merged['SKU001']['price']}")
