<script setup>
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
import { pageLabel, pagePath } from '../../utils/pageLabel'

const props = defineProps({
  token: { type: String, required: true },
})

const emit = defineEmits(['unauthorized'])

const PERIODS = [
  { id: 1, label: 'Сегодня' },
  { id: 7, label: '7 дней' },
  { id: 30, label: '30 дней' },
  { id: 90, label: '90 дней' },
]

const CLICK_NAMES = {
  'calc-header': 'Калькулятор · шапка',
  'calc-hero': 'Калькулятор · главный экран',
  'calc-footer': 'Калькулятор · подвал',
  'calc-widget': 'Калькулятор · виджет связи',
  'calc-mode-details': 'Калькулятор · режим «детали»',
  'calc-mode-object': 'Калькулятор · режим «объект»',
  'calc-get-quote': 'Калькулятор · точный расчёт',
  'tel-header': 'Шапка',
  'tel-banner': 'Баннер на главной',
  'tel-widget': 'Виджет связи',
  'tel-footer': 'Подвал',
  'tel-contacts': 'Страница контактов',
  'tel-proizvodstvo': 'Страница производства',
  'tel-requisites': 'Страница реквизитов',
  'tel-form-error': 'Ошибка отправки заявки',
  'tel-privacy': 'Политика ПДн',
  'tel-checklist': 'Чек-лист ТЗ',
  'mail-footer': 'Подвал',
  'mail-contacts': 'Страница контактов',
  'mail-requisites': 'Страница реквизитов',
  'mail-widget': 'Виджет связи',
  'mail-privacy': 'Политика ПДн',
  'mail-checklist': 'Чек-лист ТЗ',
  'expert-fab': 'Виджет «связь с инженером»',
    'lead-submit': 'Отправка заявки',
    checklist: 'Чек-лист подготовки ТЗ',
}

const EVENT_NAMES = {
  pageview: 'Просмотр',
  click: 'Клик',
  outbound: 'Внешняя ссылка',
  tel: 'Звонок',
  mail: 'Почта',
  form_start: 'Форма: начало',
  form_submit: 'Форма: заявка',
  form_error: 'Форма: ошибка',
  calc: 'Калькулятор',
}

const FEED_FILTERS = [
  { id: 'all', label: 'Все' },
  { id: 'calc', label: 'Калькулятор' },
  { id: 'form', label: 'Формы' },
  { id: 'click', label: 'Клики' },
  { id: 'contact', label: 'Звонки и почта' },
]

const DEVICE_NAMES = {
  mobile: 'Телефон',
  tablet: 'Планшет',
  desktop: 'Компьютер',
  'неизвестно': 'Неизвестно',
}

const MAIL_PROVIDERS = {
  gmail: 'Gmail',
  yandex: 'Яндекс.Почта',
  copy: 'Скопировали адрес',
  mailto: 'Программа на компьютере',
  unknown: 'Не указано',
}

const TEL_SPOTS = [
  'tel-header',
  'tel-banner',
  'tel-widget',
  'tel-footer',
  'tel-contacts',
  'tel-proizvodstvo',
  'tel-requisites',
  'tel-form-error',
  'tel-privacy',
  'tel-checklist',
]

const MAIL_SPOTS = [
  'mail-footer',
  'mail-contacts',
  'mail-requisites',
  'mail-widget',
  'mail-privacy',
  'mail-checklist',
]

function mergeSpots(known, rows) {
  const map = new Map(rows.map((r) => [r.label, r.count]))
  const extra = rows.filter((r) => !known.includes(r.label))
  return [
    ...known.map((label) => ({ label, count: map.get(label) || 0 })),
    ...extra.map((r) => ({ label: r.label, count: r.count })),
  ]
}

const days = ref(7)
const loading = ref(false)
const loadError = ref('')
const data = ref(null)
const feedFilter = ref('all')
let timer = 0

const kpis = computed(() => data.value?.kpis || {})
const series = computed(() => data.value?.timeseries || [])
const maxVisitors = computed(() => Math.max(1, ...series.value.map((r) => r.visitors)))
const maxPageviews = computed(() => Math.max(1, ...series.value.map((r) => r.pageviews)))
const funnel = computed(() => data.value?.funnel || [])
const funnelMax = computed(() => Math.max(1, funnel.value[0]?.count || 1))
const calc = computed(() => data.value?.calculator || {})
const calcModes = computed(() => calc.value.modes || [])
const calcModeTotal = computed(() => Math.max(1, calcModes.value.reduce((s, m) => s + m.sessions, 0)))
const contactPlaces = computed(() => data.value?.contact?.places || [])
const telPlaces = computed(() => mergeSpots(TEL_SPOTS, contactPlaces.value.filter((p) => p.kind === 'tel')))
const mailPlaces = computed(() => mergeSpots(MAIL_SPOTS, contactPlaces.value.filter((p) => p.kind === 'mail')))
const mailProviders = computed(() => data.value?.contact?.mail_providers || [])
const contactRows = computed(() => data.value?.contact?.rows || [])

const filteredRecent = computed(() => {
  const rows = data.value?.recent || []
  if (feedFilter.value === 'calc') return rows.filter((e) => e.event === 'calc')
  if (feedFilter.value === 'form') {
    return rows.filter((e) => e.event.startsWith('form_'))
  }
  if (feedFilter.value === 'click') {
    return rows.filter((e) => ['click', 'outbound', 'tel', 'mail'].includes(e.event))
  }
  if (feedFilter.value === 'contact') {
    return rows.filter((e) => {
      if (e.event === 'tel' || e.event === 'mail') return true
      const href = e.href || ''
      return e.event === 'outbound' && (href.startsWith('tel:') || href.startsWith('mailto:'))
    })
  }
  return rows
})

const hourBars = computed(() => {
  const map = new Map((data.value?.hours || []).map((h) => [h.hour, h.sessions]))
  const max = Math.max(1, ...[...map.values(), 0])
  return Array.from({ length: 24 }, (_, hour) => ({
    hour,
    sessions: map.get(hour) || 0,
    max,
  }))
})

function pageName(path) {
  return pageLabel(path)
}

function clickName(label) {
  return CLICK_NAMES[label] || label || '—'
}

function providerName(id) {
  return MAIL_PROVIDERS[id] || id || '—'
}

function feedLabel(ev) {
  const name = clickName(ev.label)
  const base = name !== '—' ? name : ev.href || ''
  if (ev.event === 'mail' && ev.provider) {
    return `${base} · ${providerName(ev.provider)}`
  }
  return base
}

function sourceName(src) {
  if (!src || src === 'прямой заход') return 'Прямой заход'
  try {
    const u = src.startsWith('http') ? new URL(src) : null
    if (u) return u.host.replace(/^www\./, '')
  } catch {
    /* ignore */
  }
  return src
}

function fmtNum(n) {
  return Number(n || 0).toLocaleString('ru-RU')
}

function fmtPct(n) {
  return `${((Number(n) || 0) * 100).toFixed(1)}%`
}

function fmtDur(sec) {
  const s = Math.round(Number(sec) || 0)
  if (s < 1) return '—'
  if (s < 60) return `${s} с`
  const m = Math.floor(s / 60)
  const r = s % 60
  return r ? `${m} мин ${r} с` : `${m} мин`
}

function fmtTick(iso, byHour) {
  const d = new Date(iso)
  if (Number.isNaN(d.getTime())) return ''
  if (byHour) {
    return d.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })
  }
  return d.toLocaleDateString('ru-RU', { day: '2-digit', month: '2-digit' })
}

function fmtTime(iso) {
  return new Date(iso).toLocaleString('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  })
}

async function load() {
  if (!props.token) return
  loading.value = true
  loadError.value = ''
  try {
    const res = await fetch(`/api/admin/analytics?days=${days.value}`, {
      headers: { Authorization: `Bearer ${props.token}` },
    })
    if (res.status === 401) {
      emit('unauthorized')
      return
    }
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    data.value = await res.json()
  } catch {
    loadError.value = 'Не удалось загрузить статистику'
  } finally {
    loading.value = false
  }
}

watch(days, load)
onMounted(() => {
  load()
  timer = window.setInterval(load, 60_000)
})
onUnmounted(() => {
  if (timer) clearInterval(timer)
})
</script>

<template>
  <section class="st">
    <div class="st-toolbar">
      <div class="st-periods">
        <button
          v-for="p in PERIODS"
          :key="p.id"
          type="button"
          class="st-chip"
          :class="{ on: days === p.id }"
          @click="days = p.id"
        >
          {{ p.label }}
        </button>
      </div>
      <button class="st-refresh" type="button" :disabled="loading" @click="load">
        {{ loading ? 'Обновляем…' : 'Обновить' }}
      </button>
    </div>

    <p v-if="loadError" class="st-error">{{ loadError }}</p>

    <div v-if="kpis.live" class="st-live">
      <span class="st-live-dot"></span>
      Сейчас на сайте: {{ fmtNum(kpis.live) }}
    </div>

    <div class="st-kpis">
      <article class="st-kpi">
        <p class="st-kpi-label">Посетители</p>
        <p class="st-kpi-val">{{ fmtNum(kpis.visitors) }}</p>
        <p class="st-kpi-sub">уникальные браузеры</p>
      </article>
      <article class="st-kpi">
        <p class="st-kpi-label">Сессии</p>
        <p class="st-kpi-val">{{ fmtNum(kpis.sessions) }}</p>
        <p class="st-kpi-sub">ср. {{ fmtDur(kpis.avg_session_sec) }} · {{ (kpis.pages_per_session || 0).toFixed(1) }} стр.</p>
      </article>
      <article class="st-kpi">
        <p class="st-kpi-label">Просмотры</p>
        <p class="st-kpi-val">{{ fmtNum(kpis.pageviews) }}</p>
        <p class="st-kpi-sub">отказы {{ fmtPct(kpis.bounce_rate) }}</p>
      </article>
      <article class="st-kpi st-kpi--acc">
        <p class="st-kpi-label">Заявки</p>
        <p class="st-kpi-val">{{ fmtNum(kpis.leads) }}</p>
        <p class="st-kpi-sub">конверсия {{ fmtPct(kpis.conversion) }}</p>
      </article>
      <article class="st-kpi">
        <p class="st-kpi-label">Звонки</p>
        <p class="st-kpi-val">{{ fmtNum(kpis.tel_clicks) }}</p>
        <p class="st-kpi-sub">нажатия на телефон</p>
      </article>
      <article class="st-kpi">
        <p class="st-kpi-label">Почта</p>
        <p class="st-kpi-val">{{ fmtNum(kpis.mail_clicks) }}</p>
        <p class="st-kpi-sub">открыли письмо или скопировали</p>
      </article>
      <article class="st-kpi">
        <p class="st-kpi-label">Клики</p>
        <p class="st-kpi-val">{{ fmtNum(kpis.clicks) }}</p>
        <p class="st-kpi-sub">все нажатия на сайте</p>
      </article>
      <article class="st-kpi">
        <p class="st-kpi-label">Начали форму</p>
        <p class="st-kpi-val">{{ fmtNum(kpis.form_starts) }}</p>
        <p class="st-kpi-sub">ошибки {{ fmtNum(kpis.form_errors) }} · дожали {{ fmtNum(kpis.leads) }}</p>
      </article>
    </div>

    <div class="st-card st-card--contact">
      <header class="st-card-h">
        <h2>Звонки и почта</h2>
        <p>каждое нажатие: откуда и чем открыли письмо</p>
      </header>

      <div class="st-contact-kpis">
        <div>
          <em>Звонки</em>
          <strong>{{ fmtNum(kpis.tel_clicks) }}</strong>
          <span>нажатия на номер</span>
        </div>
        <div>
          <em>Почта</em>
          <strong>{{ fmtNum(kpis.mail_clicks) }}</strong>
          <span>выбрали Gmail, Яндекс или скопировали</span>
        </div>
      </div>

      <ul v-if="mailProviders.length" class="st-providers">
        <li v-for="p in mailProviders" :key="p.provider">
          <span>{{ providerName(p.provider) }}</span>
          <strong>{{ fmtNum(p.count) }}</strong>
        </li>
      </ul>

      <div class="st-contact">
        <div>
          <h3 class="st-subh">Откуда звонили</h3>
          <table class="st-table">
            <thead>
              <tr><th>Место</th><th></th></tr>
            </thead>
            <tbody>
              <tr v-for="p in telPlaces" :key="'tel-' + p.label" :class="{ 'is-zero': !p.count }">
                <td>{{ clickName(p.label) }}</td>
                <td>{{ fmtNum(p.count) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div>
          <h3 class="st-subh">Откуда писали</h3>
          <table class="st-table">
            <thead>
              <tr><th>Место</th><th></th></tr>
            </thead>
            <tbody>
              <tr v-for="p in mailPlaces" :key="'mail-' + p.label" :class="{ 'is-zero': !p.count }">
                <td>{{ clickName(p.label) }}</td>
                <td>{{ fmtNum(p.count) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <h3 class="st-subh st-subh--mt">По страницам</h3>
      <table v-if="contactRows.length" class="st-table">
        <thead>
          <tr>
            <th>Действие</th>
            <th>Место</th>
            <th>Страница</th>
            <th>Чем открыли</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(r, i) in contactRows" :key="r.kind + r.label + r.path + r.provider + i">
            <td>{{ r.kind === 'tel' ? 'Звонок' : 'Почта' }}</td>
            <td>{{ clickName(r.label) }}</td>
            <td>{{ pageName(r.path) }}</td>
            <td>{{ r.provider ? providerName(r.provider) : '—' }}</td>
            <td>{{ fmtNum(r.count) }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else class="st-empty st-empty--sm">Пока нет нажатий на телефон и почту за период</p>
    </div>

    <div class="st-card">
      <header class="st-card-h">
        <h2>Трафик</h2>
        <p>{{ data?.period?.by_hour ? 'по часам, МСК' : 'по дням, МСК' }}</p>
      </header>
      <div v-if="series.length" class="st-chart">
        <div
          v-for="(row, i) in series"
          :key="row.t + i"
          class="st-col"
          :title="`${fmtTick(row.t, data?.period?.by_hour)} · ${row.visitors} пос. · ${row.pageviews} просм. · ${row.leads} заявок`"
        >
          <div class="st-col-bars">
            <div
              class="st-bar st-bar--pv"
              :style="{ height: `${(row.pageviews / maxPageviews) * 100}%` }"
            ></div>
            <div class="st-bar" :style="{ height: `${(row.visitors / maxVisitors) * 100}%` }"></div>
          </div>
          <span v-if="row.leads" class="st-col-lead">{{ row.leads }}</span>
          <em>{{ fmtTick(row.t, data?.period?.by_hour) }}</em>
        </div>
      </div>
      <p v-else class="st-empty">Пока нет визитов за выбранный период</p>
      <p v-if="series.length" class="st-legend">
        <i class="st-lg st-lg--v"></i> посетители
        <i class="st-lg st-lg--p"></i> просмотры
        <span>цифра сверху — заявки</span>
      </p>
    </div>

    <div class="st-grid">
      <div class="st-card">
        <header class="st-card-h">
          <h2>Воронка</h2>
          <p>сессии, дошедшие до шага</p>
        </header>
        <ul class="st-funnel">
          <li v-for="step in funnel" :key="step.step">
            <div class="st-funnel-row">
              <span>{{ step.label }}</span>
              <strong>{{ fmtNum(step.count) }}</strong>
            </div>
            <div class="st-funnel-track">
              <div
                class="st-funnel-fill"
                :style="{ width: `${(step.count / funnelMax) * 100}%` }"
              ></div>
            </div>
          </li>
        </ul>
      </div>

      <div class="st-card">
        <header class="st-card-h">
          <h2>Активность по часам</h2>
          <p>когда заходят, МСК</p>
        </header>
        <div class="st-hours">
          <div
            v-for="h in hourBars"
            :key="h.hour"
            class="st-hour"
            :title="`${String(h.hour).padStart(2, '0')}:00 · ${h.sessions} сессий`"
          >
            <div
              class="st-hour-bar"
              :style="{ height: `${(h.sessions / h.max) * 100}%` }"
            ></div>
            <span v-if="h.hour % 3 === 0">{{ h.hour }}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="st-card">
      <header class="st-card-h">
        <h2>Калькулятор</h2>
        <p>что считают посетители</p>
      </header>
      <div class="st-calc-kpis">
        <div>
          <em>Заходили</em>
          <strong>{{ fmtNum(calc.sessions) }}</strong>
          <span>сессий · {{ fmtNum(calc.visitors) }} чел.</span>
        </div>
        <div>
          <em>Время на странице</em>
          <strong>{{ fmtDur(calc.avg_sec) }}</strong>
          <span>среднее</span>
        </div>
        <div>
          <em>Начали форму</em>
          <strong>{{ fmtNum(calc.form_starts) }}</strong>
          <span>с калькулятора</span>
        </div>
        <div>
          <em>Заявки</em>
          <strong>{{ fmtNum(calc.leads) }}</strong>
          <span>{{ fmtPct(calc.sessions ? calc.leads / calc.sessions : 0) }} сессий</span>
        </div>
      </div>

      <div class="st-modes">
        <div
          v-for="m in calcModes"
          :key="m.id"
          class="st-mode"
          :class="'st-mode--' + m.id"
        >
          <div class="st-mode-h">
            <strong>{{ m.label }}</strong>
            <span>{{ fmtPct(m.share) }}</span>
          </div>
          <div class="st-funnel-track">
            <div
              class="st-funnel-fill"
              :style="{ width: `${(m.sessions / calcModeTotal) * 100}%` }"
            ></div>
          </div>
          <p class="st-mode-meta">{{ fmtNum(m.sessions) }} сессий · {{ fmtNum(m.events) }} выборов</p>
        </div>
      </div>

      <div class="st-grid st-grid--calc">
        <div>
          <h3 class="st-subh">Тип изделия</h3>
          <table v-if="calc.types?.length" class="st-table">
            <thead>
              <tr><th>Что считают</th><th>Сессии</th></tr>
            </thead>
            <tbody>
              <tr v-for="t in calc.types" :key="'type-' + t.id">
                <td>{{ t.label || t.id }}</td>
                <td>{{ fmtNum(t.sessions) }}</td>
              </tr>
            </tbody>
          </table>
          <p v-else class="st-empty st-empty--sm">Пока нет выборов в режиме «детали»</p>
        </div>
        <div>
          <h3 class="st-subh">Тип объекта</h3>
          <table v-if="calc.kinds?.length" class="st-table">
            <thead>
              <tr><th>Что считают</th><th>Сессии</th></tr>
            </thead>
            <tbody>
              <tr v-for="t in calc.kinds" :key="'kind-' + t.id">
                <td>{{ t.label || t.id }}</td>
                <td>{{ fmtNum(t.sessions) }}</td>
              </tr>
            </tbody>
          </table>
          <p v-else class="st-empty st-empty--sm">Пока нет выборов в режиме «объект»</p>
        </div>
        <div>
          <h3 class="st-subh">Покрытие</h3>
          <table v-if="calc.coatings?.length" class="st-table">
            <thead>
              <tr><th></th><th>Сессии</th></tr>
            </thead>
            <tbody>
              <tr v-for="t in calc.coatings" :key="'coat-' + t.id">
                <td>{{ t.label || t.id }}</td>
                <td>{{ fmtNum(t.sessions) }}</td>
              </tr>
            </tbody>
          </table>
          <p v-else class="st-empty st-empty--sm">Нет данных</p>
        </div>
        <div>
          <h3 class="st-subh">Доставка</h3>
          <table v-if="calc.deliveries?.length" class="st-table">
            <thead>
              <tr><th></th><th>Сессии</th></tr>
            </thead>
            <tbody>
              <tr v-for="t in calc.deliveries" :key="'del-' + t.id">
                <td>{{ t.label || t.id }}</td>
                <td>{{ fmtNum(t.sessions) }}</td>
              </tr>
            </tbody>
          </table>
          <p v-else class="st-empty st-empty--sm">Нет данных</p>
        </div>
      </div>
      <div v-if="calc.regions?.length" class="st-regions">
        <h3 class="st-subh">Регионы</h3>
        <ul>
          <li v-for="r in calc.regions" :key="r.id">
            <span>{{ r.label || r.id }}</span>
            <strong>{{ fmtNum(r.sessions) }}</strong>
          </li>
        </ul>
      </div>
    </div>

    <div class="st-grid">
      <div class="st-card">
        <header class="st-card-h">
          <h2>Страницы</h2>
          <p>куда заходят</p>
        </header>
        <table v-if="data?.pages?.length" class="st-table">
          <thead>
            <tr>
              <th>Страница</th>
              <th>Просмотры</th>
              <th>Люди</th>
              <th>Время</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in data.pages" :key="p.path">
              <td>
                <strong>{{ pageName(p.path) }}</strong>
                <small class="st-path">{{ pagePath(p.path) }}</small>
              </td>
              <td>{{ fmtNum(p.views) }}</td>
              <td>{{ fmtNum(p.visitors) }}</td>
              <td>{{ fmtDur(p.avg_sec) }}</td>
            </tr>
          </tbody>
        </table>
        <p v-else class="st-empty">Нет просмотров</p>
      </div>

      <div class="st-card">
        <header class="st-card-h">
          <h2>Клики</h2>
          <p>что нажимают</p>
        </header>
        <table v-if="data?.clicks?.length" class="st-table">
          <thead>
            <tr>
              <th>Действие</th>
              <th>Где</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="c in data.clicks" :key="c.label + c.path + c.event">
              <td>
                <strong>{{ clickName(c.label) }}</strong>
                <small v-if="c.event === 'outbound'">внешняя</small>
                <small v-else-if="c.event === 'tel'">звонок</small>
                <small v-else-if="c.event === 'mail'">почта</small>
              </td>
              <td>{{ pageName(c.path) }}</td>
              <td>{{ fmtNum(c.count) }}</td>
            </tr>
          </tbody>
        </table>
        <p v-else class="st-empty">Кликов пока нет</p>
      </div>
    </div>

    <div class="st-grid st-grid--3">
      <div class="st-card">
        <header class="st-card-h">
          <h2>Источники</h2>
          <p>откуда пришли</p>
        </header>
        <table v-if="data?.sources?.length" class="st-table">
          <thead>
            <tr>
              <th>Источник</th>
              <th>Люди</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="s in data.sources" :key="s.source">
              <td>{{ sourceName(s.source) }}</td>
              <td>{{ fmtNum(s.visitors) }}</td>
            </tr>
          </tbody>
        </table>
        <p v-else class="st-empty">Нет данных</p>
      </div>

      <div class="st-card">
        <header class="st-card-h">
          <h2>Кампании UTM</h2>
          <p>метки в ссылках</p>
        </header>
        <table v-if="data?.campaigns?.length" class="st-table">
          <thead>
            <tr>
              <th>Метка</th>
              <th>Люди</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="c in data.campaigns" :key="c.utm_source + c.utm_campaign">
              <td>
                <strong>{{ c.utm_source }}</strong>
                <small>{{ [c.utm_medium, c.utm_campaign].filter(Boolean).join(' · ') || '—' }}</small>
              </td>
              <td>{{ fmtNum(c.visitors) }}</td>
            </tr>
          </tbody>
        </table>
        <p v-else class="st-empty">UTM-меток пока нет</p>
      </div>

      <div class="st-card">
        <header class="st-card-h">
          <h2>Устройства</h2>
          <p>с чего смотрят</p>
        </header>
        <ul v-if="data?.devices?.length" class="st-devices">
          <li v-for="d in data.devices" :key="d.device">
            <span>{{ DEVICE_NAMES[d.device] || d.device }}</span>
            <strong>{{ fmtNum(d.visitors) }}</strong>
          </li>
        </ul>
        <p v-else class="st-empty">Нет данных</p>
      </div>
    </div>

    <div class="st-grid">
      <div class="st-card">
        <header class="st-card-h">
          <h2>Посадочные</h2>
          <p>с какой страницы начинают визит</p>
        </header>
        <table v-if="data?.landings?.length" class="st-table">
          <thead>
            <tr>
              <th>Страница</th>
              <th>Сессии</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="s in data.landings" :key="'land-' + s.path">
              <td>{{ pageName(s.path) }}</td>
              <td>{{ fmtNum(s.sessions) }}</td>
            </tr>
          </tbody>
        </table>
        <p v-else class="st-empty">Нет данных</p>
      </div>
      <div class="st-card">
        <header class="st-card-h">
          <h2>Заявки по страницам</h2>
          <p>где оставляют телефон</p>
        </header>
        <table v-if="data?.leads_by_page?.length" class="st-table">
          <thead>
            <tr>
              <th>Страница</th>
              <th>Заявки</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="s in data.leads_by_page" :key="'leadp-' + s.path">
              <td>{{ pageName(s.path) }}</td>
              <td>{{ fmtNum(s.leads) }}</td>
            </tr>
          </tbody>
        </table>
        <p v-else class="st-empty">Заявок за период нет</p>
      </div>
    </div>

    <div class="st-card">
      <header class="st-card-h">
        <h2>Живая лента</h2>
        <div class="st-periods">
          <button
            v-for="f in FEED_FILTERS"
            :key="f.id"
            type="button"
            class="st-chip"
            :class="{ on: feedFilter === f.id }"
            @click="feedFilter = f.id"
          >
            {{ f.label }}
          </button>
        </div>
      </header>
      <div v-if="filteredRecent.length" class="st-feed">
        <div v-for="(ev, i) in filteredRecent" :key="ev.t + i" class="st-feed-row">
          <time>{{ fmtTime(ev.t) }}</time>
          <span class="st-ev" :data-ev="ev.event">{{ EVENT_NAMES[ev.event] || ev.event }}</span>
          <span class="st-feed-path">{{ pageName(ev.path) }}</span>
          <span class="st-feed-label">{{ feedLabel(ev) }}</span>
          <span class="st-feed-dev">{{ DEVICE_NAMES[ev.device] || ev.device }}</span>
        </div>
      </div>
      <p v-else class="st-empty">{{ data?.recent?.length ? 'Нет событий в этом фильтре' : 'Лента появится после первых визитов' }}</p>
    </div>
  </section>
</template>

<style scoped>
.st { display: flex; flex-direction: column; gap: 22px; min-width: 0; overflow-wrap: anywhere; }

.st-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
}
.st-periods { display: flex; gap: 8px; flex-wrap: wrap; }
.st-chip {
  font-family: var(--font-m);
  font-size: 12px;
  padding: 8px 14px;
  border-radius: 999px;
  border: none;
  background: transparent;
  color: var(--w-soft);
  box-shadow: inset 0 0 0 1.5px var(--line-d);
}
.st-chip.on,
.st-chip:hover { color: var(--white); background: rgba(255, 255, 255, 0.06); }
.st-chip.on { box-shadow: inset 0 0 0 1.5px var(--acc); color: var(--acc-hot); }

.st-refresh {
  font-family: var(--font-m);
  font-size: 12.5px;
  font-weight: 600;
  padding: 11px 20px;
  border-radius: var(--r-sm);
  border: none;
  background: var(--acc);
  color: #fff;
}
.st-refresh:hover { background: var(--acc-hot); }
.st-refresh:disabled { opacity: 0.6; cursor: default; }

.st-error {
  font-size: 13.5px;
  color: var(--acc-hot);
}

.st-live {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-family: var(--font-m);
  font-size: 12px;
  color: var(--ok);
}
.st-live-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--ok);
  box-shadow: 0 0 0 4px rgba(53, 201, 126, 0.18);
  animation: pulse 1.6s infinite;
}
@keyframes pulse {
  50% { opacity: 0.45; }
}

.st-kpis {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}
.st-contact {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 28px;
}
.st-card--contact {
  border-top: 3px solid var(--acc);
}
.st-contact-kpis {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 16px;
}
.st-contact-kpis div {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--line-d);
  border-radius: 12px;
  padding: 12px 14px;
}
.st-contact-kpis em {
  display: block;
  font-style: normal;
  font-family: var(--font-m);
  font-size: 10.5px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--w-faint);
  margin-bottom: 6px;
}
.st-contact-kpis strong {
  font-family: var(--font-d);
  font-size: 22px;
}
.st-contact-kpis span {
  display: block;
  margin-top: 4px;
  font-size: 12px;
  color: var(--w-soft);
}
.st-subh--mt { margin-top: 22px; }
.st-table tr.is-zero td { opacity: 0.38; }
.st-providers {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 14px;
}
.st-providers li {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.05);
  font-size: 12.5px;
  color: var(--w-soft);
}
.st-providers strong { color: var(--white); font-family: var(--font-m); }
.st-kpi {
  background: var(--bg1);
  border: 1px solid var(--line-d);
  border-radius: var(--r);
  padding: 16px 18px;
}
.st-kpi--acc { border-top: 3px solid var(--acc); }
.st-kpi-label {
  font-family: var(--font-m);
  font-size: 10.5px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--w-faint);
  margin-bottom: 8px;
}
.st-kpi-val {
  font-family: var(--font-d);
  font-size: 26px;
  font-weight: 700;
  line-height: 1;
}
.st-kpi-sub {
  margin-top: 8px;
  font-size: 12.5px;
  color: var(--w-soft);
}

.st-card {
  background: var(--bg1);
  border: 1px solid var(--line-d);
  border-radius: var(--r);
  padding: 20px 22px 18px;
  overflow-x: auto;
  min-width: 0;
}
.st-card-h {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 16px;
}
.st-card-h h2 {
  font-family: var(--font-d);
  font-size: 14px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}
.st-card-h p { font-size: 12.5px; color: var(--w-faint); }

.st-chart {
  display: flex;
  align-items: stretch;
  gap: 4px;
  height: 160px;
  overflow-x: auto;
  padding-bottom: 4px;
}
.st-col {
  flex: 1 0 22px;
  min-width: 18px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
  gap: 4px;
}
.st-col-bars {
  flex: 1;
  width: 100%;
  display: flex;
  align-items: flex-end;
  justify-content: center;
  gap: 2px;
}
.st-bar {
  width: 6px;
  min-height: 2px;
  background: var(--acc);
  border-radius: 3px 3px 0 0;
}
.st-bar--pv { background: rgba(255, 255, 255, 0.22); }
.st-col-lead {
  font-family: var(--font-m);
  font-size: 10px;
  color: var(--acc-hot);
}
.st-col em {
  font-style: normal;
  font-family: var(--font-m);
  font-size: 9px;
  color: var(--w-faint);
  white-space: nowrap;
}

.st-legend {
  display: flex;
  gap: 14px;
  align-items: center;
  margin-top: 12px;
  font-size: 12px;
  color: var(--w-faint);
}
.st-lg {
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 2px;
  margin-right: 4px;
  vertical-align: middle;
}
.st-lg--v { background: var(--acc); }
.st-lg--p { background: rgba(255, 255, 255, 0.22); }

.st-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}
.st-grid--3 { grid-template-columns: 1.2fr 1.2fr 0.8fr; }
.st-grid--calc { grid-template-columns: 1fr 1fr 1fr 1fr; margin-top: 18px; }

.st-calc-kpis {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin-bottom: 18px;
}
.st-calc-kpis div {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--line-d);
  border-radius: 12px;
  padding: 12px 14px;
}
.st-calc-kpis em {
  display: block;
  font-style: normal;
  font-family: var(--font-m);
  font-size: 10.5px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--w-faint);
  margin-bottom: 6px;
}
.st-calc-kpis strong {
  font-family: var(--font-d);
  font-size: 22px;
}
.st-calc-kpis span {
  display: block;
  margin-top: 4px;
  font-size: 12px;
  color: var(--w-soft);
}

.st-modes {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}
.st-mode-h {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 14px;
}
.st-mode-h span { font-family: var(--font-m); color: var(--acc-hot); }
.st-mode--object .st-funnel-fill { background: #5b8def; }
.st-mode-meta {
  margin-top: 8px;
  font-size: 12px;
  color: var(--w-faint);
}
.st-subh {
  font-family: var(--font-m);
  font-size: 11px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--w-faint);
  margin-bottom: 8px;
}
.st-empty--sm { padding: 16px 4px; font-size: 12.5px; }
.st-regions { margin-top: 16px; }
.st-regions ul {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.st-regions li {
  display: inline-flex;
  gap: 8px;
  align-items: center;
  padding: 6px 10px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.05);
  font-size: 12.5px;
  color: var(--w-soft);
}
.st-regions strong { font-family: var(--font-m); color: var(--white); }

.st-funnel { display: flex; flex-direction: column; gap: 12px; }
.st-funnel-row {
  display: flex;
  justify-content: space-between;
  font-size: 13.5px;
  margin-bottom: 6px;
}
.st-funnel-row strong { font-family: var(--font-m); }
.st-funnel-track {
  height: 8px;
  background: rgba(255, 255, 255, 0.06);
  border-radius: 99px;
  overflow: hidden;
}
.st-funnel-fill {
  height: 100%;
  background: var(--acc);
  border-radius: 99px;
}

.st-hours {
  display: flex;
  align-items: stretch;
  gap: 3px;
  height: 110px;
}
.st-hour {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  align-items: center;
  gap: 4px;
}
.st-hour-bar {
  width: 100%;
  max-width: 14px;
  min-height: 2px;
  background: rgba(255, 125, 63, 0.75);
  border-radius: 3px 3px 0 0;
}
.st-hour span {
  font-family: var(--font-m);
  font-size: 9px;
  color: var(--w-faint);
}

.st-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}
.st-table th {
  font-family: var(--font-m);
  font-size: 10.5px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--w-faint);
  text-align: left;
  padding: 0 8px 10px;
}
.st-table td {
  padding: 9px 8px;
  border-top: 1px solid var(--line-d);
  color: var(--w-soft);
  vertical-align: top;
  overflow-wrap: anywhere;
  word-break: break-word;
}
.st-table strong {
  display: block;
  color: var(--white);
  font-weight: 600;
}
.st-table small {
  display: block;
  margin-top: 2px;
  color: var(--w-faint);
  font-size: 11.5px;
}
.st-path {
  font-family: var(--font-m);
  font-size: 11px;
  overflow-wrap: anywhere;
  word-break: break-all;
}

.st-devices { display: flex; flex-direction: column; gap: 10px; }
.st-devices li {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid var(--line-d);
  color: var(--w-soft);
}
.st-devices li:last-child { border-bottom: none; }
.st-devices strong { color: var(--white); font-family: var(--font-m); }

.st-feed {
  display: flex;
  flex-direction: column;
  max-height: 420px;
  overflow: auto;
}
.st-feed-row {
  display: grid;
  grid-template-columns: 132px 140px 1fr 1.2fr 90px;
  gap: 10px;
  align-items: center;
  padding: 9px 4px;
  border-top: 1px solid var(--line-d);
  font-size: 12.5px;
  color: var(--w-soft);
}
.st-feed-row time { font-family: var(--font-m); color: var(--w-faint); font-size: 11.5px; }
.st-ev {
  font-family: var(--font-m);
  font-size: 10.5px;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  padding: 3px 8px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.06);
  width: fit-content;
}
.st-ev[data-ev='form_submit'] { background: rgba(53, 201, 126, 0.16); color: var(--ok); }
.st-ev[data-ev='outbound'] { background: var(--acc-dim); color: var(--acc-hot); }
.st-ev[data-ev='tel'] { background: rgba(53, 201, 126, 0.16); color: var(--ok); }
.st-ev[data-ev='mail'] { background: rgba(91, 141, 239, 0.16); color: #8eb0ff; }
.st-ev[data-ev='click'] { color: var(--white); }
.st-ev[data-ev='form_start'] { color: var(--ok); }
.st-ev[data-ev='calc'] { background: rgba(91, 141, 239, 0.16); color: #8eb0ff; }
.st-feed-path {
  color: var(--white);
  overflow-wrap: anywhere;
  word-break: break-word;
  min-width: 0;
}
.st-feed-label {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  min-width: 0;
}
.st-feed-dev { color: var(--w-faint); text-align: right; }

.st-empty {
  padding: 28px 8px;
  text-align: center;
  color: var(--w-faint);
  font-size: 13.5px;
}

@media (max-width: 1100px) {
  .st-kpis { grid-template-columns: repeat(4, 1fr); }
  .st-contact { grid-template-columns: 1fr; }
  .st-grid, .st-grid--3 { grid-template-columns: 1fr; }
  .st-grid--calc { grid-template-columns: 1fr 1fr; }
  .st-calc-kpis { grid-template-columns: 1fr 1fr; }
  .st-feed-row { grid-template-columns: 120px 1fr; }
  .st-feed-dev { display: none; }
}
@media (max-width: 760px) {
  .st { gap: 12px; }
  .st-kpis { grid-template-columns: 1fr 1fr; gap: 8px; }
  .st-kpi { padding: 10px 10px 8px; border-radius: 10px; }
  .st-kpi-label {
    font-size: 9px;
    letter-spacing: 0.04em;
    margin-bottom: 4px;
  }
  .st-kpi-val {
    font-family: var(--font-b);
    font-size: 17px;
    letter-spacing: -0.02em;
  }
  .st-kpi-sub { font-size: 11px; margin-top: 4px; line-height: 1.35; }
  .st-card { padding: 12px 10px 10px; border-radius: 12px; }
  .st-card-h {
    flex-direction: column;
    align-items: flex-start;
    gap: 4px;
    margin-bottom: 10px;
  }
  .st-card-h h2 {
    font-family: var(--font-b);
    font-size: 13px;
    letter-spacing: 0;
    text-transform: none;
  }
  .st-card-h p { font-size: 11px; }
  .st-calc-kpis { gap: 8px; }
  .st-calc-kpis div { padding: 8px 10px; }
  .st-calc-kpis strong {
    font-family: var(--font-b);
    font-size: 16px;
  }
  .st-calc-kpis em { font-size: 9px; letter-spacing: 0.04em; }
  .st-calc-kpis span { font-size: 11px; }
  .st-modes { grid-template-columns: 1fr; }
  .st-grid--calc { grid-template-columns: 1fr; }
  .st-mode-h { font-size: 13px; }
  .st-table { font-size: 12px; }
  .st-table th { font-size: 9.5px; padding: 0 4px 8px; letter-spacing: 0.04em; }
  .st-table td { padding: 8px 4px; }
  .st-table .st-path { display: none; }
  .st-chip { font-size: 11px; padding: 8px 12px; }
  .st-refresh { font-size: 12px; padding: 9px 14px; }
  .st-chart { height: 120px; }
  .st-legend { flex-wrap: wrap; font-size: 11px; }
  .st-hours { overflow-x: auto; }
  .st-feed-row {
    grid-template-columns: 1fr;
    gap: 4px;
    padding: 10px 0;
    font-size: 12px;
  }
  .st-feed-label { white-space: normal; overflow: visible; }
  .st-funnel-row { font-size: 12.5px; }
}
@media (max-width: 420px) {
  .st-kpis { gap: 6px; }
  .st-kpi { padding: 8px 8px 7px; }
  .st-kpi-val { font-size: 15px; }
  .st-kpi-sub { font-size: 10px; }
  .st-calc-kpis { grid-template-columns: 1fr 1fr; }
  .st-calc-kpis strong { font-size: 15px; }
  .st-toolbar { gap: 8px; }
  .st-chip { padding: 7px 10px; font-size: 10.5px; }
}
</style>
