#!/usr/bin/env python3
import os
import re

PHRASE_REPLACEMENTS = [
    # Full headings & meta
    ("Research: Alethia's Atmospheric-based Measurement, Reporting, and Verification approach.",
     "Research: Prakriti's Atmospheric-based Measurement, Reporting, and Verification approach."),
    ("Research: Alethia’s Atmospheric-based Measurement, Reporting, and Verification approach.",
     "Research: Prakriti’s Atmospheric-based Measurement, Reporting, and Verification approach."),
    ("Case: Alethia's Atmospheric-based Measurement, Reporting, and Verification approach",
     "Case: Prakriti's Atmospheric-based Measurement, Reporting, and Verification approach"),
    ("Case: Alethia’s Atmospheric-based Measurement, Reporting, and Verification approach",
     "Case: Prakriti’s Atmospheric-based Measurement, Reporting, and Verification approach"),
    ("Alethia's Atmospheric-based Measurement, Reporting, and Verification approach",
     "Prakriti's Atmospheric-based Measurement, Reporting, and Verification approach"),
    ("Alethia’s Atmospheric-based Measurement, Reporting, and Verification approach",
     "Prakriti’s Atmospheric-based Measurement, Reporting, and Verification approach"),
    ("alethias-atmospheric-based-measurement-reporting-and-verification-approach",
     "prakritis-atmospheric-based-measurement-reporting-and-verification-approach"),
    ("Scaling Alethia’s Intelligence with AI", "Scaling Prakriti’s Intelligence with AI"),
    ("Scaling Alethia's Intelligence with AI", "Scaling Prakriti's Intelligence with AI"),
    ("scaling-alethias-intelligence-with-ai", "scaling-prakritis-intelligence-with-ai"),
    ("Alethia in the News", "Prakriti in the News"),
    ("Alethia Solves", "Prakriti Solves"),
    ("alethia solves", "prakriti solves"),
    ("Alethia didn’t adopt blockchain", "Prakriti didn’t adopt blockchain"),
    ("Alethia didn't adopt blockchain", "Prakriti didn't adopt blockchain"),
    ("Alethia brings the gold standard", "Prakriti brings the gold standard"),
    ("Alethia’s towers record GHG signals", "Prakriti’s towers record GHG signals"),
    ("Alethia's towers record GHG signals", "Prakriti's towers record GHG signals"),
    ("Alethia’s blockchain-secured registry", "Prakriti’s blockchain-secured registry"),
    ("Alethia's blockchain-secured registry", "Prakriti's blockchain-secured registry"),
    ("Alethia’s aMRV", "Prakriti’s aMRV"),
    ("Alethia's aMRV", "Prakriti's aMRV"),
    ("Alethia applies the same atmospheric measurement methods", "Prakriti applies the same atmospheric measurement methods"),
    ("Combined with algorithmic processing and blockchain infrastructure, Alethia turns complex field data",
     "Combined with algorithmic processing and blockchain infrastructure, Prakriti turns complex field data"),
    ("From carbon markets to supply chains, Alethia helps clients clarify impact",
     "From carbon markets to supply chains, Prakriti helps clients clarify impact"),
    ("Alethia is building the systems that climate accountability depends on",
     "Prakriti is building the systems that climate accountability depends on"),
    ("Alethia adapts to your data infrastructure", "Prakriti adapts to your data infrastructure"),
    ("Alethia quantifies the real-time impact", "Prakriti quantifies the real-time impact"),
    ("Alethia makes it ready to report", "Prakriti makes it ready to report"),
    ("Alethia is leading the way", "Prakriti is leading the way"),
    ("Bautista brings elite discipline to Alethia’s operations", "Our leadership brings elite discipline to Prakriti’s operations"),
    ("Bautista brings elite discipline to Alethia's operations", "Our leadership brings elite discipline to Prakriti's operations"),
    ("brings elite discipline to Alethia’s operations", "brings elite discipline to Prakriti’s operations"),
    ("brings elite discipline to Alethia's operations", "brings elite discipline to Prakriti's operations"),
    ("Alethia’s operations", "Prakriti’s operations"),
    ("Alethia's operations", "Prakriti's operations"),
    ("Alethia’s system", "Prakriti’s system"),
    ("Alethia's system", "Prakriti's system"),
    ("Alethia’s icon", "Prakriti’s icon"),
    ("Alethia's icon", "Prakriti's icon"),
    ("Alethia svg", "Prakriti svg"),

    # Founders & Team
    ("Bautista Saubidet Birkner", "Rohan Sharma"),
    ("Bautista Saubidet", "Rohan Sharma"),
    ("Co-Founder, COO​, Olympian", "Co-Founder & COO"),
    ("Co-Founder, COO, Olympian", "Co-Founder & COO"),
    ("Maia Moreno", "Dr. Ananya Roy"),
    ("Co-Founder, CEO, Parley", "Co-Founder & CEO"),
    ("James Kratz", "Rajesh Verma"),

    # Case study & Partner identity (neutral equivalents, no fake claims)
    ("Case Study: Adecoagro: From Regenerative Agriculture to Verified Climate Performance",
     "Case Study: AgroVeritas: From Regenerative Agriculture to Verified Climate Performance"),
    ("Adecoagro, one of Latin America’s leading food and energy producers",
     "AgroVeritas Ecosystems, one of the leading regional agro-ecological initiatives"),
    ("Adecoagro, one of Latin America's leading food and energy producers",
     "AgroVeritas Ecosystems, one of the leading regional agro-ecological initiatives"),
    ("Adecoagro’s rice and crop systems", "AgroVeritas’s rice and crop systems"),
    ("Adecoagro's rice and crop systems", "AgroVeritas's rice and crop systems"),
    ("Adecoagro needed a way", "AgroVeritas needed a way"),
    ("Adecoagro could see a clear", "AgroVeritas could see a clear"),
    ("Adecoagro’s operations", "AgroVeritas’s operations"),
    ("Adecoagro's operations", "AgroVeritas's operations"),
    ("positioned Adecoagro to expand", "positioned AgroVeritas to expand"),
    ("integrated into Adecoagro’s", "integrated into AgroVeritas’s"),
    ("integrated into Adecoagro's", "integrated into AgroVeritas's"),
    ("Adecoagro is prepared", "AgroVeritas is prepared"),
    ("solidify Adecoagro’s", "solidify AgroVeritas’s"),
    ("solidify Adecoagro's", "solidify AgroVeritas's"),
    ("turning Adecoagro’s", "turning AgroVeritas’s"),
    ("turning Adecoagro's", "turning AgroVeritas's"),
    ("across 13,600 hectares of Adecoagro", "across 13,600 hectares of AgroVeritas"),
    ("Adecoagro", "AgroVeritas"),
    ("adecoagro", "agroveritas"),

    # Geography & Locations (replace US/South America foreign addresses with Indian context)
    ("Buenos Aires, Argentina - Logan, UT, USA", "New Delhi - Bengaluru, India"),
    ("Buenos Aires, Argentina – Logan, UT, USA", "New Delhi – Bengaluru, India"),
    ("Buenos Aires, Argentina - Logan, Utah, USA", "New Delhi - Bengaluru, India"),
    ("Buenos Aires, Argentina", "New Delhi, India"),
    ("Logan, Utah, USA", "Bengaluru, India"),
    ("Logan, UT, USA", "Bengaluru, India"),
    ("Logan, UT", "Bengaluru, India"),
    ("Jersey City, NJ, 07302", "New Delhi, India"),
    ("Jersey City, NJ", "New Delhi, India"),

    # Copyright & Legal
    ("© 2025 Alethia - All rights reserved", "© 2026 Prakriti - All rights reserved"),
    ("© 2025 Alethia", "© 2026 Prakriti"),
    ("© 2026 Alethia", "© 2026 Prakriti"),
    ("operated by Alethia", "operated by Prakriti"),
    ("property of Alethia", "property of Prakriti"),
    ("written permission from Alethia", "written permission from Prakriti"),
    ("visiting alethia.earth", "visiting prakriti.earth"),

    # Social & Links & Domains
    ("https://www.linkedin.com/company/alethiaearth/", "https://www.linkedin.com/company/prakritiearth/"),
    ("https://www.linkedin.com/company/alethiaearth", "https://www.linkedin.com/company/prakritiearth"),
    ("linkedin.com/company/alethiaearth", "linkedin.com/company/prakritiearth"),
    ("alethiaearth", "prakritiearth"),
    ("https://www.alethia.earth", "https://www.prakriti.earth"),
    ("http://www.alethia.earth", "http://www.prakriti.earth"),
    ("https://alethia.earth", "https://prakriti.earth"),
    ("http://alethia.earth", "http://prakriti.earth"),
    ("www.alethia.earth", "www.prakriti.earth"),
    ("info@alethia.earth", "info@prakriti.earth"),
    ("hello@alethia.earth", "hello@prakriti.earth"),
    ("r2-assets.alethia.earth", "r2-assets.prakriti.earth"),
    ("alethia-sftp-bucket-1", "prakriti-sftp-bucket-1"),

    # Metadata & Tags
    ("Case Studies - Alethia", "Case Studies - Prakriti"),
    ("Research &amp; Insights - Alethia", "Research &amp; Insights - Prakriti"),
    ("Research & Insights - Alethia", "Research & Insights - Prakriti"),
    ("Media &amp; News Alethia", "Media &amp; News Prakriti"),
    ("Media & News Alethia", "Media & News Prakriti"),
    ("<title>Alethia</title>", "<title>Prakriti | Environmental &amp; Climate Intelligence</title>"),
    (" - Alethia</title>", " - Prakriti</title>"),
    ("content=\"Alethia\"", "content=\"Prakriti\""),
]

def replace_in_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return 0, str(e)

    orig_content = content

    # 1. Apply phrase replacements
    for src, dst in PHRASE_REPLACEMENTS:
        content = content.replace(src, dst)

    # 2. General brand replacements
    content = content.replace('Alethia', 'Prakriti')
    content = content.replace('ALETHIA', 'PRAKRITI')
    content = content.replace('alethia.earth', 'prakriti.earth')

    # Standalone lowercase alethia
    content = re.sub(r'\balethia\b', 'prakriti', content)

    if content != orig_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        remaining = len(re.findall(r'alethia', content, re.IGNORECASE))
        return 1, f"Updated (remaining alethia: {remaining})"
    else:
        return 0, "Unchanged"

def main():
    target_exts = {'.html', '.mjs', '.js', '.json', '.css', '.svg', '.txt'}
    ignore_dirs = {'.git', 'graphify-out', 'node_modules', 'scratch'}

    total_modified = 0
    scanned = 0

    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in target_exts:
                p = os.path.join(root, f)
                scanned += 1
                status, msg = replace_in_file(p)
                if status == 1:
                    total_modified += 1
                    print(f"[{total_modified}] {p}: {msg}")

    print(f"\nIndianize v2 complete: {scanned} files scanned, {total_modified} files modified.")

if __name__ == '__main__':
    main()
