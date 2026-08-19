# Split The Farm — Opt-In Funnel

Lead-gen landing page for the "Split The Farm Between Your Kids" free training, exported from
[Claude Design](https://claude.ai/design). It's a static site — no build step, no framework install.
The page's interactivity (the modal, the state machine) runs via `support.js`, a small runtime that
loads React/ReactDOM from a CDN at page-load and hydrates the `<x-dc>` component in
`Split The Farm Optin.dc.html`.

## Structure

- `Split The Farm Optin.dc.html` — the opt-in landing page (served at `/` via `vercel.json`).
- `_ds/.../` — the shared design-system bundle (fonts, base styles) this page imports.
- `image-slot.js` / `support.js` — the Claude Design runtime the page depends on.
- `assets/` — brand assets (logo, etc).

## ⚠️ Two things still need to be dropped in

**1. The HubSpot form.** The modal ("Enter Your Info To Watch The Training") has a placeholder
`<div id="hubspot-form-target">` waiting for the real embed. Open
`Split The Farm Optin.dc.html`, find the `HUBSPOT FORM EMBED GOES HERE` comment, and paste the
embed snippet HubSpot gives you (the `<script>` + `hbspt.forms.create({...})` call, or the newer
`<div class="hs-form-frame" ...>` + loader script) right there — either replacing that div or
dropping the snippet inside it.

The page already listens for HubSpot's `onFormSubmitted` postMessage event and will automatically
flip the modal to the "You're in" success view once the real form submits — no extra wiring needed.

**2. Two binary assets.** The Claude Design API this was pulled from caps individual file reads at
~256 KB, which is too small for the Inter webfont files and the full-resolution logo PNG. The page
falls back gracefully without them (system sans-serif instead of Inter, no logo image), but for a
pixel-perfect match, copy these in from the original Claude Design project:

- `assets/legacy-farmer-logo.png`
- `_ds/software-legacy-farmer-design-system-v2-b0e1703c-9f94-4b37-a392-3e409d3a3459/fonts/inter-latin*.woff2`
  (the `400`, `500`, `600`, `700` weights, both `latin` and `latin-ext` variants — 8 files)

## Local preview

Because the page fetches its own HTML at load (`fetch(location.href)`) to finish hydrating, open it
through a local server rather than double-clicking the file:

```bash
python3 -m http.server 4173
```

then visit `http://localhost:4173/Split The Farm Optin.dc.html`. (`.claude/launch.json` runs the
same command if you're previewing inside Claude Code.)

## Deploying on Vercel

1. Import this repo into Vercel (New Project → pick `cassxed/succession`).
2. No build command / output directory needed — it's a static site, Vercel will serve it as-is.
3. `vercel.json` rewrites `/` to `Split The Farm Optin.dc.html`, so the funnel is live at the
   project's root domain.
4. Every push to the connected branch redeploys automatically.
