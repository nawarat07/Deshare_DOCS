# DeShare Evidence-First Documentation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the marketing-led static whitepaper with a verifiable protocol, deployment, security, developer, and offering documentation site, including bilingual Kimi offering pages.

**Architecture:** Keep the site build-free and static. A shared `site.js` module owns navigation and mobile-menu behavior, `style.css` owns the documentation design system, and a checked-in deployment manifest separates time-sensitive chain facts from page prose. Python standard-library tests validate required routes, internal links, deployment data, evidence language, ABI publication, audit artifact integrity, and Kimi bilingual parity.

**Tech Stack:** HTML5, CSS, browser JavaScript, JSON, Python 3 standard library, Foundry `cast`, local HTTP server.

## Global Constraints

- Preserve the user's existing uncommitted changes in `terms.html`.
- Do not modify `/Users/jerry/Project/Deshare/contract/contract`.
- Label claims as `On-chain verified`, `Third-party assessed`, `Operator disclosed`, or `Unavailable`.
- Publish unresolved Aegixe findings as open; do not imply that the assessed source is bytecode-identical to the deployed implementation.
- Publish `https://dshare-zkfetch.zkpass.org` with a visible “service in progress” limitation.
- Do not state that `PreKimiToken` is deployed until a verified address exists.
- Present the Kimi 8% fee and 20% carry as operator-disclosed offering terms, not as the current generic on-chain IPO fee.
- Keep the site usable without a build step and provide a non-JavaScript route back to `index.html` on every page.

---

### Task 1: Verification Harness and Evidence Fixtures

**Files:**
- Create: `tests/test_site.py`
- Create: `assets/data/deployments.json`
- Create: `assets/data/evidence.json`

**Interfaces:**
- Produces: `load_deployments() -> dict`, `iter_html_files() -> list[Path]`, and a unittest suite consumed by every later task.
- Produces: deployment records with `network`, `chainId`, `status`, `lastVerified`, and `contracts` fields.

- [ ] **Step 1: Write failing route, link, evidence, deployment, and Kimi tests**

```python
import hashlib, json, re, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    "index.html", "4-2-deployments.html", "4-3-security-audit.html",
    "5-developer-docs.html", "5-1-api-reference.html",
    "5-2-contract-reference.html", "6-3-pre-kimi-zh.html",
    "6-3-pre-kimi-en.html", "site.js",
}

class SiteTests(unittest.TestCase):
    def test_required_routes_exist(self):
        self.assertFalse([name for name in REQUIRED if not (ROOT / name).exists()])

    def test_internal_links_resolve(self):
        broken = []
        for page in ROOT.glob("*.html"):
            for href in re.findall(r'href="([^"]+)"', page.read_text()):
                if href.startswith(("http", "mailto:", "#")):
                    continue
                target = href.split("#", 1)[0]
                if target and not (ROOT / target).exists():
                    broken.append(f"{page.name} -> {href}")
        self.assertEqual([], broken)

    def test_kimi_terms_match(self):
        for name in ("6-3-pre-kimi-zh.html", "6-3-pre-kimi-en.html"):
            text = (ROOT / name).read_text()
            for value in ("31.5", "10,000", "100 USDT", "8%", "20%", "PreKimiToken"):
                self.assertIn(value, text)
```

- [ ] **Step 2: Run the tests and verify the new routes fail**

Run: `python3 -m unittest tests/test_site.py -v`
Expected: FAIL in `test_required_routes_exist` and Kimi file reads.

- [ ] **Step 3: Add initial evidence manifests**

`deployments.json` records Arbitrum One as active and Sepolia/Monad as pending implementation-time verification. `evidence.json` records the audit PDF hash, zkPass URL, and verification timestamps.

- [ ] **Step 4: Re-run focused manifest tests**

Run: `python3 -m unittest tests.test_site.SiteTests.test_deployment_manifest -v`
Expected: PASS after the schema assertions and fixtures are present.

- [ ] **Step 5: Commit**

```bash
git add tests/test_site.py assets/data/deployments.json assets/data/evidence.json
git commit -m "test: add evidence documentation verification"
```

### Task 2: Shared Navigation and Documentation Design System

**Files:**
- Create: `site.js`
- Modify: `style.css`
- Modify: all root HTML pages to load `site.js` and expose `data-page`.

**Interfaces:**
- Produces: `window.DESHARE_NAV`, `renderNavigation()`, `toggleMobileNavigation()`.
- Consumes: stable page keys such as `overview`, `deployments`, `audit`, `api`, `contracts`, and `kimi-zh`.

- [ ] **Step 1: Add failing shared-navigation assertions**

```python
def test_pages_use_shared_navigation(self):
    for page in ROOT.glob("*.html"):
        text = page.read_text()
        self.assertIn('src="site.js"', text, page.name)
        self.assertRegex(text, r'<body[^>]+data-page="[^"]+"')
        self.assertIn('href="index.html"', text, page.name)
```

- [ ] **Step 2: Run and confirm failure**

Run: `python3 -m unittest tests.test_site.SiteTests.test_pages_use_shared_navigation -v`
Expected: FAIL on existing pages.

- [ ] **Step 3: Implement shared navigation**

`site.js` defines the seven navigation groups, renders links into `[data-site-nav]`, applies `aria-current="page"`, and controls a button using `aria-expanded`. No external framework is introduced.

- [ ] **Step 4: Replace the visual system**

`style.css` adds evidence badges, status cards, deployment tables, code blocks, copyable address rows, warning/caveat panels, sequence steps, audit severity summaries, mobile drawer navigation, and focus-visible states. The sidebar is no longer hidden without replacement below 768 px.

- [ ] **Step 5: Run navigation and link tests**

Run: `python3 -m unittest tests.test_site.SiteTests.test_pages_use_shared_navigation tests.test_site.SiteTests.test_internal_links_resolve -v`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add site.js style.css ./*.html tests/test_site.py
git commit -m "feat: add shared evidence documentation shell"
```

### Task 3: Protocol and Architecture Rewrite

**Files:**
- Modify: `index.html`
- Modify: `2-platform-features.html`
- Modify: `2-1-core-features.html`
- Modify: `2-2-product-suite.html`
- Modify: `2-3-ipo-investing.html`
- Modify: `3-architecture.html`
- Modify: `3-1-technical-architecture.html`
- Modify: `3-2-protocol-mechanism.html`
- Modify: `assets/technical-architecture.svg`
- Modify: `assets/protocol-mechanism.svg`

**Interfaces:**
- Consumes: evidence labels and shell classes from Task 2.
- Produces: accurate implemented transaction flows referenced by security and developer pages.

- [ ] **Step 1: Add failing prohibited-claim and required-trust-boundary tests**

```python
def test_protocol_copy_is_evidence_led(self):
    combined = "\n".join((ROOT / p).read_text().lower() for p in (
        "index.html", "2-2-product-suite.html", "3-2-protocol-mechanism.html"))
    for phrase in ("perfectly trustless", "unquestionable", "absolute non-custodial"):
        self.assertNotIn(phrase, combined)
    for phrase in ("operator disclosed", "event-based", "privileged"):
        self.assertIn(phrase, combined)
```

- [ ] **Step 2: Run and confirm failure**

Run: `python3 -m unittest tests.test_site.SiteTests.test_protocol_copy_is_evidence_led -v`
Expected: FAIL on current marketing copy.

- [ ] **Step 3: Rewrite overview and product model**

Lead with an evidence dashboard, system boundary, asset-rights model, and a concise statement of what the protocol does and does not verify. Replace broad global-access claims with component-specific descriptions.

- [ ] **Step 4: Rewrite transaction and contract architecture**

Document `createBuyOrder`, `createSellOrder`, `OrderCreated`, backend brokerage handling, owner-only fill/cancel/mint/burn actions, funds receivers, token factory ownership, UUPS upgrades, fee calculation, and failure/refund paths.

- [ ] **Step 5: Replace misleading RFQ diagrams and copy**

The diagrams show event-based chain activity and off-chain execution. ECDSA RFQ validation is excluded because it is not present in the supplied verified implementation evidence.

- [ ] **Step 6: Run evidence and link tests**

Run: `python3 -m unittest tests/test_site.py -v`
Expected: protocol-copy tests PASS; only future-page tests may remain failing.

- [ ] **Step 7: Commit**

```bash
git add index.html 2-*.html 3-*.html assets/*.svg tests/test_site.py
git commit -m "docs: rewrite protocol around implemented trust boundaries"
```

### Task 4: Deployments, ABI, and API Reference

**Files:**
- Create: `4-2-deployments.html`
- Create: `5-developer-docs.html`
- Create: `5-1-api-reference.html`
- Create: `5-2-contract-reference.html`
- Create: `assets/abi/StockTrading.json`
- Create: `assets/abi/StockTokenFactory.json`
- Create: `assets/abi/StandardStockToken.json`
- Modify: `assets/data/deployments.json`
- Modify: `tests/test_site.py`

**Interfaces:**
- Consumes: supplied ABI/API document and public contract repository artifacts.
- Produces: stable download paths under `assets/abi/` and deployment tables linked from all technical pages.

- [ ] **Step 1: Add failing ABI hash/signature and deployment assertions**

```python
def test_contract_reference_uses_current_signature(self):
    text = (ROOT / "5-2-contract-reference.html").read_text()
    self.assertIn("createBuyOrder", text)
    for parameter in ("_marginLevel", "_interest", "_assetType"):
        self.assertIn(parameter, text)

def test_active_proxy_address(self):
    data = json.loads((ROOT / "assets/data/deployments.json").read_text())
    arb = next(item for item in data["networks"] if item["chainId"] == 42161)
    self.assertEqual("0x9748C6B5E16599E78351339CA2E24268B5C39C3E", arb["contracts"]["proxy"])
```

- [ ] **Step 2: Verify active chain values before publication**

Run `cast code`, `cast storage` for EIP-1967, and `cast call` for `owner`, `feeRate`, `assetFeeRates(5)`, `minFeeAmount`, `usdtContract`, and `stockTokenFactory` against Arbitrum One. Verify Sepolia and Monad values where RPC access succeeds. Store the date and evidence URL in the manifest.

- [ ] **Step 3: Publish selected ABI artifacts**

Copy only the three public ABI JSON files from the supplied contract repository. Do not copy operational scripts, credentials, logs, balances, or untracked files.

- [ ] **Step 4: Write deployment and developer pages**

Include network status, proxy/implementation mechanics, current parameters, REST endpoint examples, signature-based cancellation, precision rules, enum values, event definitions, current eight-argument order functions, error behavior, and source/evidence links.

- [ ] **Step 5: Run tests**

Run: `python3 -m unittest tests/test_site.py -v`
Expected: route, ABI, signature, deployment, and link tests PASS.

- [ ] **Step 6: Commit**

```bash
git add 4-2-deployments.html 5-*.html assets/abi assets/data/deployments.json tests/test_site.py
git commit -m "docs: publish deployments ABI and API references"
```

### Task 5: Audit, Reserve Proof, and Custody Transparency

**Files:**
- Modify: `4-security.html`
- Modify: `4-1-trusted-custody.html`
- Create: `4-3-security-audit.html`
- Create: `assets/reports/deshare-stock-contract-security-assessment-aegixe-2026-04-27.pdf`
- Modify: `tests/test_site.py`

**Interfaces:**
- Consumes: Aegixe PDF and hash in `assets/data/evidence.json`.
- Produces: public audit download and zkPass service-status link.

- [ ] **Step 1: Add failing audit integrity and disclosure tests**

```python
def test_audit_artifact_and_disclosure(self):
    pdf = ROOT / "assets/reports/deshare-stock-contract-security-assessment-aegixe-2026-04-27.pdf"
    self.assertEqual("437d248e1d4854e3342d6085d08fd7ab466591e3bb4df6dbd4ca31b04a77e7d2",
                     hashlib.sha256(pdf.read_bytes()).hexdigest())
    text = (ROOT / "4-3-security-audit.html").read_text()
    for value in ("0 Critical", "0 High", "1 Medium", "1 Low", "MED-01", "LOW-01", "Open"):
        self.assertIn(value, text)
```

- [ ] **Step 2: Run and confirm failure**

Run: `python3 -m unittest tests.test_site.SiteTests.test_audit_artifact_and_disclosure -v`
Expected: FAIL because the report page and artifact are absent.

- [ ] **Step 3: Publish the assessment and open findings**

Copy the exact supplied PDF, publish its hash, name Aegixe and the assessment date, show both findings as open, and disclose the missing commit/deployment/bytecode mapping plus the Base/staking overview-page inconsistency.

- [ ] **Step 4: Rewrite security and custody pages**

Separate smart-contract controls, admin controls, operational execution, custody disclosures, reserve evidence, and unavailable evidence. Link zkPass with “service in progress” text and no verified badge.

- [ ] **Step 5: Run tests and hash check**

Run: `python3 -m unittest tests/test_site.py -v && shasum -a 256 assets/reports/*.pdf`
Expected: all audit and evidence tests PASS; hash starts `437d248e`.

- [ ] **Step 6: Commit**

```bash
git add 4-security.html 4-1-trusted-custody.html 4-3-security-audit.html assets/reports tests/test_site.py
git commit -m "docs: publish audit and reserve transparency"
```

### Task 6: Bilingual Kimi Offering and Campaign Normalization

**Files:**
- Create: `6-3-pre-kimi-zh.html`
- Create: `6-3-pre-kimi-en.html`
- Modify: `6-1-pre-spacex-zh.html`
- Modify: `6-1-pre-spacex-en.html`
- Modify: `6-2-pre-anthropic-zh.html`
- Modify: `6-2-pre-anthropic-en.html`
- Modify: `tests/test_site.py`

**Interfaces:**
- Produces: Kimi bilingual route pair and normalized campaign evidence labels.

- [ ] **Step 1: Add failing confidentiality, restriction, and non-deployment assertions**

```python
def test_kimi_disclosures(self):
    for name in ("6-3-pre-kimi-zh.html", "6-3-pre-kimi-en.html"):
        text = (ROOT / name).read_text()
        self.assertIn("bd@deshare.finance", text)
        self.assertIn("NDA", text)
        self.assertNotRegex(text, r'0x[a-fA-F0-9]{40}')
```

- [ ] **Step 2: Run and confirm failure**

Run: `python3 -m unittest tests.test_site.SiteTests.test_kimi_terms_match tests.test_site.SiteTests.test_kimi_disclosures -v`
Expected: FAIL because the Kimi pages do not exist.

- [ ] **Step 3: Implement Chinese Kimi page**

Include the 31.5 billion USD pre-money reference valuation, L1 Hong Kong LPF structure, 10,000 maximum interests, 100 USDT unit price, 8% subscription/management fee, 20% carry, US/Mainland China restriction, NDA process, non-deployment state, rights limitations, settlement uncertainty, liquidity risk, and final-document precedence.

- [ ] **Step 4: Implement equivalent English Kimi page**

Use the same facts and section sequence as the Chinese page. Translate meaning rather than inventing additional commercial terms.

- [ ] **Step 5: Normalize campaign evidence language**

Add operator-disclosed labels and consistent rights/restriction caveats to SpaceX and Anthropic without changing their supplied commercial numbers.

- [ ] **Step 6: Run bilingual and link tests**

Run: `python3 -m unittest tests/test_site.py -v`
Expected: Kimi parity, restriction, NDA, and local-link tests PASS.

- [ ] **Step 7: Commit**

```bash
git add 6-*.html tests/test_site.py
git commit -m "docs: add bilingual PreKimiToken offering"
```

### Task 7: Final Integration, Visual QA, and Evidence Verification

**Files:**
- Modify: `5-faq.html`
- Modify: any HTML/CSS/JS/data files required by discovered defects.
- Preserve: `terms.html` user changes.

**Interfaces:**
- Consumes: every page and artifact from Tasks 1-6.
- Produces: verified, deployable static site.

- [ ] **Step 1: Rewrite FAQ as operational documentation**

Answer how to verify contracts, inspect proxy implementation, read fees, download ABI, understand owner privileges, interpret the audit, use zkPass while incomplete, and request Kimi NDA materials.

- [ ] **Step 2: Run the complete automated suite**

Run: `python3 -m unittest tests/test_site.py -v`
Expected: all tests PASS.

- [ ] **Step 3: Run contract tests as supporting evidence**

Run: `forge test` in `/Users/jerry/Project/Deshare/contract/contract` without modifying files.
Expected: capture pass/fail honestly; do not relabel tests as an external audit.

- [ ] **Step 4: Serve and crawl the site**

Run: `python3 -m http.server 8765` from the documentation root and load representative pages over HTTP. Check console errors and all navigation groups.

- [ ] **Step 5: Inspect desktop and mobile rendering**

Capture `index.html`, `4-2-deployments.html`, `4-3-security-audit.html`, `5-2-contract-reference.html`, and both Kimi pages at 1440x1000 and 390x844. Verify no clipping, horizontal overflow, inaccessible menu state, or unreadable tables.

- [ ] **Step 6: Re-query high-value chain facts**

Repeat Arbitrum proxy bytecode, implementation slot, owner, fee, IPO fee, minimum fee, USDT, and factory reads. Confirm they match `deployments.json` and the rendered deployment page.

- [ ] **Step 7: Check worktree isolation**

Run: `git status --short && git diff -- terms.html`
Expected: user changes in `terms.html` remain intact; no contract-repository files were modified; no temporary PDF renders are staged.

- [ ] **Step 8: Final commit**

```bash
git add 5-faq.html style.css site.js ./*.html assets/data tests/test_site.py
git commit -m "docs: complete evidence-first documentation restructure"
```
