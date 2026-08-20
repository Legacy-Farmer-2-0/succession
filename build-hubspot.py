#!/usr/bin/env python3
"""
Builds self-contained, single-file versions of the .dc.html pages for pasting
directly into HubSpot's Design Manager (or anywhere else that can't serve the
sibling files — support.js, tracking.js, image-slot.js, the _ds/ design-system
folder, assets/ — at their relative paths).

Inlines:
  - fonts.css + _ds_bundle.css into one <style> block (Inter woff2 files
    embedded as base64 data URIs; only the 8 weights actually used by these
    pages, not the full design-system font set)
  - support.js / image-slot.js / tracking.js as `<script src="data:...">`
    (NOT inlined as literal text — several of these files contain the
    substrings "<!--" and "<script" inside their own documentation comments,
    which trips an obscure part of the HTML tokenizer spec — the "script data
    double escaped" state — when pasted as literal <script> text content, and
    silently corrupts/merges adjacent <script> tags. Data-URI src sidesteps
    the entire problem class.)
  - the logo PNG as a base64 data URI

Run this again any time Split The Farm Optin.dc.html / Split The Farm
Watch.dc.html / tracking.js change, to regenerate hubspot/*.hubspot.html.
"""
import base64
import os

DS = "_ds/software-legacy-farmer-design-system-v2-b0e1703c-9f94-4b37-a392-3e409d3a3459"

FONT_WEIGHTS = [
    ("400", "inter-latin-400-normal.woff2", "inter-latin-ext-400-normal.woff2"),
    ("500", "inter-latin-500-normal.woff2", "inter-latin-ext-500-normal.woff2"),
    ("600", "inter-latin-600-normal.woff2", "inter-latin-ext-600-normal.woff2"),
    ("700", "inter-latin-700-normal.woff2", "inter-latin-ext-700-normal.woff2"),
]
LATIN_RANGE = (
    "U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, "
    "U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, "
    "U+2212, U+2215, U+FEFF, U+FFFD"
)
EXT_RANGE = (
    "U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, "
    "U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, "
    "U+20A0-20AB, U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF"
)


def read_text(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def read_b64(p):
    with open(p, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


def js_data_uri(path):
    b64 = base64.b64encode(read_text(path).encode("utf-8")).decode("ascii")
    return f"data:text/javascript;base64,{b64}"


def build_inline_font_css():
    parts = []
    for weight, latin_file, ext_file in FONT_WEIGHTS:
        latin_b64 = read_b64(f"{DS}/fonts/{latin_file}")
        ext_b64 = read_b64(f"{DS}/fonts/{ext_file}")
        parts.append(
            f"@font-face{{font-family:'Inter';font-style:normal;font-display:swap;"
            f"font-weight:{weight};src:url(data:font/woff2;base64,{ext_b64}) "
            f"format('woff2');unicode-range:{EXT_RANGE};}}\n"
            f"@font-face{{font-family:'Inter';font-style:normal;font-display:swap;"
            f"font-weight:{weight};src:url(data:font/woff2;base64,{latin_b64}) "
            f"format('woff2');unicode-range:{LATIN_RANGE};}}"
        )
    return "\n".join(parts)


def main():
    inlined_fonts_css = build_inline_font_css()
    ds_bundle_css = read_text(f"{DS}/_ds_bundle.css")
    logo_data_uri = f"data:image/png;base64,{read_b64('assets/legacy-farmer-logo.png')}"
    tracking_uri = js_data_uri("tracking.js")
    support_uri = js_data_uri("support.js")
    image_slot_uri = js_data_uri("image-slot.js")

    link_block = (
        f'<link rel="stylesheet" href="{DS}/fonts/fonts.css">\n'
        f'<link rel="stylesheet" href="{DS}/_ds_bundle.css">\n'
        f'<link rel="stylesheet" href="{DS}/styles.css">'
    )
    inline_style = f"<style>\n{inlined_fonts_css}\n{ds_bundle_css}\n</style>"

    def build(src_path, out_path):
        html = read_text(src_path)
        assert link_block in html, f"link block not found in {src_path}"
        html = html.replace(link_block, inline_style)
        for src, data_uri in [
            ("./tracking.js", tracking_uri),
            ("./support.js", support_uri),
            ("./image-slot.js", image_slot_uri),
        ]:
            tag = f'<script src="{src}"></script>'
            if tag in html:
                html = html.replace(tag, f'<script src="{data_uri}"></script>')
        html = html.replace(
            'src="assets/legacy-farmer-logo.png"', f'src="{logo_data_uri}"'
        )
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(out_path, len(html), "bytes")

    os.makedirs("hubspot", exist_ok=True)
    build("Split The Farm Optin.dc.html", "hubspot/Split The Farm Optin.hubspot.html")
    build("Split The Farm Watch.dc.html", "hubspot/Split The Farm Watch.hubspot.html")


if __name__ == "__main__":
    main()
