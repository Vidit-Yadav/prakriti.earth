const http = require('http');
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

// Route redirects for deleted legacy pages directly to single-page homepage anchors
const ROUTE_REDIRECTS = [
  { match: /^\/solutions(\/.*)?$/, target: '/#solutions' },
  { match: /^\/our-tech(\/.*)?$/, target: '/#technology' },
  { match: /^\/resources\/case-studies(\/.*)?$/, target: '/#impact' },
  { match: /^\/resources\/research-and-insights(\/.*)?$/, target: '/#research' },
  { match: /^\/resources\/news-and-media(\/.*)?$/, target: '/#research' },
  { match: /^\/resources(\/.*)?$/, target: '/#impact' },
  { match: /^\/our-company(\/.*)?$/, target: '/#contact' },
  { match: /^\/contact(\/.*)?$/, target: '/#contact' },
  { match: /^\/privacy-policy(\/.*)?$/, target: '/#contact' },
  { match: /^\/terms-of-use(\/.*)?$/, target: '/#contact' },
  { match: /^\/home(\/.*)?$/, target: '/' },
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
  // CORS Headers
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

  // Route redirects for deleted multi-page paths
  for (const r of ROUTE_REDIRECTS) {
    if (r.match.test(cleanPath)) {
      res.writeHead(302, { 'Location': r.target });
      res.end();
      return;
    }
  }

  const filePath = resolveFilePath(req.url);

  if (!filePath) {
    // If request has no extension, redirect to single-page homepage root
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

  // Optimized Cache-Control:
  // Static hashed assets (images, frames, fonts, scripts, videos) cached immutably
  // HTML documents revalidated
  if (ext === '.html') {
    res.setHeader('Cache-Control', 'no-cache, no-store, must-revalidate');
  } else {
    res.setHeader('Cache-Control', 'public, max-age=31536000, immutable');
  }

  // Range requests for audio/video streaming & canvas scrubber preloading
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
    console.log(`\n==============================================`);
    console.log(`🚀 Prakriti.earth (Single-Page Production) is LIVE!`);
    console.log(`📡 Local URL: http://localhost:${port}`);
    console.log(`==============================================\n`);
  });
}

const initialPort = parseInt(process.env.PORT, 10) || 3000;
startServer(initialPort);
