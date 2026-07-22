import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_COMMIT = "a0ccc1d"
PAGES = {
    "en": "6-1-pre-spacex-en.html",
    "zh": "6-1-pre-spacex-zh.html",
}


def import_page(source):
    style_match = re.search(r"<style>(.*?)</style>", source, re.S)
    main_match = re.search(
        r'<main class="main-content">(.*?)</main>', source, re.S
    )
    if not style_match or not main_match:
        raise ValueError("source page is missing its style or main-content block")
    return style_match.group(1).strip(), main_match.group(1).strip()


def read_source(filename):
    result = subprocess.run(
        ["git", "show", f"{SOURCE_COMMIT}:{filename}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def main():
    content_dir = ROOT / "content" / "campaigns"
    styles_dir = ROOT / "assets" / "styles"
    content_dir.mkdir(parents=True, exist_ok=True)
    styles_dir.mkdir(parents=True, exist_ok=True)

    for language, filename in PAGES.items():
        style, body = import_page(read_source(filename))
        (content_dir / f"spacex-{language}.html").write_text(
            body + "\n", encoding="utf-8"
        )
        (styles_dir / f"spacex-{language}.css").write_text(
            style + "\n", encoding="utf-8"
        )
        print(
            f"Imported {filename}: {len(body):,} body characters, "
            f"{len(style):,} style characters"
        )


if __name__ == "__main__":
    main()
