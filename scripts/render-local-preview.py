from __future__ import annotations

import html
import json
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "tmp" / "local-site"
PAGE_FILES = [
    "index.md",
    "products/index.md",
    "how-it-works/index.md",
    "security/index.md",
    "knowledge/index.md",
    "editorial-policy/index.md",
    "about/index.md",
    "en/index.md",
    "404.html",
]


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def parse_page(relative_path: str) -> tuple[dict[str, str], str]:
    source = read(relative_path)
    match = re.match(r"^---\r?\n([\s\S]*?)\r?\n---\r?\n([\s\S]*)$", source)
    if not match:
        raise ValueError(f"Missing front matter: {relative_path}")

    data: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data, match.group(2)


def absolute_url(url: str) -> str:
    if url.startswith("http"):
        return url
    return f"https://guides.chonggrok.com{url}"


def render_head(page: dict[str, str]) -> str:
    title = page.get("seo_title", page["title"])
    canonical = page.get("canonical", absolute_url(page["permalink"]))
    language = page.get("lang", "zh-CN")
    robots = page.get(
        "robots",
        "index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1",
    )
    schema_type = page.get("schema_type", "WebPage")

    head = read("_includes/head.html")
    keep_hreflang = page["permalink"] in {"/", "/en/"}
    head = re.sub(
        r'{% if page\.url == "/" or page\.url == "/en/" %}([\s\S]*?){% endif %}',
        lambda match: match.group(1) if keep_hreflang else "",
        head,
    )
    replacements = {
        "{{ page.seo_title | default: page.title }}": html.escape(title),
        "{{ page.description | escape }}": html.escape(page["description"], quote=True),
        "{{ page.robots | default: 'index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1' }}": html.escape(
            robots, quote=True
        ),
        "{{ page.canonical | default: page.url | absolute_url }}": canonical,
        "{{ page.title | escape }}": html.escape(page["title"], quote=True),
        "{{ page.og_locale | default: 'zh_CN' }}": page.get("og_locale", "zh_CN"),
        "{{ page.title | jsonify }}": json.dumps(page["title"], ensure_ascii=False),
        "{{ page.description | jsonify }}": json.dumps(
            page["description"], ensure_ascii=False
        ),
        "{{ page.schema_type | default: 'WebPage' }}": schema_type,
        "{{ page.lang | default: 'zh-CN' }}": language,
        "{{ page.last_modified_at | default: '2026-07-31' }}": page.get(
            "last_modified_at", "2026-07-31"
        ),
    }
    for token, value in replacements.items():
        head = head.replace(token, value)
    return head


def render_header(page: dict[str, str]) -> str:
    header = read("_includes/header.html")
    return re.sub(
        r'{% if page\.current == "([^"]+)" %}aria-current="page"{% endif %}',
        lambda match: (
            'aria-current="page"' if match.group(1) == page.get("current") else ""
        ),
        header,
    )


def output_path(page: dict[str, str]) -> Path:
    if page["permalink"] == "/404.html":
        return OUTPUT / "404.html"
    clean = page["permalink"].strip("/")
    return OUTPUT / clean / "index.html"


if OUTPUT.exists():
    shutil.rmtree(OUTPUT)
OUTPUT.mkdir(parents=True)
shutil.copytree(ROOT / "assets", OUTPUT / "assets")

layout = read("_layouts/default.html")
footer = read("_includes/footer.html")
for relative_path in PAGE_FILES:
    page, content = parse_page(relative_path)
    rendered = layout
    rendered = rendered.replace(
        "{{ page.lang | default: 'zh-CN' }}", page.get("lang", "zh-CN")
    )
    rendered = rendered.replace("{% include head.html %}", render_head(page))
    rendered = rendered.replace("{% include header.html %}", render_header(page))
    rendered = rendered.replace("{% include footer.html %}", footer)
    rendered = rendered.replace("{{ content }}", content)

    target = output_path(page)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(rendered, encoding="utf-8")

(OUTPUT / "llms.txt").write_text(read("llms.txt"), encoding="utf-8")
for static_file in ["robots.txt", "sitemap.xml"]:
    _, content = parse_page(static_file)
    (OUTPUT / static_file).write_text(content, encoding="utf-8")

print(OUTPUT)
