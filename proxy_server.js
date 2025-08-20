const http = require('http');
const httpProxy = require('http-proxy-middleware');
const express = require('express');
const path = require('path');

const app = express();

// Serve static files (like public_access.html)
app.use(express.static(path.join(__dirname)));

// Proxy API requests to FastAPI backend (port 8000)
const apiProxy = httpProxy.createProxyMiddleware({
    target: 'http://localhost:8000',
    changeOrigin: true,
    logLevel: 'info'
});

// Proxy Streamlit requests to Streamlit server (port 8502)
const streamlitProxy = httpProxy.createProxyMiddleware({
    target: 'http://localhost:8502',
    changeOrigin: true,
    logLevel: 'info',
    ws: true // Enable WebSocket proxying for Streamlit
});

// Route API requests to FastAPI
app.use('/api', apiProxy);

// Route Streamlit requests to Streamlit server
app.use('/streamlit', streamlitProxy);

// Serve main Streamlit app at root for dashboard access
app.use('/', (req, res, next) => {
    // If it's the main page or any Streamlit-related request, proxy to Streamlit
    if (req.path === '/' || req.path.startsWith('/_stcore') || req.path.startsWith('/component') || req.path.startsWith('/static')) {
        return streamlitProxy(req, res, next);
    }
    next();
});

const PORT = 9000;
app.listen(PORT, '0.0.0.0', () => {
    console.log(`🚀 Proxy server running on port ${PORT}`);
    console.log(`📊 Streamlit Dashboard: http://localhost:${PORT}/`);
    console.log(`🔗 API Access: http://localhost:${PORT}/api/`);
    console.log(`🌐 Public Access: http://localhost:${PORT}/public_access.html`);
});
