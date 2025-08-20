import React, { useState } from 'react'
import axios from 'axios'

export default function Chat({ messages, setMessages }){
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)

  async function send(){
    if(!input) return
    const userMsg = { role: 'user', content: input }
    setMessages(prev => [...prev, userMsg])
    setInput('')
    setLoading(true)

    try{
      const res = await axios.post('/api/agent/chat', { query: input })
      const assistant = { role: 'assistant', content: res.data.answer }
      setMessages(prev => [...prev, assistant])
    }catch(e){
      const err = { role: 'assistant', content: 'Error contacting backend' }
      setMessages(prev => [...prev, err])
    }finally{
      setLoading(false)
    }
  }

  return (
    <div className="chat">
      <div className="messages">
        {messages.map((m,i) => (
          <div key={i} className={`msg ${m.role}`}>
            <div className="role">{m.role}</div>
            <div className="content">{m.content}</div>
          </div>
        ))}
      </div>
      <div className="input">
        <input value={input} onChange={e=>setInput(e.target.value)} placeholder="Ask about Ola, Ather, Ampere..." />
        <button onClick={send} disabled={loading}>{loading? '...' : 'Send'}</button>
      </div>
    </div>
  )
}
