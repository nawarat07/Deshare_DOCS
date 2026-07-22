# SpaceX Content Restoration and Kimi K3 Offering Expansion

Date: 2026-07-22
Status: Approved design, pending implementation review

## Objective

Restore the complete pre-restructure SpaceX offering content while retaining the current evidence-first site shell, and expand both Kimi offering pages with sourced company/model context plus precise subscription, liquidity, and lock-up disclosures.

## Source Boundaries

- The complete SpaceX English and Chinese content comes from Git commit `a0ccc1d`, immediately before the evidence-first restructure.
- Kimi and Moonshot AI product facts come from Kimi's official Help Center and product documentation.
- Offering dates, pricing, eligibility, internal-market behavior, lock-up terms, fees, legal structure, and NDA availability are operator disclosures supplied by DeShare.
- Model capability statements must not be presented as evidence of valuation, investment performance, IPO timing, or liquidity.

## SpaceX Pages

The English and Chinese SpaceX pages will recover all substantive content from commit `a0ccc1d`. No product description, investment rationale, mechanics, parameter, timeline, eligibility rule, rights limitation, or risk disclosure may be removed or summarized.

The restored content will use the current shared header, sidebar navigation, footer, favicon, and responsive behavior. SpaceX-specific styles needed by the original long-form presentation may remain scoped to those pages. Duplicated legacy navigation and global shell markup will not be restored.

To prevent another accidental reduction, the long-form bodies will be stored as dedicated content fragments and loaded by the documentation generator instead of being compressed into short Python string literals.

## Kimi Company and K3 Model Context

Both Kimi pages will add a clearly separated company/product section describing Kimi as an AI assistant developed by Moonshot AI.

The Kimi K3 section will state, with official links:

- Kimi K3 was released on 2026-07-16.
- Kimi describes it as its most capable model at the time of publication.
- It has 2.8 trillion parameters.
- It uses Kimi Delta Attention and Attention Residuals.
- It supports native vision and a context window of up to one million tokens.
- It is positioned for chat, agent tasks, long-horizon coding, knowledge work, and reasoning.

Primary references:

- <https://www.kimi.com/help/agent/agent-overview>
- <https://www.kimi.com/help/getting-started/agentic-chat>

The page will explicitly distinguish these official product facts from DeShare's offering disclosures.

## Kimi Subscription and Liquidity Timeline

The offering parameters and timeline will state:

- Subscription window: 2026-07-23 through 2026-07-28.
- After subscription is completed, DeShare plans to open internal platform trading.
- Internal-market liquidity is typically limited. A listing or order does not ensure a buyer, seller, execution time, execution price, or completed trade.
- If Kimi completes a public listing, the interest is expected to remain locked for 6–12 months after the listing date.
- The actual lock-up and unlock arrangements depend on the structure used at listing and are governed by post-listing official announcements and final transaction documents.
- No exact unlock date, public listing date, external-market liquidity, or completed sale is promised.

These statements will appear in both the offering table and a dedicated timeline/risk section, in natural Chinese and English rather than literal machine translation.

## Existing Kimi Terms to Preserve

- Reference pre-money valuation: USD 31.5 billion.
- Structure: L1 Hong Kong LPF.
- Subscription plus management fee: 8%.
- Performance carry: 20%.
- Maximum issuance: 1,000,000 interests.
- Token name: `PreKimiToken`.
- Unit price: 100 USDT.
- Users from the United States and Mainland China may not participate.
- The underlying fund is confidential at the fund provider's request; details are available through `bd@deshare.finance` after NDA execution.
- No token contract address is currently published, so the documentation must not imply that the token is deployed.

## Verification

Automated tests will fail before implementation and then verify:

- Both SpaceX pages retain the long-form content size and representative original sections.
- Both Kimi pages contain the subscription dates, K3 model name, official-source links, internal-market liquidity warning, 6–12 month post-listing lock-up, and no-guaranteed-trade language.
- Existing Kimi valuation, structure, fee, eligibility, issuance, pricing, NDA, and deployment-status disclosures remain intact.
- Internal links, unique IDs, favicon, shared navigation, and single-page heading constraints still pass.

Browser verification will cover the restored long-form SpaceX page and expanded Kimi page at desktop and mobile widths, including navigation, overflow, tables, and long-section readability.

## Out of Scope

- Predicting or promising a Kimi IPO date.
- Publishing an exact unlock date before the listing structure is known.
- Representing platform internal trading as guaranteed liquidity.
- Changing the SpaceX commercial terms or rewriting its original substantive content.
- Modifying the user's separate uncommitted legal text changes in `terms.html`.
