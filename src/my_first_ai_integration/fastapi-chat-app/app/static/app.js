/* ============================================================
   AI Chat – Frontend Application
   ============================================================ */

// ---- Markdown + highlight setup ----
marked.setOptions({ breaks: true, gfm: true });

const renderer = new marked.Renderer();

renderer.code = (code, lang) => {
  const language = (lang || "").split(" ")[0];
  let highlighted = code;
  if (language && hljs.getLanguage(language)) {
    try { highlighted = hljs.highlight(code, { language }).value; } catch {}
  } else {
    try { highlighted = hljs.highlightAuto(code).value; } catch {}
  }
  const escapedCode = code.replace(/`/g, "&#96;");
  return `
    <div class="code-block-wrap">
      <div class="code-block-header">
        <span class="code-lang">${language || "code"}</span>
        <button class="copy-code-btn" data-code="${encodeURIComponent(escapedCode)}">Copy</button>
      </div>
      <pre><code class="hljs ${language}">${highlighted}</code></pre>
    </div>`;
};

marked.use({ renderer });

// ---- State ----
let token     = localStorage.getItem("chat_token") || null;
let username  = localStorage.getItem("chat_user")  || null;
let convs     = [];          // [{id, title, updated_at}]
let activeId  = null;        // current conversation id

// ---- DOM refs ----
const $ = id => document.getElementById(id);

const authScreen    = $("auth-screen");
const chatScreen    = $("chat-screen");
const loginForm     = $("login-form");
const registerForm  = $("register-form");
const loginError    = $("login-error");
const registerError = $("register-error");
const loginSubmit   = $("login-submit");
const regSubmit     = $("register-submit");

const usernameLabel  = $("username-label");
const userAvatar     = $("user-avatar");
const convList       = $("conversation-list");
const chatMessages   = $("chat-messages");
const messageInput   = $("message-input");
const sendBtn        = $("send-btn");
const convTitleHdr   = $("conv-title-header");
const mobileConvTitle = $("mobile-conv-title");
const charCount      = $("char-count");
const renameBtn      = $("rename-conv-btn");
const deleteBtn      = $("delete-conv-btn");

const renameModal    = $("rename-modal");
const renameInput    = $("rename-input");
const renameCancel   = $("rename-cancel");
const renameConfirm  = $("rename-confirm");

const deleteModal    = $("delete-modal");
const deleteCancel   = $("delete-cancel");
const deleteConfirm  = $("delete-confirm");

const sidebar        = $("sidebar");
const sidebarBackdrop = $("sidebar-backdrop");
const sidebarToggle  = $("sidebar-toggle");

// ============================================================
// API helpers
// ============================================================
async function api(path, opts = {}) {
  const headers = { "Content-Type": "application/json", ...(opts.headers || {}) };
  if (token) headers["Authorization"] = `Bearer ${token}`;
  const res = await fetch(path, { ...opts, headers });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.detail || `HTTP ${res.status}`);
  return data;
}

function setError(el, msg) { el.textContent = msg; }
function clearErrors() { loginError.textContent = ""; registerError.textContent = ""; }

// ============================================================
// Toast
// ============================================================
let toastTimer = null;
function toast(msg, duration = 2600) {
  const el = $("toast");
  el.textContent = msg;
  el.classList.add("show");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => el.classList.remove("show"), duration);
}

// ============================================================
// Auth tabs
// ============================================================
document.querySelectorAll(".tab").forEach(btn => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
    btn.classList.add("active");
    const tab = btn.dataset.tab;
    loginForm.classList.toggle("hidden", tab !== "login");
    registerForm.classList.toggle("hidden", tab !== "register");
    clearErrors();
  });
});

// Password visibility toggles
document.querySelectorAll(".toggle-pass").forEach(btn => {
  btn.addEventListener("click", () => {
    const input = btn.previousElementSibling;
    input.type = input.type === "password" ? "text" : "password";
    btn.style.opacity = input.type === "text" ? "1" : "";
  });
});

// ============================================================
// Login
// ============================================================
loginForm.addEventListener("submit", async e => {
  e.preventDefault();
  clearErrors();
  const uname = $("login-username").value.trim();
  const pass  = $("login-password").value;
  if (!uname || !pass) return setError(loginError, "Please fill in all fields.");
  setBtnLoading(loginSubmit, true);
  try {
    const data = await api("/api/auth/login", {
      method: "POST",
      body: JSON.stringify({ username: uname, password: pass }),
    });
    token = data.access_token;
    username = uname;
    localStorage.setItem("chat_token", token);
    localStorage.setItem("chat_user", username);
    enterChat();
  } catch (err) {
    setError(loginError, err.message);
  } finally {
    setBtnLoading(loginSubmit, false);
  }
});

// ============================================================
// Register
// ============================================================
registerForm.addEventListener("submit", async e => {
  e.preventDefault();
  clearErrors();
  const uname = $("reg-username").value.trim();
  const email = $("reg-email").value.trim();
  const pass  = $("reg-password").value;
  if (!uname || !email || !pass) return setError(registerError, "Please fill in all fields.");
  setBtnLoading(regSubmit, true);
  try {
    await api("/api/auth/register", {
      method: "POST",
      body: JSON.stringify({ username: uname, email, password: pass }),
    });
    const data = await api("/api/auth/login", {
      method: "POST",
      body: JSON.stringify({ username: uname, password: pass }),
    });
    token = data.access_token;
    username = uname;
    localStorage.setItem("chat_token", token);
    localStorage.setItem("chat_user", username);
    enterChat();
  } catch (err) {
    setError(registerError, err.message);
  } finally {
    setBtnLoading(regSubmit, false);
  }
});

function setBtnLoading(btn, loading) {
  btn.disabled = loading;
  btn.querySelector(".btn-label").classList.toggle("hidden", loading);
  btn.querySelector(".spinner").classList.toggle("hidden", !loading);
}

// ============================================================
// Logout
// ============================================================
$("logout-btn").addEventListener("click", logout);

function logout() {
  token = null; username = null; activeId = null; convs = [];
  localStorage.removeItem("chat_token");
  localStorage.removeItem("chat_user");
  chatScreen.classList.add("hidden");
  authScreen.classList.remove("hidden");
  loginForm.reset();
  registerForm.reset();
}

// ============================================================
// Enter chat
// ============================================================
async function enterChat() {
  authScreen.classList.add("hidden");
  chatScreen.classList.remove("hidden");
  usernameLabel.textContent = username;
  userAvatar.textContent = (username || "U")[0].toUpperCase();
  await loadConversations(true);
}

// ============================================================
// Load conversations
// ============================================================
async function loadConversations(selectFirst = false) {
  try {
    convs = await api("/api/chat/conversations");
    renderSidebar();
    if (selectFirst && convs.length > 0) {
      await selectConv(convs[0].id);
    } else if (convs.length === 0) {
      activeId = null;
      renderSidebar();
      showWelcome();
      updateHeader(null);
    }
  } catch {
    logout();
  }
}

function renderSidebar() {
  convList.innerHTML = "";
  if (convs.length === 0) {
    const li = document.createElement("li");
    li.style.cssText = "color:var(--text-dim);font-size:0.82rem;padding:14px 12px;cursor:default";
    li.textContent = "No conversations yet";
    convList.appendChild(li);
    return;
  }
  convs.forEach(c => {
    const li = document.createElement("li");
    li.dataset.id = c.id;
    if (c.id === activeId) li.classList.add("active");
    li.setAttribute("role", "option");
    li.setAttribute("aria-selected", c.id === activeId ? "true" : "false");

    const titleSpan = document.createElement("span");
    titleSpan.className = "conv-title";
    titleSpan.textContent = c.title || "New Chat";

    const menuBtn = document.createElement("button");
    menuBtn.className = "conv-menu-btn";
    menuBtn.innerHTML = "&#8942;";
    menuBtn.setAttribute("aria-label", "Conversation options");
    menuBtn.addEventListener("click", e => { e.stopPropagation(); showCtxMenu(e, c); });

    li.appendChild(titleSpan);
    li.appendChild(menuBtn);
    li.addEventListener("click", () => selectConv(c.id));
    convList.appendChild(li);
  });
}

// ============================================================
// Context menu (rename / delete)
// ============================================================
let activeCtxMenu = null;

function showCtxMenu(e, conv) {
  closeCtxMenu();
  const menu = document.createElement("div");
  menu.className = "ctx-menu";

  const renameItem = document.createElement("button");
  renameItem.innerHTML = `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg> Rename`;
  renameItem.addEventListener("click", () => { closeCtxMenu(); openRenameModal(conv); });

  const deleteItem = document.createElement("button");
  deleteItem.className = "danger";
  deleteItem.innerHTML = `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/></svg> Delete`;
  deleteItem.addEventListener("click", () => { closeCtxMenu(); openDeleteModal(conv.id); });

  menu.appendChild(renameItem);
  menu.appendChild(deleteItem);
  document.body.appendChild(menu);
  activeCtxMenu = menu;

  const rect = e.currentTarget.getBoundingClientRect();
  menu.style.top = `${rect.bottom + 4}px`;
  menu.style.left = `${Math.min(rect.left, window.innerWidth - 170)}px`;

  setTimeout(() => document.addEventListener("click", closeCtxMenu, { once: true }), 0);
}

function closeCtxMenu() {
  if (activeCtxMenu) { activeCtxMenu.remove(); activeCtxMenu = null; }
}

// ============================================================
// Select conversation
// ============================================================
async function selectConv(id) {
  activeId = id;
  closeSidebar();
  renderSidebar();
  chatMessages.innerHTML = "";
  const conv = convs.find(c => c.id === id);
  updateHeader(conv ? conv.title : "");
  await loadMessages(id);
}

async function loadMessages(convId) {
  try {
    const msgs = await api(`/api/chat/conversations/${convId}/messages`);
    if (msgs.length === 0) { showWelcome("Send a message to start the conversation."); return; }
    msgs.forEach(m => appendMessage(m.sender, m.content, new Date(m.created_at)));
    scrollToBottom(false);
  } catch {}
}

function updateHeader(title) {
  const t = title || "AI Chat";
  convTitleHdr.textContent = t;
  mobileConvTitle.textContent = t;
  const hasConv = !!title;
  renameBtn.style.display = hasConv ? "" : "none";
  deleteBtn.style.display = hasConv ? "" : "none";
}

// ============================================================
// New conversation
// ============================================================
$("new-chat-btn").addEventListener("click", () => {
  activeId = null;
  renderSidebar();
  chatMessages.innerHTML = "";
  updateHeader(null);
  showWelcome("What's on your mind?");
  closeSidebar();
  messageInput.focus();
});

// ============================================================
// Send message
// ============================================================
async function sendMessage() {
  const content = messageInput.value.trim();
  if (!content || sendBtn.disabled) return;

  messageInput.value = "";
  resizeInput();
  updateCharCount();
  sendBtn.disabled = true;

  appendMessage("user", content);
  const typingRow = appendTyping();
  scrollToBottom();

  try {
    const data = await api("/api/chat/send", {
      method: "POST",
      body: JSON.stringify({ content, conversation_id: activeId || undefined }),
    });

    typingRow.remove();
    appendMessage("ai", data.ai_reply.content);
    scrollToBottom();

    // Update conversation list
    const isNew = !activeId || activeId !== data.conversation_id;
    activeId = data.conversation_id;
    await loadConversations(false);
    renderSidebar();
    updateHeader(data.conversation_title);

    if (isNew) {
      // scroll sidebar to top to show new conv
      convList.scrollTop = 0;
    }
  } catch (err) {
    typingRow.remove();
    appendMessage("ai", `**Error:** ${err.message}`);
    scrollToBottom();
  } finally {
    sendBtn.disabled = false;
    messageInput.focus();
  }
}

sendBtn.addEventListener("click", sendMessage);

messageInput.addEventListener("keydown", e => {
  if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); sendMessage(); }
});

messageInput.addEventListener("input", () => { resizeInput(); updateCharCount(); });

function resizeInput() {
  messageInput.style.height = "auto";
  messageInput.style.height = Math.min(messageInput.scrollHeight, 180) + "px";
}

function updateCharCount() {
  const len = messageInput.value.length;
  if (len === 0) { charCount.textContent = ""; return; }
  charCount.textContent = `${len}`;
  charCount.className = len > 3500 ? "over" : len > 2800 ? "warn" : "";
}

// ============================================================
// Message rendering
// ============================================================
function appendMessage(sender, content, date = new Date()) {
  // Remove welcome state if present
  chatMessages.querySelector(".welcome-state")?.remove();

  const row = document.createElement("div");
  row.className = `msg-row ${sender}`;

  const senderLabel = document.createElement("div");
  senderLabel.className = "msg-sender";
  senderLabel.textContent = sender === "user" ? username || "You" : "AI";

  const bubble = document.createElement("div");
  bubble.className = `message ${sender}`;

  if (sender === "ai") {
    const mdBody = document.createElement("div");
    mdBody.className = "md-body";
    mdBody.innerHTML = marked.parse(content);
    // Wire up copy-code buttons
    mdBody.querySelectorAll(".copy-code-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        copyToClipboard(decodeURIComponent(btn.dataset.code));
        btn.textContent = "Copied!";
        btn.classList.add("copied");
        setTimeout(() => { btn.textContent = "Copy"; btn.classList.remove("copied"); }, 2000);
      });
    });
    bubble.appendChild(mdBody);
  } else {
    bubble.textContent = content;
  }

  const meta = document.createElement("div");
  meta.className = "msg-meta";

  const time = document.createElement("span");
  time.className = "msg-time";
  time.textContent = formatTime(date);

  const copyBtn = document.createElement("button");
  copyBtn.className = "copy-msg-btn";
  copyBtn.textContent = "copy";
  copyBtn.addEventListener("click", () => {
    copyToClipboard(content);
    copyBtn.textContent = "copied!";
    setTimeout(() => { copyBtn.textContent = "copy"; }, 2000);
  });

  meta.appendChild(time);
  meta.appendChild(copyBtn);

  row.appendChild(senderLabel);
  row.appendChild(bubble);
  row.appendChild(meta);
  chatMessages.appendChild(row);
  return row;
}

function appendTyping() {
  chatMessages.querySelector(".welcome-state")?.remove();

  const row = document.createElement("div");
  row.className = "msg-row ai";

  const senderLabel = document.createElement("div");
  senderLabel.className = "msg-sender";
  senderLabel.textContent = "AI";

  const bubble = document.createElement("div");
  bubble.className = "message ai";
  bubble.innerHTML = `<div class="typing-dots"><span></span><span></span><span></span></div>`;

  row.appendChild(senderLabel);
  row.appendChild(bubble);
  chatMessages.appendChild(row);
  scrollToBottom();
  return row;
}

function showWelcome(subtitle = "Start a new conversation or select one from the sidebar.") {
  chatMessages.innerHTML = `
    <div class="welcome-state">
      <svg width="52" height="52" viewBox="0 0 36 36" fill="none">
        <circle cx="18" cy="18" r="18" fill="#6c63ff" opacity="0.18"/>
        <path d="M11 18c0-3.866 3.134-7 7-7s7 3.134 7 7-3.134 7-7 7" stroke="#6c63ff" stroke-width="2.2" stroke-linecap="round"/>
        <circle cx="18" cy="18" r="2.5" fill="#6c63ff"/>
      </svg>
      <h2>AI Chat</h2>
      <p>${subtitle}</p>
    </div>`;
}

// ============================================================
// Rename
// ============================================================
renameBtn.addEventListener("click", () => {
  const conv = convs.find(c => c.id === activeId);
  if (conv) openRenameModal(conv);
});

function openRenameModal(conv) {
  renameInput.value = conv.title || "";
  renameModal.classList.remove("hidden");
  renameModal.dataset.convId = conv.id;
  renameInput.focus();
  renameInput.select();
}

renameCancel.addEventListener("click", () => renameModal.classList.add("hidden"));
renameModal.addEventListener("click", e => { if (e.target === renameModal) renameModal.classList.add("hidden"); });

renameConfirm.addEventListener("click", async () => {
  const id = parseInt(renameModal.dataset.convId);
  const title = renameInput.value.trim();
  if (!title) return;
  renameModal.classList.add("hidden");
  try {
    await api(`/api/chat/conversations/${id}`, {
      method: "PATCH",
      body: JSON.stringify({ title }),
    });
    await loadConversations(false);
    renderSidebar();
    if (id === activeId) updateHeader(title);
    toast("Conversation renamed.");
  } catch (err) {
    toast(`Rename failed: ${err.message}`);
  }
});

renameInput.addEventListener("keydown", e => { if (e.key === "Enter") renameConfirm.click(); });

// ============================================================
// Delete
// ============================================================
deleteBtn.addEventListener("click", () => openDeleteModal(activeId));

function openDeleteModal(id) {
  deleteModal.classList.remove("hidden");
  deleteModal.dataset.convId = id;
}

deleteCancel.addEventListener("click", () => deleteModal.classList.add("hidden"));
deleteModal.addEventListener("click", e => { if (e.target === deleteModal) deleteModal.classList.add("hidden"); });

deleteConfirm.addEventListener("click", async () => {
  const id = parseInt(deleteModal.dataset.convId);
  deleteModal.classList.add("hidden");
  try {
    await api(`/api/chat/conversations/${id}`, { method: "DELETE" });
    if (activeId === id) {
      activeId = null;
      chatMessages.innerHTML = "";
      updateHeader(null);
    }
    await loadConversations(false);
    if (!activeId && convs.length > 0) await selectConv(convs[0].id);
    else if (convs.length === 0) showWelcome();
    toast("Conversation deleted.");
  } catch (err) {
    toast(`Delete failed: ${err.message}`);
  }
});

// ============================================================
// Header rename/delete (also tied to header buttons above)
// ============================================================

// ============================================================
// Mobile sidebar
// ============================================================
sidebarToggle.addEventListener("click", () => {
  sidebar.classList.toggle("open");
  sidebarBackdrop.classList.toggle("show", sidebar.classList.contains("open"));
});

sidebarBackdrop.addEventListener("click", closeSidebar);

function closeSidebar() {
  sidebar.classList.remove("open");
  sidebarBackdrop.classList.remove("show");
}

// ============================================================
// Utility
// ============================================================
function scrollToBottom(smooth = true) {
  chatMessages.scrollTo({ top: chatMessages.scrollHeight, behavior: smooth ? "smooth" : "instant" });
}

function formatTime(date) {
  const now = new Date();
  const sameDay = date.toDateString() === now.toDateString();
  if (sameDay) return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  return date.toLocaleDateString([], { month: "short", day: "numeric" }) +
         " " + date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

function copyToClipboard(text) {
  if (navigator.clipboard) {
    navigator.clipboard.writeText(text).catch(() => fallbackCopy(text));
  } else {
    fallbackCopy(text);
  }
}

function fallbackCopy(text) {
  const ta = document.createElement("textarea");
  ta.value = text;
  ta.style.cssText = "position:fixed;opacity:0";
  document.body.appendChild(ta);
  ta.select();
  document.execCommand("copy");
  ta.remove();
}

// ============================================================
// Keyboard shortcuts
// ============================================================
document.addEventListener("keydown", e => {
  if ((e.metaKey || e.ctrlKey) && e.key === "k") {
    e.preventDefault();
    $("new-chat-btn").click();
  }
  if (e.key === "Escape") {
    renameModal.classList.add("hidden");
    deleteModal.classList.add("hidden");
    closeCtxMenu();
    closeSidebar();
  }
});

// ============================================================
// Init
// ============================================================

// Add PATCH endpoint support — wire rename to the backend
// The API needs a PATCH /api/chat/conversations/{id} endpoint
// (added in router below)

if (token) {
  enterChat();
} else {
  authScreen.classList.remove("hidden");
}
