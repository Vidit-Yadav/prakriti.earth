import os
import re
import shutil

ROOT_DIR = '/Users/vidit/Documents/Prakriti.earth'
INDEX_PATH = os.path.join(ROOT_DIR, 'www.alethia.earth', 'index.html')

print("Starting Phase 3 execution...")

# ----------------------------------------------------------------------
# 1. Update index.html
# ----------------------------------------------------------------------
with open(INDEX_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

# Assign Section Anchor IDs
# Hero Desktop & Mobile
html = html.replace('data-framer-name="Hero c ov"', 'data-framer-name="Hero c ov" id="hero"')
html = html.replace('data-framer-name="Hero s ov"', 'data-framer-name="Hero s ov" id="hero-mob"')

# Technology Desktop & Mobile
html = html.replace('data-framer-name="Our Tech DSK"', 'data-framer-name="Our Tech DSK" id="technology"')
html = html.replace('data-framer-name="Our Tech MOB"', 'data-framer-name="Our Tech MOB" id="technology-mob"')

# Impact / Case Studies
html = html.replace('data-framer-name="Case studies"', 'data-framer-name="Case studies" id="impact"')

# Research / Blog preview
html = html.replace('data-framer-name="Blog preview"', 'data-framer-name="Blog preview" id="research"')

# Contact / Footers
html = html.replace('data-framer-name="Big" style="background-color:var(--token-89eb458f-c22d-4db9-991d-dedbff9f9de0', 'data-framer-name="Big" id="contact" style="background-color:var(--token-89eb458f-c22d-4db9-991d-dedbff9f9de0')
html = html.replace('data-framer-name="MOB Big" style="background-color:var(--token-89eb458f-c22d-4db9-991d-dedbff9f9de0', 'data-framer-name="MOB Big" id="contact-mob" style="background-color:var(--token-89eb458f-c22d-4db9-991d-dedbff9f9de0')

# Update Anchor Links in index.html
link_replacements = [
    (r'href="\./solutions/nature-based"', 'href="#solutions"'),
    (r'href="\./solutions/supply-chain"', 'href="#solutions"'),
    (r'href="\./solutions"', 'href="#solutions"'),
    (r'href="\./our-tech/amrv"', 'href="#technology"'),
    (r'href="\./our-tech/blockchain"', 'href="#technology"'),
    (r'href="\./our-tech"', 'href="#technology"'),
    (r'href="\./resources/case-studies/[^"]*"', 'href="#impact"'),
    (r'href="\./resources/case-studies"', 'href="#impact"'),
    (r'href="\./resources/news-and-media/[^"]*"', 'href="#research"'),
    (r'href="\./resources/news-and-media"', 'href="#research"'),
    (r'href="\./resources/research-and-insights/[^"]*"', 'href="#research"'),
    (r'href="\./resources/research-and-insights"', 'href="#research"'),
    (r'href="\./contact"', 'href="#contact"'),
    (r'href="\./our-company"', 'href="#contact"'),
    (r'href="\./home"', 'href="#hero"'),
]

for pat, repl in link_replacements:
    html = re.sub(pat, repl, html)

# Content Adaptations:
# 1. Hero Subhead
old_hero_subhead = "Know your impact—precisely.  End-to-end environmental intelligence powered by science, blockchain, and transparent data you can trust."
new_hero_subhead = "Quantify atmospheric carbon fluxes with physical precision. Verifiable environmental intelligence across India’s agricultural, forest, and industrial landscapes."
html = html.replace(old_hero_subhead, new_hero_subhead)
html = html.replace("Know your impact—precisely. End-to-end environmental intelligence powered by science, blockchain, and transparent data you can trust.", new_hero_subhead)

# 2. Testimonial / Showcase (AgroVeritas Ecosystems)
old_testimonial_title = "How GreenFuture reduced carbon emissions by 25% in 12 months"
new_testimonial_title = "How AgroVeritas Ecosystems Verified 1.87 t CO₂/ha Annual Sequestration Across the Indo-Gangetic Basin"
html = html.replace(old_testimonial_title, new_testimonial_title)

old_quote = "“The thing we appreciated most about GreenFuture was that their carbon-tracking technology wasn’t just a tool – it was a full-fledged, scientifically-backed solution tailored for our industry. \u2028\u2028The transparency of their platform is unparalleled; we could always trace exactly how our carbon data was being calculated, and their team was always ready to guide us through any questions.”"
new_quote = "“Prakriti’s atmospheric flux monitoring provided empirical verification where legacy estimates always fell short. Direct eddy covariance coupled with cryptographic proof gave our agricultural partners indisputable climate credibility with zero greenwashing.”"
html = html.replace(old_quote, new_quote)

html = html.replace("CEO, Greentech Corp", "Lead Agronomist & Research Director, AgroVeritas")

# 3. Meta Tags and Title
html = re.sub(r'<title>.*?</title>', '<title>Prakriti — Atmospheric Environmental Intelligence &amp; Verifiable Climate Ledger</title>', html, count=1)
html = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{new_hero_subhead}">', html, count=1)
html = re.sub(r'<meta property="og:title" content=".*?">', '<meta property="og:title" content="Prakriti — Atmospheric Environmental Intelligence &amp; Verifiable Climate Ledger">', html, count=1)
html = re.sub(r'<meta property="og:description" content=".*?">', f'<meta property="og:description" content="{new_hero_subhead}">', html, count=1)
html = re.sub(r'<meta name="twitter:title" content=".*?">', '<meta name="twitter:title" content="Prakriti — Atmospheric Environmental Intelligence &amp; Verifiable Climate Ledger">', html, count=1)
html = re.sub(r'<meta name="twitter:description" content=".*?">', f'<meta name="twitter:description" content="{new_hero_subhead}">', html, count=1)

# Add Canonical link if not present
if 'rel="canonical"' not in html:
    html = html.replace('</head>', '    <link rel="canonical" href="https://prakriti.earth">\n</head>')

# Inject smooth scroll styles and global click handler for single-page navigation
single_page_script = """
    <!-- Single-Page Smooth Scroll & Interceptor -->
    <style>
      html {
        scroll-behavior: smooth !important;
      }
      #hero, #hero-mob, #solutions, #technology, #technology-mob, #impact, #research, #contact, #contact-mob {
        scroll-margin-top: 88px;
      }
    </style>
    <script>
      (function() {
        function scrollToTarget(id) {
          var el = document.getElementById(id);
          if (!el && id === 'technology') el = document.getElementById('technology-mob');
          if (!el && id === 'hero') el = document.getElementById('hero-mob');
          if (!el && id === 'contact') el = document.getElementById('contact-mob');
          if (el) {
            el.scrollIntoView({ behavior: 'smooth', block: 'start' });
            if (window.history && window.history.pushState) {
              window.history.pushState(null, null, '#' + id);
            } else {
              window.location.hash = '#' + id;
            }
          }
        }

        document.addEventListener('click', function(e) {
          var link = e.target.closest('a');
          if (link) {
            var href = link.getAttribute('href');
            if (href) {
              if (href.startsWith('#')) {
                e.preventDefault();
                e.stopPropagation();
                scrollToTarget(href.slice(1));
                return;
              }
              if (href.indexOf('solutions') !== -1) {
                e.preventDefault();
                e.stopPropagation();
                scrollToTarget('solutions');
                return;
              }
              if (href.indexOf('our-tech') !== -1 || href.indexOf('technology') !== -1 || href.indexOf('amrv') !== -1 || href.indexOf('blockchain') !== -1) {
                e.preventDefault();
                e.stopPropagation();
                scrollToTarget('technology');
                return;
              }
              if (href.indexOf('case-studies') !== -1 || href.indexOf('impact') !== -1) {
                e.preventDefault();
                e.stopPropagation();
                scrollToTarget('impact');
                return;
              }
              if (href.indexOf('research') !== -1 || href.indexOf('news') !== -1 || href.indexOf('media') !== -1) {
                e.preventDefault();
                e.stopPropagation();
                scrollToTarget('research');
                return;
              }
              if (href.indexOf('contact') !== -1 || href.indexOf('our-company') !== -1) {
                e.preventDefault();
                e.stopPropagation();
                scrollToTarget('contact');
                return;
              }
            }
          }

          var navBtn = e.target.closest('[data-framer-name="solu"], [name="solu"], [data-framer-name="tech"], [name="tech"], [data-framer-name="resources"], [name="resources"], [data-framer-name="company"], [name="company"]');
          if (navBtn) {
            var name = (navBtn.getAttribute('data-framer-name') || navBtn.getAttribute('name') || '').toLowerCase();
            if (name.indexOf('solu') !== -1) {
              e.preventDefault();
              e.stopPropagation();
              scrollToTarget('solutions');
              return;
            }
            if (name.indexOf('tech') !== -1) {
              e.preventDefault();
              e.stopPropagation();
              scrollToTarget('technology');
              return;
            }
            if (name.indexOf('resources') !== -1) {
              e.preventDefault();
              e.stopPropagation();
              scrollToTarget('impact');
              return;
            }
            if (name.indexOf('company') !== -1) {
              e.preventDefault();
              e.stopPropagation();
              scrollToTarget('contact');
              return;
            }
          }
        }, true);

        window.addEventListener('DOMContentLoaded', function() {
          if (window.location.hash) {
            var id = window.location.hash.slice(1);
            setTimeout(function() {
              scrollToTarget(id);
            }, 600);
          }
        });
      })();
    </script>
    <!-- End Single-Page Script -->
"""

if '<!-- Single-Page Smooth Scroll & Interceptor -->' not in html:
    html = html.replace('</body>', single_page_script + '\n</body>')

with open(INDEX_PATH, 'w', encoding='utf-8') as f:
    f.write(html)

print("index.html successfully updated.")

# ----------------------------------------------------------------------
# 2. Update server.js
# ----------------------------------------------------------------------
server_js_code = """const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.htm': 'text/html; charset=utf-8',
  '.mjs': 'text/javascript; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.webp': 'image/webp',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
  '.woff': 'font/woff',
  '.woff2': 'font/woff2',
  '.ttf': 'font/ttf',
  '.otf': 'font/otf',
  '.webm': 'video/webm',
  '.mp4': 'video/mp4',
  '.ogg': 'video/ogg',
  '.mp3': 'audio/mpeg',
  '.wav': 'audio/wav',
  '.framercms': 'application/octet-stream',
};

const ROOT_DIR = __dirname;
const MAIN_INDEX = path.join(ROOT_DIR, 'www.prakriti.earth', 'index.html');

// Route redirects to single-page homepage anchors
const ROUTE_REDIRECTS = [
  { match: /^\\/solutions(\\/.*)?$/, target: '/#solutions' },
  { match: /^\\/our-tech(\\/.*)?$/, target: '/#technology' },
  { match: /^\\/resources\\/case-studies(\\/.*)?$/, target: '/#impact' },
  { match: /^\\/resources\\/research-and-insights(\\/.*)?$/, target: '/#research' },
  { match: /^\\/resources\\/news-and-media(\\/.*)?$/, target: '/#research' },
  { match: /^\\/resources(\\/.*)?$/, target: '/#impact' },
  { match: /^\\/our-company(\\/.*)?$/, target: '/#contact' },
  { match: /^\\/contact(\\/.*)?$/, target: '/#contact' },
  { match: /^\\/privacy-policy(\\/.*)?$/, target: '/#contact' },
  { match: /^\\/terms-of-use(\\/.*)?$/, target: '/#contact' },
  { match: /^\\/home(\\/.*)?$/, target: '/' },
];

function resolveFilePath(reqPath) {
  const decodedPath = decodeURIComponent(reqPath.split('?')[0]);

  if (decodedPath === '/' || decodedPath === '/index.html') {
    if (fs.existsSync(MAIN_INDEX)) return MAIN_INDEX;
    const rootIndex = path.join(ROOT_DIR, 'index.html');
    if (fs.existsSync(rootIndex)) return rootIndex;
  }

  const candidates = [
    path.join(ROOT_DIR, decodedPath),
    path.join(ROOT_DIR, 'www.prakriti.earth', decodedPath),
    path.join(ROOT_DIR, 'framerusercontent.com', decodedPath),
    path.join(ROOT_DIR, 'r2-assets.prakriti.earth', decodedPath),
  ];

  for (const candidate of candidates) {
    if (fs.existsSync(candidate)) {
      const stat = fs.statSync(candidate);
      if (stat.isFile()) {
        return candidate;
      }
    }
  }

  return null;
}

function handleRequest(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, HEAD, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', '*');

  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }

  if (req.method !== 'GET' && req.method !== 'HEAD') {
    res.writeHead(405, { 'Content-Type': 'text/plain' });
    res.end('Method Not Allowed');
    return;
  }

  const cleanPath = req.url.split('?')[0];

  // Check route redirects for deleted pages
  for (const r of ROUTE_REDIRECTS) {
    if (r.match.test(cleanPath)) {
      res.writeHead(302, { 'Location': r.target });
      res.end();
      return;
    }
  }

  const filePath = resolveFilePath(req.url);

  if (!filePath) {
    // If request has no file extension (e.g. unknown subpage), redirect to root /
    if (!path.extname(cleanPath)) {
      res.writeHead(302, { 'Location': '/' });
      res.end();
      return;
    }

    res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
    res.end('404 Not Found: ' + req.url);
    return;
  }

  const ext = path.extname(filePath).toLowerCase();
  const contentType = MIME_TYPES[ext] || 'application/octet-stream';
  const stat = fs.statSync(filePath);
  const totalSize = stat.size;

  // Range requests for audio/video
  const range = req.headers.range;
  if (range) {
    const parts = range.replace(/bytes=/, '').split('-');
    const start = parseInt(parts[0], 10);
    const end = parts[1] ? parseInt(parts[1], 10) : totalSize - 1;

    if (start >= totalSize || end >= totalSize || start > end) {
      res.writeHead(416, { 'Content-Range': `bytes */${totalSize}` });
      res.end();
      return;
    }

    const chunksize = end - start + 1;
    res.writeHead(206, {
      'Content-Range': `bytes ${start}-${end}/${totalSize}`,
      'Accept-Ranges': 'bytes',
      'Content-Length': chunksize,
      'Content-Type': contentType,
    });

    if (req.method === 'HEAD') {
      res.end();
      return;
    }

    fs.createReadStream(filePath, { start, end }).pipe(res);
  } else {
    res.writeHead(200, {
      'Content-Length': totalSize,
      'Content-Type': contentType,
      'Accept-Ranges': 'bytes',
    });

    if (req.method === 'HEAD') {
      res.end();
      return;
    }

    fs.createReadStream(filePath).pipe(res);
  }
}

function startServer(port, maxAttempts = 10) {
  const server = http.createServer(handleRequest);

  server.on('error', (err) => {
    if (err.code === 'EADDRINUSE' && maxAttempts > 0) {
      console.log(`Port ${port} is in use, trying port ${port + 1}...`);
      startServer(port + 1, maxAttempts - 1);
    } else {
      console.error('Failed to start server:', err);
      process.exit(1);
    }
  });

  server.listen(port, () => {
    console.log(`\\n==============================================`);
    console.log(`🚀 Prakriti.earth (Single-Page) is LIVE!`);
    console.log(`📡 Local URL: http://localhost:${port}`);
    console.log(`==============================================\\n`);
  });
}

const initialPort = parseInt(process.env.PORT, 10) || 3000;
startServer(initialPort);
"""

with open(os.path.join(ROOT_DIR, 'server.js'), 'w', encoding='utf-8') as f:
    f.write(server_js_code)

print("server.js successfully updated.")

# ----------------------------------------------------------------------
# 3. Delete obsolete route directories in www.alethia.earth
# ----------------------------------------------------------------------
obsolete_items = [
    'our-company',
    'our-company.html',
    'our-tech',
    'our-tech.html',
    'solutions',
    'solutions.html',
    'resources',
    'resources.html',
    'contact',
    'contact.html',
    'privacy-policy',
    'privacy-policy.html',
    'terms-of-use',
    'terms-of-use.html',
    'home',
    'home.html',
    'rendered_source.html'
]

alethia_dir = os.path.join(ROOT_DIR, 'www.alethia.earth')
deleted_count = 0
for item in obsolete_items:
    target = os.path.join(alethia_dir, item)
    if os.path.isdir(target):
        shutil.rmtree(target)
        print(f"Deleted directory: {item}")
        deleted_count += 1
    elif os.path.isfile(target):
        os.remove(target)
        print(f"Deleted file: {item}")
        deleted_count += 1

print(f"Cleanup complete. Deleted {deleted_count} items from www.alethia.earth.")
