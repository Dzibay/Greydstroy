<script setup>
import { ref, computed, watch, nextTick, onUnmounted } from 'vue'
import russiaSvg from '../../data/russia.svg?raw'
import { SNOW_REGIONS } from '../../data/snowRegions'

const props = defineProps({
  modelValue: { type: String, required: true },
  snowLabel: { type: String, default: '' },
  snowNote: { type: String, default: '' },
})

const emit = defineEmits(['update:modelValue'])

const open = ref(false)
const query = ref('')
const hoverId = ref('')
const mapRef = ref(null)

const svgMarkup = russiaSvg.replace(/<\?xml[\s\S]*?\?>/, '').trim()

const current = computed(() => SNOW_REGIONS[props.modelValue] || SNOW_REGIONS.NIZ)

const list = computed(() => {
  const s = query.value.trim().toLowerCase()
  return Object.entries(SNOW_REGIONS)
    .map(([id, r]) => ({ id, ...r }))
    .filter((r) => {
      if (!s) return true
      return r.title.toLowerCase().includes(s) || r.snow.toLowerCase() === s
    })
    .sort((a, b) => a.title.localeCompare(b.title, 'ru'))
})

const hover = computed(() => (hoverId.value && SNOW_REGIONS[hoverId.value]) || null)

function paint() {
  const root = mapRef.value
  if (!root) return
  root.querySelectorAll('.russia-region').forEach((el) => {
    const id = el.id.replace(/^RU-/, '')
    const r = SNOW_REGIONS[id]
    if (r) el.dataset.snow = r.snow
    el.classList.toggle('is-on', id === props.modelValue)
    const searching = Boolean(query.value.trim())
    el.classList.toggle(
      'is-hit',
      id === hoverId.value || (searching && list.value.some((x) => x.id === id)),
    )
  })
}

function codeFromEvent(e) {
  const path = e.target.closest?.('.russia-region')
  if (!path?.id) return ''
  return path.id.replace(/^RU-/, '')
}

function pick(id) {
  if (!SNOW_REGIONS[id]) return
  emit('update:modelValue', id)
  close()
}

function onMapClick(e) {
  const id = codeFromEvent(e)
  if (id) pick(id)
}

function onMapMove(e) {
  hoverId.value = codeFromEvent(e)
}

function onKey(e) {
  if (e.key === 'Escape') close()
}

function close() {
  open.value = false
  query.value = ''
  hoverId.value = ''
}

async function show() {
  open.value = true
  await nextTick()
  paint()
}

watch(open, (v) => {
  document.body.style.overflow = v ? 'hidden' : ''
  if (v) window.addEventListener('keydown', onKey)
  else window.removeEventListener('keydown', onKey)
})

watch([() => props.modelValue, query, list, hoverId], () => {
  if (open.value) nextTick(paint)
})

onUnmounted(() => {
  document.body.style.overflow = ''
  window.removeEventListener('keydown', onKey)
})
</script>

<template>
  <div class="snow-wrap">
    <button type="button" class="snow-btn" :class="{ open }" @click="show">
      <span class="snow-btn-ic" aria-hidden="true">
        <svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="16" cy="16" r="10" />
          <path d="M16 6v20M6 16h20" />
          <ellipse cx="16" cy="16" rx="4.5" ry="10" />
        </svg>
      </span>
      <span class="snow-btn-body">
        <span class="snow-btn-title">{{ current.title }}</span>
        <span class="snow-btn-note">район {{ current.snow }} · {{ snowNote || snowLabel }}</span>
      </span>
      <span class="snow-btn-cta">Карта</span>
    </button>

    <Teleport to="body">
      <div v-if="open" class="snow-modal" role="dialog" aria-modal="true" aria-label="Выбор региона">
        <button class="snow-scrim" type="button" aria-label="Закрыть" @click="close"></button>
        <div class="snow-card">
          <div class="snow-card-h">
            <div>
              <p class="snow-card-tag">Снеговой район</p>
              <h3 class="snow-card-title">Где будет стоять здание?</h3>
            </div>
            <button type="button" class="snow-x" aria-label="Закрыть" @click="close">✕</button>
          </div>

          <label class="snow-search">
            <span class="sr">Поиск региона</span>
            <input v-model="query" type="search" placeholder="Найти область, край, республику…" />
          </label>

          <div class="snow-body">
            <div
              ref="mapRef"
              class="snow-map"
              v-html="svgMarkup"
              @click="onMapClick"
              @mousemove="onMapMove"
              @mouseleave="hoverId = ''"
            ></div>

            <div class="snow-side">
              <p class="snow-hint">Нажмите регион на карте или выберите из списка</p>
              <p class="snow-hover">
                <b>{{ (hover || current).title }}</b>
                <span>район {{ (hover || current).snow }}</span>
              </p>
              <ul class="snow-list">
                <li v-for="r in list" :key="r.id">
                  <button
                    type="button"
                    :class="{ active: r.id === modelValue }"
                    @click="pick(r.id)"
                    @mouseenter="hoverId = r.id"
                  >
                    <span>{{ r.title }}</span>
                    <em>{{ r.snow }}</em>
                  </button>
                </li>
              </ul>
            </div>
          </div>

          <div class="snow-legend">
            <span v-for="d in ['I', 'II', 'III', 'IV', 'V', 'VI']" :key="d" :data-snow="d">{{ d }}</span>
            <p>Ориентир по центру субъекта, СП 20.13330. На площадке район может отличаться.</p>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<style scoped>
.snow-btn {
  display: flex;
  align-items: center;
  gap: 14px;
  width: 100%;
  padding: 16px 18px;
  background: var(--card-d);
  border: 1px solid var(--line-d);
  border-radius: var(--r-sm);
  text-align: left;
  color: var(--white);
  transition: border-color 0.25s, background 0.25s;
}
.snow-btn:hover, .snow-btn.open {
  border-color: var(--acc);
  background: linear-gradient(160deg, rgba(255, 90, 31, 0.12), var(--card-d) 60%);
}
.snow-btn-ic {
  width: 42px;
  height: 42px;
  flex-shrink: 0;
  display: grid;
  place-items: center;
  border-radius: 10px;
  background: var(--acc-dim);
  color: var(--acc-hot);
}
.snow-btn-ic svg { width: 22px; height: 22px; }
.snow-btn-body { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 3px; }
.snow-btn-title { font-weight: 700; font-size: 14.5px; }
.snow-btn-note { font-size: 12.5px; color: var(--w-faint); }
.snow-btn-cta {
  font-family: var(--font-m);
  font-size: 11px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--acc-hot);
}

.snow-modal {
  position: fixed;
  inset: 0;
  z-index: 80;
  display: grid;
  place-items: center;
  padding: 18px;
}
.snow-scrim {
  position: absolute;
  inset: 0;
  background: rgba(7, 9, 12, 0.72);
  border: 0;
  cursor: pointer;
}
.snow-card {
  position: relative;
  z-index: 1;
  width: min(980px, 100%);
  max-height: min(92vh, 820px);
  display: flex;
  flex-direction: column;
  background: var(--bg1);
  border: 1px solid rgba(255, 90, 31, 0.35);
  border-radius: var(--r);
  padding: 22px 22px 16px;
  box-shadow: 0 24px 60px rgba(0, 0, 0, 0.45);
}
.snow-card-h {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: flex-start;
  margin-bottom: 14px;
}
.snow-card-tag {
  font-family: var(--font-m);
  font-size: 11px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--acc);
  margin-bottom: 6px;
}
.snow-card-title {
  font-family: var(--font-d);
  font-size: 18px;
  font-weight: 700;
  text-transform: uppercase;
}
.snow-x {
  width: 36px;
  height: 36px;
  border: 1px solid var(--line-d);
  border-radius: 8px;
  background: transparent;
  color: var(--w-soft);
  font-size: 16px;
}
.snow-x:hover { color: var(--white); border-color: var(--acc); }

.snow-search input {
  width: 100%;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--line-d);
  border-radius: var(--r-sm);
  color: var(--white);
  padding: 12px 14px;
  margin-bottom: 14px;
}
.snow-search input:focus { outline: none; border-color: var(--acc); }
.sr { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); }

.snow-body {
  display: grid;
  grid-template-columns: 1.35fr 0.65fr;
  gap: 16px;
  min-height: 0;
  flex: 1;
}
.snow-map {
  background: #0d1116;
  border: 1px solid var(--line-d);
  border-radius: var(--r-sm);
  overflow: hidden;
  cursor: pointer;
}
.snow-map :deep(svg) {
  display: block;
  width: 100%;
  height: auto;
}
.snow-map :deep(.russia-region) {
  fill: #1b232c;
  stroke: #0b0e11;
  stroke-width: 0.45;
  transition: fill 0.15s;
}
.snow-map :deep(.russia-region[data-snow="I"]) { fill: #2c4a3d; }
.snow-map :deep(.russia-region[data-snow="II"]) { fill: #2d4a5c; }
.snow-map :deep(.russia-region[data-snow="III"]) { fill: #3a4560; }
.snow-map :deep(.russia-region[data-snow="IV"]) { fill: #6a3a28; }
.snow-map :deep(.russia-region[data-snow="V"]) { fill: #5a2d3c; }
.snow-map :deep(.russia-region[data-snow="VI"]) { fill: #3d2a55; }
.snow-map :deep(.russia-region:hover),
.snow-map :deep(.russia-region.is-hit) { fill: var(--acc-hot); }
.snow-map :deep(.russia-region.is-on) {
  fill: var(--acc);
  stroke: #fff;
  stroke-width: 1.1;
}

.snow-side { min-width: 0; display: flex; flex-direction: column; min-height: 0; }
.snow-hint {
  font-size: 12px;
  color: var(--w-faint);
  margin-bottom: 6px;
  line-height: 1.35;
}
.snow-hover {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 10px;
  min-height: 1.35em;
  margin-bottom: 8px;
  font-size: 13.5px;
  color: var(--w-soft);
  white-space: nowrap;
}
.snow-hover b {
  color: var(--acc-hot);
  overflow: hidden;
  text-overflow: ellipsis;
}
.snow-hover span {
  flex-shrink: 0;
  font-family: var(--font-m);
  font-size: 11px;
  color: var(--w-faint);
}
.snow-list {
  overflow: auto;
  flex: 1;
  max-height: 360px;
  border: 1px solid var(--line-d);
  border-radius: var(--r-sm);
}
.snow-list button {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  width: 100%;
  padding: 9px 12px;
  background: transparent;
  border: 0;
  border-bottom: 1px dashed var(--line-d);
  color: var(--white);
  text-align: left;
  font-size: 13px;
}
.snow-list button:hover { background: rgba(255, 90, 31, 0.08); }
.snow-list button.active { background: rgba(255, 90, 31, 0.16); color: var(--acc-hot); }
.snow-list em {
  font-style: normal;
  font-family: var(--font-m);
  font-size: 11px;
  color: var(--w-faint);
}

.snow-legend {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px 12px;
  margin-top: 12px;
  font-size: 12px;
  color: var(--w-faint);
}
.snow-legend span {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-family: var(--font-m);
  font-size: 11px;
  color: var(--w-soft);
}
.snow-legend span::before {
  content: '';
  width: 10px;
  height: 10px;
  border-radius: 2px;
}
.snow-legend span[data-snow="I"]::before { background: #2c4a3d; }
.snow-legend span[data-snow="II"]::before { background: #2d4a5c; }
.snow-legend span[data-snow="III"]::before { background: #3a4560; }
.snow-legend span[data-snow="IV"]::before { background: #6a3a28; }
.snow-legend span[data-snow="V"]::before { background: #5a2d3c; }
.snow-legend span[data-snow="VI"]::before { background: #3d2a55; }
.snow-legend p { flex: 1 1 220px; margin: 0; }

@media (max-width: 800px) {
  .snow-body { grid-template-columns: 1fr; }
  .snow-list { max-height: 180px; }
  .snow-card { padding: 16px 14px 12px; }
}
</style>
