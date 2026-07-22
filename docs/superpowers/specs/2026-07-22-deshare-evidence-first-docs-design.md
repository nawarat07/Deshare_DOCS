# DeShare Evidence-First Documentation Redesign

Date: 2026-07-22
Status: Approved direction; implementation pending specification review

## 1. Objective

Rebuild the DeShare documentation site as an evidence-first protocol and developer reference. The site must let a reader distinguish between facts that can be verified on-chain, conclusions made by an independent assessor, and statements disclosed by DeShare or an offering operator.

The redesign also adds bilingual Kimi offering pages and keeps the existing SpaceX, Anthropic, Terms of Service, and Privacy Policy pages accessible.

## 2. Goals

- Put verifiable deployment, source, ABI, API, audit, and reserve-proof information ahead of promotional product language.
- Describe the implemented order lifecycle accurately, including its off-chain dependencies and administrator-controlled operations.
- Publish current contract addresses, network identifiers, implementation relationships, and configuration values with verification timestamps.
- Publish the Aegixe assessment without hiding its open findings or evidence-chain limitations.
- Link the zkPass reserve-verification service while clearly showing that its root page is still being completed.
- Add English and Chinese Kimi offering pages using the commercial terms supplied by DeShare.
- Reduce duplicated navigation and provide a usable mobile navigation experience.

## 3. Non-Goals

- Do not change smart contracts, backend APIs, custody arrangements, or offering terms.
- Do not claim that an audit finding has been remediated unless a follow-up report or verifiable code/deployment evidence establishes that status.
- Do not claim that the Aegixe report proves the deployed bytecode is identical to the assessed source; the report does not state a commit hash, bytecode hash, or deployment address.
- Do not expose confidential fund identities or documents for the Kimi offering.
- Do not fabricate a public proof record for the current zkPass endpoint.
- Do not provide investment advice or imply direct ownership of Kimi or any other target-company shares where only an economic-interest structure is offered.

## 4. Evidence Model

Every material technical or asset-backing statement must carry one of these labels:

| Label | Meaning | Permitted evidence |
| --- | --- | --- |
| `On-chain verified` | Read directly from a public chain or explorer | RPC reads, EIP-1967 storage, verified explorer source, emitted events |
| `Third-party assessed` | Reported by an identified independent party | Aegixe report, zkPass-generated verification record when available |
| `Operator disclosed` | Stated by DeShare, a custodian, issuer, or fund operator but not independently reproduced by this site | Custody structure, campaign terms, confidential fund structure |
| `Unavailable` | Evidence is not public or cannot currently be queried | NDA-only Kimi fund details, incomplete zkPass root page, missing audit-to-bytecode mapping |

Marketing superlatives such as “perfectly trustless,” “unquestionable,” “absolute,” and “fully compliant” must be removed. Statements should identify the responsible component and its trust assumption.

## 5. Source-of-Truth Precedence

When sources conflict, the site uses this order:

1. Live public-chain reads for current deployed addresses and configuration.
2. Verified explorer source and proxy implementation slots for deployed implementation identity.
3. The Aegixe PDF for audit scope, findings, and assessment conclusions.
4. A pinned source-code commit and checked-in ABI for implementation documentation.
5. Operator-provided campaign and custody disclosures.
6. Historical README or API examples.

Conflicts must not be silently normalized. The documentation should show a short note when a historical document differs from current on-chain state.

Known conflicts already identified:

- The ABI document contains two different Arbitrum proxy addresses; the active proxy must be established by live-chain verification.
- The contract README describes different IPO fee values in different sections. On 2026-07-22, the active Arbitrum proxy returned a 15 bp global fee, an 1,800 bp `AssetType.IPO` fee, and a 1 USDT minimum fee.
- The current local contract checkout is commit `3e10d6608bd248d15b4c126e5c1501e1032a78a2`, while the public GitHub remote HEAD observed on 2026-07-22 was `d4878d01cc286dbfa0edd32fab610b5a464bfc83`; source links must therefore point to a verified public commit or to explorer-verified source rather than imply that these revisions are identical.
- The Kimi commercial fee is 8%, which must be presented as an offering term. It must not be described as enforced by the current generic on-chain IPO fee configuration without separate deployment or transaction evidence.

## 6. Information Architecture

The site remains deployable as static HTML, CSS, JavaScript, SVG, JSON, and PDF files.

### 6.1 Protocol

- `index.html` - Protocol Overview and evidence-status dashboard.
- `2-platform-features.html` - Capabilities and system boundaries.
- `2-1-core-features.html` - Buy, sell, cancel, mint, and burn lifecycle.
- `2-2-product-suite.html` - Asset model, custody roles, and trust boundaries.
- `2-3-ipo-investing.html` - IPO/Pre-IPO structure, SPV/fund flow, and economic-rights limitations.

### 6.2 Architecture

- `3-architecture.html` - System components and responsibility map.
- `3-1-technical-architecture.html` - `StockTrading`, `StockTokenFactory`, and `StandardStockToken` relationships.
- `3-2-protocol-mechanism.html` - Event-based order lifecycle, backend brokerage execution, settlement, and failure paths.

The current claim that the deployed contract validates ECDSA RFQ quotes must be removed unless a verified contract or API specification demonstrates that behavior. The documented implementation emits order events and relies on privileged backend calls for fill, cancel, mint, and burn operations.

### 6.3 Deployments and Developer Reference

- `4-2-deployments.html` - Network table, addresses, explorer links, proxy/implementation relationship, owner, and current parameters.
- `5-developer-docs.html` - Developer quick start and integration prerequisites.
- `5-1-api-reference.html` - Published REST endpoints, headers, payloads, responses, authentication assumptions, and errors.
- `5-2-contract-reference.html` - ABI, function signatures, events, enum values, precision, fee calculation, and example calls.
- `5-faq.html` - Technical and operational FAQ rather than marketing claims.

Downloadable ABI JSON files will be copied into `assets/abi/`. Examples must match the active function signatures with `_marginLevel`, `_interest`, and `_assetType`; obsolete five-argument order examples must not be presented as current.

### 6.4 Security and Transparency

- `4-security.html` - Security model, trust boundaries, privileged roles, and evidence summary.
- `4-1-trusted-custody.html` - Custody and reserve-verification model.
- `4-3-security-audit.html` - Aegixe assessment summary, findings, limitations, and original report download.

The audit artifact will be published as `assets/reports/deshare-stock-contract-security-assessment-aegixe-2026-04-27.pdf` with SHA-256:

`437d248e1d4854e3342d6085d08fd7ab466591e3bb4df6dbd4ca31b04a77e7d2`

Audit presentation requirements:

- Assessor: Aegixe.
- Assessment date: 2026-04-27; the PDF metadata indicates final generation in May 2026.
- Scope: `StockTrading`, `StockTokenFactory`, and `StandardStockToken` implementations named in the report.
- Findings: 0 Critical, 0 High, 1 Medium, 1 Low.
- MED-01: event-only orders with no verifiable on-chain order state - open in the currently inspected source.
- LOW-01: centralized administrator/configuration control - open in the currently inspected source.
- Limitation: no audited commit, deployed address, bytecode hash, remediation table, or follow-up assessment is provided.
- Document inconsistency: the report overview page refers to a Base DeFi staking/settlement system even though the detailed scope is the DeShare stock contracts.

The reserve section will link to `https://dshare-zkfetch.zkpass.org` as `Third-party assessed / service in progress`. It will state that the root URL currently does not expose a human-readable proof record and may return a not-found response until the service is completed. The site must not display a “verified” badge based solely on the existence of this URL.

Custody claims must be separated by product. General stock custody statements, DigiFT-linked campaign structures, and the confidential Kimi offshore fund must not be collapsed into a single claim that all assets are held at one broker.

### 6.5 Campaigns

Existing SpaceX and Anthropic pages remain accessible. Their statements will be edited only where necessary to use the evidence labels and consistent risk language.

New pages:

- `6-3-pre-kimi-zh.html`
- `6-3-pre-kimi-en.html`

Kimi facts supplied by DeShare:

| Field | Value |
| --- | --- |
| Offering | Kimi - offshore USD fund - new-share interest |
| Reference valuation | USD 31.5 billion pre-money |
| Legal structure | L1 - Hong Kong Limited Partnership Fund (LPF) |
| Token name | `PreKimiToken` |
| Maximum issuance | 10,000 interests/tokens |
| Unit price | 100 USDT |
| Subscription and management fee | 8% |
| Performance carry | 20% |
| Restricted users | United States users and Mainland China users |
| Underlying fund disclosure | Confidential at the fund manager's request |
| Due-diligence contact | `bd@deshare.finance`; details available after NDA execution and approval |

Kimi content rules:

- Describe the valuation as a reference pre-money valuation, not a guaranteed execution or future listing value.
- Describe LPF as the stated legal structure, not as regulatory approval or a guarantee.
- Do not name or imply the confidential underlying fund.
- Distinguish token/economic interests from direct target-company shares, voting rights, information rights, dividends, or redemption guarantees unless definitive legal documents state otherwise.
- State that offering availability is subject to eligibility review and final offering documents.
- Do not state that `PreKimiToken` has been deployed until a contract address is supplied and verified.
- Present 8% and 20% as operator-disclosed commercial terms; include timing and calculation-base limitations where final subscription documents control.
- Provide equivalent English and Chinese disclosure, parameter, process, fee, confidentiality, settlement, and risk sections.

### 6.6 Legal

- `terms.html` and `privacy.html` remain in the Legal group.
- Existing uncommitted edits in `terms.html` are user-owned and must be preserved.
- Campaign restriction language must be consistent with the Terms, while campaign pages may list only the explicitly supplied United States and Mainland China restrictions plus a reference to any other restrictions imposed by final documents.

## 7. Page Design

The visual direction remains dark and technical but removes promotional landing-page patterns.

- Use compact evidence cards for network, address, audit, reserve, and update status.
- Display contract addresses in monospace with copy and explorer actions.
- Use callouts for trust assumptions, privileged actions, open findings, and unavailable evidence.
- Use tables for deployments, functions, events, fees, and campaign parameters.
- Use sequence diagrams for buy, sell, cancel, and reserve verification flows.
- Add visible “Last verified” dates to dynamic technical facts.
- Add a mobile menu instead of hiding navigation below 768 px.
- Preserve readable line lengths and accessible contrast; do not encode meaning by color alone.

## 8. Navigation Implementation

Create a shared, build-free navigation module in `site.js` and a common page shell in `style.css`. Pages identify themselves with a stable page key, and the shared script renders desktop and mobile navigation with the active state.

The site must remain usable if JavaScript fails: each page keeps a minimal header link back to `index.html`, while the full navigation is enhanced by JavaScript.

This removes the current requirement to edit the same sidebar in every HTML file when a page is added.

## 9. Data and Update Strategy

Create `assets/data/deployments.json` as the human-maintained deployment manifest used to render or cross-check deployment tables. Each record includes:

- network name and environment;
- chain ID and RPC/explorer links;
- proxy, implementation, factory, settlement token, and owner addresses where verified;
- evidence URL or RPC method;
- `lastVerified` date;
- status: active, test, experimental, or unverified.

Implementation must re-query chain state before publishing. Networks or values that cannot be verified are displayed as unverified rather than silently copied from README files.

## 10. Error and Evidence-State Handling

- External proof or explorer links open in a new tab with safe `rel` attributes.
- An unavailable zkPass root page shows a neutral “service in progress” state, not an error disguised as success.
- Missing contract addresses render as “Not published” rather than a zero address or placeholder.
- API examples identify whether they were tested against production, derived from supplied documentation, or not independently verified.
- Conflicting values include a short discrepancy note and link to the higher-precedence source.
- Confidential evidence renders as “Available under NDA” with `mailto:bd@deshare.finance`.

## 11. Verification and Acceptance Criteria

### Content verification

- All published active-chain addresses have non-empty bytecode where applicable.
- The Arbitrum EIP-1967 implementation slot matches the published implementation address.
- Published fee, minimum-fee, owner, token, and factory values are read from the active proxy at implementation time.
- Function signatures and examples match the checked-in ABI.
- The audit summary matches the original PDF, includes both findings, and links the original file with the documented SHA-256.
- The zkPass section does not claim a successful public proof while the root endpoint is incomplete.
- Kimi English and Chinese parameter tables contain equivalent values.

### Site verification

- Every local link resolves.
- Every page has one active navigation item and a route back to the overview.
- Desktop and mobile layouts are visually inspected.
- Navigation works at widths below and above 768 px.
- Pages load without a build step and without console errors.
- The legal pages and user-modified `terms.html` content are preserved.

### Automated checks

- Run a local HTTP server and crawl all internal links.
- Validate HTML structure and duplicate IDs.
- Verify deployment manifest address format and uniqueness.
- Compare ABI function signatures used in code examples with the published ABI JSON.
- Run available contract tests as supporting evidence, but label test results separately from the independent audit.

## 12. Implementation Boundaries

The documentation repository may copy public artifacts from the supplied contract repository, but it must not modify the contract repository. Sensitive files, operational logs, private deployment material, and untracked contract-repository files must not be copied or published.

Only the supplied Aegixe report, selected ABI JSON, public source/explorer links, and deliberately written documentation artifacts are in scope.
