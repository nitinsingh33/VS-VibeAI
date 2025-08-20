import React from 'react'

export default function Sidebar(){
  return (
    <div className="sidebar">
      <div className="brand">SolysAI</div>
      <div className="controls">
        <button id="run-scrape">Run Scrape</button>
        <button id="open-data">Open Data Folder</button>
      </div>
      <div className="info">
        <h4>OEMs</h4>
        <ul>
          <li>Ola Electric</li>
          <li>Ather</li>
          <li>Bajaj Chetak</li>
          <li>TVS iQube</li>
          <li>Hero Vida</li>
          <li>Ampere</li>
          <li>River Mobility</li>
          <li>Ultraviolette</li>
          <li>Revolt</li>
          <li>BGauss</li>
        </ul>
      </div>
    </div>
  )
}
