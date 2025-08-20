import React, { useState } from 'react'
import Chat from './components/Chat'
import Sidebar from './components/Sidebar'

export default function App(){
  const [messages, setMessages] = useState([])

  return (
    <div className="app">
      <Sidebar />
      <Chat messages={messages} setMessages={setMessages} />
    </div>
  )
}
