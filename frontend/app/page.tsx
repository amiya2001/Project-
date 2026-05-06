'use client';
import { useState, useRef, useEffect } from 'react';
import { api } from '../lib/api';

type Message = {
  role: 'user' | 'ai';
  content: string;
  sources?: {id: string; content: string; score: number; metadata: any}[];
};

export default function Home() {
  const [messages, setMessages]     = useState<Message[]>([]);
  const [input, setInput]           = useState('');
  const [sessionId, setSessionId]   = useState('session_1');
  const [topK, setTopK]             = useState(3);
  const [thinking, setThinking]     = useState(false);
  const [docContent, setDocContent] = useState('');
  const [docName, setDocName]       = useState('');
  const [view, setView]             = useState<'chat'|'upload'>('chat');
  const [ingesting, setIngesting]   = useState(false);
  const [ingestMsg, setIngestMsg]   = useState('');
  const messagesEnd = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEnd.current?.scrollIntoView({behavior: 'smooth'});
  }, [messages, thinking]);

  const send = async () => {
    if (!input.trim() || thinking) return;
    const text = input.trim();
    setInput('');
    setMessages(m => [...m, {role: 'user', content: text}]);
    setThinking(true);
    try {
      const res = await api.chat(sessionId, text, topK);
      setMessages(m => [...m, {
        role: 'ai',
        content: res.answer,
        sources: res.sources
      }]);
    } catch {
      setMessages(m => [...m, {
        role: 'ai',
        content: 'Error — is your FastAPI server running on port 8000?'
      }]);
    }
    setThinking(false);
  };

  const handleIngest = async () => {
    if (!docName || !docContent) return;
    setIngesting(true);
    setIngestMsg('');
    try {
      const res = await api.ingest(docName, docContent);
      setIngestMsg(`✅ Ingested "${res.filename}" — ${res.chunks_created} chunks created`);
      setDocName('');
      setDocContent('');
    } catch {
      setIngestMsg('❌ Error — is FastAPI running?');
    }
    setIngesting(false);
  };

  return (
    <div style={{display:'flex',height:'100vh',background:'#0D1117',color:'#E6EDF3',fontFamily:'system-ui,sans-serif'}}>

      {/* Sidebar */}
      <div style={{width:52,background:'#161B22',borderRight:'1px solid #30363D',display:'flex',flexDirection:'column',alignItems:'center',padding:'12px 0',gap:4}}>
        <div style={{width:32,height:32,background:'#F0A500',borderRadius:8,display:'flex',alignItems:'center',justifyContent:'center',marginBottom:16,fontWeight:700,color:'#000',fontSize:14}}>P</div>
        {[
          {id:'chat', icon:'💬'},
          {id:'upload', icon:'📄'},
        ].map(({id,icon}) => (
          <button key={id} onClick={() => setView(id as any)}
            style={{width:36,height:36,borderRadius:8,border:'none',background: view===id ? '#2D1F00' : 'transparent',color: view===id ? '#F0A500' : '#8B949E',cursor:'pointer',fontSize:16}}>
            {icon}
          </button>
        ))}
      </div>

      {/* Chat View */}
      {view === 'chat' && (
        <div style={{flex:1,display:'flex',flexDirection:'column',overflow:'hidden'}}>

          {/* Header */}
          <div style={{padding:'0 20px',height:52,borderBottom:'1px solid #30363D',display:'flex',alignItems:'center',justifyContent:'space-between',flexShrink:0}}>
            <div>
              <div style={{fontSize:14,fontWeight:500}}>PAKS — Personal AI Knowledge System</div>
              <div style={{fontSize:11,color:'#6E7681',fontFamily:'monospace'}}>{sessionId}</div>
            </div>
            <div style={{display:'flex',gap:8}}>
              <button onClick={() => {setMessages([]); api.clearSession(sessionId);}}
                style={{background:'#21262D',border:'1px solid #30363D',color:'#8B949E',padding:'5px 10px',borderRadius:6,fontSize:11,cursor:'pointer'}}>
                Clear
              </button>
              <button onClick={() => setView('upload')}
                style={{background:'#2D1F00',border:'1px solid #4D3200',color:'#F0A500',padding:'5px 10px',borderRadius:6,fontSize:11,cursor:'pointer'}}>
                + Ingest
              </button>
            </div>
          </div>

          {/* Messages */}
          <div style={{flex:1,overflowY:'auto',padding:20,display:'flex',flexDirection:'column',gap:16}}>
            {messages.length === 0 && (
              <div style={{flex:1,display:'flex',flexDirection:'column',alignItems:'center',justifyContent:'center',gap:12,color:'#6E7681'}}>
                <div style={{width:48,height:48,background:'#2D1F00',borderRadius:12,display:'flex',alignItems:'center',justifyContent:'center',fontSize:20}}>🧠</div>
                <div style={{fontSize:16,color:'#E6EDF3',fontWeight:500}}>Ask your knowledge base</div>
                <div style={{fontSize:13,textAlign:'center',maxWidth:280,lineHeight:1.6}}>
                  Ingest documents then ask questions — Claude answers from your data only
                </div>
                <div style={{display:'flex',flexWrap:'wrap',gap:6,justifyContent:'center',marginTop:4}}>
                  {['What is RAG?','How does ChromaDB work?','Explain embeddings'].map(s => (
                    <button key={s} onClick={() => {setInput(s); setTimeout(send, 100);}}
                      style={{padding:'6px 12px',borderRadius:20,border:'1px solid #30363D',fontSize:11,color:'#8B949E',cursor:'pointer',background:'#161B22'}}>
                      {s}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {messages.map((m, i) => (
              <div key={i} style={{display:'flex',gap:10,justifyContent: m.role==='user' ? 'flex-end' : 'flex-start'}}>
                {m.role === 'ai' && (
                  <div style={{width:28,height:28,borderRadius:8,background:'#21262D',border:'1px solid #30363D',display:'flex',alignItems:'center',justifyContent:'center',fontSize:11,flexShrink:0}}>AI</div>
                )}
                <div style={{maxWidth:'75%'}}>
                  <div style={{
                    padding:'10px 14px',borderRadius:10,fontSize:13,lineHeight:1.6,
                    background: m.role==='user' ? '#2D1F00' : '#161B22',
                    border: m.role==='user' ? '1px solid #4D3200' : '1px solid #30363D'
                  }}>
                    {m.content}
                  </div>
                  {m.sources && m.sources.length > 0 && (
                    <div style={{display:'flex',flexWrap:'wrap',gap:4,marginTop:6}}>
                      {m.sources.map((s,j) => (
                        <span key={j} style={{fontSize:10,padding:'2px 7px',borderRadius:4,background:'#0D2137',color:'#58A6FF',border:'1px solid #0D2C4A',fontFamily:'monospace'}}>
                          {s.metadata?.source || s.id} · {s.score?.toFixed(2)}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
                {m.role === 'user' && (
                  <div style={{width:28,height:28,borderRadius:8,background:'#F0A500',display:'flex',alignItems:'center',justifyContent:'center',fontSize:11,fontWeight:700,color:'#000',flexShrink:0}}>AP</div>
                )}
              </div>
            ))}

            {thinking && (
              <div style={{display:'flex',gap:10}}>
                <div style={{width:28,height:28,borderRadius:8,background:'#21262D',border:'1px solid #30363D',display:'flex',alignItems:'center',justifyContent:'center',fontSize:11}}>AI</div>
                <div style={{padding:'12px 14px',background:'#161B22',border:'1px solid #30363D',borderRadius:10,display:'flex',gap:4,alignItems:'center'}}>
                  {[0,1,2].map(i => (
                    <div key={i} style={{width:6,height:6,borderRadius:'50%',background:'#6E7681',animation:`pulse 1.2s ${i*0.2}s infinite`}}/>
                  ))}
                </div>
              </div>
            )}
            <div ref={messagesEnd}/>
          </div>

          {/* Input */}
          <div style={{padding:'12px 20px',borderTop:'1px solid #30363D',flexShrink:0}}>
            <div style={{display:'flex',alignItems:'center',gap:8,marginBottom:8}}>
              <span style={{fontSize:11,color:'#6E7681'}}>Sources:</span>
              <select value={topK} onChange={e => setTopK(Number(e.target.value))}
                style={{background:'#21262D',border:'1px solid #30363D',color:'#8B949E',padding:'2px 6px',borderRadius:5,fontSize:11}}>
                {[1,2,3,5].map(n => <option key={n} value={n}>{n}</option>)}
              </select>
              <span style={{fontSize:11,color:'#6E7681',marginLeft:'auto'}}>
                session: <span style={{color:'#F0A500',fontFamily:'monospace'}}>{sessionId}</span>
              </span>
            </div>
            <div style={{display:'flex',gap:8}}>
              <textarea value={input} onChange={e => setInput(e.target.value)}
                onKeyDown={e => {if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();send();}}}
                placeholder="Ask your knowledge base..."
                rows={1}
                style={{flex:1,background:'#161B22',border:'1px solid #30363D',borderRadius:10,padding:'10px 14px',color:'#E6EDF3',fontSize:13,fontFamily:'system-ui,sans-serif',resize:'none',outline:'none'}}/>
              <button onClick={send} disabled={thinking}
                style={{width:40,height:40,borderRadius:8,background:'#F0A500',border:'none',cursor:'pointer',fontSize:18,display:'flex',alignItems:'center',justifyContent:'center'}}>
                ↑
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Upload View */}
      {view === 'upload' && (
        <div style={{flex:1,display:'flex',flexDirection:'column',overflow:'hidden'}}>
          <div style={{padding:'0 20px',height:52,borderBottom:'1px solid #30363D',display:'flex',alignItems:'center',justifyContent:'space-between',flexShrink:0}}>
            <div style={{fontSize:14,fontWeight:500}}>Ingest Document</div>
            <button onClick={() => setView('chat')}
              style={{background:'#21262D',border:'1px solid #30363D',color:'#8B949E',padding:'5px 10px',borderRadius:6,fontSize:11,cursor:'pointer'}}>
              ← Back to Chat
            </button>
          </div>
          <div style={{flex:1,padding:24,display:'flex',flexDirection:'column',gap:16,maxWidth:640}}>
            <div>
              <label style={{fontSize:12,color:'#8B949E',display:'block',marginBottom:6}}>Filename</label>
              <input value={docName} onChange={e => setDocName(e.target.value)}
                placeholder="my-document.txt"
                style={{width:'100%',background:'#161B22',border:'1px solid #30363D',borderRadius:8,padding:'10px 14px',color:'#E6EDF3',fontSize:13,outline:'none'}}/>
            </div>
            <div style={{flex:1}}>
              <label style={{fontSize:12,color:'#8B949E',display:'block',marginBottom:6}}>Content</label>
              <textarea value={docContent} onChange={e => setDocContent(e.target.value)}
                placeholder="Paste your document content here..."
                style={{width:'100%',height:300,background:'#161B22',border:'1px solid #30363D',borderRadius:8,padding:'10px 14px',color:'#E6EDF3',fontSize:13,outline:'none',resize:'vertical',fontFamily:'monospace'}}/>
            </div>
            <button onClick={handleIngest} disabled={ingesting || !docName || !docContent}
              style={{background: ingesting ? '#2D1F00' : '#F0A500',color: ingesting ? '#F0A500' : '#000',border:'none',borderRadius:8,padding:'12px 20px',fontSize:13,fontWeight:600,cursor:'pointer'}}>
              {ingesting ? 'Ingesting...' : 'Ingest Document'}
            </button>
            {ingestMsg && (
              <div style={{padding:'10px 14px',background:'#0A1F0C',border:'1px solid #1a4a1a',borderRadius:8,fontSize:13,color:'#3FB950'}}>
                {ingestMsg}
              </div>
            )}
          </div>
        </div>
      )}

      <style>{`@keyframes pulse{0%,80%,100%{opacity:.3}40%{opacity:1}}`}</style>
    </div>
  );
}