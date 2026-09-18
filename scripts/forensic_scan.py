import os
import re
import sys

ROOT_DIR = '/Users/vidit/Documents/Prakriti.earth'
INDEX_HTML = os.path.join(ROOT_DIR, 'index.html')

FORBIDDEN_BRAND_TERMS = [
    r'\balethia\b',
    r'buenos aires',
    r'bautista',
    r'saubidet',
    r'maia moreno',
    r'adecoagro',
    r'logan, ut',
    r'greenfuture',
    r'greentech corp'
]

DELETED_ROUTE_PATTERNS = [
    r'our-company\.html',
    r'solutions\/nature-based\.html',
    r'solutions\/supply-chain\.html',
    r'our-tech\/amrv\.html',
    r'our-tech\/blockchain\.html',
    r'resources\/case-studies\.html',
    r'contact\.html',
    r'privacy-policy\.html',
    r'terms-of-use\.html',
    r'home\.html',
]

def run_scan():
    print("====================================================")
    print("🕵️  STARTING FINAL FORENSIC SCAN")
    print("====================================================\n")

    total_issues = 0

    # 1. Check for Forbidden Brand / Legacy Terms
    print("1. Scanning for Forbidden Brand / Legacy Terms...")
    brand_leaks = []
    scanned_exts = {'.html', '.js', '.mjs', '.json', '.css'}

    for root, dirs, files in os.walk(ROOT_DIR):
        if any(d in root for d in ['node_modules', '.git', 'graphify-out', 'scripts', '.system_generated']):
            continue
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in scanned_exts:
                fpath = os.path.join(root, file)
                try:
                    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    for term in FORBIDDEN_BRAND_TERMS:
                        matches = list(re.finditer(term, content, re.IGNORECASE))
                        if matches:
                            brand_leaks.append((fpath, term, len(matches)))
                except Exception as e:
                    pass

    if brand_leaks:
        print(f"  ❌ Found {len(brand_leaks)} files with forbidden brand leaks:")
        for path, term, count in brand_leaks:
            print(f"    - {path}: term '{term}' ({count} matches)")
        total_issues += len(brand_leaks)
    else:
        print("  ✅ 0 Brand / Legacy Leaks found across all files.")

    # 2. Check for Deleted HTML Route References
    print("\n2. Scanning for Deleted Multi-Page Route References...")
    deleted_route_refs = []
    for root, dirs, files in os.walk(ROOT_DIR):
        if any(d in root for d in ['node_modules', '.git', 'graphify-out', 'scripts', '.system_generated']):
            continue
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in scanned_exts:
                fpath = os.path.join(root, file)
                try:
                    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    for pattern in DELETED_ROUTE_PATTERNS:
                        matches = list(re.finditer(pattern, content, re.IGNORECASE))
                        if matches:
                            deleted_route_refs.append((fpath, pattern, len(matches)))
                except Exception as e:
                    pass

    if deleted_route_refs:
        print(f"  ❌ Found {len(deleted_route_refs)} deleted route references:")
        for path, pat, count in deleted_route_refs:
            print(f"    - {path}: pattern '{pat}' ({count} matches)")
        total_issues += len(deleted_route_refs)
    else:
        print("  ✅ 0 Deleted route references found.")

    # 3. Check for Localhost URLs in Production index.html
    print("\n3. Scanning for Localhost URLs in index.html...")
    with open(INDEX_HTML, 'r', encoding='utf-8') as f:
        html = f.read()

    localhost_matches = list(re.finditer(r'https?:\/\/(localhost|127\.0\.0\.1)', html, re.IGNORECASE))
    if localhost_matches:
        print(f"  ❌ Found {len(localhost_matches)} localhost URLs in index.html:")
        for m in localhost_matches:
            print(f"    - Offset {m.start()}: {m.group(0)}")
        total_issues += len(localhost_matches)
    else:
        print("  ✅ 0 Localhost URLs in index.html.")

    # 4. Verify SEO & Production Metadata in index.html
    print("\n4. Verifying SEO & Social Metadata...")
    has_title = bool(re.search(r'<title>.*Prakriti.*<\/title>', html, re.IGNORECASE))
    has_desc = bool(re.search(r'<meta\s+name=["\']description["\']\s+content=["\'][^"\']+["\']', html))
    has_og_title = bool(re.search(r'<meta\s+property=["\']og:title["\']', html))
    has_canonical = bool(re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\']https:\/\/prakriti\.earth["\']', html))
    has_favicon = bool(re.search(r'<link\s+[^>]*rel=["\']icon["\']', html))

    print(f"  - Title valid: {has_title}")
    print(f"  - Meta description valid: {has_desc}")
    print(f"  - OpenGraph title valid: {has_og_title}")
    print(f"  - Canonical URL (https://prakriti.earth) valid: {has_canonical}")
    print(f"  - Favicon valid: {has_favicon}")

    if not (has_title and has_desc and has_og_title and has_canonical and has_favicon):
        print("  ❌ Metadata verification failed!")
        total_issues += 1
    else:
        print("  ✅ All SEO, Social & Canonical metadata verified.")

    # 5. Check Single-Page Anchors in index.html
    print("\n5. Verifying Single-Page Target Anchors...")
    required_anchors = ['hero', 'solutions', 'technology', 'impact', 'research', 'contact']
    missing_anchors = []
    for a in required_anchors:
        if not re.search(r'id=["\']' + a + r'["\']', html):
            missing_anchors.append(a)

    if missing_anchors:
        print(f"  ❌ Missing anchor IDs: {missing_anchors}")
        total_issues += len(missing_anchors)
    else:
        print("  ✅ All 6 section anchor IDs verified (#hero, #solutions, #technology, #impact, #research, #contact).")

    print("\n====================================================")
    if total_issues == 0:
        print("🏆 FORENSIC SCAN PASSED: 0 ISSUES FOUND!")
    else:
        print(f"⚠️  FORENSIC SCAN FAILED WITH {total_issues} ISSUES!")
    print("====================================================\n")

    return total_issues

if __name__ == '__main__':
    errs = run_scan()
    sys.exit(1 if errs > 0 else 0)
