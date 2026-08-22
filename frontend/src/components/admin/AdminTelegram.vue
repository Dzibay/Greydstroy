<script setup>
import { onMounted, ref } from 'vue'

const props = defineProps({
  token: { type: String, required: true },
})
const emit = defineEmits(['unauthorized'])

const loading = ref(false)
const loadError = ref('')
const actionError = ref('')
const configured = ref(false)
const bot = ref({ username: '', name: '', ok: false })
const joinCode = ref('')
const recipients = ref([])
const pending = ref([])
const addingId = ref('')
const testing = ref(false)
const testOk = ref('')
const manualId = ref('')
const manualName = ref('')

async function api(path, options = {}) {
  const res = await fetch(path, {
    ...options,
    headers: {
      Authorization: `Bearer ${props.token}`,
      ...(options.body ? { 'Content-Type': 'application/json' } : {}),
      ...(options.headers || {}),
    },
  })
  if (res.status === 401) {
    emit('unauthorized')
    throw new Error('unauthorized')
  }
  return res
}

async function load() {
  loading.value = true
  loadError.value = ''
  actionError.value = ''
  try {
    const res = await api('/api/admin/telegram')
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    const data = await res.json()
    configured.value = data.configured
    bot.value = data.bot || {}
    joinCode.value = data.join_code || ''
    recipients.value = data.recipients || []
    pending.value = data.pending || []
  } catch (err) {
    if (err.message !== 'unauthorized') loadError.value = 'Не удалось загрузить Telegram'
  } finally {
    loading.value = false
  }
}

async function addPerson(chatId, name = '', username = '') {
  addingId.value = chatId
  actionError.value = ''
  testOk.value = ''
  try {
    const res = await api('/api/admin/telegram/recipients', {
      method: 'POST',
      body: JSON.stringify({ chat_id: chatId, name, username }),
    })
    if (!res.ok) throw new Error('add')
    manualId.value = ''
    manualName.value = ''
    await load()
  } catch (err) {
    if (err.message !== 'unauthorized') actionError.value = 'Не удалось добавить получателя'
  } finally {
    addingId.value = ''
  }
}

async function toggle(person) {
  actionError.value = ''
  try {
    const res = await api(`/api/admin/telegram/recipients/${person.id}`, {
      method: 'PATCH',
      body: JSON.stringify({ enabled: !person.enabled }),
    })
    if (!res.ok) throw new Error('toggle')
    person.enabled = !person.enabled
  } catch (err) {
    if (err.message !== 'unauthorized') actionError.value = 'Не удалось изменить получателя'
  }
}

async function removePerson(person) {
  if (!confirm(`Убрать «${person.name || person.chat_id}» из рассылки?`)) return
  actionError.value = ''
  try {
    const res = await api(`/api/admin/telegram/recipients/${person.id}`, { method: 'DELETE' })
    if (!res.ok) throw new Error('del')
    recipients.value = recipients.value.filter((r) => r.id !== person.id)
  } catch (err) {
    if (err.message !== 'unauthorized') actionError.value = 'Не удалось удалить'
  }
}

async function sendTest() {
  testing.value = true
  actionError.value = ''
  testOk.value = ''
  try {
    const res = await api('/api/admin/telegram/test', { method: 'POST' })
    const data = await res.json().catch(() => ({}))
    if (!res.ok) {
      actionError.value = data.detail || 'Тест не отправился'
      return
    }
    testOk.value = `Отправлено: ${data.sent} из ${data.total}`
  } catch (err) {
    if (err.message !== 'unauthorized') actionError.value = 'Тест не отправился'
  } finally {
    testing.value = false
  }
}

const botLink = () => (bot.value.username ? `https://t.me/${bot.value.username}` : '')

onMounted(load)
</script>

<template>
  <section class="tg">
    <p v-if="loadError" class="adm-error">{{ loadError }}</p>
    <p v-if="actionError" class="adm-error">{{ actionError }}</p>
    <p v-if="testOk" class="tg-ok">{{ testOk }}</p>

    <div v-if="!configured" class="tg-card">
      <h2>Бот ещё не подключён</h2>
      <ol class="tg-steps">
        <li>В Telegram откройте @BotFather → /newbot и скопируйте токен.</li>
        <li>Вставьте его в <code>backend/.env</code> как <code>TELEGRAM_BOT_TOKEN</code>.</li>
        <li>Перезапустите бэкенд и напишите боту «Старт».</li>
        <li>Вернитесь сюда — вы сами появитесь в списке ожидающих.</li>
      </ol>
    </div>

    <template v-else>
      <div class="tg-card">
        <header class="tg-card-h">
          <div>
            <h2>Как добавить человека</h2>
            <p v-if="bot.username">
              Пусть откроет
              <a :href="botLink()" target="_blank" rel="noopener">@{{ bot.username }}</a>
              и нажмёт <b>Start</b>. Затем обновите список — он появится ниже.
            </p>
            <p v-else>Напишите боту Start и нажмите «Обновить».</p>
            <p v-if="joinCode">
              Или сразу: человек пишет боту <code>/join {{ joinCode }}</code> — попадёт в рассылку сам.
            </p>
          </div>
          <div class="tg-actions">
            <button type="button" class="adm-btn" :disabled="loading" @click="load">
              {{ loading ? 'Обновляем…' : 'Обновить' }}
            </button>
            <button
              type="button"
              class="adm-btn adm-btn--ghost"
              :disabled="testing || !recipients.length"
              @click="sendTest"
            >
              {{ testing ? 'Отправляем…' : 'Тестовое сообщение' }}
            </button>
          </div>
        </header>
      </div>

      <div v-if="pending.length" class="tg-card">
        <h2>Написали боту — добавьте в рассылку</h2>
        <ul class="tg-list">
          <li v-for="p in pending" :key="p.chat_id">
            <div>
              <strong>{{ p.name }}</strong>
              <small>
                <span v-if="p.username">@{{ p.username }} · </span>{{ p.chat_id }}
              </small>
            </div>
            <button
              type="button"
              class="adm-btn"
              :disabled="addingId === p.chat_id"
              @click="addPerson(p.chat_id, p.name, p.username)"
            >
              {{ addingId === p.chat_id ? '…' : 'Добавить' }}
            </button>
          </li>
        </ul>
      </div>

      <div class="tg-card">
        <h2>Получают заявки <em>{{ recipients.filter((r) => r.enabled).length }}</em></h2>
        <ul v-if="recipients.length" class="tg-list">
          <li v-for="r in recipients" :key="r.id">
            <div>
              <strong :class="{ off: !r.enabled }">{{ r.name || r.chat_id }}</strong>
              <small>
                <span v-if="r.username">@{{ r.username }} · </span>{{ r.chat_id }}
                <span v-if="!r.enabled"> · выключен</span>
              </small>
            </div>
            <div class="tg-row-actions">
              <button type="button" class="adm-file-btn" @click="toggle(r)">
                {{ r.enabled ? 'Пауза' : 'Включить' }}
              </button>
              <button type="button" class="adm-del-btn" @click="removePerson(r)">Убрать</button>
            </div>
          </li>
        </ul>
        <p v-else class="tg-empty">Пока никого нет — напишите боту Start и нажмите «Обновить».</p>

        <form class="tg-manual" @submit.prevent="addPerson(manualId, manualName)">
          <p>Или вставьте chat id вручную</p>
          <div class="tg-manual-row">
            <input v-model.trim="manualId" class="field" placeholder="Chat ID" />
            <input v-model.trim="manualName" class="field" placeholder="Имя (необязательно)" />
            <button class="adm-btn" type="submit" :disabled="!manualId || addingId === manualId">
              Добавить
            </button>
          </div>
        </form>
      </div>
    </template>
  </section>
</template>

<style scoped>
.tg { display: flex; flex-direction: column; gap: 18px; }
.tg-card {
  background: var(--bg1);
  border: 1px solid var(--line-d);
  border-radius: var(--r);
  padding: 22px 24px;
}
.tg-card h2 {
  font-family: var(--font-d);
  font-size: 15px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  margin-bottom: 10px;
}
.tg-card h2 em {
  font-style: normal;
  color: var(--acc-hot);
  margin-left: 6px;
}
.tg-card-h {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  align-items: flex-start;
  flex-wrap: wrap;
}
.tg-card p { color: var(--w-soft); font-size: 14.5px; line-height: 1.5; }
.tg-card a { color: var(--acc-hot); }
.tg-card code {
  font-family: var(--font-m);
  font-size: 12.5px;
  background: rgba(255, 255, 255, 0.06);
  padding: 1px 6px;
  border-radius: 6px;
}
.tg-actions { display: flex; gap: 10px; flex-wrap: wrap; }
.tg-steps {
  list-style: decimal;
  padding-left: 20px;
  color: var(--w-soft);
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.tg-list { display: flex; flex-direction: column; }
.tg-list li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  padding: 12px 0;
  border-top: 1px solid var(--line-d);
}
.tg-list li:first-child { border-top: none; }
.tg-list strong { color: var(--white); display: block; }
.tg-list strong.off { color: var(--w-faint); }
.tg-list small { color: var(--w-faint); font-size: 12.5px; }
.tg-row-actions { display: flex; gap: 8px; }
.tg-empty { color: var(--w-faint); padding: 12px 0; }
.tg-ok { color: var(--ok); font-size: 13.5px; }
.tg-manual { margin-top: 18px; padding-top: 16px; border-top: 1px dashed var(--line-d); }
.tg-manual p { margin-bottom: 10px; font-size: 13px; }
.tg-manual-row {
  display: grid;
  grid-template-columns: 1fr 1fr auto;
  gap: 10px;
}
@media (max-width: 700px) {
  .tg { gap: 12px; }
  .tg-card { padding: 14px 12px; }
  .tg-card h2 { font-size: 13px; }
  .tg-card p, .tg-steps { font-size: 13px; }
  .tg-list li {
    flex-direction: column;
    align-items: stretch;
    gap: 10px;
  }
  .tg-row-actions { width: 100%; }
  .tg-row-actions button { flex: 1; }
  .tg-manual-row { grid-template-columns: 1fr; }
  .tg-actions { width: 100%; }
  .tg-actions .adm-btn { flex: 1; }
}

.adm-error { font-size: 13.5px; color: var(--acc-hot); }
.adm-btn {
  font-family: var(--font-m);
  font-size: 12.5px;
  font-weight: 600;
  padding: 11px 20px;
  border-radius: var(--r-sm);
  border: none;
  background: var(--acc);
  color: #fff;
}
.adm-btn:hover { background: var(--acc-hot); }
.adm-btn:disabled { opacity: 0.6; cursor: default; }
.adm-btn--ghost {
  background: transparent;
  color: var(--w-soft);
  box-shadow: inset 0 0 0 1.5px var(--line-d);
}
.adm-btn--ghost:hover { background: rgba(255, 255, 255, 0.06); color: var(--white); }
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
}
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
}
.field { width: 100%; }
</style>
