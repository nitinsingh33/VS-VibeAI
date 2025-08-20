const express = require('express')
const { createProxyMiddleware } = require('http-proxy-middleware')
const path = require('path')

const app = express()
const PORT = process.env.PORT || 3001

// Proxy API calls to Python backend
app.use('/api', createProxyMiddleware({ target: 'http://localhost:8000', changeOrigin: true }))

// Serve frontend static in production build
app.use(express.static(path.join(__dirname, '..', 'dist')))

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, '..', 'dist', 'index.html'))
})

app.listen(PORT, ()=>{
  console.log('Proxy server running on', PORT)
})
