# Kimi Risk Disclosure and Issuance Correction Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Correct the Kimi maximum issuance to 10,000 interests and add a complete bilingual seven-item important-terms and risk-disclosure section adapted from the SpaceX structure.

**Architecture:** Keep `scripts/build_docs.py` as the single production source for both Kimi pages. Strengthen `tests/test_site.py` so generated output must contain the corrected issuance and each risk category while rejecting stale issuance and SpaceX-specific terms.

**Tech Stack:** Python 3 standard library, static HTML, `unittest`, Git.

## Global Constraints

- Maximum Kimi issuance is exactly 10,000 interests in Chinese and English.
- Do not leave `1,000,000` in either rendered Kimi page or its production source.
- Preserve the 100 USDT unit price, 8% subscription/management fee, 20% carry, 2026-07-23–2026-07-28 subscription window, and all existing Kimi K3, NDA, internal-market, and lock-up disclosures.
- The complete risk section contains nature of rights, non-affiliation, jurisdiction restrictions, investment risk, liquidity risk, fund/due-diligence risk, and lock-up/unlock risk.
- Do not introduce `PreSPX`, SpaceX, DigiFT, or a fixed six-month lock-up into Kimi pages.
- Do not stage the user's separate `terms.html` legal-copy changes.

---

### Task 1: Enforce the Corrected Issuance

**Files:**
- Modify: `tests/test_site.py:241-248`
- Modify: `scripts/build_docs.py:360-402`
- Regenerate: `6-3-pre-kimi-en.html`
- Regenerate: `6-3-pre-kimi-zh.html`
- Modify: `docs/superpowers/plans/2026-07-22-deshare-evidence-first-docs.md`

**Interfaces:**
- Consumes: the corrected DeShare operator disclosure of 10,000 interests.
- Produces: bilingual generated output containing `10,000` and excluding `1,000,000`.

- [ ] **Step 1: Change the existing Kimi terms test before production copy**

```python
for value in ("31.5", "10,000", "100 USDT", "8%", "20%", "PreKimiToken"):
    self.assertIn(value, text, f"{name}: {value}")
self.assertNotIn("1,000,000", text, f"{name}: stale issuance amount")
```

- [ ] **Step 2: Run the focused test and verify it fails on the stale amount**

Run: `python3 -m unittest tests.test_site.SiteTests.test_kimi_terms_match -v`

Expected: FAIL because `10,000` is missing from the current generated page.

- [ ] **Step 3: Replace the stale amount in the generator and historical implementation plan**

Update both parameter-panel summaries and both maximum-issuance table rows to `10,000`; update the earlier plan's test example and term summary to the corrected value.

```html
<p>10,000 maximum interests<br>100 USDT per interest</p>
<tr><th>Maximum issuance</th><td>10,000 interests / PreKimiToken</td></tr>
<p>最大发行 10,000 份<br>每份 100 USDT</p>
<tr><th>最大发行</th><td>10,000 份 / PreKimiToken</td></tr>
```

- [ ] **Step 4: Regenerate and verify the focused test passes**

Run: `python3 scripts/build_docs.py && python3 -m unittest tests.test_site.SiteTests.test_kimi_terms_match -v`

Expected: PASS.

---

### Task 2: Add the Complete Bilingual Risk Section

**Files:**
- Modify: `tests/test_site.py:249-265`
- Modify: `scripts/build_docs.py:380-414`
- Regenerate: `6-3-pre-kimi-en.html`
- Regenerate: `6-3-pre-kimi-zh.html`

**Interfaces:**
- Consumes: the seven risk categories from `docs/superpowers/specs/2026-07-22-spacex-content-and-kimi-k3-design.md`.
- Produces: one `disclaimer-box` section per language with an `h2` heading and seven labeled list items.

- [ ] **Step 1: Write the failing bilingual risk-section test**

```python
def test_kimi_complete_risk_disclosure(self):
    english = (ROOT / "6-3-pre-kimi-en.html").read_text(encoding="utf-8")
    chinese = (ROOT / "6-3-pre-kimi-zh.html").read_text(encoding="utf-8")
    for value in (
        "Important Terms &amp; Risk Disclosure",
        "Nature of Rights",
        "Non-Affiliation Disclaimer",
        "Jurisdictional Restrictions",
        "Investment Risk",
        "Liquidity Risk",
        "Fund and Due-Diligence Risk",
        "Lock-Up and Unlock Risk",
    ):
        self.assertIn(value, english)
    for value in (
        "重要条款与风险提示",
        "权益性质",
        "非关联声明",
        "司法管辖限制",
        "投资风险",
        "流动性风险",
        "基金与尽调风险",
        "锁定与解锁风险",
    ):
        self.assertIn(value, chinese)
    for text in (english, chinese):
        for stale in ("PreSPX", "DigiFT"):
            self.assertNotIn(stale, text)
```

- [ ] **Step 2: Run the test and verify it fails for the missing complete section**

Run: `python3 -m unittest tests.test_site.SiteTests.test_kimi_complete_risk_disclosure -v`

Expected: FAIL because the current Kimi pages only contain two short risk callouts.

- [ ] **Step 3: Replace the short callouts with one complete section**

Use this structure in each language:

```html
<div class="disclaimer-box">
  <h2>⚠️ Important Terms &amp; Risk Disclosure</h2>
  <ul>
    <li><strong>Nature of Rights:</strong> PreKimiToken is an economic interest through the disclosed structure and is not direct Kimi or Moonshot AI equity.</li>
    <li><strong>Non-Affiliation Disclaimer:</strong> Kimi and Moonshot AI have not endorsed, approved, or authorized this offering.</li>
    <li><strong>Jurisdictional Restrictions:</strong> United States, Mainland China, and other restricted-jurisdiction users may not participate.</li>
    <li><strong>Investment Risk:</strong> Investors may lose some or all principal; model capability does not establish company value or investment return.</li>
    <li><strong>Liquidity Risk:</strong> Internal platform trading does not guarantee liquidity, price, timing, or completion.</li>
    <li><strong>Fund and Due-Diligence Risk:</strong> The confidential fund must be evaluated through NDA-gated materials.</li>
    <li><strong>Lock-Up and Unlock Risk:</strong> The expected 6–12 month post-listing lock-up depends on the listing structure and final documents.</li>
  </ul>
</div>
```

Every item must use Kimi, Moonshot AI, Hong Kong LPF, NDA, internal-market, and 6–12 month terminology appropriate to the approved specification. Preserve the no-published-contract-address and no-guaranteed-IPO/unlock statements inside the relevant items.

- [ ] **Step 4: Regenerate and run focused and full tests**

Run: `python3 scripts/build_docs.py && python3 -m unittest tests.test_site.SiteTests.test_kimi_complete_risk_disclosure -v && python3 -m unittest tests/test_site.py -v`

Expected: all 18 tests PASS.

- [ ] **Step 5: Commit implementation files without `terms.html`**

```bash
git add scripts/build_docs.py tests/test_site.py 6-3-pre-kimi-en.html 6-3-pre-kimi-zh.html docs/superpowers/plans/2026-07-22-deshare-evidence-first-docs.md
git commit -m "docs: correct Kimi issuance and expand risk disclosures"
```

---

### Task 3: Verify and Publish

**Files:**
- Verify: `6-3-pre-kimi-en.html`
- Verify: `6-3-pre-kimi-zh.html`

**Interfaces:**
- Consumes: committed generated pages.
- Produces: a verified `origin/main` at the same commit as local `HEAD`.

- [ ] **Step 1: Run final generation and validation**

Run: `python3 scripts/build_docs.py && python3 scripts/upgrade_legal_shell.py && python3 -m unittest tests/test_site.py -v && git diff --check`

Expected: all 18 tests PASS and `git diff --check` emits no output.

- [ ] **Step 2: Confirm the corrected terms directly**

Run: `rg -n '1,000,000|1000000' scripts/build_docs.py tests/test_site.py 6-3-pre-kimi-en.html 6-3-pre-kimi-zh.html`

Expected: only the negative test assertion contains `1,000,000`; no production or rendered page contains the stale amount.

- [ ] **Step 3: Confirm the mixed worktree boundary**

Run: `git status -sb && git diff -- terms.html`

Expected: only the user's local `terms.html` changes remain unstaged.

- [ ] **Step 4: Push main**

Run: `git push origin main && git status -sb && git ls-remote --heads origin main`

Expected: `origin/main` matches local `HEAD`; `terms.html` remains local and uncommitted.
