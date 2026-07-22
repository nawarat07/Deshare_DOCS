# Kimi Overall Subscription Failure Refund Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a bilingual Kimi section that defines two overall subscription-failure triggers and promises a full refund of subscription principal plus the complete 8% subscription and management fee.

**Architecture:** Add the content to the Kimi source blocks in `scripts/build_docs.py` immediately after each participation timeline, then regenerate both static pages. Protect the operator-disclosed refund terms with a focused `unittest` regression test.

**Tech Stack:** Python 3 standard library, static HTML/CSS, `unittest`, Git.

## Global Constraints

- Trigger one is aggregate subscriptions below the fund's USD 500,000 minimum subscription threshold.
- Trigger two is the fund's failure to complete subscription for or acquisition of the target underlying interest during execution.
- Either trigger refunds 100% of each participant's subscription principal and the entire 8% subscription and management fee already charged.
- No platform fee, management fee, or other offering fee is deducted from the refund.
- Do not promise a specific arrival time or blockchain confirmation time; final documents and the refund announcement control execution method and timing.
- State that this applies only to failure of the offering as a whole and does not create a discretionary individual cancellation right.
- Preserve all existing Kimi issuance, model, timeline, liquidity, lock-up, eligibility, NDA, and risk terms.
- Do not stage the user's separate `terms.html` legal-copy changes.

---

### Task 1: Add and Test the Bilingual Refund Section

**Files:**
- Modify: `tests/test_site.py:275-305`
- Modify: `scripts/build_docs.py:375-430`
- Regenerate: `6-3-pre-kimi-en.html`
- Regenerate: `6-3-pre-kimi-zh.html`

**Interfaces:**
- Consumes: the approved overall-failure and full-refund operator disclosure.
- Produces: one English and one Chinese static section between participation timeline and liquidity/unlock content.

- [ ] **Step 1: Write the failing regression test**

```python
def test_kimi_overall_subscription_failure_refund(self):
    english = (ROOT / "6-3-pre-kimi-en.html").read_text(encoding="utf-8")
    chinese = (ROOT / "6-3-pre-kimi-zh.html").read_text(encoding="utf-8")
    for value in (
        "Overall Subscription Failure and Full Refund",
        "USD 500,000",
        "Target acquisition not completed",
        "100% of each participant's subscription principal",
        "entire 8% subscription and management fee",
        "does not create an individual cancellation right",
    ):
        self.assertIn(value, english)
    for value in (
        "整体认购失败与全额退款",
        "500,000 美元",
        "目标标的认购未完成",
        "100% 认购本金",
        "完整 8% 手续费及管理费",
        "不构成参与者任意取消认购的权利",
    ):
        self.assertIn(value, chinese)
```

- [ ] **Step 2: Run the focused test and verify it fails**

Run: `python3 -m unittest tests.test_site.SiteTests.test_kimi_overall_subscription_failure_refund -v`

Expected: FAIL because the new section heading is absent.

- [ ] **Step 3: Add the English production section**

```html
<h2>Overall Subscription Failure and Full Refund</h2>
<div class="grid">
  <article class="card"><h3>1. Below the fund threshold</h3><p>If aggregate confirmed subscriptions do not reach the fund's USD 500,000 minimum subscription threshold, the offering fails as a whole.</p></article>
  <article class="card"><h3>2. Target acquisition not completed</h3><p>If the fund cannot complete its subscription for or acquisition of the target underlying interest during execution, the offering fails as a whole.</p></article>
</div>
<div class="callout verified-callout"><strong>Full refund.</strong> If either condition occurs, DeShare will refund 100% of each participant's subscription principal and the entire 8% subscription and management fee already charged. No platform fee, management fee or other offering fee will be deducted.</div>
<div class="callout risk"><strong>Scope and timing.</strong> This policy applies only to failure of the offering as a whole and does not create an individual cancellation right. Refund method and timing are governed by the final offering documents and refund announcement; no specific arrival or blockchain confirmation time is promised.</div>
```

- [ ] **Step 4: Add the Chinese production section**

```html
<h2>整体认购失败与全额退款</h2>
<div class="grid">
  <article class="card"><h3>1. 未达到基金认购门槛</h3><p>若经确认的总认购金额未达到基金要求的 500,000 美元最低认购门槛，本次发行视为整体认购失败。</p></article>
  <article class="card"><h3>2. 目标标的认购未完成</h3><p>若基金在执行过程中未能完成目标标的权益认购或收购，本次发行视为整体认购失败。</p></article>
</div>
<div class="callout verified-callout"><strong>全额退款。</strong>出现任一情况，DeShare 将向每位参与者退还 100% 认购本金以及已收取的完整 8% 手续费及管理费，不扣除任何平台费、管理费或其他发行费用。</div>
<div class="callout risk"><strong>适用范围及时间。</strong>该政策仅适用于本次发行整体认购失败，不构成参与者任意取消认购的权利。退款方式及执行时间以最终发行文件和退款公告为准，不承诺具体到账时间或链上交易确认时间。</div>
```

- [ ] **Step 5: Regenerate and verify focused and full tests**

Run: `python3 scripts/build_docs.py && python3 -m unittest tests.test_site.SiteTests.test_kimi_overall_subscription_failure_refund -v && python3 -m unittest tests/test_site.py -v`

Expected: focused test and all 19 tests PASS.

- [ ] **Step 6: Commit implementation files without `terms.html`**

```bash
git add scripts/build_docs.py tests/test_site.py 6-3-pre-kimi-en.html 6-3-pre-kimi-zh.html
git commit -m "docs: add Kimi subscription failure refunds"
```

---

### Task 2: Final Verification

**Files:**
- Verify: `6-3-pre-kimi-en.html`
- Verify: `6-3-pre-kimi-zh.html`

**Interfaces:**
- Consumes: committed generated pages.
- Produces: verified local `main` with the unrelated legal copy left untouched.

- [ ] **Step 1: Run clean generation and all checks**

Run: `python3 scripts/build_docs.py && python3 scripts/upgrade_legal_shell.py && python3 -m unittest tests/test_site.py -v && git diff --check`

Expected: all 19 tests PASS and `git diff --check` emits no output.

- [ ] **Step 2: Confirm the exact refund terms in both pages**

Run: `rg -n '500,000|100%|8%|整体认购失败|Overall Subscription Failure' 6-3-pre-kimi-en.html 6-3-pre-kimi-zh.html`

Expected: both pages contain the threshold, full-principal refund, complete-fee refund, and overall-failure heading.

- [ ] **Step 3: Confirm the mixed worktree boundary**

Run: `git status -sb && git diff -- terms.html`

Expected: only the user's local `terms.html` changes remain unstaged.
