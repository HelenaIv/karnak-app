#!/usr/bin/env python3
"""Build the installable offline app from the content repository.

    python scripts/build.py                 # builds ../karnak-field-guide, then the app into www/
    python scripts/build.py --skip-content  # reuse the content repo's existing dist/
    python scripts/build.py --content PATH  # content repo somewhere else

The content repository is never modified, except for its own build output (dist/, git-ignored there).
Output: www/ = the content site + web app manifest, icons, service worker (whole guide cached for offline use)
and offline.js (offline status in the header).
"""
import argparse, hashlib, json, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / 'app'          # files this repo adds on top of the content build
WWW = ROOT / 'www'

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--content', default=str(ROOT.parent / 'karnak-field-guide'))
    ap.add_argument('--skip-content', action='store_true')
    a = ap.parse_args()
    content = Path(a.content).resolve()
    if not (content / 'scripts' / 'build_review_site.py').exists():
        sys.exit(f'Content repository not found at {content}')
    if not a.skip_content:
        subprocess.run([sys.executable, 'scripts/build_review_site.py'], cwd=content, check=True)
    dist = content / 'dist'
    if not (dist / 'index.html').exists():
        sys.exit(f'No build in {dist}; run without --skip-content')

    WWW.mkdir(exist_ok=True)
    for old in WWW.iterdir():  # empty www/ but keep the folder (a local test server may be running in it)
        shutil.rmtree(old) if old.is_dir() else old.unlink()
    shutil.copytree(dist, WWW, dirs_exist_ok=True)
    for f in APP.iterdir():
        if f.is_dir():
            shutil.copytree(f, WWW / f.name, dirs_exist_ok=True)
        elif f.name != 'sw.js':
            shutil.copy2(f, WWW / f.name)

    # Head additions: manifest, iOS home-screen tags, offline script.
    html = (WWW / 'index.html').read_text(encoding='utf-8')
    head = ('<link rel="manifest" href="manifest.webmanifest">'
            '<link rel="icon" href="icons/icon-192.png" type="image/png">'
            '<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">'
            '<meta name="apple-mobile-web-app-capable" content="yes">'
            '<meta name="mobile-web-app-capable" content="yes">'
            '<meta name="apple-mobile-web-app-status-bar-style" content="default">'
            '<meta name="apple-mobile-web-app-title" content="Karnak">'
            '<script src="offline.js" defer></script>')
    if '</head>' not in html:
        sys.exit('index.html has no </head>; the content build changed shape')
    html = html.replace('</head>', head + '</head>', 1)
    (WWW / 'index.html').write_text(html, encoding='utf-8')

    # Service worker: every file in www/ is precached. The version is a hash of all files,
    # so any content change installs a new cache and removes the old one.
    files = sorted(p for p in WWW.rglob('*') if p.is_file())
    h = hashlib.sha256()
    entries = []
    for p in files:
        rel = p.relative_to(WWW).as_posix()
        h.update(rel.encode()); h.update(p.read_bytes())
        entries.append({'url': rel, 'bytes': p.stat().st_size})
    version = h.hexdigest()[:12]
    sw = (APP / 'sw.js').read_text(encoding='utf-8')
    sw = sw.replace('__VERSION__', version).replace('__FILES__', json.dumps(entries, separators=(',', ':')))
    (WWW / 'sw.js').write_text(sw, encoding='utf-8')

    total = sum(e['bytes'] for e in entries)
    (WWW / 'version.json').write_text(json.dumps({'version': version, 'files': len(entries), 'bytes': total}), encoding='utf-8')
    print(f'Built www/: {len(entries)} files, {total/1e6:.1f} MB, version {version}')

if __name__ == '__main__':
    main()
