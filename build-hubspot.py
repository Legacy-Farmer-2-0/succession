#!/usr/bin/env python3
"""
Builds self-contained, single-file versions of the .dc.html pages for pasting
directly into HubSpot's Design Manager (or anywhere else that can't serve the
sibling files — support.js, tracking.js, image-slot.js, the _ds/ design-system
folder, assets/ — at their relative paths).

Inlines, unless a hosted URL override is given for that page (see
HOSTED_OVERRIDES below):
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

HOSTED_OVERRIDES lets a specific page reference already-hosted copies of
these files by absolute URL instead of embedding them — much smaller output,
since the file no longer carries its own copy of the asset. Only applies to
the four assets listed (support.js/image-slot.js/tracking.js/the logo); the
design-system CSS + fonts are always inlined since no hosted URL for those
has been given.

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

HS_BASE = "https://43573758.fs1.hubspotusercontent-na1.net/hubfs/43573758/Succession%20Funnel"

# Page (source .dc.html) -> hosted URLs for support.js/image-slot.js/tracking.js/logo.
# Leave a page out of this dict to fall back to fully embedding everything.
HOSTED_OVERRIDES = {
    "Split The Farm Optin.dc.html": {
        "support.js": f"{HS_BASE}/support.js",
        "image-slot.js": f"{HS_BASE}/image-slot.js",
        "tracking.js": f"{HS_BASE}/tracking.js",
        "logo": f"{HS_BASE}/legacy-farmer-logo.png",
    },
    "Split The Farm Watch.dc.html": {
        "support.js": f"{HS_BASE}/support.js",
        "image-slot.js": f"{HS_BASE}/image-slot.js",
        "tracking.js": f"{HS_BASE}/tracking.js",
        "logo": f"{HS_BASE}/legacy-farmer-logo.png",
    },
}


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

    link_block = (
        f'<link rel="stylesheet" href="{DS}/fonts/fonts.css">\n'
        f'<link rel="stylesheet" href="{DS}/_ds_bundle.css">\n'
        f'<link rel="stylesheet" href="{DS}/styles.css">'
    )
    inline_style = f"<style>\n{inlined_fonts_css}\n{ds_bundle_css}\n</style>"

    def build(src_path, out_path):
        hosted = HOSTED_OVERRIDES.get(src_path, {})
        html = read_text(src_path)
        assert link_block in html, f"link block not found in {src_path}"
        html = html.replace(link_block, inline_style)

        for local_src, key in [
            ("./tracking.js", "tracking.js"),
            ("./support.js", "support.js"),
            ("./image-slot.js", "image-slot.js"),
        ]:
            tag = f'<script src="{local_src}"></script>'
            if tag not in html:
                continue
            if key in hosted:
                html = html.replace(tag, f'<script src="{hosted[key]}"></script>')
            else:
                html = html.replace(
                    tag, f'<script src="{js_data_uri(key)}"></script>'
                )

        logo_url = hosted.get(
            "logo",
            f"data:image/png;base64,{read_b64('assets/legacy-farmer-logo.png')}",
        )
        html = html.replace('src="assets/legacy-farmer-logo.png"', f'src="{logo_url}"')

        # HubSpot serves Design Manager .html files as "HTML + HubL" —
        # HubL (its server-side templating language) ALSO uses {{ ... }}
        # syntax, identical to this page's own client-side template
        # placeholders ({{ openModal }}, {{ hasLogo }}, etc). Without this,
        # HubL silently evaluates our placeholders as undefined HubL
        # variables and replaces them with empty strings *before* the
        # browser ever sees them — e.g. onClick="{{ openModal }}" becomes
        # onClick="" server-side, so the button does nothing and support.js
        # never gets a real value to work with. {% raw %}/{% endraw %} is
        # HubL's (Jinja's) own escape hatch for exactly this: everything
        # between is passed through completely unprocessed.
        #
        # Scoped to just the <x-dc>...</x-dc> element — the only place any
        # {{ }} placeholder actually appears (confirmed: none in <head>, the
        # inlined CSS, or the trailing <script> logic block). Wrapping the
        # *entire* ~540KB file in one raw block published with a bare,
        # detail-free "Error: Error" from HubSpot — a much smaller raw
        # region avoids whatever that was tripping on, on top of being the
        # more correct scoping regardless.
        assert html.count("<x-dc>") == 1 and html.count("</x-dc>") == 1
        html = html.replace("<x-dc>", "<x-dc>{% raw %}", 1)
        html = html.replace("</x-dc>", "{% endraw %}</x-dc>", 1)

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(out_path, len(html), "bytes")

    os.makedirs("hubspot", exist_ok=True)
    build("Split The Farm Optin.dc.html", "hubspot/Split The Farm Optin.hubspot.html")
    build("Split The Farm Watch.dc.html", "hubspot/Split The Farm Watch.hubspot.html")


if __name__ == "__main__":
    main()
