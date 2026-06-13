let todos = [];
let currentFilter = 'all';

const list = document.getElementById('todo-list');
const loading = document.getElementById('loading');
const empty = document.getElementById('empty');
const form = document.getElementById('todo-form');
const formError = document.getElementById('form-error');

async function api(method, path, body) {
  const res = await fetch(path, {
    method,
    headers: body ? { 'Content-Type': 'application/json' } : {},
    body: body ? JSON.stringify(body) : undefined,
  });
  if (res.status === 204) return null;
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Request failed');
  }
  return res.json();
}

async function loadTodos() {
  try {
    todos = await api('GET', '/api/todos');
    renderTodos();
    loadStats();
  } catch (e) {
    loading.textContent = 'Failed to load todos.';
  }
}

async function loadStats() {
  const s = await api('GET', '/api/stats');
  document.getElementById('stat-total').textContent = s.total;
  document.getElementById('stat-active').textContent = s.active;
  document.getElementById('stat-done').textContent = s.completed;
}

function renderTodos() {
  loading.classList.add('hidden');
  const filtered = todos.filter(t => {
    if (currentFilter === 'active') return !t.completed;
    if (currentFilter === 'completed') return t.completed;
    return true;
  });

  if (filtered.length === 0) {
    empty.classList.remove('hidden');
    list.innerHTML = '';
    return;
  }
  empty.classList.add('hidden');

  list.innerHTML = filtered.map(t => `
    <li class="todo-item ${t.completed ? 'done' : ''}" data-id="${t.id}">
      <button class="toggle-btn" onclick="toggleTodo(${t.id})" title="${t.completed ? 'Mark active' : 'Mark done'}">
        ${t.completed ? '✓' : '○'}
      </button>
      <div class="todo-body">
        <span class="todo-title">${escHtml(t.title)}</span>
        ${t.description ? `<span class="todo-desc">${escHtml(t.description)}</span>` : ''}
      </div>
      <span class="priority-badge priority-${t.priority}">${t.priority}</span>
      <span class="todo-date">${formatDate(t.created_at)}</span>
      <button class="delete-btn" onclick="deleteTodo(${t.id})" title="Delete">✕</button>
    </li>
  `).join('');
}

async function toggleTodo(id) {
  try {
    const updated = await api('PATCH', `/api/todos/${id}/toggle`);
    const idx = todos.findIndex(t => t.id === id);
    if (idx !== -1) todos[idx] = updated;
    renderTodos();
    loadStats();
  } catch (e) {
    showError(e.message);
  }
}

async function deleteTodo(id) {
  try {
    await api('DELETE', `/api/todos/${id}`);
    todos = todos.filter(t => t.id !== id);
    renderTodos();
    loadStats();
  } catch (e) {
    showError(e.message);
  }
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const title = document.getElementById('title').value.trim();
  const description = document.getElementById('description').value.trim();
  const priority = document.getElementById('priority').value;
  if (!title) return;
  try {
    const created = await api('POST', '/api/todos', { title, description, priority });
    todos.unshift(created);
    form.reset();
    formError.classList.add('hidden');
    renderTodos();
    loadStats();
  } catch (e) {
    showError(e.message);
  }
});

document.querySelectorAll('.filter-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    currentFilter = btn.dataset.filter;
    renderTodos();
  });
});

function showError(msg) {
  formError.textContent = msg;
  formError.classList.remove('hidden');
  setTimeout(() => formError.classList.add('hidden'), 4000);
}

function escHtml(str) {
  return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

function formatDate(iso) {
  if (!iso) return '';
  return new Date(iso + 'Z').toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
}

loadTodos();
