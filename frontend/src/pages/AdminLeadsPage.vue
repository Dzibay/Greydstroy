<script setup>
import { ref, onMounted } from 'vue'

const TOKEN_KEY = 'gs_admin_token'

const token = ref(sessionStorage.getItem(TOKEN_KEY) || '')
const password = ref('')
const loginError = ref('')
const loggingIn = ref(false)

const leads = ref([])
const total = ref(0)
const loading = ref(false)
const loadError = ref('')

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
          <h1>Заявки <span class="adm-count">{{ total }}</span></h1>
        </div>
        <div class="adm-actions">
          <button class="adm-btn" :disabled="loading" @click="loadLeads">
            {{ loading ? 'Обновляем…' : 'Обновить' }}
          </button>
          <button class="adm-btn adm-btn--ghost" @click="logout">Выйти</button>
        </div>
      </header>

      <p v-if="loadError" class="adm-error">{{ loadError }}</p>

      <div v-if="!leads.length && !loading && !loadError" class="adm-empty">
        Заявок пока нет
      </div>

      <div v-if="leads.length" class="adm-table-wrap">
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
            </tr>
          </thead>
          <tbody>
            <tr v-for="lead in leads" :key="lead.id">
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
              <td class="adm-file">{{ lead.file_name || '—' }}</td>
              <td class="adm-comment">{{ lead.comment || '—' }}</td>
              <td class="adm-nowrap">{{ lead.source || '—' }}</td>
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

.adm-actions { display: flex; gap: 10px; }
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
</style>
