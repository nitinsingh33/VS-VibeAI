Frontend (React + Vite) and Node proxy for SolysAI

Quick start (dev):

1. cd web
2. npm install
3. npm run dev (starts Vite on :5173)
4. In a separate terminal run `node server/index.js` to start proxy on :3001 (proxies /api to http://localhost:8000)

To create production build:

1. cd web
2. npm run build
3. node server/index.js

The frontend expects the Python backend to be available at http://localhost:8000 and exposes a /api/agent/chat endpoint for chat queries.
