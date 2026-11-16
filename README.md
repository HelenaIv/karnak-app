# karnak-app

Installable, offline Karnak field guide for iPhone, Android and desktop. Built from the content repository (`../karnak-field-guide`), which this repo never edits. WordPress work is separate (`../karnak-wp`).

## What it is

An installable web app (PWA): the existing guide (`web/` + content bundle) plus a web app manifest, icons and a service worker. On first open with internet it saves the **whole guide** (all text, images, videos, both languages, about 60 MB) on the device. After that it opens and works with no connection. The header shows `↓ 45%` while saving and `✓ Offline` when done.

Bookmarks: the guide's existing **Saved** notebook (save button on entries, `#saved` page). Stored on the device, works offline, survives content updates.

Needs internet only for: first install, updates, and outside links (source websites, licence pages).

## Install for friends (no App Store, no Google Play)

Send the GitHub Pages link (see Hosting).

- **iPhone/iPad**: open the link in Safari → Share → **Add to Home Screen**. Open it once from the home screen with internet and wait for `✓ Offline`.
- **Android**: open the link in Chrome → menu ⋮ → **Install app** (or Add to Home screen). Open once with internet, wait for `✓ Offline`.
- **Desktop Chrome/Edge**: install icon in the address bar.

Updates: run the Pages workflow (see Hosting); each phone downloads the new version in the background next time it opens with internet, keeping the old copy until the new one is complete.

## Build

```
python scripts/build.py                 # builds the content repo, then the app into www/
python scripts/build.py --skip-content  # reuse the content repo's current dist/
```

`scripts/make_icons.py` redraws the icons from the pylon logo (needs Pillow).

Layout: `app/` = files added on top of the content build (manifest, `sw.js` template, `offline.js`, icons); `www/` = output (git-ignored), upload this folder.

## Hosting: GitHub Pages

`.github/workflows/pages.yml` builds the app on GitHub (it fetches the public `HelenaIv/karnak-field-guide`, builds it, then this app) and publishes `www/`. Expected address: `https://helenaiv.github.io/karnak-app/`.

One-time setup:

1. GitHub Desktop → File → Add local repository → `karnak-app` → **Publish repository**. Untick "Keep this code private" (Pages on a free GitHub plan needs a public repo; the content repo is public already).
2. On github.com: repo **Settings → Pages → Source: GitHub Actions**.
3. **Actions** tab → "Build and publish the app to GitHub Pages" → **Run workflow** (or push any commit).

New content: push the content repo as usual, then **Run workflow** here. Phones pick up the new version next time they open the app with internet.

## Tested (2026-11-16)

Headless Chrome, phone-size window, local server: install completes (177 cached files), then offline: home, a place article, Hall guide, Read the walls, Explore map, big picture, Saved, Ukrainian version, video playback ranges; no broken images, no errors; a bookmark saved online is still there offline.

Not yet tested: real iPhone and Android phones, the in-app browser pane (it refuses service workers), low storage.

## Later options

- Android APK file (Capacitor) for friends who prefer a real app file; needs the Android SDK or a GitHub Actions build.
- Native iPhone app only through Apple: Developer Program ($99/year) + TestFlight.
