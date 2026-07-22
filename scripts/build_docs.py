from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def badge(kind, label):
    return f'<span class="badge {kind}">{label}</span>'


def head(kicker, title, lede):
    return f'''<header class="page-head">
<p class="eyebrow">{kicker}</p><h1>{title}</h1><p class="lede">{lede}</p>
<p class="meta">Evidence scope · implementation, public chain state, third-party reports, operator disclosures</p>
</header>'''


def shell(title, key, body, lang="en"):
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="Evidence-first DeShare protocol documentation">
<title>{title} · DeShare Documentation</title>
<link rel="icon" href="logo.svg" type="image/svg+xml">
<link rel="stylesheet" href="style.css"><script src="site.js" defer></script>
</head>
<body data-page="{key}">
<header class="site-header">
<a class="brand" href="index.html"><img src="logo.svg" alt="DeShare"><span class="brand-note">Evidence documentation</span></a>
<div class="header-status"><span class="status-dot"></span>Chain data checked 2026-07-22</div>
<button class="nav-toggle" type="button" data-nav-toggle aria-expanded="false" aria-label="Toggle documentation navigation">Menu</button>
</header>
<div class="site-layout"><aside class="sidebar" data-sidebar><nav data-site-nav aria-label="Documentation"></nav></aside>
<main class="main-content">{body}<p class="footer-note">DeShare documentation · Facts are labeled by evidence type · Last content review 2026-07-22</p></main></div>
</body></html>
'''


def nav(prev_href, prev_label, next_href, next_label):
    return f'<div class="page-nav"><a href="{prev_href}">← {prev_label}</a><a href="{next_href}">{next_label} →</a></div>'


def campaign_head(kicker, title, lede, side):
    return f'<div class="campaign-hero">{head(kicker, title, lede)}<aside class="parameter-panel">{side}</aside></div>'


PAGES = {}

PAGES["index.html"] = ("Protocol overview", "overview", "en", head(
    "Protocol / 01", "Verify the system, not the slogan.",
    "DeShare connects self-custodied wallets to an event-based stock-order contract and an off-chain execution operation. This site documents what is on-chain, what is assessed, and what still requires trust."
) + f'''
<div class="evidence-rail">
<div class="rail-item">{badge("verified", "On-chain verified")}<b>Arbitrum One</b><small>Proxy and implementation relationship re-read from public RPC.</small></div>
<div class="rail-item">{badge("assessed", "Third-party assessed")}<b>0 critical / 0 high</b><small>Aegixe found one Medium and one Low issue; both remain open.</small></div>
<div class="rail-item">{badge("disclosed", "Operator disclosed")}<b>Asset backing</b><small>Custody differs by product and is not proven by contract state alone.</small></div>
<div class="rail-item">{badge("unavailable", "Unavailable")}<b>zkPass proof view</b><small>The supplied verification root is online but its human-readable proof view is in progress.</small></div>
</div>
<h2>What the deployed system does</h2>
<div class="grid three">
<article class="card"><h3>Records order intent</h3><p>Users transfer margin or tokens and emit <code>OrderCreated</code> through <code>StockTrading</code>.</p></article>
<article class="card"><h3>Delegates execution</h3><p>An off-chain operator observes events, routes brokerage activity, and invokes privileged completion operations.</p></article>
<article class="card"><h3>Represents exposure</h3><p>Owner-controlled mint and burn operations reconcile stock-token balances after off-chain execution.</p></article>
</div>
<div class="callout risk"><strong>Trust boundary.</strong> Orders have no on-chain lifecycle state. Fill, cancel, mint, burn, receiver configuration, and upgrades depend on the privileged owner and operational controls.</div>
<h2>Start with evidence</h2>
<div class="grid">
<article class="card"><h3><a href="4-2-deployments.html">Inspect deployments</a></h3><p>Chain IDs, proxy addresses, implementation slots, owners, settlement tokens, and current fee parameters.</p></article>
<article class="card"><h3><a href="4-3-security-audit.html">Read the assessment</a></h3><p>Download the original Aegixe report, verify its hash, and review both open findings.</p></article>
<article class="card"><h3><a href="5-2-contract-reference.html">Use the ABI</a></h3><p>Current eight-argument order signatures, events, enums, precision, and downloadable JSON.</p></article>
<article class="card"><h3><a href="4-1-trusted-custody.html">Check reserve status</a></h3><p>Separate operator custody disclosures from zkPass verification availability.</p></article>
</div>''')

PAGES["2-platform-features.html"] = ("Capabilities and boundaries", "capabilities", "en", head(
    "Protocol / 02", "Capabilities and system boundaries",
    "The implementation coordinates wallet-originated orders and token accounting. It does not remove the broker, administrator, issuer, or custodian from the trust model."
) + f'''
<div class="table-wrap"><table><thead><tr><th>Capability</th><th>On-chain</th><th>Off-chain dependency</th><th>Evidence</th></tr></thead><tbody>
<tr><td>Create buy / sell intent</td><td>Transfers assets and emits an event</td><td>Frontend supplies order inputs</td><td>{badge("verified", "On-chain verified")}</td></tr>
<tr><td>Execute securities order</td><td>No broker execution in contract</td><td>Operator and brokerage workflow</td><td>{badge("disclosed", "Operator disclosed")}</td></tr>
<tr><td>Issue stock token</td><td>Owner calls mint against factory token</td><td>Operator reconciles execution</td><td>{badge("verified", "On-chain verified")}</td></tr>
<tr><td>Prove reserves</td><td>No reserve registry in supplied contracts</td><td>zkPass verification service</td><td>{badge("unavailable", "Service in progress")}</td></tr>
</tbody></table></div>
<h2>Implemented concepts</h2><div class="grid">
<article class="card"><h3>Markets</h3><p><code>AssetType</code> defines HK, US, SG, JP, KR, IPO and OT categories for fee selection.</p></article>
<article class="card"><h3>Leverage</h3><p>Margin level is capped at 100x in the inspected implementation; financing risk remains product-dependent.</p></article>
<article class="card"><h3>Settlement token</h3><p>Each deployment points to one ERC-20 settlement token. Verify it before approval.</p></article>
<article class="card"><h3>Upgradeable logic</h3><p>The proxy delegates to an owner-authorized implementation that can change without changing the proxy address.</p></article>
</div>''' + nav("index.html", "Protocol overview", "2-1-core-features.html", "Transaction lifecycle"))

PAGES["2-1-core-features.html"] = ("Transaction lifecycle", "transactions", "en", head(
    "Protocol / 03", "Transaction lifecycle",
    "The contract records transfers and events. The operational order lifecycle continues off-chain and returns through owner-only functions."
) + '''
<h2>Buy order</h2><div class="sequence">
<div class="sequence-step"><h3>Approve settlement token</h3><p>The wallet approves the active proxy for margin, fee and interest.</p></div>
<div class="sequence-step"><h3>Create the order</h3><p><code>createBuyOrder</code> transfers margin to <code>fundReceiver</code>, collects fee and interest, and emits <code>OrderCreated</code>.</p></div>
<div class="sequence-step"><h3>Execute off-chain</h3><p>The backend observes the event and manages brokerage execution. This state is not stored in the contract.</p></div>
<div class="sequence-step"><h3>Complete or cancel</h3><p>The owner emits fill status and mints tokens, or invokes cancellation and refund logic.</p></div></div>
<h2>Sell order</h2><div class="sequence">
<div class="sequence-step"><h3>Approve stock token and USDT</h3><p>The wallet approves token margin plus USDT for fee and interest.</p></div>
<div class="sequence-step"><h3>Create and execute</h3><p>Token margin moves to <code>tokenReceiver</code>; the off-chain operator handles brokerage execution.</p></div>
<div class="sequence-step"><h3>Reconcile</h3><p>The owner burns stock tokens after execution or invokes the refund path.</p></div></div>
<div class="callout risk"><strong>Open finding MED-01.</strong> The contract stores no order status and validates no state transition. Events are not a complete on-chain order book.</div>
''' + nav("2-platform-features.html", "Capabilities", "2-2-product-suite.html", "Asset model"))

PAGES["2-2-product-suite.html"] = ("Asset and custody model", "asset-model", "en", head(
    "Protocol / 04", "Asset and custody model",
    "A stock token is an on-chain representation managed by the trading owner. Its economic backing depends on product-specific issuer, fund, broker, and custody arrangements."
) + f'''
<h2>Three records, three authorities</h2><div class="grid three">
<article class="card">{badge("verified", "On-chain verified")}<h3>Token ledger</h3><p>ERC-20 balances, mint and burn events, proxy configuration, and transfers.</p></article>
<article class="card">{badge("disclosed", "Operator disclosed")}<h3>Broker / fund ledger</h3><p>Underlying securities and cash sit outside the supplied contracts.</p></article>
<article class="card">{badge("assessed", "Third-party assessed")}<h3>Attestation layer</h3><p>Audit and zkPass evidence can assess selected controls or data.</p></article>
</div>
<h2>Product-specific custody</h2><p>General stock trading, DigiFT-linked Pre-IPO offerings, and the Kimi offshore USD fund use different legal and custody descriptions. This documentation does not collapse them into one “all assets at one broker” claim.</p>
<div class="callout"><strong>Operator disclosed.</strong> Institutional brokerage custody is described by DeShare, but complete public account-level reserve statements were not supplied.</div>
<h2>What holders should verify</h2><ul><li>The exact token contract and network.</li><li>The rights in final product documents.</li><li>The issuer, fund, custodian and redemption path.</li><li>Whether a current proof covers that token and reporting period.</li></ul>
''' + nav("2-1-core-features.html", "Transactions", "2-3-ipo-investing.html", "IPO model"))

PAGES["2-3-ipo-investing.html"] = ("IPO and Pre-IPO model", "ipo-model", "en", head(
    "Protocol / 05", "IPO and Pre-IPO model",
    "These offerings provide structured economic exposure through a fund, SPV or issuer. A token is not automatically direct equity in the target company."
) + f'''
<div class="sequence">
<div class="sequence-step"><h3>Offering terms</h3><p>{badge("disclosed", "Operator disclosed")} Valuation, price, fees, eligibility and legal vehicle are published.</p></div>
<div class="sequence-step"><h3>Wallet commitment</h3><p>Eligible users commit stablecoins under campaign and final subscription documents.</p></div>
<div class="sequence-step"><h3>Allocation</h3><p>Economic interests are represented by campaign tokens; refund rules are offering-specific.</p></div>
<div class="sequence-step"><h3>Trading and settlement</h3><p>Transferability, lock-up, liquidity, IPO timing and settlement form remain product-specific.</p></div></div>
<div class="callout risk"><strong>Rights limitation.</strong> Unless definitive documents say otherwise, campaign tokens grant no direct target-company ownership, voting, information, dividend, guaranteed-liquidity or guaranteed-redemption rights.</div>
<h2>Fee evidence</h2><p>The Arbitrum <code>AssetType.IPO</code> fee was 18% on 2026-07-22. Campaign fees may differ and are not described as enforced by that generic setting without transaction evidence.</p>
''' + nav("2-2-product-suite.html", "Asset model", "3-architecture.html", "System map"))

PAGES["3-architecture.html"] = ("System map", "architecture", "en", head(
    "Architecture / 01", "System map and responsibility boundary",
    "The chain secures transfers and contract execution. Off-chain services supply brokerage execution, reconciliation, custody, compliance and reserve data."
) + f'''
<div class="grid">
<article class="card">{badge("verified", "On-chain verified")}<h3>Wallet + proxy</h3><p>Approvals, transfers, order events, fee reads and token balances.</p></article>
<article class="card">{badge("verified", "On-chain verified")}<h3>Factory + tokens</h3><p>Symbol mapping and owner-controlled creation, minting and burning.</p></article>
<article class="card">{badge("disclosed", "Operator disclosed")}<h3>Order service</h3><p>Event monitoring, brokerage routing, cancellation and reconciliation.</p></article>
<article class="card">{badge("disclosed", "Operator disclosed")}<h3>Issuer / custody</h3><p>Underlying assets, funds, SPVs, brokers and final settlement.</p></article></div>
<h2>Data flow</h2><pre>Wallet → StockTrading proxy → transfer + OrderCreated
                              |
                              v
                    operator → broker / fund
                              |
                              v
              owner fill / cancel / mint / burn</pre>
<div class="callout risk"><strong>Not atomic end-to-end securities settlement.</strong> Contract token transfers are atomic, but brokerage execution and underlying-asset reconciliation are off-chain.</div>
''' + nav("2-3-ipo-investing.html", "IPO model", "3-1-technical-architecture.html", "Contract architecture"))

PAGES["3-1-technical-architecture.html"] = ("Contract architecture", "contracts-architecture", "en", head(
    "Architecture / 02", "Contract architecture",
    "Three core contract types implement upgradeable trading coordination and symbol-specific ERC-20 representations."
) + '''
<div class="grid three">
<article class="card"><h3>StockTrading</h3><p>UUPS-upgradeable coordinator for order transfers, events, fees, refunds and owner-only token operations.</p></article>
<article class="card"><h3>StockTokenFactory</h3><p>Creates and indexes one <code>StandardStockToken</code> per symbol.</p></article>
<article class="card"><h3>StandardStockToken</h3><p>ERC-20 representation with 8 decimals and owner-controlled mint / burn.</p></article></div>
<h2>Upgradeable path</h2><pre>User → Proxy (stable address) → Current implementation
                                  ^
                                  |
                           owner authorizes</pre>
<h2>Privileged surface</h2><div class="table-wrap"><table><thead><tr><th>Control</th><th>Effect</th></tr></thead><tbody>
<tr><td><code>setReceivers</code></td><td>Changes fund, token and fee destinations.</td></tr>
<tr><td><code>setUsdtContract</code></td><td>Changes settlement-token contract.</td></tr>
<tr><td><code>setStockTokenFactory</code></td><td>Changes symbol-to-token resolution.</td></tr>
<tr><td><code>mintStockTokens</code> / <code>burnStockTokens</code></td><td>Changes user token supply.</td></tr>
<tr><td><code>_authorizeUpgrade</code></td><td>Allows owner-approved implementation replacement.</td></tr>
</tbody></table></div>
''' + nav("3-architecture.html", "System map", "3-2-protocol-mechanism.html", "Order lifecycle"))

PAGES["3-2-protocol-mechanism.html"] = ("Order lifecycle", "order-lifecycle", "en", head(
    "Architecture / 03", "Event-based order lifecycle",
    "The implemented contract is an event-driven coordination layer. It does not contain the ECDSA RFQ quote-validation path previously described by this site."
) + f'''
<h2>State held on-chain</h2><ul><li>Receiver, USDT, factory, fee and owner configuration.</li><li>ERC-20 balances and allowances.</li><li>Order nonce and create/fill/cancel logs.</li></ul>
<h2>State not held on-chain</h2><ul><li>An order struct containing original terms.</li><li>A pending / filled / cancelled state machine.</li><li>Broker execution price or trade confirmation.</li><li>A signed market-maker quote validated by the supplied implementation.</li></ul>
<div class="callout risk">{badge("open", "Open finding MED-01")}<p><strong>Events are not enforceable order state.</strong> Privileged calls can emit fill or cancellation without proving order existence, pending status or parameter match.</p></div>
<h2>Cancellation</h2><p>The user signs an order ID for the API. The privileged backend verifies it and calls <code>markOrderCancelled</code>. Refunds require configured receiver allowances and balances.</p>
''' + nav("3-1-technical-architecture.html", "Contracts", "4-security.html", "Security model"))

PAGES["4-security.html"] = ("Security model", "security", "en", head(
    "Verification / 01", "Security model and open trust",
    "Security is split across contract code, privileged administration, off-chain execution, custody and external evidence. No single badge covers the whole system."
) + f'''
<div class="evidence-rail">
<div class="rail-item">{badge("verified", "On-chain verified")}<b>Reentrancy guard</b><small>Applied to orders, cancellation and withdrawals.</small></div>
<div class="rail-item">{badge("assessed", "Third-party assessed")}<b>Aegixe</b><small>0 Critical, 0 High, 1 Medium, 1 Low.</small></div>
<div class="rail-item">{badge("open", "Open")}<b>Admin control</b><small>Owner controls upgrades, receivers, fees, mint and burn.</small></div>
<div class="rail-item">{badge("unavailable", "Unavailable")}<b>Audit-bytecode link</b><small>No commit or deployed bytecode hash in report.</small></div></div>
<h2>Control layers</h2><div class="grid">
<article class="card"><h3>Contract controls</h3><p>Input bounds, allowance checks, transfer checks, reentrancy guard, fee caps and disabled implementation initializers.</p></article>
<article class="card"><h3>Operational controls</h3><p>Owner-key security, deployment review, broker reconciliation and receiver-account management are not contract-governed.</p></article></div>
<div class="callout risk"><strong>Current limitation.</strong> The audit recommends multisig/timelock governance and on-chain order state. Both findings remain observable.</div>
''' + nav("3-2-protocol-mechanism.html", "Order lifecycle", "4-1-trusted-custody.html", "Custody & reserves"))

PAGES["4-1-trusted-custody.html"] = ("Custody and reserves", "reserves", "en", head(
    "Verification / 02", "Custody and reserve evidence",
    "On-chain supply is observable. Matching underlying assets remain off-chain facts that must be established per product and reporting period."
) + f'''
<h2>Evidence chain</h2><div class="sequence">
<div class="sequence-step"><h3>Read token supply</h3><p>{badge("verified", "On-chain verified")} Inspect token balances and mint/burn events.</p></div>
<div class="sequence-step"><h3>Identify legal holder</h3><p>{badge("disclosed", "Operator disclosed")} Product documents identify issuer, fund, broker or custodian.</p></div>
<div class="sequence-step"><h3>Verify external data</h3><p>{badge("assessed", "Third-party assessed")} zkPass is intended to prove selected account facts while preserving confidentiality.</p></div>
<div class="sequence-step"><h3>Match scope and time</h3><p>Confirm proof covers the exact product, asset, account and measurement time.</p></div></div>
<div class="callout"><p>{badge("unavailable", "Service in progress")}</p><p>The zkPass service is temporarily linked at <a href="https://dshare-zkfetch.zkpass.org" target="_blank" rel="noopener noreferrer">dshare-zkfetch.zkpass.org</a>. Its root returned not found on 2026-07-22 and did not expose a readable proof, so no completed-proof status is shown.</p></div>
<h2>Product distinctions</h2><div class="table-wrap"><table><thead><tr><th>Product</th><th>Custody statement</th><th>Status</th></tr></thead><tbody>
<tr><td>General stock tokens</td><td>Institutional brokerage arrangement described by operator.</td><td>{badge("disclosed", "Operator disclosed")}</td></tr>
<tr><td>SpaceX / Anthropic</td><td>DigiFT-linked fund mapping in campaign materials.</td><td>{badge("disclosed", "Operator disclosed")}</td></tr>
<tr><td>Kimi</td><td>Hong Kong LPF; offshore fund identity under NDA.</td><td>{badge("unavailable", "Available under NDA")}</td></tr>
</tbody></table></div>
''' + nav("4-security.html", "Security model", "4-2-deployments.html", "Deployments"))

PAGES["4-2-deployments.html"] = ("Deployments", "deployments", "en", head(
    "Verification / 03", "Verified deployments",
    "Addresses and parameters below were read from public RPC endpoints on 2026-07-22. Re-check before approving tokens or sending a transaction."
) + '''
<h2>Arbitrum One · production</h2><div class="address-list">
<div class="address-row"><span class="label">Chain ID</span><span class="address">42161</span><a class="external" href="https://arbiscan.io" target="_blank" rel="noopener noreferrer">Explorer ↗</a></div>
<div class="address-row"><span class="label">Trading proxy</span><span class="address">0x9748C6B5E16599E78351339CA2E24268B5C39C3E</span><a class="external" href="https://arbiscan.io/address/0x9748C6B5E16599E78351339CA2E24268B5C39C3E#code" target="_blank" rel="noopener noreferrer">Code ↗</a></div>
<div class="address-row"><span class="label">Implementation</span><span class="address">0x43AEaF1BE7c6f22DDc59D2339Ee103c537F4318F</span><a class="external" href="https://arbiscan.io/address/0x43AEaF1BE7c6f22DDc59D2339Ee103c537F4318F#code" target="_blank" rel="noopener noreferrer">Code ↗</a></div>
<div class="address-row"><span class="label">Token factory</span><span class="address">0x4D823Cdbbc26078Cc026229622a9ae169Eb94b43</span><a class="external" href="https://arbiscan.io/address/0x4D823Cdbbc26078Cc026229622a9ae169Eb94b43#code" target="_blank" rel="noopener noreferrer">Code ↗</a></div>
<div class="address-row"><span class="label">Settlement USDT</span><span class="address">0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9</span><a class="external" href="https://arbiscan.io/address/0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9" target="_blank" rel="noopener noreferrer">Token ↗</a></div>
<div class="address-row"><span class="label">Owner</span><span class="address">0xA1107e707aDde5E98255988163DBb48BEFA2BBd1</span><a class="external" href="https://arbiscan.io/address/0xA1107e707aDde5E98255988163DBb48BEFA2BBd1" target="_blank" rel="noopener noreferrer">Account ↗</a></div></div>
<div class="grid three"><article class="card"><span class="metric">0.15%</span><span class="metric-label">Global fee · 15 bps</span></article><article class="card"><span class="metric">18%</span><span class="metric-label">IPO fee · 1800 bps</span></article><article class="card"><span class="metric">1 USDT</span><span class="metric-label">Minimum fee</span></article></div>
<h2>Other verified deployments</h2><div class="table-wrap"><table><thead><tr><th>Network</th><th>Status</th><th>Proxy</th><th>Implementation</th><th>Parameters</th></tr></thead><tbody>
<tr><td>Sepolia · 11155111</td><td>Test</td><td class="address">0x07B179A011e6FB72F09A5DEc685c285c22d0b3c9</td><td class="address">0xdACAdbb693FcEba041aBa6592825a15C161AE8c9</td><td>100 bps global · 5 bps IPO · 0.5 test USDC</td></tr>
<tr><td>Monad · 143</td><td>Experimental</td><td class="address">0x66da08c521323a094cc5fb5c9f37e43e8884c1b0</td><td class="address">0x3765fEd8439E7F3B202645B6514C13a7DC6D1976</td><td>10 bps global · 5 bps IPO · 1 USDT</td></tr>
</tbody></table></div>
<div class="callout verified-callout"><strong>Method.</strong> Non-empty proxy bytecode, EIP-1967 implementation storage, and view calls for owner, fees, settlement token and factory. <a href="assets/data/deployments.json">Machine-readable manifest</a>.</div>
''' + nav("4-1-trusted-custody.html", "Custody & reserves", "4-3-security-audit.html", "Security assessment"))

PAGES["4-3-security-audit.html"] = ("Security assessment", "audit", "en", head(
    "Verification / 04", "Aegixe security assessment",
    "The report found no confirmed Critical or High vulnerability, one Medium design risk and one Low centralized-control risk. Both findings remain visible."
) + f'''
<div class="severity"><div class="severity-item"><b>0</b>0 Critical</div><div class="severity-item"><b>0</b>0 High</div><div class="severity-item medium"><b>1</b>1 Medium</div><div class="severity-item low"><b>1</b>1 Low</div></div>
<div class="finding"><div class="finding-head"><h3>MED-01 · Event-only orders</h3>{badge("open", "Open")}</div><p>No verifiable order state or enforced lifecycle transition.</p></div>
<div class="finding"><div class="finding-head"><h3>LOW-01 · Administrator controls</h3>{badge("open", "Open")}</div><p>Owner controls receivers, addresses, fees, minting, burning, withdrawals and upgrades.</p></div>
<h2>Report artifact</h2><div class="card"><p><strong>Assessor:</strong> Aegixe<br><strong>Assessment date:</strong> 2026-04-27<br><strong>Scope:</strong> StockTrading, StockTokenFactory and StandardStockToken</p><p class="address">SHA-256 · 437d248e1d4854e3342d6085d08fd7ab466591e3bb4df6dbd4ca31b04a77e7d2</p><p><a href="assets/reports/deshare-stock-contract-security-assessment-aegixe-2026-04-27.pdf">Download original PDF</a></p></div>
<div class="callout risk"><strong>Limitations.</strong> No Git commit, deployment address, bytecode hash or remediation table is identified. The overview page also says Base DeFi staking/settlement while detailed scope says stock contracts. Bytecode equivalence is not claimed.</div>
''' + nav("4-2-deployments.html", "Deployments", "5-developer-docs.html", "Developer overview"))

PAGES["5-developer-docs.html"] = ("Developer overview", "developer", "en", head(
    "Developers / 01", "Integrate against published evidence",
    "Confirm the active proxy, network and settlement token, load the checked-in ABI, then calculate fees from the contract rather than hard-coding historical values."
) + '''
<h2>Quick start</h2><div class="sequence">
<div class="sequence-step"><h3>Verify network</h3><p>Arbitrum One chain ID is <code>42161</code>.</p></div>
<div class="sequence-step"><h3>Load proxy ABI</h3><p>Use the active proxy with <a href="assets/abi/StockTrading.json">StockTrading.json</a>.</p></div>
<div class="sequence-step"><h3>Read configuration</h3><p>Read settlement token, factory, fee, asset fee and minimum fee.</p></div>
<div class="sequence-step"><h3>Approve exact assets</h3><p>Show spender and requested amount before ERC-20 approval.</p></div></div>
<pre>const provider = new ethers.BrowserProvider(window.ethereum);
const signer = await provider.getSigner();
const network = await provider.getNetwork();
if (network.chainId !== 42161n) throw new Error('Switch to Arbitrum One');
const trading = new ethers.Contract(TRADING_PROXY, STOCK_TRADING_ABI, signer);
const fee = await trading.calculateFee(orderValue, 1);</pre>
<div class="grid"><article class="card"><h3><a href="5-1-api-reference.html">REST API</a></h3><p>Portfolio reads and signature-authorized cancellation.</p></article><article class="card"><h3><a href="5-2-contract-reference.html">Contract & ABI</a></h3><p>Functions, events, enums and downloads.</p></article></div>
''' + nav("4-3-security-audit.html", "Assessment", "5-1-api-reference.html", "API reference"))

PAGES["5-1-api-reference.html"] = ("API reference", "api", "en", head(
    "Developers / 02", "REST API reference",
    "The supplied integration document identifies a production API base and two portfolio operations. These examples are operator-documented and not independently authenticated here."
) + f'''
<div class="callout">{badge("disclosed", "Operator documented")}<p><strong>Base:</strong> <code>https://api.deshare.finance/api/v1/</code>. Use documented resource paths.</p></div>
<h2>GET /portfolio/positions/{{symbol}}</h2><p>Returns position details for one symbol. Required header: <code>X-User-Address</code>.</p>
<pre>fetch(API_BASE_URL + '/portfolio/positions/AAPL', {{
  headers: {{ accept: 'application/json', 'X-User-Address': userAddress }}
}});</pre>
<h2>POST /portfolio/cancel-order</h2><p>The user signs the order ID. The backend verifies the recovered signer and invokes privileged cancellation.</p>
<pre>const signature = await signer.signMessage(orderId);
fetch(API_BASE_URL + '/portfolio/cancel-order', {{
  method: 'POST',
  headers: {{ 'Content-Type': 'application/json' }},
  body: JSON.stringify({{ order_id: orderId, signature, user_address: userAddress }})
}});</pre>
<div class="callout risk"><strong>Not user-executed on-chain.</strong> Cancellation depends on API acceptance, owner action, receiver allowances and balances.</div>
''' + nav("5-developer-docs.html", "Developer overview", "5-2-contract-reference.html", "Contract reference"))

PAGES["5-2-contract-reference.html"] = ("Contract and ABI reference", "contract-reference", "en", head(
    "Developers / 03", "Contract and ABI reference",
    "Use the active proxy with the ABI below. Order quantity uses 8 decimals; settlement price, fees and interest use 6 decimals."
) + '''
<h2>Downloads</h2><p><a href="assets/abi/StockTrading.json">StockTrading.json</a> · <a href="assets/abi/StockTokenFactory.json">StockTokenFactory.json</a> · <a href="assets/abi/StandardStockToken.json">StandardStockToken.json</a></p>
<h2>Current order signatures</h2><pre>function createBuyOrder(
 string _stockSymbol, OrderType _orderType, uint256 _amount,
 uint256 _price, uint256 _expiresAt, uint256 _marginLevel,
 uint256 _interest, AssetType _assetType
) returns (uint256 orderId)

function createSellOrder(
 string _stockSymbol, OrderType _orderType, uint256 _amount,
 uint256 _price, uint256 _expiresAt, uint256 _marginLevel,
 uint256 _interest, AssetType _assetType
) returns (uint256 orderId)</pre>
<h2>Enums and precision</h2><div class="table-wrap"><table><thead><tr><th>Type</th><th>Values</th></tr></thead><tbody>
<tr><td><code>OrderType</code></td><td>0 LIMIT · 1 MARKET</td></tr>
<tr><td><code>AssetType</code></td><td>0 HK · 1 US · 2 SG · 3 JP · 4 KR · 5 IPO · 6 OT</td></tr>
<tr><td>Stock amount</td><td>8 decimals</td></tr><tr><td>USDT / price / interest</td><td>6 decimals</td></tr>
</tbody></table></div>
<h2>Events</h2><p><code>OrderCreated</code>, <code>OrderFilled</code>, <code>OrderCancelled</code>, <code>USDTTransferred</code>, <code>StockTokenTransferred</code>, <code>FeeCharged</code>, <code>StockTokensMinted</code> and <code>StockTokensBurned</code>.</p>
<div class="callout"><strong>Version correction.</strong> Older five-argument examples do not match the current inspected implementation. This page uses the eight-argument signature.</div>
''' + nav("5-1-api-reference.html", "API reference", "5-faq.html", "Operational FAQ"))

PAGES["5-faq.html"] = ("Operational FAQ", "faq", "en", head(
    "Developers / 04", "Operational FAQ",
    "Answers are scoped to available evidence and point to the exact place a reader can verify or challenge them."
) + '''
<h2>How do I verify the implementation?</h2><p>Read the EIP-1967 slot and compare it with <a href="4-2-deployments.html">Deployments</a>.</p>
<h2>Does the audit cover deployed bytecode?</h2><p>No commit, address or bytecode hash is named, so bytecode equivalence is not claimed.</p>
<h2>Are orders fully on-chain?</h2><p>Transfers and events are on-chain. Brokerage execution and order reconciliation are operational dependencies.</p>
<h2>How do I calculate fees?</h2><p>Call <code>calculateFee(orderValue, assetType)</code> on the active proxy.</p>
<h2>Where is the reserve proof?</h2><p>The zkPass URL is on the custody page; its human-readable view is still in progress.</p>
<h2>How can I review the Kimi fund?</h2><p>Contact <a href="mailto:bd@deshare.finance">bd@deshare.finance</a> for NDA-gated materials.</p>
''' + nav("5-2-contract-reference.html", "Contract reference", "6-1-pre-spacex-en.html", "Offerings"))

PAGES["6-1-pre-spacex-en.html"] = ("Pre SpaceX", "spacex-en", "en", campaign_head(
    "Offering / Operator disclosed", "Pre SpaceX",
    "Economic exposure linked to an offshore fund holding SpaceX equity. This is not direct ownership of SpaceX shares.",
    '<span class="metric">PreSPX</span><span class="metric-label">Token label</span><p>77,400 max supply<br>6.46 USDT unit price<br>5% subscription fee<br>15% performance carry</p>'
) + '''
<div class="language-switch"><a href="6-1-pre-spacex-zh.html">中文</a><a href="6-1-pre-spacex-en.html">English</a></div>
<h2>Structure and lifecycle</h2><p>Campaign materials describe a DigiFT-linked asset mapping and lottery allocation. Unallocated principal and the corresponding fee are stated to be refunded. Allocated tokens may trade on the campaign OTC venue.</p>
<div class="callout risk"><strong>Risk and rights.</strong> No direct ownership, voting, dividend or information rights; no SpaceX affiliation; limited liquidity; possible partial or total loss; unavailable to US, Mainland China and other restricted users.</div>
''' + nav("5-faq.html", "Documentation", "6-2-pre-anthropic-en.html", "Pre Anthropic"))

PAGES["6-1-pre-spacex-zh.html"] = ("Pre SpaceX", "spacex-zh", "zh-CN", campaign_head(
    "发行计划 / 运营方披露", "Pre SpaceX",
    "通过境外基金所持 SpaceX 股权取得经济收益敞口，不构成对 SpaceX 股份的直接持有。",
    '<span class="metric">PreSPX</span><span class="metric-label">代币名称</span><p>最大发行 77,400 份<br>每份 6.46 USDT<br>认购费 5%<br>收益分成 15%</p>'
) + '''
<div class="language-switch"><a href="6-1-pre-spacex-zh.html">中文</a><a href="6-1-pre-spacex-en.html">English</a></div>
<h2>结构与生命周期</h2><p>活动资料描述了与 DigiFT 相关的资产映射及抽签分配机制，未获分配部分的本金及对应费用按规则退回；获配代币可按平台规则在 OTC 市场交易。</p>
<div class="callout risk"><strong>权利与风险。</strong> 不享有直接股权、投票权、分红权或信息权；与 SpaceX 无关联；可能缺乏流动性并损失部分或全部本金；美国、中国大陆及其他受限地区用户不得参与。</div>
''' + nav("5-faq.html", "技术文档", "6-2-pre-anthropic-zh.html", "Pre Anthropic"))

PAGES["6-2-pre-anthropic-en.html"] = ("Pre Anthropic", "anthropic-en", "en", campaign_head(
    "Offering / Operator disclosed", "Pre Anthropic",
    "Economic exposure linked to a fund holding Anthropic equity. This is not direct ownership of Anthropic shares.",
    '<span class="metric">PREANTHROPIC</span><span class="metric-label">Token label</span><p>USD 900B reference valuation<br>18% subscription fee<br>20% performance carry</p>'
) + '''
<div class="language-switch"><a href="6-2-pre-anthropic-zh.html">中文</a><a href="6-2-pre-anthropic-en.html">English</a></div>
<h2>Structure and lifecycle</h2><p>Campaign materials describe a DigiFT-linked mapping and lottery allocation. Unallocated principal and the corresponding fee are stated to be refunded; allocated tokens may trade on the campaign OTC venue.</p>
<div class="callout risk"><strong>Risk and rights.</strong> No direct ownership, voting, dividend or information rights; no Anthropic affiliation; limited liquidity; possible partial or total loss; unavailable to US, Mainland China and other restricted users.</div>
''' + nav("6-1-pre-spacex-en.html", "Pre SpaceX", "6-3-pre-kimi-en.html", "Pre Kimi"))

PAGES["6-2-pre-anthropic-zh.html"] = ("Pre Anthropic", "anthropic-zh", "zh-CN", campaign_head(
    "发行计划 / 运营方披露", "Pre Anthropic",
    "通过基金所持 Anthropic 股权取得经济收益敞口，不构成对 Anthropic 股份的直接持有。",
    '<span class="metric">PREANTHROPIC</span><span class="metric-label">代币名称</span><p>参考估值 9,000 亿美元<br>认购费 18%<br>收益分成 20%</p>'
) + '''
<div class="language-switch"><a href="6-2-pre-anthropic-zh.html">中文</a><a href="6-2-pre-anthropic-en.html">English</a></div>
<h2>结构与生命周期</h2><p>活动资料描述了与 DigiFT 相关的资产映射及抽签分配机制，未获分配部分的本金及对应费用按规则退回；获配代币可按平台规则在 OTC 市场交易。</p>
<div class="callout risk"><strong>权利与风险。</strong> 不享有直接股权、投票权、分红权或信息权；与 Anthropic 无关联；可能缺乏流动性并损失部分或全部本金；美国、中国大陆及其他受限地区用户不得参与。</div>
''' + nav("6-1-pre-spacex-zh.html", "Pre SpaceX", "6-3-pre-kimi-zh.html", "Pre Kimi"))

PAGES["6-3-pre-kimi-en.html"] = ("Pre Kimi", "kimi-en", "en", campaign_head(
    "Offering / Operator disclosed", "Kimi · offshore USD fund new-share interest",
    "A structured economic interest through an L1 Hong Kong LPF at a USD 31.5 billion pre-money reference valuation.",
    '<span class="metric">PreKimiToken</span><span class="metric-label">Token name · not yet deployed</span><p>1,000,000 maximum interests<br>100 USDT per interest<br>8% subscription + management fee<br>20% performance carry</p>'
) + f'''
<div class="language-switch"><a href="6-3-pre-kimi-zh.html">中文</a><a href="6-3-pre-kimi-en.html">English</a></div>
<div class="callout">{badge("disclosed", "Operator disclosed")}<p>Legal structure: L1 – Hong Kong Limited Partnership Fund (LPF). LPF formation is not regulatory approval, allocation guarantee or return guarantee.</p></div>
<h2>Offering parameters</h2><div class="table-wrap"><table><tbody>
<tr><th>Reference valuation</th><td>USD 31.5 billion pre-money</td></tr><tr><th>Legal structure</th><td>L1 – Hong Kong LPF</td></tr>
<tr><th>Maximum issuance</th><td>1,000,000 interests / PreKimiToken</td></tr><tr><th>Unit price</th><td>100 USDT</td></tr>
<tr><th>Subscription + management fee</th><td>8%</td></tr><tr><th>Performance carry</th><td>20%</td></tr>
<tr><th>Restricted users</th><td>United States and Mainland China users</td></tr></tbody></table></div>
<h2>Confidential fund due diligence</h2><p>The offshore USD fund is not publicly identified at the fund manager's request. Eligible counterparties may contact <a href="mailto:bd@deshare.finance">bd@deshare.finance</a> for materials after signing an NDA and completing approval.</p>
<h2>Participation</h2><div class="sequence"><div class="sequence-step"><h3>Eligibility and documents</h3><p>Confirm jurisdiction and review final documents.</p></div><div class="sequence-step"><h3>Subscription</h3><p>Commit USDT under final rules; fee timing and base are controlled by definitive documents.</p></div><div class="sequence-step"><h3>Allocation and settlement</h3><p>Allocation, refund, transfer, lock-up, liquidity and settlement remain subject to final documents.</p></div></div>
<div class="callout risk"><strong>Rights and risk.</strong> PreKimiToken has no published contract address and is not presented as deployed. Unless final documents say otherwise, it grants no direct target-company shares, voting, information or dividend rights. Valuation may change and investors may lose part or all capital.</div>
''' + nav("6-2-pre-anthropic-en.html", "Pre Anthropic", "terms.html", "Terms of Service"))

PAGES["6-3-pre-kimi-zh.html"] = ("Pre Kimi", "kimi-zh", "zh-CN", campaign_head(
    "发行计划 / 运营方披露", "Kimi · 境外美元基金新股份额",
    "通过 L1 香港有限合伙基金（LPF）取得结构化经济权益，投前参考估值为 315 亿美元。",
    '<span class="metric">PreKimiToken</span><span class="metric-label">Token 名称 · 尚未公布部署</span><p>最大发行 1,000,000 份<br>每份 100 USDT<br>手续费及管理费 8%<br>收益分成 20%</p>'
) + f'''
<div class="language-switch"><a href="6-3-pre-kimi-zh.html">中文</a><a href="6-3-pre-kimi-en.html">English</a></div>
<div class="callout">{badge("disclosed", "运营方披露")}<p>法律结构为 L1 – 香港有限合伙基金（LPF）。采用 LPF 结构不代表监管批准、获配保证或收益保证。</p></div>
<h2>发行参数</h2><div class="table-wrap"><table><tbody>
<tr><th>投前参考估值</th><td>315 亿美元（USD 31.5 billion）</td></tr><tr><th>法律结构</th><td>L1 – 香港 LPF</td></tr>
<tr><th>最大发行</th><td>1,000,000 份 / PreKimiToken</td></tr><tr><th>每份定价</th><td>100 USDT</td></tr>
<tr><th>手续费及管理费</th><td>8%</td></tr><tr><th>收益分成</th><td>20%</td></tr>
<tr><th>受限用户</th><td>美国用户及中国大陆用户</td></tr></tbody></table></div>
<h2>保密基金尽调</h2><p>因基金方要求，具体境外美元基金名称及详细资料不对外公开。符合条件的合作方可联系 <a href="mailto:bd@deshare.finance">bd@deshare.finance</a>，在签署 NDA 并通过审核后获取资料。</p>
<h2>参与流程</h2><div class="sequence"><div class="sequence-step"><h3>资格与文件</h3><p>确认司法辖区资格并阅读最终发行文件。</p></div><div class="sequence-step"><h3>提交认购</h3><p>按最终规则提交 USDT；费用时点及计算基数以正式文件为准。</p></div><div class="sequence-step"><h3>分配与交割</h3><p>分配、退款、转让、锁定期、流动性及交割均以最终文件为准。</p></div></div>
<div class="callout risk"><strong>权利与风险。</strong> PreKimiToken 尚未公布合约地址，本页不将其描述为已部署。除非正式文件另有约定，其不代表目标公司的直接股份、投票权、信息权或分红权。估值可能变化，投资者可能损失部分或全部本金。</div>
''' + nav("6-2-pre-anthropic-zh.html", "Pre Anthropic", "terms.html", "服务条款"))

for filename, (title, key, lang, body) in PAGES.items():
    (ROOT / filename).write_text(shell(title, key, body, lang), encoding="utf-8")

print(f"Generated {len(PAGES)} documentation pages")
