# PILOT Trust website

Static rebuild of [impilot.org](https://impilot.org/) — Preparing India’s Leaders of Tomorrow Trust.

HTML, CSS, and JavaScript only. No WordPress. Designed as an editorial site (midnight teal, gold, cream) and ready to publish on Netlify.

## Local preview

```bash
python3 -m http.server 4173
```

Then open `http://127.0.0.1:4173`.

## Deploy on Netlify later

1. In Netlify, add a new site from this GitHub repo.
2. Publish directory: site root (leave build command empty).
3. Enable **Forms** so the contact and scholarship forms collect submissions.
4. Point the `impilot.org` domain at the new site when you are ready to switch.

Pretty URLs work automatically (`/about` serves `about.html`). The scholarship application and contact form use Netlify Forms and redirect to `/thank-you`.
