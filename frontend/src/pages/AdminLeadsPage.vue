<script setup>
import { ref, computed, onMounted } from 'vue'

const TOKEN_KEY = 'gs_admin_token'

const token = ref(sessionStorage.getItem(TOKEN_KEY) || '')
const password = ref('')
const loginError = ref('')
const loggingIn = ref(false)

const leads = ref([])
const total = ref(0)
const loading = ref(false)
const loadError = ref('')
const onlyWithFiles = ref(false)

const filteredLeads = computed(() =>
  onlyWithFiles.value ? leads.value.filter((l) => l.file_path) : leads.value,
)

const filesCount = computed(() => leads.value.filter((l) => l.file_path).length)

const fileError = ref('')
const deleteError = ref('')
const deletingId = ref(null)

function fileApiUrl(lead, download = false) {
  const q = download ? '?disposition=attachment' : ''
  return `/api/admin/leads/${lead.id}/file${q}`
}

async function fetchLeadFile(lead, download = false) {
  fileError.value = ''
  const res = await fetch(fileApiUrl(lead, download), {
    headers: { Authorization: `Bearer ${token.value}` },
  })
  if (res.status === 401) {
    logout()
    return null
  }
  if (!res.ok) {
    fileError.value = 'Файл не найден на сервере'
    return null
  }
  return res.blob()
}

async function openFile(lead) {
  if (!lead.file_path) return
  const blob = await fetchLeadFile(lead)
  if (!blob) return
  const url = URL.createObjectURL(blob)
  window.open(url, '_blank', 'noopener')
  setTimeout(() => URL.revokeObjectURL(url), 60_000)
}

async function downloadFile(lead) {
  if (!lead.file_path) return
  const blob = await fetchLeadFile(lead, true)
  if (!blob) return
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = lead.file_name || 'file'
  a.rel = 'noopener'
  document.body.appendChild(a)
  a.click()
  a.remove()
  URL.revokeObjectURL(url)
}

async function deleteLead(lead) {
  const label = lead.name || lead.phone || `#${lead.id}`
  if (!confirm(`Удалить заявку «${label}»? Это действие нельзя отменить.`)) return

  deletingId.value = lead.id
  deleteError.value = ''
  try {
    const res = await fetch(`/api/admin/leads/${lead.id}`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${token.value}` },
    })
    if (res.status === 401) {
      logout()
      return
    }
    if (res.status === 404) {
      deleteError.value = 'Заявка уже удалена'
      await loadLeads()
      return
    }
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    leads.value = leads.value.filter((l) => l.id !== lead.id)
    total.value = Math.max(0, total.value - 1)
  } catch {
    deleteError.value = 'Не удалось удалить заявку'
  } finally {
    deletingId.value = null
  }
}

async function login() {
  if (!password.value) return
  loggingIn.value = true
  loginError.value = ''
  try {
    const res = await fetch('/api/admin/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ password: password.value }),
    })
    if (res.status === 401) {
      loginError.value = 'Неверный пароль'
      return
    }
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    const data = await res.json()
    token.value = data.token
    sessionStorage.setItem(TOKEN_KEY, data.token)
    password.value = ''
    await loadLeads()
  } catch {
    loginError.value = 'Сервер недоступен, попробуйте позже'
  } finally {
    loggingIn.value = false
  }
}

function logout() {
  token.value = ''
  sessionStorage.removeItem(TOKEN_KEY)
  leads.value = []
  total.value = 0
}

async function loadLeads() {
  if (!token.value) return
  loading.value = true
  loadError.value = ''
  try {
    const res = await fetch('/api/admin/leads?limit=500', {
      headers: { Authorization: `Bearer ${token.value}` },
    })
    if (res.status === 401) {
      logout()
      return
    }
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    const data = await res.json()
    leads.value = data.items
    total.value = data.total
  } catch {
    loadError.value = 'Не удалось загрузить заявки'
  } finally {
    loading.value = false
  }
}

function formatDate(iso) {
  return new Date(iso).toLocaleString('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

function formatBytes(v) {
  const n = Number(v || 0)
  if (!n) return ''
  if (n < 1024) return `${n} Б`
  if (n < 1024 * 1024) return `${Math.round(n / 1024)} КБ`
  return `${(n / (1024 * 1024)).toFixed(1)} МБ`
}

onMounted(loadLeads)
</script>

<template>
  <main class="adm">
    <!-- вход -->
    <div v-if="!token" class="adm-login">
      <form class="adm-login-card" @submit.prevent="login">
        <p class="adm-tag">Грэйдстрой · Админка</p>
        <h1>Вход</h1>
        <input
          v-model="password"
          class="field"
          type="password"
          placeholder="Пароль"
          autocomplete="current-password"
          autofocus
        />
        <p v-if="loginError" class="adm-error">{{ loginError }}</p>
        <button class="btn btn--block" type="submit" :disabled="loggingIn">
          {{ loggingIn ? 'Проверяем…' : 'Войти' }}
        </button>
      </form>
    </div>

    <!-- заявки -->
    <div v-else class="adm-panel">
      <header class="adm-head">
        <div>
          <p class="adm-tag">Грэйдстрой · Админка</p>
          <h1>
            Заявки
            <span class="adm-count">{{ onlyWithFiles ? filteredLeads.length : total }}</span>
            <span v-if="onlyWithFiles" class="adm-count-sub">из {{ total }}</span>
          </h1>
        </div>
        <div class="adm-actions">
          <label class="adm-filter">
            <input v-model="onlyWithFiles" type="checkbox" />
            <span>Только с файлами</span>
            <em v-if="filesCount">{{ filesCount }}</em>
          </label>
          <button class="adm-btn" :disabled="loading" @click="loadLeads">
            {{ loading ? 'Обновляем…' : 'Обновить' }}
          </button>
          <button class="adm-btn adm-btn--ghost" @click="logout">Выйти</button>
        </div>
      </header>

      <p v-if="loadError" class="adm-error">{{ loadError }}</p>
      <p v-if="fileError" class="adm-error">{{ fileError }}</p>
      <p v-if="deleteError" class="adm-error">{{ deleteError }}</p>

      <div v-if="!filteredLeads.length && !loading && !loadError" class="adm-empty">
        {{ onlyWithFiles ? 'Заявок с файлами пока нет' : 'Заявок пока нет' }}
      </div>

      <div v-if="filteredLeads.length" class="adm-table-wrap">
        <table class="adm-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Дата</th>
              <th>Имя</th>
              <th>Телефон</th>
              <th>Чертёж</th>
              <th>Файл</th>
              <th>Комментарий</th>
              <th>Страница</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="lead in filteredLeads" :key="lead.id">
              <td class="adm-num">{{ lead.id }}</td>
              <td class="adm-nowrap">{{ formatDate(lead.created_at) }}</td>
              <td>{{ lead.name || '—' }}</td>
              <td class="adm-nowrap">
                <a :href="`tel:${lead.phone}`" class="adm-phone">{{ lead.phone }}</a>
              </td>
              <td>
                <span class="adm-badge" :class="lead.has_drawing ? 'yes' : 'no'">
                  {{ lead.has_drawing ? 'Есть' : 'Нет' }}
                </span>
              </td>
              <td class="adm-file">
                <template v-if="lead.file_path">
                  <p class="adm-file-name">{{ lead.file_name || 'Файл' }}</p>
                  <small v-if="lead.file_size" class="adm-file-meta">
                    {{ formatBytes(lead.file_size) }}
                  </small>
                  <div class="adm-file-actions">
                    <button type="button" class="adm-file-btn" @click="openFile(lead)">
                      Открыть
                    </button>
                    <button type="button" class="adm-file-btn adm-file-btn--dl" @click="downloadFile(lead)">
                      Скачать
                    </button>
                  </div>
                </template>
                <span v-else>—</span>
              </td>
              <td class="adm-comment">{{ lead.comment || '—' }}</td>
              <td class="adm-nowrap">{{ lead.source || '—' }}</td>
              <td class="adm-row-actions">
                <button
                  type="button"
                  class="adm-del-btn"
                  :disabled="deletingId === lead.id"
                  @click="deleteLead(lead)"
                >
                  {{ deletingId === lead.id ? '…' : 'Удалить' }}
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </main>
</template>

<style scoped>
.adm {
  min-height: 100vh;
  background: var(--bg0);
  color: var(--white);
  padding: 40px 24px;
}

.adm-tag {
  font-family: var(--font-m);
  font-size: 11px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--acc);
  margin-bottom: 10px;
}

.adm h1 {
  font-family: var(--font-d);
  font-size: 24px;
  font-weight: 700;
  text-transform: uppercase;
}

/* ---- вход ---- */
.adm-login {
  min-height: calc(100vh - 80px);
  display: flex;
  align-items: center;
  justify-content: center;
}
.adm-login-card {
  width: 360px;
  max-width: 100%;
  background: var(--bg1);
  border: 1px solid var(--line-d);
  border-top: 3px solid var(--acc);
  border-radius: var(--r);
  padding: 34px 30px;
}
.adm-login-card h1 { margin-bottom: 22px; }
.adm-login-card .field { margin-bottom: 14px; }

/* ---- панель ---- */
.adm-panel {
  max-width: 1400px;
  margin: 0 auto;
}
.adm-head {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 20px;
  flex-wrap: wrap;
  margin-bottom: 28px;
}
.adm-count {
  font-family: var(--font-m);
  font-size: 16px;
  color: var(--acc-hot);
  margin-left: 8px;
}
.adm-count-sub {
  font-family: var(--font-m);
  font-size: 13px;
  color: var(--w-faint);
  margin-left: 6px;
  text-transform: none;
  font-weight: 400;
}

.adm-actions {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.adm-filter {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-family: var(--font-m);
  font-size: 12px;
  color: var(--w-soft);
  cursor: pointer;
  user-select: none;
  padding: 9px 14px;
  border-radius: var(--r-sm);
  box-shadow: inset 0 0 0 1.5px var(--line-d);
}
.adm-filter input { accent-color: var(--acc); width: 15px; height: 15px; }
.adm-filter em {
  font-style: normal;
  font-size: 11px;
  color: var(--acc-hot);
  background: var(--acc-dim);
  padding: 2px 7px;
  border-radius: 999px;
}
.adm-btn {
  font-family: var(--font-m);
  font-size: 12.5px;
  font-weight: 600;
  padding: 11px 20px;
  border-radius: var(--r-sm);
  border: none;
  background: var(--acc);
  color: #fff;
  transition: background 0.2s;
}
.adm-btn:hover { background: var(--acc-hot); }
.adm-btn:disabled { opacity: 0.6; cursor: default; }
.adm-btn--ghost {
  background: transparent;
  color: var(--w-soft);
  box-shadow: inset 0 0 0 1.5px var(--line-d);
}
.adm-btn--ghost:hover { background: rgba(255, 255, 255, 0.06); color: var(--white); }

.adm-error {
  font-size: 13.5px;
  color: var(--acc-hot);
  margin-bottom: 14px;
}

.adm-empty {
  padding: 60px 20px;
  text-align: center;
  color: var(--w-faint);
  font-family: var(--font-m);
  font-size: 14px;
  border: 1.5px dashed var(--line-d);
  border-radius: var(--r);
}

/* ---- таблица ---- */
.adm-table-wrap {
  overflow-x: auto;
  border: 1px solid var(--line-d);
  border-radius: var(--r);
  background: var(--bg1);
}
.adm-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13.5px;
}
.adm-table th {
  font-family: var(--font-m);
  font-size: 10.5px;
  font-weight: 600;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--w-faint);
  text-align: left;
  padding: 14px 16px;
  border-bottom: 1px solid var(--line-d);
  white-space: nowrap;
}
.adm-table td {
  padding: 13px 16px;
  border-bottom: 1px solid var(--line-d);
  vertical-align: top;
  color: var(--w-soft);
}
.adm-table tbody tr:last-child td { border-bottom: none; }
.adm-table tbody tr:hover td { background: rgba(255, 255, 255, 0.025); }

.adm-num { font-family: var(--font-m); color: var(--w-faint); }
.adm-nowrap { white-space: nowrap; }
.adm-phone {
  font-family: var(--font-m);
  color: var(--white);
  font-weight: 600;
}
.adm-phone:hover { color: var(--acc-hot); }

.adm-badge {
  display: inline-block;
  font-family: var(--font-m);
  font-size: 10.5px;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  padding: 4px 10px;
  border-radius: 999px;
}
.adm-badge.yes { background: rgba(53, 201, 126, 0.14); color: var(--ok); }
.adm-badge.no { background: rgba(255, 255, 255, 0.07); color: var(--w-faint); }

.adm-file, .adm-comment {
  max-width: 260px;
  overflow-wrap: break-word;
}

.adm-file-name {
  font-size: 13px;
  color: var(--white);
  margin-bottom: 4px;
  word-break: break-word;
}
.adm-file-meta {
  display: block;
  margin-bottom: 8px;
  color: var(--w-faint);
  font-family: var(--font-m);
  font-size: 11px;
}
.adm-file-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}
.adm-file-btn {
  font-family: var(--font-m);
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  padding: 6px 10px;
  border-radius: 6px;
  color: var(--acc-hot);
  background: rgba(255, 90, 31, 0.12);
  border: none;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
}
.adm-file-btn:hover {
  background: var(--acc);
  color: #fff;
}

.adm-row-actions { white-space: nowrap; }
.adm-del-btn {
  font-family: var(--font-m);
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  padding: 6px 10px;
  border-radius: 6px;
  color: #ff8a8a;
  background: rgba(255, 90, 90, 0.1);
  border: none;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
}
.adm-del-btn:hover:not(:disabled) {
  background: rgba(255, 90, 90, 0.22);
  color: #ffb4b4;
}
.adm-del-btn:disabled {
  opacity: 0.5;
  cursor: default;
}
</style>
