# Split The Farm — Opt-In Funnel

Lead-gen landing page for the "Split The Farm Between Your Kids" free training, exported from
[Claude Design](https://claude.ai/design). It's a static site — no build step, no framework install.
The page's interactivity (the modal, the state machine) runs via `support.js`, a small runtime that
loads React/ReactDOM from a CDN at page-load and hydrates the `<x-dc>` component in
`Split The Farm Optin.dc.html`.

## Structure

- `Split The Farm Optin.dc.html` — the opt-in landing page (served at `/` via `vercel.json`).
- `Split The Farm Watch.dc.html` — the VSL page the opt-in's "You're in" success view links to
  once the HubSpot form submits. Static (no interactive state) — just the video-slot embed and a
  CTA. The `TALK WITH AN AG EXPERT [FREE]` button is still a `href="#"` placeholder.
- `_ds/.../` — the shared design-system bundle (fonts, base styles) both pages import.
- `image-slot.js` / `support.js` — the Claude Design runtime both pages depend on.
- `tracking.js` — site-wide tracking (Meta Pixel, Cometly), loaded via a single
  `<script src="./tracking.js">` in the `<head>` of every page. Keep pixel IDs / tracking snippets
  here rather than pasting them into each page — add a new page by referencing this same file.
- `assets/` — brand assets (logo, etc).

## The HubSpot form

The modal ("Enter Your Info To Watch The Training") loads a real HubSpot form — portal `43573758`,
form `3bd92e18-1b6f-4522-a7f3-83cfba8e4d1b`. It's injected imperatively from `openModal()` /
`_mountHubspotForm()` in the `<script type="text/x-dc">` block at the bottom of
`Split The Farm Optin.dc.html`, targeting `#hubspot-form-target`, rather than pasted into the
template as raw `<script>` tags — those don't reliably execute once rendered through this page's
React-based runtime. It renders inside HubSpot's own sandboxed iframe, so styling it to match the
page's dark theme happens in HubSpot itself (Marketing → Forms → this form → Style & preview), not
in this file's CSS.

The page listens for HubSpot's `onFormSubmitted` callback (with a `postMessage` listener kept as a
fallback) and flips to the "You're in" success view only once the form actually submits.

To swap in a different form, change the `HUBSPOT_FORM` constant (`portalId` / `formId` / `region`)
near the top of that script block.

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
