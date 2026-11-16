# karnak-app

Installable, offline Karnak field guide for iPhone, Android and desktop. Built from the content repository (`../karnak-field-guide`), which this repo never edits. WordPress work is separate (`../karnak-wp`).

## What it is

An installable web app (PWA): the existing guide (`web/` + content bundle) plus a web app manifest, icons and a service worker. On first open with internet it saves the **whole guide** (all text, images, videos, both languages, about 60 MB) on the device. After that it opens and works with no connection. The header shows `↓ 45%` while saving and `✓ Offline` when done.

Bookmarks: the guide's existing **Saved** notebook (save button on entries, `#saved` page). Stored on the device, works offline, survives content updates.

Needs internet only for: first install, updates, and outside links (source websites, licence pages).

## Install for friends (no App Store, no Google Play)

The app must be on an HTTPS address (see Hosting). Send the link.

- **iPhone/iPad**: open the link in Safari → Share → **Add to Home Screen**. Open it once from the home screen with internet and wait for `✓ Offline`.
- **Android**: open the link in Chrome → menu ⋮ → **Install app** (or Add to Home screen). Open once with internet, wait for `✓ Offline`.
- **Desktop Chrome/Edge**: install icon in the address bar.

Updates: rebuild and re-upload; each phone downloads the new version in the background next time it opens with internet, keeping the old copy until the new one is complete.

## Build

```
python scripts/build.py                 # builds the content repo, then the app into www/
python scripts/build.py --skip-content  # reuse the content repo's current dist/
```

`scripts/make_icons.py` redraws the icons from the pylon logo (needs Pillow).

Layout: `app/` = files added on top of the content build (manifest, `sw.js` template, `offline.js`, icons); `www/` = output (git-ignored), upload this folder.

## Hosting

Not decided yet. Any static HTTPS host works: GitHub Pages from this repo, Netlify (drag the `www/` folder), Cloudflare Pages. The address is public but unlisted.

## Tested (2026-11-16)

Headless Chrome, phone-size window, local server: install completes (177 cached files), then offline: home, a place article, Hall guide, Read the walls, Explore map, big picture, Saved, Ukrainian version, video playback ranges; no broken images, no errors; a bookmark saved online is still there offline.

Not yet tested: real iPhone and Android phones, the in-app browser pane (it refuses service workers), low storage.

## Later options

- Android APK file (Capacitor) for friends who prefer a real app file; needs the Android SDK or a GitHub Actions build.
- Native iPhone app only through Apple: Developer Program ($99/year) + TestFlight.
