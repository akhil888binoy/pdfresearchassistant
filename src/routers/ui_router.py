from fastapi import APIRouter
from fastapi.responses import HTMLResponse


ui_router = APIRouter(tags=["ui"])


@ui_router.get("/", response_class=HTMLResponse)
async def home_page():
    return """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>PDF Research Assistant</title>
    <style>
      :root {
        --bg: #0b1220;
        --bg-soft: #111b2e;
        --panel: rgba(15, 23, 42, 0.82);
        --panel-strong: rgba(15, 23, 42, 0.96);
        --line: rgba(148, 163, 184, 0.18);
        --text: #e5eefc;
        --muted: #94a3b8;
        --accent: #35c3a7;
        --accent-2: #f5a524;
        --accent-3: #5eead4;
        --danger: #fb7185;
        --shadow: 0 24px 80px rgba(2, 6, 23, 0.45);
      }

      * { box-sizing: border-box; }
      html, body { min-height: 100%; }
      body {
        margin: 0;
        font-family: "Aptos", "Segoe UI", "Helvetica Neue", Arial, sans-serif;
        color: var(--text);
        background:
          radial-gradient(circle at top left, rgba(53, 195, 167, 0.18), transparent 28%),
          radial-gradient(circle at 80% 10%, rgba(245, 165, 36, 0.14), transparent 26%),
          linear-gradient(160deg, #050816 0%, #0b1220 55%, #111827 100%);
        overflow-x: hidden;
      }

      body::before {
        content: "";
        position: fixed;
        inset: 0;
        background-image:
          linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
          linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
        background-size: 48px 48px;
        mask-image: linear-gradient(to bottom, rgba(0,0,0,0.5), transparent 90%);
        pointer-events: none;
      }

      .shell {
        width: min(1200px, calc(100% - 32px));
        margin: 0 auto;
        padding: 28px 0 40px;
        position: relative;
        z-index: 1;
      }

      .hero {
        display: grid;
        grid-template-columns: 1.3fr 0.7fr;
        gap: 20px;
        align-items: stretch;
      }

      .brand, .panel, .stat, .chip, .dropzone, .message {
        border: 1px solid var(--line);
        background: var(--panel);
        backdrop-filter: blur(18px);
        box-shadow: var(--shadow);
      }

      .brand {
        border-radius: 28px;
        padding: 28px;
        position: relative;
        overflow: hidden;
        animation: rise 0.7s ease both;
      }

      .brand::after {
        content: "";
        position: absolute;
        inset: auto -10% -40% auto;
        width: 280px;
        height: 280px;
        background: radial-gradient(circle, rgba(53, 195, 167, 0.32), transparent 70%);
        filter: blur(12px);
        pointer-events: none;
      }

      .eyebrow {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        padding: 8px 14px;
        border-radius: 999px;
        border: 1px solid rgba(94, 234, 212, 0.22);
        background: rgba(6, 182, 212, 0.08);
        color: #bffaf2;
        font-size: 12px;
        letter-spacing: 0.08em;
        text-transform: uppercase;
      }

      .eyebrow span {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: var(--accent);
        box-shadow: 0 0 18px var(--accent);
      }

      h1, h2, h3, p { margin: 0; }

      h1 {
        margin-top: 18px;
        font-family: "Georgia", "Times New Roman", serif;
        font-weight: 700;
        font-size: clamp(2.6rem, 4vw, 5rem);
        line-height: 0.96;
        letter-spacing: -0.05em;
        max-width: 10ch;
      }

      .lede {
        margin-top: 18px;
        max-width: 62ch;
        color: var(--muted);
        font-size: 1.03rem;
        line-height: 1.7;
      }

      .hero-actions {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        margin-top: 24px;
      }

      .button {
        appearance: none;
        border: 0;
        border-radius: 16px;
        padding: 12px 16px;
        font: inherit;
        font-weight: 700;
        cursor: pointer;
        transition: transform 0.18s ease, box-shadow 0.18s ease, background 0.18s ease;
      }

      .button:hover { transform: translateY(-1px); }
      .button.primary {
        color: #04111a;
        background: linear-gradient(135deg, var(--accent-3), var(--accent));
        box-shadow: 0 16px 34px rgba(53, 195, 167, 0.24);
      }
      .button.secondary {
        color: var(--text);
        background: rgba(148, 163, 184, 0.12);
        border: 1px solid rgba(148, 163, 184, 0.18);
      }
      .button.ghost {
        color: var(--muted);
        background: transparent;
        border: 1px dashed rgba(148, 163, 184, 0.24);
      }

      .hero-side {
        display: grid;
        gap: 16px;
      }

      .stat-grid {
        display: grid;
        gap: 16px;
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }

      .stat {
        border-radius: 22px;
        padding: 18px;
      }

      .stat .label {
        color: var(--muted);
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
      }

      .stat .value {
        margin-top: 10px;
        font-size: 1.7rem;
        font-weight: 800;
      }

      .stat .hint {
        margin-top: 8px;
        color: var(--muted);
        font-size: 0.88rem;
        line-height: 1.5;
      }

      .panel {
        border-radius: 28px;
        padding: 22px;
        margin-top: 18px;
      }

      .panel-header {
        display: flex;
        justify-content: space-between;
        gap: 12px;
        align-items: center;
        margin-bottom: 16px;
      }

      .panel-header h2 {
        font-size: 1.15rem;
        letter-spacing: -0.03em;
      }

      .panel-header small {
        color: var(--muted);
      }

      .grid {
        display: grid;
        grid-template-columns: 1.05fr 0.95fr;
        gap: 18px;
      }

      .dropzone {
        border-radius: 24px;
        padding: 18px;
        min-height: 210px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        background:
          linear-gradient(180deg, rgba(53, 195, 167, 0.08), transparent 75%),
          rgba(15, 23, 42, 0.68);
      }

      .dropzone.dragover {
        border-color: rgba(94, 234, 212, 0.6);
        transform: translateY(-1px);
      }

      .dropzone h3 {
        font-size: 1.05rem;
        margin-bottom: 8px;
      }

      .dropzone p {
        color: var(--muted);
        line-height: 1.6;
      }

      .dropzone input[type="file"] {
        margin-top: 16px;
        color: var(--muted);
      }

      .meta-row {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 14px;
      }

      .chip {
        border-radius: 999px;
        padding: 9px 12px;
        font-size: 0.85rem;
        color: #d7fdf5;
        background: rgba(94, 234, 212, 0.08);
      }

      .conversation-list {
        display: grid;
        gap: 10px;
        max-height: 330px;
        overflow: auto;
        padding-right: 4px;
      }

      .conversation-item {
        border: 1px solid rgba(148, 163, 184, 0.14);
        background: rgba(2, 6, 23, 0.32);
        border-radius: 18px;
        padding: 14px;
        cursor: pointer;
        transition: border-color 0.18s ease, transform 0.18s ease;
      }

      .conversation-item:hover {
        transform: translateY(-1px);
        border-color: rgba(53, 195, 167, 0.45);
      }

      .conversation-item.active {
        border-color: rgba(53, 195, 167, 0.8);
        background: rgba(53, 195, 167, 0.09);
      }

      .conversation-item strong {
        display: block;
        font-size: 0.95rem;
      }

      .conversation-item span {
        display: block;
        margin-top: 6px;
        color: var(--muted);
        font-size: 0.83rem;
        word-break: break-word;
      }

      .timeline {
        margin-top: 18px;
        display: grid;
        gap: 10px;
      }

      .message {
        border-radius: 20px;
        padding: 14px 16px;
      }

      .message .role {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        font-size: 0.76rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--muted);
      }

      .message .bubble {
        margin-top: 10px;
        line-height: 1.65;
        white-space: pre-wrap;
        word-break: break-word;
      }

      .message.user {
        background: rgba(245, 165, 36, 0.08);
      }

      .message.assistant {
        background: rgba(53, 195, 167, 0.08);
      }

      .trace {
        margin-top: 18px;
        display: grid;
        gap: 10px;
      }

      .trace-item {
        border-radius: 18px;
        padding: 14px 16px;
        border: 1px solid rgba(148, 163, 184, 0.16);
        background: rgba(2, 6, 23, 0.34);
      }

      .trace-item .meta {
        display: flex;
        justify-content: space-between;
        gap: 12px;
        color: var(--muted);
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
      }

      .trace-item .snippet {
        margin-top: 10px;
        line-height: 1.6;
        white-space: pre-wrap;
        word-break: break-word;
      }

      .status {
        margin-top: 18px;
        border-radius: 18px;
        padding: 14px 16px;
        border: 1px solid rgba(148, 163, 184, 0.16);
        background: rgba(2, 6, 23, 0.42);
        color: var(--muted);
        white-space: pre-wrap;
      }

      .query-box {
        display: grid;
        gap: 12px;
      }

      textarea {
        width: 100%;
        min-height: 132px;
        resize: vertical;
        border-radius: 18px;
        border: 1px solid rgba(148, 163, 184, 0.18);
        background: rgba(2, 6, 23, 0.38);
        color: var(--text);
        padding: 14px;
        font: inherit;
        line-height: 1.6;
      }

      textarea::placeholder { color: #64748b; }

      .toolbar {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        align-items: center;
        justify-content: space-between;
      }

      .toolbar .hint {
        color: var(--muted);
        font-size: 0.92rem;
      }

      .footer-note {
        margin-top: 18px;
        color: var(--muted);
        font-size: 0.82rem;
      }

      @keyframes rise {
        from { opacity: 0; transform: translateY(12px); }
        to { opacity: 1; transform: translateY(0); }
      }

      @media (max-width: 980px) {
        .hero, .grid { grid-template-columns: 1fr; }
        h1 { max-width: 12ch; }
      }

      @media (max-width: 640px) {
        .shell { width: min(100% - 18px, 1200px); padding-top: 12px; }
        .brand, .panel { border-radius: 22px; padding: 18px; }
        .stat-grid { grid-template-columns: 1fr; }
        .hero-actions, .toolbar { flex-direction: column; align-items: stretch; }
        .button { width: 100%; text-align: center; }
      }
    </style>
  </head>
  <body>
    <main class="shell">
      <section class="hero">
        <div class="brand">
          <div class="eyebrow"><span></span> PDF Research Assistant</div>
          <h1>RAG over PDFs, with the retrieval path visible.</h1>
          <p class="lede">
            This is a dummy frontend for the FastAPI backend. Upload a PDF, build a
            conversation, and ask questions against retrieved chunks that ground the answer.
          </p>
          <div class="hero-actions">
            <button class="button primary" id="createConversationTop">Create conversation</button>
            <button class="button secondary" id="refreshAllTop">Refresh data</button>
            <button class="button ghost" id="loadDemoQuestion">Load demo prompt</button>
          </div>
        </div>

        <div class="hero-side">
          <div class="stat-grid">
            <div class="stat">
              <div class="label">Mode</div>
              <div class="value">RAG UI</div>
              <div class="hint">Frontend only. It uses retrieval, then generation.</div>
            </div>
            <div class="stat">
              <div class="label">Pipeline</div>
              <div class="value">RAG</div>
              <div class="hint">Upload, chunk, embed, retrieve, answer.</div>
            </div>
            <div class="stat">
              <div class="label">Upload cap</div>
              <div class="value">25 MB</div>
              <div class="hint">Matches the server-side validator.</div>
            </div>
            <div class="stat">
              <div class="label">Style</div>
              <div class="value">Glass</div>
              <div class="hint">Dark, high-contrast, and responsive.</div>
            </div>
          </div>
        </div>
      </section>

      <section class="panel">
        <div class="panel-header">
          <h2>Workspace</h2>
          <small id="sessionHint">No conversation selected yet.</small>
        </div>

        <div class="grid">
          <div class="dropzone" id="dropzone">
            <div>
              <h3>Upload a PDF</h3>
              <p>Drop a file here or choose one manually. The backend stores it, chunks text, and indexes embeddings for retrieval.</p>
              <input id="pdfInput" type="file" accept="application/pdf" />
              <div class="meta-row">
                <div class="chip">Drag and drop enabled</div>
                <div class="chip">Upload endpoint: /api/pdf/upload/single</div>
              </div>
            </div>
            <div class="toolbar">
              <span class="hint" id="uploadLabel">Waiting for a PDF.</span>
              <button class="button primary" id="uploadButton">Upload PDF</button>
            </div>
          </div>

          <div class="dropzone">
            <div>
              <h3>Conversations</h3>
              <p>Select or create a conversation to keep a thread of questions and answers.</p>
              <div class="meta-row">
                <div class="chip">GET /api/pdf/conversations</div>
                <div class="chip">POST /api/pdf/conversation</div>
              </div>
            </div>
            <div class="conversation-list" id="conversationList"></div>
            <div class="toolbar">
              <span class="hint">Active conversation drives the query form.</span>
              <button class="button secondary" id="createConversationBottom">New conversation</button>
            </div>
          </div>
        </div>

        <div class="grid" style="margin-top:18px;">
          <div class="dropzone">
            <div>
              <h3>Ask a question</h3>
              <p>Send a prompt to the query endpoint. The response includes the answer and the retrieved chunks used to ground it.</p>
              <div class="meta-row">
                <div class="chip">POST /api/pdf/query</div>
                <div class="chip">GET /api/pdf/messages/{conversation_id}</div>
              </div>
            </div>

            <div class="query-box">
              <textarea id="questionInput" placeholder="Example: Summarize the main argument in the uploaded paper and mention the strongest supporting evidence."></textarea>
              <div class="toolbar">
                <span class="hint">The prompt is sent with the selected conversation id.</span>
                <button class="button primary" id="askButton">Send question</button>
              </div>
            </div>
          </div>

          <div class="dropzone">
            <div>
              <h3>Retrieved context</h3>
              <p>The top chunks returned by Chroma are shown here after each question.</p>
              <div class="meta-row">
                <div class="chip">Chroma hits</div>
                <div class="chip">Grounded answer path</div>
              </div>
            </div>
            <div class="trace" id="retrievalTrace"></div>
            <div style="margin-top: 18px;">
              <h3>Conversation timeline</h3>
              <p>Messages are pulled from the backend after each action.</p>
            </div>
            <div class="timeline" id="timeline"></div>
            <div class="status" id="status">Ready.</div>
          </div>
        </div>
      </section>

      <p class="footer-note">
        This page is intentionally simple and local. It is meant to validate the API wiring, not replace a production UI.
      </p>
    </main>

    <script>
      const state = {
        conversationId: localStorage.getItem("pdfassistant.conversationId") || "",
        pendingFile: null,
      };

      const conversationList = document.getElementById("conversationList");
      const timeline = document.getElementById("timeline");
      const retrievalTrace = document.getElementById("retrievalTrace");
      const statusBox = document.getElementById("status");
      const sessionHint = document.getElementById("sessionHint");
      const questionInput = document.getElementById("questionInput");
      const uploadLabel = document.getElementById("uploadLabel");
      const pdfInput = document.getElementById("pdfInput");
      const dropzone = document.getElementById("dropzone");

      const demoQuestion = "What are the key findings, assumptions, and unresolved questions in this PDF?";
      document.getElementById("loadDemoQuestion").addEventListener("click", () => {
        questionInput.value = demoQuestion;
        questionInput.focus();
      });

      function setStatus(message) {
        statusBox.textContent = message;
      }

      function shortId(value) {
        return value ? value.slice(0, 8) + "…" + value.slice(-6) : "none";
      }

      function setActiveConversation(id) {
        state.conversationId = id;
        localStorage.setItem("pdfassistant.conversationId", id);
        sessionHint.textContent = id ? `Active conversation ${shortId(id)}` : "No conversation selected yet.";
      }

      async function fetchJson(url, options) {
        const response = await fetch(url, options);
        const text = await response.text();
        let payload = text;
        try {
          payload = text ? JSON.parse(text) : null;
        } catch (_) {}
        if (!response.ok) {
          const detail = typeof payload === "object" ? JSON.stringify(payload, null, 2) : String(payload);
          throw new Error(`${response.status} ${response.statusText}\\n${detail}`);
        }
        return payload;
      }

      function renderConversations(items) {
        conversationList.innerHTML = "";
        if (!items.length) {
          conversationList.innerHTML = '<div class="status">No conversations loaded yet.</div>';
          return;
        }

        items.forEach((conversation) => {
          const item = document.createElement("button");
          item.type = "button";
          item.className = "conversation-item" + (String(conversation.id) === String(state.conversationId) ? " active" : "");
          item.innerHTML = `
            <strong>${shortId(conversation.id)}</strong>
            <span>${new Date(conversation.created_at).toLocaleString()}</span>
          `;
          item.addEventListener("click", async () => {
            setActiveConversation(conversation.id);
            await loadMessages();
          });
          conversationList.appendChild(item);
        });
      }

      function renderTimeline(messages) {
        timeline.innerHTML = "";
        if (!messages.length) {
          timeline.innerHTML = '<div class="status">No messages yet for this conversation.</div>';
          return;
        }

        messages.forEach((message) => {
          const node = document.createElement("div");
          node.className = `message ${message.role === "assistant" ? "assistant" : "user"}`;
          node.innerHTML = `
            <div class="role">${message.role}</div>
            <div class="bubble"></div>
          `;
          node.querySelector(".bubble").textContent = message.content;
          timeline.appendChild(node);
        });
      }

      function renderRetrievalTrace(items) {
        retrievalTrace.innerHTML = "";
        if (!items.length) {
          retrievalTrace.innerHTML = '<div class="status">No retrieval trace yet. Ask a question to inspect the grounded context.</div>';
          return;
        }

        items.forEach((item, index) => {
          const node = document.createElement("div");
          node.className = "trace-item";
          const metadata = item.metadata || {};
          node.innerHTML = `
            <div class="meta">
              <span>Chunk ${index + 1}</span>
              <span>page ${metadata.page_number ?? "?"} · rank ${metadata.chunk_number ?? "?"}</span>
            </div>
            <div class="snippet"></div>
          `;
          node.querySelector(".snippet").textContent = item.snippet || "";
          retrievalTrace.appendChild(node);
        });
      }

      async function loadConversations() {
        const conversations = await fetchJson("/api/pdf/conversations");
        if (Array.isArray(conversations)) {
          if (!state.conversationId && conversations.length) {
            setActiveConversation(conversations[0].id);
          } else {
            sessionHint.textContent = state.conversationId ? `Active conversation ${shortId(state.conversationId)}` : "No conversation selected yet.";
          }
          renderConversations(conversations);
        }
        return conversations;
      }

      async function loadMessages() {
        if (!state.conversationId) {
          renderTimeline([]);
          return [];
        }
        const messages = await fetchJson(`/api/pdf/messages/${state.conversationId}`);
        renderTimeline(Array.isArray(messages) ? messages : []);
        return messages;
      }

      async function refreshAll() {
        await loadConversations();
        if (state.conversationId) {
          await loadMessages();
        }
      }

      async function createConversation() {
        setStatus("Creating conversation...");
        const payload = await fetchJson("/api/pdf/conversation", { method: "POST" });
        const id = payload.conversation;
        setActiveConversation(id);
        await refreshAll();
        setStatus(`Created conversation ${id}`);
      }

      async function uploadPdf(file) {
        if (!file) {
          throw new Error("Choose a PDF first.");
        }

        const formData = new FormData();
        formData.append("file", file);
        uploadLabel.textContent = `Uploading ${file.name}...`;
        setStatus(`Uploading ${file.name} (${Math.round(file.size / 1024)} KB)`);

        const response = await fetch("/api/pdf/upload/single", {
          method: "POST",
          body: formData,
        });

        const bodyText = await response.text();
        if (!response.ok) {
          throw new Error(bodyText || response.statusText);
        }

        state.pendingFile = null;
        pdfInput.value = "";
        uploadLabel.textContent = `Uploaded ${file.name}`;
        setStatus(`Upload complete:\\n${bodyText}`);
        await refreshAll();
      }

      async function askQuestion() {
        const question = questionInput.value.trim();
        if (!state.conversationId) {
          throw new Error("Create or select a conversation first.");
        }
        if (!question) {
          throw new Error("Write a question first.");
        }

        setStatus("Sending question...");
        const payload = await fetchJson("/api/pdf/query", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            conversation_id: state.conversationId,
            question,
          }),
        });

        renderRetrievalTrace(Array.isArray(payload.retrieval_trace) ? payload.retrieval_trace : []);
        setStatus(`Assistant response:\\n${payload.response}`);
        await loadMessages();
      }

      document.getElementById("createConversationTop").addEventListener("click", () => createConversation().catch(showError));
      document.getElementById("createConversationBottom").addEventListener("click", () => createConversation().catch(showError));
      document.getElementById("refreshAllTop").addEventListener("click", () => refreshAll().catch(showError));
      document.getElementById("uploadButton").addEventListener("click", () => uploadPdf(state.pendingFile || pdfInput.files[0]).catch(showError));
      document.getElementById("askButton").addEventListener("click", () => askQuestion().catch(showError));

      pdfInput.addEventListener("change", () => {
        const file = pdfInput.files[0];
        state.pendingFile = file || null;
        uploadLabel.textContent = file ? `Ready to upload ${file.name}` : "Waiting for a PDF.";
      });

      dropzone.addEventListener("dragover", (event) => {
        event.preventDefault();
        dropzone.classList.add("dragover");
      });

      dropzone.addEventListener("dragleave", () => dropzone.classList.remove("dragover"));
      dropzone.addEventListener("drop", (event) => {
        event.preventDefault();
        dropzone.classList.remove("dragover");
        if (event.dataTransfer.files && event.dataTransfer.files.length) {
          const file = event.dataTransfer.files[0];
          state.pendingFile = file;
          uploadLabel.textContent = file ? `Ready to upload ${file.name}` : "Waiting for a PDF.";
        }
      });

      function showError(error) {
        setStatus(error.message || String(error));
      }

      (async function boot() {
        try {
          await refreshAll();
          renderRetrievalTrace([]);
          if (!state.conversationId) {
            setStatus("No conversation selected. Create one to start chatting.");
          }
        } catch (error) {
          showError(error);
        }
      })();
    </script>
  </body>
</html>
    """
