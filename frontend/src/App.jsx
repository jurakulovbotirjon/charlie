
import { useEffect, useRef, useState } from "react";
import {
  Activity,
  BrainCircuit,
  BookOpen,
  ChevronDown,
  Command,
  FileText,
  FolderOpen,
  LayoutDashboard,
  MessageSquare,
  Paperclip,
  Plus,
  Search,
  Send,
  Settings,
  Sparkles,
  Upload,
  Wifi,
  WifiOff,
  X,
  PanelLeftClose,
} from "lucide-react";
import "./App.css";

const API = "http://127.0.0.1:8000";

export default function App() {
  const [activePage, setActivePage] = useState("chat");
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [documents, setDocuments] = useState([]);
  const [backendOnline, setBackendOnline] = useState(false);
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [error, setError] = useState("");
  const messagesEnd = useRef(null);
  const fileInput = useRef(null);

  async function loadStatus() {
    try {
      const response = await fetch(`${API}/api/status`);
      setBackendOnline(response.ok);
    } catch {
      setBackendOnline(false);
    }
  }

  async function loadDocuments() {
    try {
      const response = await fetch(`${API}/api/documents`);
      if (!response.ok) throw new Error("Could not load documents");
      const data = await response.json();
      setDocuments(data);
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    loadStatus();
    loadDocuments();

    const interval = setInterval(loadStatus, 10000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    messagesEnd.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function sendMessage(event) {
    event.preventDefault();

    const text = question.trim();
    if (!text || loading) return;

    setError("");
    setQuestion("");
    setMessages((previous) => [
      ...previous,
      { role: "user", content: text },
    ]);
    setLoading(true);

    try {
      const response = await fetch(`${API}/api/search`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: text }),
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || "The request failed.");
      }

      setMessages((previous) => [
  ...previous,
  {
    role: "assistant",
    content: data.results?.length
      ? "I found some relevant passages in your knowledge library."
      : "I couldn't find supporting information in your library.",
    results: data.results || [],
  },
]);
    } catch (err) {
      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: `I couldn't reach my reasoning system. ${err.message}`,
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  async function uploadDocument(event) {
    const file = event.target.files?.[0];
    if (!file) return;

    setUploading(true);
    setError("");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(`${API}/api/ingest`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || "Upload failed.");
      }

      await loadDocuments();
      setActivePage("library");
    } catch (err) {
      setError(err.message);
    } finally {
      setUploading(false);
      event.target.value = "";
    }
  }

  function newChat() {
    setMessages([]);
    setQuestion("");
    setError("");
    setActivePage("chat");
  }

  return (
    <div className="app-shell">
      <aside className={`sidebar ${sidebarOpen ? "" : "sidebar-closed"}`}>
        <div className="brand">
          <div className="brand-mark">
            <BrainCircuit size={25} />
          </div>
          <div className="brand-copy">
            <strong>CHARLIESYNTH</strong>
            <span>PERSONAL INTELLIGENCE</span>
          </div>
          <button
            className="icon-button sidebar-toggle"
            onClick={() => setSidebarOpen(false)}
            title="Collapse sidebar"
          >
            <PanelLeftClose size={17} />
          </button>
        </div>

        <button className="new-chat-button" onClick={newChat}>
          <Plus size={18} />
          <span>New conversation</span>
          <Command size={14} className="shortcut-icon" />
        </button>

        <div className="nav-label">WORKSPACE</div>

        <nav className="navigation">
          <button
            className={activePage === "chat" ? "nav-item active" : "nav-item"}
            onClick={() => setActivePage("chat")}
          >
            <MessageSquare size={18} />
            <span>Conversations</span>
          </button>

          <button
            className={activePage === "library" ? "nav-item active" : "nav-item"}
            onClick={() => {
              setActivePage("library");
              loadDocuments();
            }}
          >
            <BookOpen size={18} />
            <span>Knowledge library</span>
            <span className="nav-count">{documents.length}</span>
          </button>

          <button
            className={activePage === "documents" ? "nav-item active" : "nav-item"}
            onClick={() => setActivePage("documents")}
          >
            <FolderOpen size={18} />
            <span>Document manager</span>
          </button>
        </nav>

        <div className="sidebar-bottom">
          <div className="connection-card">
            <div className="connection-top">
              <Activity size={16} />
              <span>CORE SYSTEM</span>
            </div>
            <div className="connection-status">
              <span className={`status-dot ${backendOnline ? "online" : ""}`} />
              {backendOnline ? "Backend connected" : "Backend offline"}
            </div>
            <div className="connection-sub">
              {backendOnline ? "Ready for requests" : "Waiting for API"}
            </div>
          </div>

          <button className="nav-item settings-button" onClick={() => setActivePage("settings")}>
            <Settings size={18} />
            <span>Settings</span>
          </button>

          <div className="user-profile">
            <div className="avatar">C</div>
            <div className="user-copy">
              <strong>CharlieSynth</strong>
              <span>Local instance · v0.1.0</span>
            </div>
            <ChevronDown size={16} />
          </div>
        </div>
      </aside>

      <main className="main-area">
        <header className="topbar">
          <div className="breadcrumb">
            {!sidebarOpen && (
              <button
                className="icon-button"
                onClick={() => setSidebarOpen(true)}
              >
                <PanelLeftClose size={18} />
              </button>
            )}
            <span>Workspace</span>
            <span className="breadcrumb-divider">/</span>
            <strong>
              {activePage === "chat" ? "Conversations" :
               activePage === "library" ? "Knowledge library" :
               activePage === "documents" ? "Documents" : "Settings"}
            </strong>
          </div>

          <div className="topbar-right">
            <div className={`system-pill ${backendOnline ? "connected" : ""}`}>
              {backendOnline ? <Wifi size={14} /> : <WifiOff size={14} />}
              {backendOnline ? "SYSTEM ONLINE" : "DISCONNECTED"}
            </div>
            <button className="icon-button" title="Search">
              <Search size={18} />
            </button>
          </div>
        </header>

        {error && (
          <div className="error-banner">
            <span>{error}</span>
            <button onClick={() => setError("")}><X size={16} /></button>
          </div>
        )}

        {activePage === "chat" && (
          <section className="chat-workspace">
            {messages.length === 0 ? (
              <div className="welcome-screen">
                <div className="orb-wrap">
                  <div className="orb-glow" />
                  <div className="orb">
                    <BrainCircuit size={42} />
                  </div>
                  <Sparkles className="orb-sparkle sparkle-one" size={18} />
                  <Sparkles className="orb-sparkle sparkle-two" size={13} />
                </div>

                <div className="welcome-eyebrow">
                  <span className="eyebrow-line" />
                  YOUR PERSONAL KNOWLEDGE SYSTEM
                  <span className="eyebrow-line" />
                </div>

                <h1>
                  Think beyond
                  <span> information.</span>
                </h1>

                <p className="welcome-description">
                  Your documents. Your knowledge. Your CharlieSynth.
                  <br />
                  Ask questions and explore what you've learned.
                </p>

                <div className="suggestion-grid">
                  <button onClick={() => setQuestion("What is cloud computing?")}>
                    <BookOpen size={18} />
                    <span>
                      <strong>Explore your textbooks</strong>
                      <small>Find information in your library</small>
                    </span>
                  </button>
                  <button onClick={() => setQuestion("Summarize the key concepts in my library.")}>
                    <LayoutDashboard size={18} />
                    <span>
                      <strong>Discover key concepts</strong>
                      <small>Connect ideas across documents</small>
                    </span>
                  </button>
                </div>
              </div>
            ) : (
              <div className="message-list">
                {messages.map((message, index) => (
                  <div className={`message-row ${message.role}`} key={index}>
                    <div className="message-avatar">
                      {message.role === "assistant"
                        ? <BrainCircuit size={19} />
                        : "Y"}
                    </div>
                    <div className="message-content">
                      <div className="message-author">
                        {message.role === "assistant" ? "CHARLIESYNTH" : "YOU"}
                      </div>
                      <div className="message-text">{message.content}</div>

                  {message.results?.length > 0 && (
                    <div className="evidence-list">
                      {message.results.map((result, index) => (
                        <details className="evidence-card" key={result.chunk_id || index}>
                          <summary>
                            <div className="evidence-number">
                              {String(index + 1).padStart(2, "0")}
                            </div>
                      
                            <div className="evidence-heading">
                              <strong>{result.filename}</strong>
                              <span>
                                {result.page_number
                                  ? `Page ${result.page_number}`
                                  : "Page unavailable"}
                              </span>
                            </div>
                                
                            <span className="evidence-label">SOURCE</span>
                          </summary>
                                
                          <div className="evidence-content">
                            {result.content}
                          </div>
                        </details>
                      ))}
                    </div>
                  )}
                    </div>
                  </div>
                ))}

                {loading && (
                  <div className="message-row assistant">
                    <div className="message-avatar"><BrainCircuit size={19} /></div>
                    <div className="message-content">
                      <div className="message-author">CHARLIESYNTH</div>
                      <div className="typing-indicator">
                        <span /><span /><span />
                        <small>Searching memory...</small>
                      </div>
                    </div>
                  </div>
                )}
                <div ref={messagesEnd} />
              </div>
            )}

            <div className="composer-area">
              <form className="composer" onSubmit={sendMessage}>
                <textarea
                  value={question}
                  onChange={(event) => setQuestion(event.target.value)}
                  placeholder="Ask CharlieSynth anything..."
                  rows={1}
                  onKeyDown={(event) => {
                    if (event.key === "Enter" && !event.shiftKey) {
                      event.preventDefault();
                      sendMessage(event);
                    }
                  }}
                />
                <div className="composer-footer">
                  <div className="composer-tools">
                    <button
                      type="button"
                      className="composer-tool"
                      onClick={() => fileInput.current?.click()}
                      title="Upload a document"
                    >
                      <Paperclip size={17} />
                      <span>Attach knowledge</span>
                    </button>
                  </div>
                  <button
                    className="send-button"
                    type="submit"
                    disabled={!question.trim() || loading}
                    title="Send message"
                  >
                    <Send size={17} />
                  </button>
                </div>
              </form>
              <input
                ref={fileInput}
                type="file"
                accept=".pdf,.txt"
                hidden
                onChange={uploadDocument}
              />
              <div className="composer-disclaimer">
                <Sparkles size={12} />
                CharlieSynth answers using its available knowledge and evidence.
              </div>
            </div>
          </section>
        )}

        {(activePage === "library" || activePage === "documents") && (
          <section className="library-page">
            <div className="page-heading">
              <div>
                <div className="section-kicker">PERSONAL MEMORY</div>
                <h1>Knowledge library<span>.</span></h1>
                <p>Your documents are the foundation of CharlieSynth's knowledge.</p>
              </div>
              <button
                className="upload-button"
                onClick={() => fileInput.current?.click()}
                disabled={uploading}
              >
                <Upload size={17} />
                {uploading ? "Processing..." : "Upload document"}
              </button>
            </div>

            <div className="library-stats">
              <div className="stat-card">
                <FileText size={19} />
                <strong>{documents.length}</strong>
                <span>Stored documents</span>
              </div>
              <div className="stat-card">
                <FolderOpen size={19} />
                <strong>{documents.filter((doc) => doc.status === "completed").length}</strong>
                <span>Processed documents</span>
              </div>
              <div className="stat-card">
                <Activity size={19} />
                <strong>{backendOnline ? "Active" : "Offline"}</strong>
                <span>Memory connection</span>
              </div>
            </div>

            <div className="documents-heading">
              <div>
                <h2>Your documents</h2>
                <span>{documents.length} items in your library</span>
              </div>
              <button className="refresh-button" onClick={loadDocuments}>
                <Activity size={15} /> Refresh
              </button>
            </div>

            <div className="document-list">
              {documents.length === 0 ? (
                <div className="empty-library">
                  <FolderOpen size={32} />
                  <strong>Your library is waiting.</strong>
                  <span>Upload your first PDF or TXT document.</span>
                </div>
              ) : documents.map((doc) => (
                <div className="document-card" key={doc.id}>
                  <div className="document-icon">
                    <FileText size={22} />
                  </div>
                  <div className="document-info">
                    <strong>{doc.filename}</strong>
                    <span>{doc.file_type?.toUpperCase() || "DOCUMENT"} · Added to memory</span>
                  </div>
                  <span className="document-status">
                    <span className="status-dot online" />
                    Stored
                  </span>
                </div>
              ))}
            </div>
            <input
              ref={fileInput}
              type="file"
              accept=".pdf,.txt"
              hidden
              onChange={uploadDocument}
            />
          </section>
        )}

        {activePage === "settings" && (
          <section className="library-page">
            <div className="page-heading">
              <div>
                <div className="section-kicker">CONFIGURATION</div>
                <h1>Settings<span>.</span></h1>
                <p>CharlieSynth local system information.</p>
              </div>
            </div>
            <div className="settings-card">
              <Activity size={20} />
              <div>
                <strong>Backend connection</strong>
                <span>{backendOnline ? "Connected to FastAPI" : "Backend is not responding"}</span>
              </div>
              <span className={`status-dot ${backendOnline ? "online" : ""}`} />
            </div>
            <div className="settings-card">
              <DatabaseIcon />
              <div>
                <strong>Knowledge storage</strong>
                <span>PostgreSQL · Local database</span>
              </div>
            </div>
          </section>
        )}

        <footer className="app-footer">
          <span>CHARLIESYNTH <b>0.1.0</b></span>
          <span>BUILT FOR KNOWLEDGE. DESIGNED FOR THINKING.</span>
        </footer>
      </main>
    </div>
  );
}

function DatabaseIcon() {
  return <FolderOpen size={20} />;
}
