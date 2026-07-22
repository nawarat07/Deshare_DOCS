import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HEADER = '''<header class="site-header">
        <a class="brand" href="index.html"><img src="logo.svg" alt="DeShare"><span class="brand-note">Evidence documentation</span></a>
        <div class="header-status"><span class="status-dot"></span>Chain data checked 2026-07-22</div>
        <button class="nav-toggle" type="button" data-nav-toggle aria-expanded="false" aria-label="Toggle documentation navigation">Menu</button>
    </header>'''
SIDEBAR = '''<aside class="sidebar" data-sidebar>
            <nav data-site-nav aria-label="Documentation"></nav>
        </aside>'''

def transform(text, key):
    if 'rel="icon"' not in text:
        text = text.replace(
            '<link rel="stylesheet" href="style.css">',
            '<link rel="icon" href="logo.svg" type="image/svg+xml">\n    <link rel="stylesheet" href="style.css">',
            1,
        )
    if 'src="site.js"' not in text:
        text = text.replace(
            '<link rel="stylesheet" href="style.css">',
            '<link rel="stylesheet" href="style.css">\n    <script src="site.js" defer></script>',
            1,
        )
    text = text.replace("<body>", f'<body data-page="{key}">', 1)
    text = re.sub(r"<header>.*?</header>", HEADER, text, count=1, flags=re.S)
    text = re.sub(r'<aside class="sidebar">.*?</aside>', SIDEBAR, text, count=1, flags=re.S)
    text = text.replace('<div class="layout">', '<div class="site-layout">', 1)
    return text


def upgrade(path, key):
    text = path.read_text(encoding="utf-8")
    text = transform(text, key)
    path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    for filename, key in (("terms.html", "terms"), ("privacy.html", "privacy")):
        upgrade(ROOT / filename, key)
    print("Updated legal page shells")
