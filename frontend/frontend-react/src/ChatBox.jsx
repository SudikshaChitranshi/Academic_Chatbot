// ChatBox.jsx
import React, { useState } from 'react';
import LoginPopup from "./LoginPopup"; 
import { useSession } from './useSession';
import GPAChart from './GPAChart';


function linkify(text) {
  // Escape HTML to prevent XSS before converting markdown
  let html = text.replace(/</g, "&lt;").replace(/>/g, "&gt;");

  // Convert **bold**
  html = html.replace(/\*\*(.*?)\*\*/g, '<b>$1</b>');

  // Convert *italic* or _italic_
  html = html.replace(/(\*|_)(.*?)\1/g, '<i>$2</i>');

  // Convert [text](url)
  html = html.replace(/\[(.*?)\]\((https?:\/\/[^\s]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>');

  // Convert plain URLs to clickable links
  html = html.replace(/(https?:\/\/[^\s]+)/g, url => {
    return `<a href="${url}" target="_blank" rel="noopener noreferrer" style="color: #f0f8ff;">${url}</a>`;
  });

  // Convert bullet list lines starting with - or *
  const lines = html.split('\n');
  let inList = false;
  const formatted = [];

  for (const line of lines) {
    if (/^(\s*[-*])\s+/.test(line)) {
      if (!inList) {
        inList = true;
        formatted.push('<ul>');
      }
      formatted.push(`<li>${line.replace(/^(\s*[-*])\s+/, '')}</li>`);
    } else {
      if (inList) {
        formatted.push('</ul>');
        inList = false;
      }
      formatted.push(line);
    }
  }
  if (inList) formatted.push('</ul>');

  return formatted.join('\n');
}

export default function ChatApp() {
  const [messages, setMessages] = useState([]);
  console.log("Debug: setMessages is", setMessages);  
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [showLoginPopup, setShowLoginPopup] = useState(false);
  const { session, saveSession } = useSession();
  
  
  const sendMessage = async () => {
    if (!input.trim()) return;
  const currentInput = input; 
  setMessages(prev => [...prev, { role: 'user', text: currentInput }]);
  setInput('');
  setLoading(true)

  const requestBody = {
    message: currentInput,
    ...(session?.enrollment && session?.password ? { session } : {})
  };
try {
  const response = await fetch('http://localhost:5000/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(requestBody),
  });

  const data = await response.json();
  const replyText = Array.isArray(data.reply)
  ? data.reply[0]
  : typeof data.reply === 'string'
    ? data.reply
    : "No reply received";

  if (replyText.includes("🔐 Please log in")) {
    setShowLoginPopup(true);
  }
  setMessages(prev => [...prev, { role: 'bot', text: replyText }]);

  const graphData = Array.isArray(data.reply) && data.reply[1]?.graph_data
  ? data.reply[1].graph_data
  : data.graph_data;

  console.log("Graph data received:", graphData);

  if (Array.isArray(graphData) && graphData.length > 0) {
  setMessages(prev => [...prev, {
    role: 'graph', graphData
  }]);
}
}catch (err) {
    console.error("Chatbot error:", err);
    setMessages(prev => [...prev, { role: 'bot', text: "❌ Something went wrong. Try again." }]);
  } finally {
    setLoading(false);  
  }
  };
const handleLoginSubmit = async (creds) => {
  saveSession(creds);
  setShowLoginPopup(false);
  if (input.trim()) await sendMessage();
};  
 
  return (
  <div style={styles.outer}>
    {/* Top Header */}
    <div style={styles.header}>
      <img
        src="/jiit-logo.png"
        alt="JIIT Logo"
        style={styles.logo}
      />
      <h2 style={styles.title}>Academic Chatbot</h2>
    </div>

    {/* Chat Container */}
    <div style={styles.container}>
      <div style={styles.chatBox}>
        {messages.map((msg, i) => 
          msg.role === 'graph' ? (
            <GPAChart key={i} data={msg.graphData} />
          ) :(
          <div
            key={i}
            style={{
              ...styles.message,
              alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start',
              backgroundColor: msg.role === 'user' ? '#ffffff' : '#007bff',
              color: msg.role === 'user' ? '#000000' : '#ffffff'
            }}
          >
            <div
              dangerouslySetInnerHTML={{
                __html: `<b>${msg.role === 'user' ? 'You' : 'Bot'}:</b> ${typeof msg.text === 'string' ? linkify(msg.text): '[Invalid response]'}`,
              }}
            />
          </div>
        ))}
      </div>
      <div style={styles.inputRow}>
        <input
          type="text"
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Type your question..."
          style={styles.input}
        />
        <button onClick={sendMessage} style={styles.button}>Send</button>
      </div>
  
        {loading && (
          <div style={{ padding: "10px", color: "#999", fontStyle: "italic" }}>
            Bot is typing...
          </div>
        )}
      
      
        {showLoginPopup && (
          <LoginPopup
          onSubmit={handleLoginSubmit}
          onClose={() => setShowLoginPopup(false)}
          />
      )}
    </div>
  </div>
);
}


const styles = {
  outer: {
    background: '#f8f9fa',
    minHeight: '100vh',
    paddingTop: 10,
    fontFamily: 'Segoe UI, sans-serif',
  },
  header: {
    display: 'flex',
    alignItems: 'center',
    padding: '10px 40px',
    backgroundColor: '#003366',
    color: '#fff',
    marginBottom: 20,
  },
  logo: {
    height: 40,
    marginRight: 15,
  },
  title: {
    fontSize: 24,
    margin: 0,
  },
  container: {
    maxWidth: 900,
    margin: '0 auto',
    padding: 20,
    background: '#fff',
    borderRadius: 10,
    boxShadow: '0 0 10px rgba(0,0,0,0.1)',
  },
  chatBox: {
    display: 'flex',
    flexDirection: 'column',
    gap: 10,
    minHeight: 400,
    maxHeight: '60vh',
    overflowY: 'auto',
    padding: 20,
    background: '#e9ecef',
    borderRadius: 8,
    marginBottom: 20,
  },
  message: {
    padding: 8,
    borderRadius: 6,
    maxWidth: '80%',
    whiteSpace: 'pre-wrap',
    fontSize: '14px' ,
    lineHeight: '1.5',
  },
  inputRow: {
    display: 'flex',
    gap: 10,
  },
  input: {
    flexGrow: 1,
    padding: 12,
    fontSize: 16,
    borderRadius: 8,
    border: '1px solid #ccc',
  },
  button: {
    padding: '12px 20px',
    fontSize: 16,
    borderRadius: 8,
    background: '#007bff',
    color: '#fff',
    border: 'none',
    cursor: 'pointer',
  },
};
