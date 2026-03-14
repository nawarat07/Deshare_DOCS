import os
import glob
import re

# 1. Update 2-1-core-features.html
with open('2-1-core-features.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = re.sub(
    r'<div class="feature-card">\s*<h4>New Listings</h4>\s*<p class="subtitle">Discover newly listed tokenized stocks\.</p>\s*<p>Capture initial market momentum by securing critically early access to newly listed tokenized stocks and emerging, high-growth market opportunities\. Seamlessly explore these diverse new assets as they incrementally become available—all actively facilitated within a singular, highly secure decentralized trading environment\.</p>\s*</div>',
    '<div class="feature-card">\n          <h4>IPO Investing</h4>\n          <p class="subtitle">Participate in exclusive IPO allocations.</p>\n          <p>Access early cornerstone allocations historically reserved strictly for institutional investors. Our protocol aggregates capital and participates via structured SPVs, tokenizing the underlying equity exposure to enable transparent, fractional, and global accessibility.</p>\n        </div>',
    text
)

with open('2-1-core-features.html', 'w', encoding='utf-8') as f:
    f.write(text)

# 2. Update 2-2-product-suite.html buttons
with open('2-2-product-suite.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace(
    '<a href="3-architecture.html" class="nav-button">Next Section: System Architecture →</a>',
    '<a href="2-3-ipo-investing.html" class="nav-button">Next Section: 2.3 IPO Investing →</a>'
)

with open('2-2-product-suite.html', 'w', encoding='utf-8') as f:
    f.write(text)

# 3. Update 3-architecture.html buttons
with open('3-architecture.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace(
    '<a href="2-2-product-suite.html" class="nav-button">← Prev: 2.2 The Deshare Solution</a>',
    '<a href="2-3-ipo-investing.html" class="nav-button">← Prev: 2.3 IPO Investing</a>'
)

with open('3-architecture.html', 'w', encoding='utf-8') as f:
    f.write(text)

# 4. Update sidebars in all HTML files
html_files = glob.glob('*.html')
if '2-3-ipo-investing.html' in html_files:
    html_files.remove('2-3-ipo-investing.html')

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    if '2-3-ipo-investing.html' not in text:
        text = text.replace(
            '<a href="2-2-product-suite.html" class="sub-link">2.2 The Deshare Solution</a>\n        </div>',
            '<a href="2-2-product-suite.html" class="sub-link">2.2 The Deshare Solution</a>\n          <a href="2-3-ipo-investing.html" class="sub-link">2.3 IPO Investing</a>\n        </div>'
        )
        text = text.replace(
            '<a href="2-2-product-suite.html" class="sub-link active">2.2 The Deshare Solution</a>\n        </div>',
            '<a href="2-2-product-suite.html" class="sub-link active">2.2 The Deshare Solution</a>\n          <a href="2-3-ipo-investing.html" class="sub-link">2.3 IPO Investing</a>\n        </div>'
        )
        
        with open(file, 'w', encoding='utf-8') as f:
            f.write(text)

print("Updates applied successfully.")
