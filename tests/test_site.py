import hashlib
import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_ROUTES = {
    "index.html",
    "4-2-deployments.html",
    "4-3-security-audit.html",
    "5-developer-docs.html",
    "5-1-api-reference.html",
    "5-2-contract-reference.html",
    "6-3-pre-kimi-zh.html",
    "6-3-pre-kimi-en.html",
    "site.js",
}
DOCUMENTATION_PAGES = {
    "index.html",
    "2-platform-features.html",
    "2-1-core-features.html",
    "2-2-product-suite.html",
    "2-3-ipo-investing.html",
    "3-architecture.html",
    "3-1-technical-architecture.html",
    "3-2-protocol-mechanism.html",
    "4-security.html",
    "4-1-trusted-custody.html",
    "4-2-deployments.html",
    "4-3-security-audit.html",
    "5-faq.html",
    "5-developer-docs.html",
    "5-1-api-reference.html",
    "5-2-contract-reference.html",
    "6-1-pre-spacex-en.html",
    "6-1-pre-spacex-zh.html",
    "6-2-pre-anthropic-en.html",
    "6-2-pre-anthropic-zh.html",
    "6-3-pre-kimi-en.html",
    "6-3-pre-kimi-zh.html",
    "privacy.html",
    "terms.html",
}


class IdParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.h1_count = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "h1":
            self.h1_count += 1


class SiteTests(unittest.TestCase):
    def test_required_routes_exist(self):
        missing = sorted(name for name in REQUIRED_ROUTES if not (ROOT / name).exists())
        self.assertEqual([], missing)

    def test_documentation_pages_use_shared_navigation(self):
        failures = []
        for name in sorted(DOCUMENTATION_PAGES):
            path = ROOT / name
            if not path.exists():
                failures.append(f"{name}: missing")
                continue
            text = path.read_text(encoding="utf-8")
            if 'src="site.js"' not in text:
                failures.append(f"{name}: no site.js")
            if not re.search(r'<body[^>]+data-page="[^"]+"', text):
                failures.append(f"{name}: no data-page")
            if 'data-site-nav' not in text:
                failures.append(f"{name}: no navigation mount")
            if 'href="index.html"' not in text:
                failures.append(f"{name}: no overview fallback")
        self.assertEqual([], failures)

    def test_internal_links_resolve(self):
        broken = []
        for page in ROOT.glob("*.html"):
            text = page.read_text(encoding="utf-8")
            for href in re.findall(r'href="([^"]+)"', text):
                if href.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                target = href.split("#", 1)[0]
                if target and not (ROOT / target).exists():
                    broken.append(f"{page.name} -> {href}")
        self.assertEqual([], broken)

    def test_html_has_single_h1_and_unique_ids(self):
        failures = []
        for name in sorted(DOCUMENTATION_PAGES):
            path = ROOT / name
            if not path.exists():
                continue
            parser = IdParser()
            parser.feed(path.read_text(encoding="utf-8"))
            duplicates = sorted({value for value in parser.ids if parser.ids.count(value) > 1})
            if parser.h1_count != 1:
                failures.append(f"{name}: {parser.h1_count} h1 elements")
            if duplicates:
                failures.append(f"{name}: duplicate ids {duplicates}")
        self.assertEqual([], failures)

    def test_pages_publish_a_favicon(self):
        missing = []
        for name in sorted(DOCUMENTATION_PAGES):
            text = (ROOT / name).read_text(encoding="utf-8")
            if 'rel="icon"' not in text:
                missing.append(name)
        self.assertEqual([], missing)

    def test_deployment_manifest(self):
        path = ROOT / "assets/data/deployments.json"
        self.assertTrue(path.exists())
        data = json.loads(path.read_text(encoding="utf-8"))
        chain_ids = [network["chainId"] for network in data["networks"]]
        self.assertEqual(len(chain_ids), len(set(chain_ids)))
        arb = next(network for network in data["networks"] if network["chainId"] == 42161)
        self.assertEqual("active", arb["status"])
        self.assertEqual(
            "0x9748C6B5E16599E78351339CA2E24268B5C39C3E",
            arb["contracts"]["proxy"],
        )
        self.assertEqual(
            "0x43AEaF1BE7c6f22DDc59D2339Ee103c537F4318F",
            arb["contracts"]["implementation"],
        )
        for network in data["networks"]:
            self.assertRegex(network["lastVerified"], r"^\d{4}-\d{2}-\d{2}$")
            for address in network["contracts"].values():
                if address:
                    self.assertRegex(address, r"^0x[a-fA-F0-9]{40}$")

    def test_protocol_copy_is_evidence_led(self):
        pages = (
            "index.html",
            "2-2-product-suite.html",
            "3-2-protocol-mechanism.html",
        )
        if any(not (ROOT / page).exists() for page in pages):
            self.fail("protocol pages missing")
        combined = "\n".join((ROOT / page).read_text(encoding="utf-8").lower() for page in pages)
        for phrase in ("perfectly trustless", "unquestionable", "absolute non-custodial"):
            self.assertNotIn(phrase, combined)
        for phrase in ("operator disclosed", "event-based", "privileged"):
            self.assertIn(phrase, combined)

    def test_contract_reference_uses_current_signature(self):
        path = ROOT / "5-2-contract-reference.html"
        self.assertTrue(path.exists())
        text = path.read_text(encoding="utf-8")
        self.assertIn("createBuyOrder", text)
        self.assertIn("createSellOrder", text)
        for parameter in ("_marginLevel", "_interest", "_assetType"):
            self.assertIn(parameter, text)
        for name in ("StockTrading.json", "StockTokenFactory.json", "StandardStockToken.json"):
            self.assertTrue((ROOT / "assets/abi" / name).exists(), name)

    def test_audit_artifact_and_disclosure(self):
        pdf = ROOT / "assets/reports/deshare-stock-contract-security-assessment-aegixe-2026-04-27.pdf"
        self.assertTrue(pdf.exists())
        self.assertEqual(
            "437d248e1d4854e3342d6085d08fd7ab466591e3bb4df6dbd4ca31b04a77e7d2",
            hashlib.sha256(pdf.read_bytes()).hexdigest(),
        )
        text = (ROOT / "4-3-security-audit.html").read_text(encoding="utf-8")
        for value in ("0 Critical", "0 High", "1 Medium", "1 Low", "MED-01", "LOW-01", "Open"):
            self.assertIn(value, text)

    def test_zkpass_is_not_presented_as_completed(self):
        text = (ROOT / "4-1-trusted-custody.html").read_text(encoding="utf-8").lower()
        self.assertIn("https://dshare-zkfetch.zkpass.org", text)
        self.assertIn("service in progress", text)
        self.assertNotIn("zkpass verified", text)

    def test_kimi_terms_match(self):
        for name in ("6-3-pre-kimi-zh.html", "6-3-pre-kimi-en.html"):
            path = ROOT / name
            self.assertTrue(path.exists(), name)
            text = path.read_text(encoding="utf-8")
            for value in ("31.5", "1,000,000", "100 USDT", "8%", "20%", "PreKimiToken"):
                self.assertIn(value, text, f"{name}: {value}")

    def test_kimi_disclosures(self):
        for name in ("6-3-pre-kimi-zh.html", "6-3-pre-kimi-en.html"):
            path = ROOT / name
            self.assertTrue(path.exists(), name)
            text = path.read_text(encoding="utf-8")
            self.assertIn("bd@deshare.finance", text)
            self.assertIn("NDA", text)
            self.assertNotRegex(text, r"0x[a-fA-F0-9]{40}")

    def test_no_empty_placeholder_file(self):
        self.assertFalse((ROOT / "deshare").exists())

    def test_stale_one_off_updater_is_removed(self):
        self.assertFalse((ROOT / "update_ipo.py").exists())


if __name__ == "__main__":
    unittest.main()
