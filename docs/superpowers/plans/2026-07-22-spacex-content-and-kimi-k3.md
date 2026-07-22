# SpaceX Content Restoration and Kimi K3 Expansion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restore the complete SpaceX offering pages and expand the bilingual Kimi offering with official K3 context, the 2026-07-23–2026-07-28 subscription window, internal-market liquidity risk, and a conditional 6–12 month post-listing lock-up.

**Architecture:** Import the two long-form SpaceX page bodies and their page-specific styles from Git commit `a0ccc1d` into dedicated content assets, then let the existing generator wrap those bodies in the shared evidence-first shell. Keep Kimi copy in `scripts/build_docs.py`, with official Kimi facts and operator-disclosed offering terms visually and semantically separated.

**Tech Stack:** Python 3 standard library, static HTML/CSS/JavaScript, `unittest`, Git, Playwright CLI.

## Global Constraints

- Preserve all substantive SpaceX English and Chinese content from commit `a0ccc1d`; do not summarize or rewrite it.
- Preserve the current shared navigation, responsive shell, favicon, and evidence-first documentation styling.
- Refer to the new model as `Kimi K3`, released 2026-07-16, using only official Kimi sources for model facts.
- State the subscription window as 2026-07-23 through 2026-07-28 without inventing start/end times or a timezone.
- State that DeShare plans to open internal platform trading after subscription completion, but low liquidity means orders and trades are not guaranteed to complete.
- State that a public listing would normally trigger a 6–12 month lock-up whose exact terms depend on the listing structure and post-listing official announcements.
- Do not promise an IPO, exact unlock date, external-market liquidity, or investment return.
- Do not stage or modify the user's separate uncommitted legal copy in `terms.html`.

---

### Task 1: Restore Long-Form SpaceX Content

**Files:**
- Create: `scripts/import_spacex_content.py`
- Create: `content/campaigns/spacex-en.html`
- Create: `content/campaigns/spacex-zh.html`
- Create: `assets/styles/spacex-en.css`
- Create: `assets/styles/spacex-zh.css`
- Modify: `scripts/build_docs.py:12-35,320-339`
- Modify: `tests/test_site.py:180-205`

**Interfaces:**
- Consumes: Git objects `a0ccc1d:6-1-pre-spacex-en.html` and `a0ccc1d:6-1-pre-spacex-zh.html`.
- Produces: `import_page(source: str) -> tuple[str, str]`, returning the original inline stylesheet and the inner HTML of `<main class="main-content">`; `campaign_fragment(name: str) -> str`, read by the generator.

- [ ] **Step 1: Write the failing SpaceX preservation test**

```python
def test_spacex_long_form_content_is_preserved(self):
    cases = {
        "6-1-pre-spacex-en.html": ("Project Overview", "Key Subscription Parameters", "How does PreIPO work?", "Trading & Settlement", "Important Terms & Risk Disclosure"),
        "6-1-pre-spacex-zh.html": ("项目简介", "核心认购参数", "IPO PRIME 如何运作？", "交易与交割机制", "重要条款与风险提示"),
    }
    for name, sections in cases.items():
        text = (ROOT / name).read_text(encoding="utf-8")
        self.assertGreater(len(text), 12000, name)
        for section in sections:
            self.assertIn(section, text, f"{name}: {section}")
```

- [ ] **Step 2: Run the test and verify the current short pages fail**

Run: `python3 -m unittest tests.test_site.SiteTests.test_spacex_long_form_content_is_preserved -v`

Expected: FAIL because each generated SpaceX page is approximately 2.5 KB and lacks the original section headings.

- [ ] **Step 3: Implement the provenance importer and content assets**

```python
def import_page(source):
    style = re.search(r"<style>(.*?)</style>", source, re.S).group(1).strip()
    main = re.search(r'<main class="main-content">(.*?)</main>', source, re.S).group(1).strip()
    return style, main
```

The importer must call `git show a0ccc1d:<filename>` with `subprocess.run(..., check=True, capture_output=True, text=True)`, write UTF-8 body fragments and CSS assets, and print the imported character counts. Run it once to materialize the four assets.

- [ ] **Step 4: Teach the generator to wrap complete fragments**

```python
def campaign_fragment(name):
    return (ROOT / "content" / "campaigns" / name).read_text(encoding="utf-8")

PAGES["6-1-pre-spacex-en.html"] = (
    "Pre SpaceX", "spacex-en", "en", campaign_fragment("spacex-en.html"),
    '<link rel="stylesheet" href="assets/styles/spacex-en.css">',
)
```

Extend `shell()` and the `PAGES` write loop with an optional `extra_head` value placed before the main `style.css` link, so the shared shell wins global selector conflicts while SpaceX-specific component rules remain available.

- [ ] **Step 5: Regenerate and verify the focused test passes**

Run: `python3 scripts/build_docs.py && python3 -m unittest tests.test_site.SiteTests.test_spacex_long_form_content_is_preserved -v`

Expected: PASS for both languages.

- [ ] **Step 6: Commit the restoration**

```bash
git add scripts/import_spacex_content.py scripts/build_docs.py tests/test_site.py content/campaigns assets/styles 6-1-pre-spacex-en.html 6-1-pre-spacex-zh.html
git commit -m "docs: restore complete SpaceX offering content"
```

---

### Task 2: Expand the Bilingual Kimi Offering

**Files:**
- Modify: `tests/test_site.py:186-205`
- Modify: `scripts/build_docs.py:360-394`
- Regenerate: `6-3-pre-kimi-en.html`
- Regenerate: `6-3-pre-kimi-zh.html`

**Interfaces:**
- Consumes: official Kimi URLs and DeShare offering disclosures from the approved specification.
- Produces: bilingual rendered sections for company context, K3 facts, subscription timeline, internal trading risk, and conditional lock-up.

- [ ] **Step 1: Write failing tests for K3, dates, and liquidity disclosures**

```python
def test_kimi_k3_and_subscription_timeline(self):
    english = (ROOT / "6-3-pre-kimi-en.html").read_text(encoding="utf-8")
    chinese = (ROOT / "6-3-pre-kimi-zh.html").read_text(encoding="utf-8")
    for value in ("Kimi K3", "2026-07-16", "2.8 trillion", "1-million-token", "https://www.kimi.com/help/agent/agent-overview"):
        self.assertIn(value, english)
    for value in ("Kimi K3", "2026-07-16", "2.8 万亿", "100 万 Token", "https://www.kimi.com/help/agent/agent-overview"):
        self.assertIn(value, chinese)
    for text in (english, chinese):
        self.assertIn("2026-07-23", text)
        self.assertIn("2026-07-28", text)
        self.assertIn("6–12", text)

def test_kimi_internal_market_does_not_promise_liquidity(self):
    english = (ROOT / "6-3-pre-kimi-en.html").read_text(encoding="utf-8").lower()
    chinese = (ROOT / "6-3-pre-kimi-zh.html").read_text(encoding="utf-8")
    self.assertIn("internal platform trading", english)
    self.assertIn("not guaranteed", english)
    self.assertIn("平台内交易", chinese)
    self.assertIn("不能确保", chinese)
```

- [ ] **Step 2: Run focused tests and verify they fail for missing content**

Run: `python3 -m unittest tests.test_site.SiteTests.test_kimi_k3_and_subscription_timeline tests.test_site.SiteTests.test_kimi_internal_market_does_not_promise_liquidity -v`

Expected: two FAIL results because the current pages contain none of the new K3, date, internal-market, or 6–12 month text.

- [ ] **Step 3: Implement Kimi K3 company/model sections**

Add an `Official Kimi product information` / `Kimi 官方产品信息` badge and a linked section that includes the approved 2026-07-16 release date, 2.8T parameter count, KDA, Attention Residuals, native vision, and up-to-one-million-token context facts. Follow it with a disclaimer that these capabilities do not establish valuation or investment return.

- [ ] **Step 4: Implement subscription and liquidity timeline**

Add the 2026-07-23–2026-07-28 window to the parameter table and participation sequence. Add a dedicated internal-market and lock-up section in each language that states planned platform trading, normally low liquidity, no guaranteed completion, and a conditional 6–12 month post-listing lock-up governed by the actual listing structure and official post-listing terms.

- [ ] **Step 5: Regenerate and verify focused and full tests**

Run: `python3 scripts/build_docs.py && python3 -m unittest tests/test_site.py -v`

Expected: all tests PASS, including the existing valuation, fee, eligibility, NDA, and no-contract-address assertions.

- [ ] **Step 6: Commit the Kimi expansion**

```bash
git add scripts/build_docs.py tests/test_site.py 6-3-pre-kimi-en.html 6-3-pre-kimi-zh.html
git commit -m "docs: expand Kimi K3 offering disclosures"
```

---

### Task 3: Browser Verification and GitHub Publication

**Files:**
- Verify: `6-1-pre-spacex-en.html`
- Verify: `6-1-pre-spacex-zh.html`
- Verify: `6-3-pre-kimi-en.html`
- Verify: `6-3-pre-kimi-zh.html`

**Interfaces:**
- Consumes: generated static pages and current shared navigation.
- Produces: validated Git commits pushed to `origin/main`.

- [ ] **Step 1: Run clean generation and all tests**

Run: `python3 scripts/build_docs.py && python3 scripts/upgrade_legal_shell.py && python3 -m unittest tests/test_site.py -v && git diff --check`

Expected: generation succeeds, all tests PASS, and `git diff --check` prints no output.

- [ ] **Step 2: Serve the site and inspect desktop pages**

Run: `python3 -m http.server 8765 --bind 127.0.0.1`

Use Playwright at 1440×1000 to inspect the English SpaceX and Chinese Kimi pages. Confirm long-form hierarchy, tables, badges, links, side navigation, and footer display correctly with zero console errors.

- [ ] **Step 3: Inspect mobile pages**

Use Playwright at 390×844 to inspect Chinese SpaceX and English Kimi pages. Confirm the menu opens, no horizontal overflow exists, tables remain readable, and all added sections are reachable.

- [ ] **Step 4: Confirm the dirty legal file remains isolated**

Run: `git status -sb && git diff -- terms.html`

Expected: only the user's pre-existing `terms.html` legal-copy change remains unstaged after implementation commits.

- [ ] **Step 5: Push the approved commits**

Run: `git push origin main && git status -sb && git ls-remote --heads origin main`

Expected: `origin/main` advances to the local `HEAD`; `terms.html` remains local and uncommitted.
