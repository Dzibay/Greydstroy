<script setup>
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import LeadForm from '../components/ui/LeadForm.vue'
import BuildingPreview from '../components/calc/BuildingPreview.vue'
import SnowRegionPicker from '../components/calc/SnowRegionPicker.vue'
import { SNOW_REGIONS, DEFAULT_REGION } from '../data/snowRegions'

/* =====================================================
   Тарифы — «примерные параметры», правятся в одном месте
   ===================================================== */
const RATES = {
  metalPerTonne: 78000, // наш металл, ₽/т (С245/С255)
  kmdShare: 0.08, // разработка КМД, доля от стоимости работ
  urgentShare: 0.25, // срочность, доля от стоимости работ
  montagePerTonne: 45000, // монтаж с окраской, ₽/т
  vatShare: 20 / 120, // НДС 20% «в том числе» (цены с НДС)
  rangeLow: 0.88, // нижняя граница вилки
  rangeHigh: 1.12, // верхняя граница вилки
}

const TYPES = [
  {
    id: 'plates',
    label: 'Закладные и детали',
    hint: 'Пластины, анкеры, кронштейны, фланцы',
    rate: 45000,
    icon: 'plate',
  },
  {
    id: 'beams',
    label: 'Балки и колонны',
    hint: 'Двутавры, связи, прогоны с обработкой',
    rate: 52000,
    icon: 'beam',
  },
  {
    id: 'frame',
    label: 'Каркасы и навесы',
    hint: 'Каркас здания, навес, эстакада',
    rate: 57000,
    icon: 'frame',
  },
  {
    id: 'truss',
    label: 'Фермы',
    hint: 'Стропильные и подстропильные фермы',
    rate: 65000,
    icon: 'truss',
  },
  {
    id: 'stairs',
    label: 'Лестницы и площадки',
    hint: 'Марши, площадки, ограждения',
    rate: 75000,
    icon: 'stairs',
  },
  {
    id: 'custom',
    label: 'Нестандарт',
    hint: 'Ёмкости, бункеры, уникальные узлы',
    rate: 95000,
    icon: 'tank',
  },
]

const COATINGS = [
  { id: 'none', label: 'Без покрытия', rate: 0, note: 'чистый металл' },
  { id: 'primer', label: 'Грунт ГФ-021', rate: 8000, note: 'огрунтовка, защита на время монтажа' },
  { id: 'paint', label: 'Грунт + эмаль', rate: 15000, note: 'финишное покрытие в цвет RAL' },
]

const DELIVERY = [
  { id: 'pickup', label: 'Самовывоз', cost: 0, note: 'Дзержинск, в день готовности' },
  { id: 'local', label: 'Дзержинск / Н. Новгород', cost: 8000, note: 'наш транспорт' },
  { id: 'region', label: 'Нижегородская область', cost: 15000, note: 'наш транспорт' },
  { id: 'russia', label: 'По России', cost: 0, note: 'по тарифу ТК', external: true },
]

const DISCOUNT_TIERS = [
  { min: 5, share: 0.05 },
  { min: 20, share: 0.1 },
  { min: 50, share: 0.15 },
]

/* =====================================================
   Объект целиком — металлоёмкость по объёму
   q, кг/м³: база при пролёте 18 м, снег IV (высота входит в м³)
   ===================================================== */
const BUILDING_KINDS = [
  {
    id: 'canopy',
    label: 'Навес',
    hint: 'Открытая зона, авто, входная группа',
    q: 22 / 6,
    icon: 'canopy',
  },
  {
    id: 'hangar',
    label: 'Холодный ангар',
    hint: 'Склад без утепления, рамный каркас',
    q: 28 / 6,
    icon: 'hangar',
  },
  {
    id: 'warm',
    label: 'Тёплый склад',
    hint: 'Каркас под сэндвич-панели',
    q: 36 / 6,
    icon: 'warm',
  },
  {
    id: 'shop',
    label: 'Цех / производство',
    hint: 'Выше нагрузки, возможны краны',
    q: 42 / 6,
    icon: 'shop',
  },
  {
    id: 'frame',
    label: 'Каркас здания',
    hint: 'Рамный каркас по вашим габаритам',
    q: 38 / 6,
    icon: 'frame',
  },
]

const ROOFS = [
  { id: 'single', label: 'Односкатная', k: 0.93 },
  { id: 'gable', label: 'Двускатная', k: 1 },
  { id: 'arch', label: 'Арочная', k: 0.88 },
]

const CRANES = [
  { id: 'none', label: 'Без крана', note: 'только каркас', addQ: 0 },
  { id: 't5', label: 'Кран-балка 5 т', note: '+ подкрановые пути', addQ: 12 },
  { id: 't10', label: 'Мостовой 10 т', note: 'усиление колонн', addQ: 22 },
  { id: 't20', label: 'Мостовой 20 т', note: 'тяжёлый режим', addQ: 35 },
]

const SNOW = [
  { id: 'I', label: 'I', note: '80 кг/м²', k: 0.82 },
  { id: 'II', label: 'II', note: '120 кг/м²', k: 0.88 },
  { id: 'III', label: 'III', note: '180 кг/м²', k: 0.94 },
  { id: 'IV', label: 'IV', note: '240 кг/м²', k: 1 },
  { id: 'V', label: 'V', note: '320 кг/м²', k: 1.12 },
  { id: 'VI', label: 'VI', note: '400 кг/м²', k: 1.22 },
]

const COL_STEPS = [
  { id: 6, label: '6 м', k: 1, note: 'типовой' },
  { id: 9, label: '9 м', k: 1.06, note: 'реже колонны' },
  { id: 12, label: '12 м', k: 1.12, note: 'тяжёлые ригели' },
]

const FOUNDATIONS = [
  { id: 'pads', label: 'Стаканный', note: 'столбы под колонны', perSqm: 4800, addQ: 0.5 },
  { id: 'strip', label: 'Ленточный', note: 'лента по периметру', perSqm: 6400, addQ: 0.35 },
  { id: 'piles', label: 'Свайный', note: 'сваи с ростверком', perSqm: 8200, addQ: 0.8 },
  { id: 'slab', label: 'Плитный', note: 'монолитная плита', perSqm: 10800, addQ: 0.25 },
]

const DIM_PRESETS = [
  { l: 18, w: 12, h: 4.5, label: '18×12×4,5' },
  { l: 36, w: 18, h: 6, label: '36×18×6' },
  { l: 48, w: 24, h: 8, label: '48×24×8' },
  { l: 60, w: 30, h: 10, label: '60×30×10' },
]

const DIM = {
  l: { min: 8, max: 120 },
  w: { min: 6, max: 48 },
  h: { min: 3, max: 18 },
}

const FRAME_TYPE = TYPES.find((t) => t.id === 'frame')

/* ---------- состояние ---------- */
const route = useRoute()

const mode = ref(route.query.tab === 'object' ? 'object' : 'details')
const type = ref(TYPES[2])
const mass = ref(3)
const ownMetal = ref(false) // false = наш металл, true = давальческий
const coating = ref(COATINGS[1])
const needKmd = ref(false)
const needMontage = ref(false)
const urgent = ref(false)
const delivery = ref(DELIVERY[0])

const bKind = ref(BUILDING_KINDS[1])
const bLength = ref(36)
const bWidth = ref(18)
const bHeight = ref(6)
const bRoof = ref(ROOFS[1])
const bCrane = ref(CRANES[0])
const bSnow = ref(SNOW[3])
const bStep = ref(COL_STEPS[0])
const bMezzanine = ref(false)
const bStairs = ref(false)
const bFound = ref(FOUNDATIONS[0])
const bRegion = ref(DEFAULT_REGION)

watch(bRegion, (code) => {
  const r = SNOW_REGIONS[code]
  if (!r) return
  const s = SNOW.find((x) => x.id === r.snow)
  if (s) bSnow.value = s
})

function setMode(next) {
  mode.value = next
}

/* ---------- масса: лог-слайдер + пресеты ---------- */
const MASS_MIN = 0.1
const MASS_MAX = 100
const massPresets = [0.5, 1, 3, 5, 10, 20, 50]

const roundMass = (m) => (m < 1 ? +m.toFixed(2) : m < 10 ? +m.toFixed(1) : Math.round(m))

const massPos = computed({
  get: () => (Math.log(mass.value / MASS_MIN) / Math.log(MASS_MAX / MASS_MIN)) * 100,
  set: (p) => {
    mass.value = roundMass(MASS_MIN * Math.pow(MASS_MAX / MASS_MIN, p / 100))
  },
})

function onMassInput(e) {
  const v = parseFloat(String(e.target.value).replace(',', '.'))
  if (!Number.isNaN(v)) mass.value = Math.min(Math.max(v, MASS_MIN), MASS_MAX)
}

function clamp(n, a, b) {
  return Math.min(b, Math.max(a, n))
}

function onDimInput(key, e) {
  const v = parseFloat(String(e.target.value).replace(',', '.'))
  if (Number.isNaN(v)) return
  if (key === 'l') bLength.value = clamp(v, DIM.l.min, DIM.l.max)
  if (key === 'w') bWidth.value = clamp(v, DIM.w.min, DIM.w.max)
  if (key === 'h') bHeight.value = clamp(v, DIM.h.min, DIM.h.max)
}

function applyPreset(p) {
  bLength.value = p.l
  bWidth.value = p.w
  bHeight.value = p.h
}

const dimPresetActive = computed(() =>
  DIM_PRESETS.find(
    (p) => p.l === bLength.value && p.w === bWidth.value && p.h === bHeight.value,
  ),
)

/* ---------- объект: металлоёмкость по м³ ---------- */
const buildingQ = computed(() => {
  const spanK = 1 + 0.015 * (bWidth.value - 18)
  let q = bKind.value.q * spanK * bSnow.value.k * bRoof.value.k * bStep.value.k
  return Math.min(16, Math.max(2, q))
})

const buildingArea = computed(() => bLength.value * bWidth.value)
const buildingVolume = computed(() => buildingArea.value * bHeight.value)
const buildingMass = computed(() => {
  const area = buildingArea.value
  let kg = buildingVolume.value * buildingQ.value
  kg += bCrane.value.addQ * area
  kg += bFound.value.addQ * area
  if (bMezzanine.value) kg += 16 * area
  if (bStairs.value) kg *= 1.06
  return roundMass(kg / 1000)
})

const activeType = computed(() => (mode.value === 'object' ? FRAME_TYPE : type.value))
const activeMass = computed(() => (mode.value === 'object' ? buildingMass.value : mass.value))

const fmtM = (n) => (Number.isInteger(n) ? String(n) : n.toFixed(1).replace('.', ','))
const fmtQ = (n) => (n < 20 ? n.toFixed(1) : Math.round(n).toString()).replace('.', ',')

const stepNo = computed(() =>
  mode.value === 'object'
    ? { kind: '01', dim: '02', extra: '03' }
    : { type: '01', mass: '02', metal: '03', coat: '04', opt: '05', del: '06' },
)

const objectCoating = COATINGS[1] // грунт — типичный ориентир для каркаса

const activeOwnMetal = computed(() => (mode.value === 'object' ? false : ownMetal.value))
const activeCoating = computed(() => (mode.value === 'object' ? objectCoating : coating.value))
const activeNeedKmd = computed(() => (mode.value === 'object' ? false : needKmd.value))
const activeNeedMontage = computed(() => (mode.value === 'object' ? false : needMontage.value))
const activeUrgent = computed(() => (mode.value === 'object' ? false : urgent.value))
const activeDelivery = computed(() => (mode.value === 'object' ? DELIVERY[0] : delivery.value))

/* ---------- скидка за объём ---------- */
const discountShare = computed(() => {
  let share = 0
  for (const t of DISCOUNT_TIERS) if (activeMass.value >= t.min) share = t.share
  return share
})

const nextTier = computed(() => {
  const t = DISCOUNT_TIERS.find((t) => activeMass.value < t.min)
  if (!t) return null
  return { need: roundMass(t.min - activeMass.value), pct: t.share * 100 }
})

/* ---------- смета ---------- */
const fmt = (n) => Math.round(n).toLocaleString('ru-RU')
const roundK = (n) => Math.round(n / 1000) * 1000

const calc = computed(() => {
  const m = activeMass.value
  const work = activeType.value.rate * m
  const kmd = activeNeedKmd.value ? work * RATES.kmdShare : 0
  const urgentFee = activeUrgent.value ? (work + kmd) * RATES.urgentShare : 0
  const material = activeOwnMetal.value ? 0 : RATES.metalPerTonne * m
  const coat = activeCoating.value.rate * m
  const montage = activeNeedMontage.value ? RATES.montagePerTonne * m : 0
  const discount = (work + kmd) * discountShare.value
  const deliveryCost = activeDelivery.value.cost
  const foundation = mode.value === 'object' ? bFound.value.perSqm * buildingArea.value : 0

  const total = work + kmd + urgentFee + material + coat + montage - discount + deliveryCost + foundation
  const vat = total * RATES.vatShare
  const area = mode.value === 'object' ? buildingArea.value : 0
  const vol = mode.value === 'object' ? buildingVolume.value : 0
  return {
    work,
    kmd,
    urgentFee,
    material,
    coat,
    montage,
    discount,
    deliveryCost,
    foundation,
    total,
    vat,
    low: roundK(total * RATES.rangeLow),
    high: roundK(total * RATES.rangeHigh),
    vatLow: roundK(total * RATES.rangeLow * RATES.vatShare),
    vatHigh: roundK(total * RATES.rangeHigh * RATES.vatShare),
    perTonne: total / m,
    perSqm: area ? total / area : 0,
    perCub: vol ? total / vol : 0,
  }
})

/* ---------- срок изготовления ---------- */
const leadTime = computed(() => {
  const m = activeMass.value
  if (activeUrgent.value) {
    if (m <= 1) return '3–5 рабочих дней'
    if (m <= 5) return '5–9 рабочих дней'
    if (m <= 20) return '10–18 рабочих дней'
    return 'обсудим отдельно'
  }
  if (m <= 1) return '5–7 рабочих дней'
  if (m <= 5) return '7–14 рабочих дней'
  if (m <= 20) return '2–4 недели'
  return 'от 4 недель'
})

/* ---------- анимация цифр ---------- */
function useTween(source, duration = 450) {
  const out = ref(source.value)
  let raf = null
  watch(source, (target) => {
    if (raf) cancelAnimationFrame(raf)
    const from = out.value
    const start = performance.now()
    const tick = (now) => {
      const p = Math.min(1, (now - start) / duration)
      out.value = from + (target - from) * (1 - Math.pow(1 - p, 3))
      if (p < 1) raf = requestAnimationFrame(tick)
    }
    raf = requestAnimationFrame(tick)
  })
  return out
}

const lowSrc = computed(() => calc.value.low)
const highSrc = computed(() => calc.value.high)
const shownLow = useTween(lowSrc)
const shownHigh = useTween(highSrc)

/* ---------- сводка для заявки ---------- */
const summary = computed(() => {
  const lines = [
    mode.value === 'object'
      ? 'Конфигурация из калькулятора (объект целиком):'
      : 'Конфигурация из калькулятора (детали и конструкции):',
  ]
  if (mode.value === 'object') {
    lines.push(`• Тип объекта: ${bKind.value.label}`)
    lines.push(
      `• Габариты: ${fmtM(bLength.value)} × ${fmtM(bWidth.value)} × ${fmtM(bHeight.value)} м (Д×Ш×В)`,
    )
    lines.push(`• Площадь: ${fmt(buildingArea.value)} м²`)
    lines.push(`• Объём: ${fmt(buildingVolume.value)} м³`)
    lines.push(`• Кровля: ${bRoof.value.label.toLowerCase()}`)
    lines.push(`• Кран: ${bCrane.value.label.toLowerCase()}`)
    lines.push(`• Регион: ${SNOW_REGIONS[bRegion.value]?.title || bRegion.value}`)
    lines.push(`• Снеговой район: ${bSnow.value.id} (${bSnow.value.note})`)
    lines.push(`• Шаг колонн: ${bStep.value.label}`)
    lines.push(`• Фундамент: ${bFound.value.label.toLowerCase()} (${bFound.value.note})`)
    const extra = []
    if (bMezzanine.value) extra.push('антресоль')
    if (bStairs.value) extra.push('лестницы и площадки')
    if (extra.length) lines.push(`• Дополнительно в каркасе: ${extra.join(', ')}`)
    lines.push(
      `• Ориентир массы каркаса: ${buildingMass.value} т (${fmtQ(buildingQ.value)} кг/м³)`,
    )
    lines.push('• В ориентир заложено: наш металл, грунт ГФ-021 и фундамент (ориентир ЖБ)')
    lines.push('• КМД, монтаж, сэндвич и доставка — уточним в точном расчёте')
  } else {
    lines.push(`• Тип: ${type.value.label}`)
    lines.push(`• Масса: ${mass.value} т`)
    lines.push(`• Металл: ${ownMetal.value ? 'давальческий (заказчика)' : 'наш, входит в смету'}`)
    lines.push(`• Покрытие: ${coating.value.label}`)
    const opts = []
    if (needKmd.value) opts.push('разработка КМД')
    if (needMontage.value) opts.push('монтаж')
    if (urgent.value) opts.push('срочно')
    if (opts.length) lines.push(`• Опции: ${opts.join(', ')}`)
    lines.push(`• Доставка: ${delivery.value.label}`)
  }
  lines.push(`• Ориентир калькулятора: ${fmt(calc.value.low)} – ${fmt(calc.value.high)} ₽`)
  lines.push(`• В т.ч. НДС 20%: ${fmt(calc.value.vatLow)} – ${fmt(calc.value.vatHigh)} ₽`)
  return lines.join('\n')
})

const breakdownOpen = ref(false)

/* мобильная схема: угол → слот в панели */
const SKETCH_MQ = 900
const sketchSlot = ref(null)
const sketchMobile = ref(
  typeof window !== 'undefined' && window.matchMedia(`(max-width: ${SKETCH_MQ}px)`).matches,
)
const flyBox = ref(null)
const sketchDocked = ref(false)
const sketchReady = ref(false)

let flyRaf = 0
function scheduleSketchFly() {
  if (flyRaf) return
  flyRaf = requestAnimationFrame(() => {
    flyRaf = 0
    updateSketchFly()
  })
}

function updateSketchFly() {
  const mobile = window.matchMedia(`(max-width: ${SKETCH_MQ}px)`).matches
  sketchMobile.value = mobile
  if (!mobile || mode.value !== 'object') {
    flyBox.value = null
    sketchDocked.value = false
    sketchReady.value = false
    return
  }
  const slot = sketchSlot.value
  const calcSec = document.getElementById('calculator')
  if (!slot || !calcSec) return

  const sr = slot.getBoundingClientRect()
  const calcTop = calcSec.getBoundingClientRect().top
  const vw = window.innerWidth
  const header = 76
  const pad = 10
  const floatW = Math.min(168, Math.max(132, vw * 0.38))
  const floatH = floatW * (210 / 400) + 8
  const floatTop = header + 10
  const floatLeft = vw - floatW - pad

  const enter = Math.min(1, Math.max(0, (header + 36 - calcTop) / 64))
  const range = Math.max(sr.height * 1.8, 260)
  let t = 1 - Math.min(1, Math.max(0, (sr.top - floatTop) / range))
  t = t * t * (3 - 2 * t)

  const left = floatLeft + (sr.left - floatLeft) * t
  const top = floatTop + (sr.top - floatTop) * t
  const width = floatW + (sr.width - floatW) * t
  const height = floatH + (sr.height - floatH) * t
  const lift = 1 - t

  flyBox.value = {
    left: `${left}px`,
    top: `${top}px`,
    width: `${width}px`,
    height: `${height}px`,
    opacity: String(enter),
    boxShadow: `0 ${10 * lift}px ${26 * lift}px rgba(0, 0, 0, ${0.45 * lift})`,
  }
  sketchDocked.value = t > 0.97
  sketchReady.value = enter > 0.02
}

let sketchRo = null
onMounted(() => {
  scheduleSketchFly()
  window.addEventListener('scroll', scheduleSketchFly, { passive: true })
  window.addEventListener('resize', scheduleSketchFly)
  sketchRo = new ResizeObserver(scheduleSketchFly)
  if (sketchSlot.value) sketchRo.observe(sketchSlot.value)
})
onUnmounted(() => {
  window.removeEventListener('scroll', scheduleSketchFly)
  window.removeEventListener('resize', scheduleSketchFly)
  sketchRo?.disconnect()
  if (flyRaf) cancelAnimationFrame(flyRaf)
})
watch([mode, breakdownOpen], () => {
  nextTick(() => {
    if (sketchRo && sketchSlot.value) sketchRo.observe(sketchSlot.value)
    scheduleSketchFly()
  })
})

/* без отдельной навигации шагов — правый блок всегда в поле зрения */
</script>

<template>
  <main>
    <!-- ============ HERO ============ -->
    <section id="calc-hero" class="sec sec--dark page-hero clc-hero">
      <div class="container">
        <RouterLink to="/" class="page-back" v-reveal>← На главную</RouterLink>
        <div class="sec-head" v-reveal="60">
          <p class="sec-tag"><span class="idx">Онлайн</span> Калькулятор</p>
          <h1 class="page-title">Калькулятор стоимости <em>металло&shy;конструкций</em></h1>
          <p class="page-desc">
            Два режима: отдельные детали по массе или каркас объекта по габаритам.
            Соберите конфигурацию — получите ориентир цены и срока без звонка.
            Точный расчёт по чертежу технолог сделает бесплатно за 1 рабочий день.
          </p>
        </div>

        <div class="clc-hero-cta" v-reveal="140">
          <a href="#calculator" class="btn" :class="{ 'btn--ghost': mode === 'object' }" @click="setMode('details')">
            Детали и конструкции
          </a>
          <a href="#calculator" class="btn" :class="{ 'btn--ghost': mode === 'details' }" @click="setMode('object')">
            Объект целиком
          </a>
        </div>
      </div>
    </section>

    <!-- ============ КАЛЬКУЛЯТОР ============ -->
    <section id="calculator" class="sec sec--deep clc-sec">
      <div class="container">
        <div class="clc-modes" v-reveal role="tablist" aria-label="Режим калькулятора">
          <button
            class="clc-mode"
            :class="{ active: mode === 'details' }"
            role="tab"
            :aria-selected="mode === 'details'"
            @click="setMode('details')"
          >
            <span class="clc-mode-icon" aria-hidden="true">
              <svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <rect x="5" y="9" width="22" height="14" rx="1.5" />
                <circle cx="10" cy="14" r="1.6" /><circle cx="22" cy="14" r="1.6" />
                <circle cx="10" cy="19" r="1.6" /><circle cx="22" cy="19" r="1.6" />
              </svg>
            </span>
            <span class="clc-mode-body">
              <span class="clc-mode-title">Детали и конструкции</span>
              <span class="clc-mode-hint">Знаете массу или тип изделия — пластины, балки, фермы, лестницы</span>
            </span>
          </button>
          <button
            class="clc-mode"
            :class="{ active: mode === 'object' }"
            role="tab"
            :aria-selected="mode === 'object'"
            @click="setMode('object')"
          >
            <span class="clc-mode-icon" aria-hidden="true">
              <svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M4 26V12l12-7 12 7v14" /><path d="M4 26h24" /><path d="M10 26V15m6 11V12m6 14V15" />
              </svg>
            </span>
            <span class="clc-mode-body">
              <span class="clc-mode-title">Объект целиком</span>
              <span class="clc-mode-hint">Ангар, склад, навес или каркас здания — считаем по длине, ширине и высоте</span>
            </span>
          </button>
        </div>

        <div class="clc-layout">
          <!-- ЛЕВАЯ КОЛОНКА: ШАГИ -->
          <div class="clc-steps">
            <!-- ===== ДЕТАЛИ ===== -->
            <template v-if="mode === 'details'">
            <!-- ШАГ 1: тип -->
            <div id="step-type" class="clc-step" v-reveal>
              <p class="clc-step-tag"><span>{{ stepNo.type }}</span> Что изготовить</p>
              <div class="type-grid">
                <button
                  v-for="t in TYPES"
                  :key="t.id"
                  class="type-card"
                  :class="{ active: type.id === t.id }"
                  @click="type = t"
                >
                  <span class="type-icon" aria-hidden="true">
                    <svg v-if="t.icon === 'plate'" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                      <rect x="5" y="9" width="22" height="14" rx="1.5" /><circle cx="10" cy="14" r="1.6" /><circle cx="22" cy="14" r="1.6" /><circle cx="10" cy="19" r="1.6" /><circle cx="22" cy="19" r="1.6" />
                    </svg>
                    <svg v-else-if="t.icon === 'beam'" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M7 6h18M7 26h18M12 6v20M20 6v20" />
                    </svg>
                    <svg v-else-if="t.icon === 'frame'" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M4 26V12l12-7 12 7v14" /><path d="M4 26h24" /><path d="M10 26V15m6 11V12m6 14V15" />
                    </svg>
                    <svg v-else-if="t.icon === 'truss'" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M3 22h26M5 22l5-9h12l5 9" /><path d="M10 13l4 9m8-9-4 9m-4-9v9" />
                    </svg>
                    <svg v-else-if="t.icon === 'stairs'" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M5 27h6v-6h6v-6h6V9h6" /><path d="M5 27 29 3" opacity="0.4" />
                    </svg>
                    <svg v-else viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M8 10a8 4 0 0 1 16 0v12a8 4 0 0 1-16 0z" /><ellipse cx="16" cy="10" rx="8" ry="4" />
                    </svg>
                  </span>
                  <span class="type-label">{{ t.label }}</span>
                  <span class="type-hint">{{ t.hint }}</span>
                </button>
              </div>
            </div>

            <!-- ШАГ 2: масса -->
            <div id="step-mass" class="clc-step" v-reveal="60">
              <p class="clc-step-tag"><span>{{ stepNo.mass }}</span> Масса конструкции</p>
              <div class="mass-box">
                <div class="mass-head">
                  <div class="mass-input-wrap">
                    <input
                      class="mass-input"
                      type="text"
                      inputmode="decimal"
                      :value="mass"
                      @change="onMassInput"
                      aria-label="Масса в тоннах"
                    />
                    <span class="mass-unit">т</span>
                  </div>
                  <div class="mass-presets">
                    <button
                      v-for="p in massPresets"
                      :key="p"
                      class="mass-preset"
                      :class="{ active: mass === p }"
                      @click="mass = p"
                    >
                      {{ p }}
                    </button>
                  </div>
                </div>
                <input
                  v-model.number="massPos"
                  type="range"
                  min="0"
                  max="100"
                  step="0.5"
                  class="clc-slider"
                  aria-label="Масса конструкции"
                />
                <div class="mass-scale">
                  <span>100 кг</span><span>1 т</span><span>10 т</span><span>100 т</span>
                </div>

                <transition name="hint-slide" mode="out-in">
                  <p v-if="nextTier" class="mass-tip" :key="'next' + nextTier.pct">
                    <span class="tip-spark">%</span>
                    До скидки −{{ nextTier.pct }}% на работы не хватает {{ nextTier.need }} т
                  </p>
                  <p v-else-if="discountShare" class="mass-tip mass-tip--ok" key="max">
                    <span class="tip-spark">✓</span>
                    Применена максимальная скидка −{{ discountShare * 100 }}% на работы
                  </p>
                </transition>

                <p class="mass-help">
                  Не знаете массу? Она указана в спецификации КМ / КМД («ведомость металла»).
                  Нет чертежа — переключитесь на «Объект целиком» или <a href="#calc-form">пришлите эскиз</a>.
                </p>
              </div>
            </div>
            </template>

            <!-- ===== ОБЪЕКТ ===== -->
            <template v-if="mode === 'object'">
            <div id="step-kind" class="clc-step" v-reveal>
              <p class="clc-step-tag"><span>{{ stepNo.kind }}</span> Какой объект</p>
              <div class="type-grid">
                <button
                  v-for="k in BUILDING_KINDS"
                  :key="k.id"
                  class="type-card"
                  :class="{ active: bKind.id === k.id }"
                  @click="bKind = k"
                >
                  <span class="type-icon" aria-hidden="true">
                    <svg v-if="k.icon === 'canopy'" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M4 12c4-5 20-5 24 0" /><path d="M6 12v14m20-14v14" /><path d="M6 20h20" />
                    </svg>
                    <svg v-else-if="k.icon === 'hangar'" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M4 24V12l12-8 12 8v12" /><path d="M4 24h24" /><path d="M12 24v-8h8v8" />
                    </svg>
                    <svg v-else-if="k.icon === 'warm'" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M5 24V13l11-7 11 7v11" /><path d="M5 24h22" /><path d="M9 18h4m6 0h4M9 21h4m6 0h4" />
                    </svg>
                    <svg v-else-if="k.icon === 'shop'" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M4 25V12l12-7 12 7v13" /><path d="M4 25h24" /><path d="M8 16h16M16 16v9" />
                    </svg>
                    <svg v-else viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M4 26V12l12-7 12 7v14" /><path d="M4 26h24" /><path d="M10 26V15m6 11V12m6 14V15" />
                    </svg>
                  </span>
                  <span class="type-label">{{ k.label }}</span>
                  <span class="type-hint">{{ k.hint }}</span>
                </button>
              </div>
            </div>

            <div id="step-dim" class="clc-step" v-reveal="60">
              <p class="clc-step-tag"><span>{{ stepNo.dim }}</span> Габариты каркаса</p>
              <div class="dim-box">
                <div class="dim-controls">
                  <div class="dim-ctl">
                    <div class="dim-ctl-h">
                      <span>Длина</span>
                      <div class="mass-input-wrap">
                        <input
                          class="mass-input mass-input--sm"
                          type="text"
                          inputmode="decimal"
                          :value="bLength"
                          @change="onDimInput('l', $event)"
                          aria-label="Длина здания в метрах"
                        />
                        <span class="mass-unit">м</span>
                      </div>
                    </div>
                    <input
                      v-model.number="bLength"
                      type="range"
                      :min="DIM.l.min"
                      :max="DIM.l.max"
                      step="0.5"
                      class="clc-slider"
                      aria-label="Длина"
                    />
                    <div class="mass-scale"><span>{{ DIM.l.min }} м</span><span>{{ DIM.l.max }} м</span></div>
                  </div>

                  <div class="dim-ctl">
                    <div class="dim-ctl-h">
                      <span>Ширина · пролёт</span>
                      <div class="mass-input-wrap">
                        <input
                          class="mass-input mass-input--sm"
                          type="text"
                          inputmode="decimal"
                          :value="bWidth"
                          @change="onDimInput('w', $event)"
                          aria-label="Ширина здания в метрах"
                        />
                        <span class="mass-unit">м</span>
                      </div>
                    </div>
                    <input
                      v-model.number="bWidth"
                      type="range"
                      :min="DIM.w.min"
                      :max="DIM.w.max"
                      step="0.5"
                      class="clc-slider"
                      aria-label="Ширина"
                    />
                    <div class="mass-scale"><span>{{ DIM.w.min }} м</span><span>{{ DIM.w.max }} м</span></div>
                  </div>

                  <div class="dim-ctl">
                    <div class="dim-ctl-h">
                      <span>Высота до низа ферм</span>
                      <div class="mass-input-wrap">
                        <input
                          class="mass-input mass-input--sm"
                          type="text"
                          inputmode="decimal"
                          :value="bHeight"
                          @change="onDimInput('h', $event)"
                          aria-label="Высота здания в метрах"
                        />
                        <span class="mass-unit">м</span>
                      </div>
                    </div>
                    <input
                      v-model.number="bHeight"
                      type="range"
                      :min="DIM.h.min"
                      :max="DIM.h.max"
                      step="0.5"
                      class="clc-slider"
                      aria-label="Высота"
                    />
                    <div class="mass-scale"><span>{{ DIM.h.min }} м</span><span>{{ DIM.h.max }} м</span></div>
                  </div>

                  <div class="mass-presets dim-presets">
                    <button
                      v-for="p in DIM_PRESETS"
                      :key="p.label"
                      class="mass-preset"
                      :class="{ active: dimPresetActive && dimPresetActive.label === p.label }"
                      @click="applyPreset(p)"
                    >
                      {{ p.label }}
                    </button>
                  </div>
                </div>
              </div>
              <p class="mass-help dim-help">
                Цена считается по объёму здания (длина × ширина × высота): чем выше каркас, тем больше колонн, связей и металла.
                В ориентир заложены металл, грунт и фундамент. Сэндвич, КМД, монтаж и доставка — в точном расчёте.
              </p>
              <transition name="hint-slide" mode="out-in">
                <p v-if="nextTier" class="mass-tip" :key="'onext' + nextTier.pct">
                  <span class="tip-spark">%</span>
                  До скидки −{{ nextTier.pct }}% на работы не хватает {{ nextTier.need }} т каркаса
                </p>
                <p v-else-if="discountShare" class="mass-tip mass-tip--ok" key="omax">
                  <span class="tip-spark">✓</span>
                  Применена скидка −{{ discountShare * 100 }}% на работы
                </p>
              </transition>
            </div>

            <div id="step-extra" class="clc-step" v-reveal="60">
              <p class="clc-step-tag"><span>{{ stepNo.extra }}</span> Что влияет на каркас</p>

              <p class="extra-label extra-label--first">Кровля</p>
              <div class="coat-row coat-row--3">
                <button
                  v-for="r in ROOFS"
                  :key="r.id"
                  class="coat-btn"
                  :class="{ active: bRoof.id === r.id }"
                  @click="bRoof = r"
                >
                  <span class="coat-label">{{ r.label }}</span>
                </button>
              </div>

              <p class="extra-label">Крановое оборудование</p>
              <div class="coat-row">
                <button
                  v-for="c in CRANES"
                  :key="c.id"
                  class="coat-btn"
                  :class="{ active: bCrane.id === c.id }"
                  @click="bCrane = c"
                >
                  <span class="coat-label">{{ c.label }}</span>
                  <span class="coat-note">{{ c.note }}</span>
                </button>
              </div>

              <p class="extra-label">Снеговой район</p>
              <SnowRegionPicker v-model="bRegion" :snow-note="bSnow.note" />
              <p class="mass-help dim-help">Район берётся по центру выбранного субъекта — СП 20.13330. На конкретной площадке может быть соседний район.</p>

              <p class="extra-label">Шаг колонн</p>
              <div class="coat-row coat-row--3">
                <button
                  v-for="s in COL_STEPS"
                  :key="s.id"
                  class="coat-btn"
                  :class="{ active: bStep.id === s.id }"
                  @click="bStep = s"
                >
                  <span class="coat-label">{{ s.label }}</span>
                  <span class="coat-note">{{ s.note }}</span>
                </button>
              </div>

              <p class="extra-label">Фундамент</p>
              <div class="coat-row">
                <button
                  v-for="f in FOUNDATIONS"
                  :key="f.id"
                  class="coat-btn"
                  :class="{ active: bFound.id === f.id }"
                  @click="bFound = f"
                >
                  <span class="coat-label">{{ f.label }}</span>
                  <span class="coat-note">{{ f.note }}</span>
                </button>
              </div>
              <p class="mass-help dim-help">Ориентир по железобетону на площадь здания. Точный тип и объём бетона считает конструктор по грунтам площадки.</p>

              <div class="opt-list extra-opts">
                <label class="opt" :class="{ active: bMezzanine }">
                  <input type="checkbox" v-model="bMezzanine" />
                  <span class="opt-check" aria-hidden="true"></span>
                  <span class="opt-body">
                    <span class="opt-title">Антресоль / перекрытие</span>
                    <span class="opt-note">добавляет балки и настил в каркас</span>
                  </span>
                  <span class="opt-price">+16 кг/м²</span>
                </label>
                <label class="opt" :class="{ active: bStairs }">
                  <input type="checkbox" v-model="bStairs" />
                  <span class="opt-check" aria-hidden="true"></span>
                  <span class="opt-body">
                    <span class="opt-title">Лестницы и площадки</span>
                    <span class="opt-note">обслуживающие марши в составе каркаса</span>
                  </span>
                  <span class="opt-price">+6% к массе</span>
                </label>
              </div>
            </div>
            </template>

            <template v-if="mode === 'details'">
            <!-- ШАГ: металл -->
            <div id="step-metal" class="clc-step" v-reveal="60">
              <p class="clc-step-tag"><span>{{ stepNo.metal }}</span> Чей металл</p>
              <div class="seg">
                <button class="seg-btn" :class="{ active: !ownMetal }" @click="ownMetal = false">
                  <span class="seg-title">Ваш металл — наша забота</span>
                  <span class="seg-note">закупим сами и включим в смету</span>
                </button>
                <button class="seg-btn" :class="{ active: ownMetal }" @click="ownMetal = true">
                  <span class="seg-title">Металл заказчика</span>
                  <span class="seg-note">давальческое сырьё, примем по накладной</span>
                </button>
              </div>
            </div>

            <!-- ШАГ 4: покрытие -->
            <div id="step-coating" class="clc-step" v-reveal="60">
              <p class="clc-step-tag"><span>{{ stepNo.coat }}</span> Покрытие</p>
              <div class="coat-row">
                <button
                  v-for="c in COATINGS"
                  :key="c.id"
                  class="coat-btn"
                  :class="{ active: coating.id === c.id }"
                  @click="coating = c"
                >
                  <span class="coat-label">{{ c.label }}</span>
                  <span class="coat-note">{{ c.note }}</span>
                </button>
              </div>
            </div>

            <!-- ШАГ 5: опции -->
            <div id="step-options" class="clc-step" v-reveal="60">
              <p class="clc-step-tag"><span>{{ stepNo.opt }}</span> Дополнительно</p>
              <div class="opt-list">
                <label class="opt" :class="{ active: needKmd }">
                  <input type="checkbox" v-model="needKmd" />
                  <span class="opt-check" aria-hidden="true"></span>
                  <span class="opt-body">
                    <span class="opt-title">Разработка КМД</span>
                    <span class="opt-note">деталировочные чертежи по вашему КМ</span>
                  </span>
                  <span class="opt-price">+{{ RATES.kmdShare * 100 }}% к работам</span>
                </label>

                <label class="opt" :class="{ active: needMontage }">
                  <input type="checkbox" v-model="needMontage" />
                  <span class="opt-check" aria-hidden="true"></span>
                  <span class="opt-body">
                    <span class="opt-title">Монтаж с окраской</span>
                    <span class="opt-note">Нижегородская область, своя бригада</span>
                  </span>
                  <span class="opt-price">+{{ fmt(RATES.montagePerTonne) }} ₽/т</span>
                </label>

                <label class="opt" :class="{ active: urgent }">
                  <input type="checkbox" v-model="urgent" />
                  <span class="opt-check" aria-hidden="true"></span>
                  <span class="opt-body">
                    <span class="opt-title">Срочное изготовление</span>
                    <span class="opt-note">встроим вне очереди, срок короче</span>
                  </span>
                  <span class="opt-price">+{{ RATES.urgentShare * 100 }}% к работам</span>
                </label>
              </div>
            </div>

            <!-- ШАГ 6: доставка -->
            <div id="step-delivery" class="clc-step" v-reveal="60">
              <p class="clc-step-tag"><span>{{ stepNo.del }}</span> Доставка</p>
              <div class="coat-row">
                <button
                  v-for="d in DELIVERY"
                  :key="d.id"
                  class="coat-btn"
                  :class="{ active: delivery.id === d.id }"
                  @click="delivery = d"
                >
                  <span class="coat-label">{{ d.label }}</span>
                  <span class="coat-note">{{ d.note }}</span>
                </button>
              </div>
            </div>
            </template>
          </div>

          <!-- ПРАВАЯ КОЛОНКА: ИТОГ -->
          <aside class="clc-panel-wrap">
            <div class="clc-panel" :class="{ 'clc-panel--object': mode === 'object' }" v-reveal="120">
              <div v-if="mode === 'object'" class="panel-visual">
                <div
                  ref="sketchSlot"
                  class="panel-sketch"
                  :class="{ 'panel-sketch--ghost': sketchMobile }"
                >
                  <BuildingPreview
                    v-if="!sketchMobile"
                    compact
                    :length="bLength"
                    :width="bWidth"
                    :height="bHeight"
                    :roof="bRoof.id"
                    :crane="bCrane.id"
                    :col-step="bStep.id"
                    :mezzanine="bMezzanine"
                    :stairs="bStairs"
                    :foundation="bFound.id"
                  />
                </div>
                <div class="panel-stats">
                  <div><b>{{ fmt(buildingArea) }}</b><span>м²</span></div>
                  <div><b>{{ fmt(buildingVolume) }}</b><span>м³</span></div>
                  <div><b>{{ buildingMass }} т</b><span>{{ fmtQ(buildingQ) }} кг/м³</span></div>
                </div>
              </div>

              <p class="panel-tag">{{ mode === 'object' ? 'Ориентир каркаса и фундамента' : 'Ориентир стоимости' }}</p>

              <p class="panel-price">
                <span class="pp-num">{{ fmt(shownLow) }}</span>
                <span class="pp-dash">—</span>
                <span class="pp-num">{{ fmt(shownHigh) }}</span>
                <span class="pp-rub">₽</span>
              </p>
              <p class="panel-per" v-if="mode === 'object'">
                ≈ {{ fmt(calc.perCub) }} ₽/м³ · каркас, грунт и фундамент
              </p>
              <p class="panel-per" v-else>
                ≈ {{ fmt(calc.perTonne) }} ₽/т · с учётом всех выбранных опций
              </p>

              <div class="panel-time">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="9" /><path d="M12 7v5l3 3" />
                </svg>
                <span>Срок изготовления: <b>{{ leadTime }}</b></span>
              </div>

              <button class="panel-toggle" @click="breakdownOpen = !breakdownOpen" :aria-expanded="breakdownOpen">
                Из чего складывается
                <span class="pt-arrow" :class="{ open: breakdownOpen }">▾</span>
              </button>

              <div class="breakdown" :class="{ open: breakdownOpen }">
                <div class="breakdown-in">
                  <p v-if="mode === 'object'" class="bd-row">
                    <span>Каркас {{ fmtM(bLength) }}×{{ fmtM(bWidth) }}×{{ fmtM(bHeight) }} м</span>
                    <b>{{ buildingMass }} т</b>
                  </p>
                  <p class="bd-row"><span>Работы ({{ activeType.label.toLowerCase() }})</span><b>{{ fmt(calc.work) }} ₽</b></p>
                  <p v-if="calc.material" class="bd-row"><span>Металл</span><b>{{ fmt(calc.material) }} ₽</b></p>
                  <p v-if="calc.coat" class="bd-row"><span>{{ activeCoating.label }}</span><b>{{ fmt(calc.coat) }} ₽</b></p>
                  <p v-if="calc.kmd" class="bd-row"><span>КМД</span><b>{{ fmt(calc.kmd) }} ₽</b></p>
                  <p v-if="calc.montage" class="bd-row"><span>Монтаж с окраской</span><b>{{ fmt(calc.montage) }} ₽</b></p>
                  <p v-if="calc.urgentFee" class="bd-row"><span>Срочность</span><b>{{ fmt(calc.urgentFee) }} ₽</b></p>
                  <p v-if="calc.discount" class="bd-row bd-row--ok"><span>Скидка за объём −{{ discountShare * 100 }}%</span><b>−{{ fmt(calc.discount) }} ₽</b></p>
                  <p v-if="calc.foundation" class="bd-row"><span>Фундамент · {{ bFound.label.toLowerCase() }}</span><b>{{ fmt(calc.foundation) }} ₽</b></p>
                  <p v-if="mode === 'details'" class="bd-row"><span>Доставка</span><b>{{ delivery.external ? 'по тарифу ТК' : calc.deliveryCost ? fmt(calc.deliveryCost) + ' ₽' : 'бесплатно' }}</b></p>
                  <p class="bd-row bd-row--vat"><span>В том числе НДС 20%</span><b>{{ fmt(calc.vat) }} ₽</b></p>
                </div>
              </div>

              <a href="#calc-form" class="btn btn--block panel-btn">Получить точный расчёт</a>
              <p class="panel-note">
                Это ориентир, а не оферта: точная цена зависит от чертежа КМ и текущей цены металла.
                <template v-if="mode === 'object'">
                  Заложены наш металл, грунт и фундамент (ориентир ЖБ). Без сэндвича, КМД, монтажа и доставки.
                </template>
                Технолог посчитает бесплатно — за 1 рабочий день.
              </p>
            </div>
          </aside>
        </div>
      </div>

      <!-- мобильная плашка с итогом -->
      <a href="#calc-form" class="clc-mobilebar">
        <span class="mb-price">{{ fmt(shownLow) }} — {{ fmt(shownHigh) }} ₽</span>
        <span class="mb-cta">Точный расчёт →</span>
      </a>
    </section>

    <!-- ============ ФОРМА ============ -->
    <section id="calc-form" class="sec sec--dark">
      <div class="container clc-form-grid">
        <div class="clc-form-left" v-reveal>
          <p class="sec-tag"><span class="idx">Финал</span> Точный расчёт</p>
          <h2 class="sec-title">Конфигурация уже в заявке — <em>допишите только телефон</em></h2>
          <p class="sec-sub">
            Всё, что вы выбрали в калькуляторе, мы приложим к заявке автоматически.
            Технолог проверит расчёт по вашему чертежу и пришлёт точную смету.
          </p>

          <div class="recap" v-reveal="80">
            <p class="recap-h">Что уйдёт вместе с заявкой:</p>
            <ul v-if="mode === 'object'">
              <li><span>Объект</span>{{ bKind.label }}</li>
              <li><span>Габариты</span>{{ fmtM(bLength) }} × {{ fmtM(bWidth) }} × {{ fmtM(bHeight) }} м</li>
              <li><span>Площадь</span>{{ fmt(buildingArea) }} м²</li>
              <li><span>Объём</span>{{ fmt(buildingVolume) }} м³</li>
              <li><span>Каркас</span>{{ buildingMass }} т · {{ fmtQ(buildingQ) }} кг/м³</li>
              <li><span>Кровля</span>{{ bRoof.label }}</li>
              <li><span>Кран</span>{{ bCrane.label }}</li>
              <li><span>Фундамент</span>{{ bFound.label }}</li>
              <li><span>Регион</span>{{ SNOW_REGIONS[bRegion]?.title }}</li>
              <li><span>Снег</span>район {{ bSnow.id }} · {{ bSnow.note }}</li>
              <li v-if="bMezzanine || bStairs">
                <span>В каркасе</span>{{ [bMezzanine && 'антресоль', bStairs && 'лестницы'].filter(Boolean).join(', ') }}
              </li>
              <li class="recap-total"><span>Ориентир</span>{{ fmt(calc.low) }} – {{ fmt(calc.high) }} ₽</li>
            </ul>
            <ul v-else>
              <li><span>Тип</span>{{ type.label }}</li>
              <li><span>Масса</span>{{ mass }} т</li>
              <li><span>Металл</span>{{ ownMetal ? 'заказчика' : 'наш' }}</li>
              <li><span>Покрытие</span>{{ coating.label }}</li>
              <li v-if="needKmd || needMontage || urgent">
                <span>Опции</span>{{ [needKmd && 'КМД', needMontage && 'монтаж', urgent && 'срочно'].filter(Boolean).join(', ') }}
              </li>
              <li><span>Доставка</span>{{ delivery.label }}</li>
              <li class="recap-total"><span>Ориентир</span>{{ fmt(calc.low) }} – {{ fmt(calc.high) }} ₽</li>
            </ul>
          </div>
        </div>

        <div class="clc-form-card" v-reveal="140">
          <LeadForm extended button-text="Отправить на точный расчёт" :comment-prefix="summary">
            Пришлём смету в течение рабочего дня. Ни к чему не обязывает.
          </LeadForm>
        </div>
      </div>
    </section>

    <Teleport to="body">
      <div
        v-if="mode === 'object' && sketchMobile && sketchReady && flyBox"
        class="sketch-fly"
        :class="{ 'sketch-fly--docked': sketchDocked }"
        :style="flyBox"
        aria-hidden="true"
      >
        <BuildingPreview
          compact
          :length="bLength"
          :width="bWidth"
          :height="bHeight"
          :roof="bRoof.id"
          :crane="bCrane.id"
          :col-step="bStep.id"
          :mezzanine="bMezzanine"
          :stairs="bStairs"
          :foundation="bFound.id"
        />
      </div>
    </Teleport>
  </main>
</template>

<style scoped>
/* ============ hero ============ */
.clc-hero { padding-bottom: 56px; }
.clc-hero-cta {
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
  margin-top: 8px;
}

/* ============ режимы ============ */
.clc-modes {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 40px;
  scroll-margin-top: 140px;
}
.clc-mode {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 20px 22px;
  background: var(--card-d);
  border: 1px solid var(--line-d);
  border-radius: var(--r);
  text-align: left;
  color: var(--white);
  transition: border-color 0.25s, background 0.25s, box-shadow 0.25s;
}
.clc-mode:hover { border-color: rgba(255, 90, 31, 0.5); }
.clc-mode.active {
  border-color: var(--acc);
  background: linear-gradient(160deg, rgba(255, 90, 31, 0.14), var(--card-d) 55%);
  box-shadow: 0 16px 36px rgba(255, 90, 31, 0.1);
}
.clc-mode-icon {
  width: 44px;
  height: 44px;
  flex-shrink: 0;
  display: grid;
  place-items: center;
  border-radius: 11px;
  background: var(--acc-dim);
  color: var(--acc-hot);
  transition: background 0.25s, color 0.25s;
}
.clc-mode.active .clc-mode-icon { background: var(--acc); color: #fff; }
.clc-mode-icon svg { width: 24px; height: 24px; }
.clc-mode-body { display: flex; flex-direction: column; gap: 4px; min-width: 0; }
.clc-mode-title {
  font-family: var(--font-d);
  font-size: 13px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.02em;
}
.clc-mode-hint {
  font-size: 13px;
  line-height: 1.45;
  color: var(--w-faint);
}

/* ============ layout ============ */
.clc-sec { padding-top: 72px; overflow: visible; }

.clc-layout {
  display: grid;
  grid-template-columns: 1fr 380px;
  gap: 40px;
  align-items: start;
  min-width: 0;
}
.clc-steps,
.clc-panel-wrap {
  min-width: 0;
}

/* ============ шаги ============ */
.clc-steps { display: flex; flex-direction: column; gap: 32px; }

/* якорная прокрутка не прячет заголовок шага под липкой навигацией */
.clc-step { scroll-margin-top: 140px; }

.clc-step-tag {
  display: flex;
  align-items: center;
  gap: 12px;
  font-family: var(--font-m);
  font-size: 12px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--w-soft);
  margin-bottom: 14px;
}
.clc-step-tag span {
  font-family: var(--font-d);
  font-size: 15px;
  font-weight: 900;
  color: transparent;
  -webkit-text-stroke: 1px var(--acc);
}

/* тип конструкции — компактные горизонтальные карточки */
.type-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}
.type-card {
  display: grid;
  grid-template-columns: 38px 1fr;
  grid-template-rows: auto auto;
  column-gap: 12px;
  row-gap: 2px;
  align-items: center;
  padding: 12px 16px;
  background: var(--card-d);
  border: 1px solid var(--line-d);
  border-radius: var(--r-sm);
  text-align: left;
  color: var(--white);
  transition: border-color 0.25s, background 0.25s;
}
.type-card:hover { border-color: rgba(255, 90, 31, 0.5); }
.type-card.active {
  border-color: var(--acc);
  background: linear-gradient(160deg, rgba(255, 90, 31, 0.12), var(--card-d) 55%);
}
.type-icon {
  grid-row: 1 / 3;
  width: 38px;
  height: 38px;
  display: grid;
  place-items: center;
  border-radius: 9px;
  background: var(--acc-dim);
  color: var(--acc-hot);
  transition: background 0.25s, color 0.25s;
}
.type-card.active .type-icon { background: var(--acc); color: #fff; }
.type-icon svg { width: 21px; height: 21px; }
.type-label {
  font-family: var(--font-d);
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  line-height: 1.25;
}
.type-hint { font-size: 11.5px; color: var(--w-faint); line-height: 1.4; }

/* масса */
.mass-box {
  background: var(--card-d);
  border: 1px solid var(--line-d);
  border-radius: var(--r);
  padding: 22px 22px 18px;
}
.mass-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
  flex-wrap: wrap;
  margin-bottom: 16px;
}
.mass-input-wrap {
  display: flex;
  align-items: baseline;
  gap: 8px;
}
.mass-input {
  width: 110px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--line-d);
  border-radius: var(--r-sm);
  color: var(--acc-hot);
  font-family: var(--font-d);
  font-size: 26px;
  font-weight: 700;
  padding: 8px 14px;
  text-align: center;
  transition: border-color 0.25s;
}
.mass-input:focus { outline: none; border-color: var(--acc); }
.mass-input--sm { width: 88px; font-size: 20px; padding: 6px 10px; }
.mass-unit {
  font-family: var(--font-d);
  font-size: 18px;
  font-weight: 700;
  color: var(--w-soft);
}
.mass-presets { display: flex; gap: 6px; flex-wrap: wrap; }
.mass-preset {
  min-width: 44px;
  padding: 8px 10px;
  background: transparent;
  border: 1px solid var(--line-d);
  border-radius: 7px;
  color: var(--w-soft);
  font-family: var(--font-m);
  font-size: 12.5px;
  transition: all 0.2s;
}
.mass-preset:hover { border-color: rgba(255, 90, 31, 0.5); color: var(--white); }
.mass-preset.active { background: var(--acc); border-color: var(--acc); color: #fff; }

.clc-slider {
  width: 100%;
  height: 4px;
  appearance: none;
  -webkit-appearance: none;
  background: rgba(255, 255, 255, 0.12);
  border-radius: 2px;
  outline: none;
  cursor: pointer;
}
.clc-slider::-webkit-slider-thumb {
  appearance: none;
  -webkit-appearance: none;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: var(--acc);
  border: 3px solid var(--bg0);
  box-shadow: 0 0 0 1.5px var(--acc), 0 0 22px rgba(255, 90, 31, 0.55);
  transition: transform 0.2s;
}
.clc-slider::-webkit-slider-thumb:hover { transform: scale(1.15); }
.clc-slider::-moz-range-thumb {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: var(--acc);
  border: 3px solid var(--bg0);
  box-shadow: 0 0 0 1.5px var(--acc), 0 0 22px rgba(255, 90, 31, 0.55);
}

.mass-scale {
  display: flex;
  justify-content: space-between;
  margin-top: 8px;
  font-family: var(--font-m);
  font-size: 10.5px;
  color: var(--w-faint);
}

.mass-tip {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 18px;
  padding: 11px 16px;
  border-radius: var(--r-sm);
  background: var(--acc-dim);
  border: 1px dashed rgba(255, 90, 31, 0.4);
  font-size: 13px;
  color: var(--acc-hot);
}
.mass-tip--ok {
  background: rgba(53, 201, 126, 0.08);
  border-color: rgba(53, 201, 126, 0.4);
  color: var(--ok);
}
.tip-spark {
  font-family: var(--font-d);
  font-weight: 900;
  font-size: 13px;
}

.hint-slide-enter-active, .hint-slide-leave-active { transition: opacity 0.25s, transform 0.25s; }
.hint-slide-enter-from, .hint-slide-leave-to { opacity: 0; transform: translateY(-4px); }

.mass-help {
  margin-top: 14px;
  font-size: 12.5px;
  line-height: 1.6;
  color: var(--w-faint);
}
.mass-help a { color: var(--acc-hot); text-decoration: underline; text-underline-offset: 2px; }

/* габариты объекта */
.dim-box {
  background: var(--card-d);
  border: 1px solid var(--line-d);
  border-radius: var(--r);
  padding: 22px 22px 18px;
}
.dim-controls {
  display: flex;
  flex-direction: column;
  gap: 14px;
  min-width: 0;
}
.dim-ctl-h {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 8px;
  font-size: 13px;
  font-weight: 600;
  color: var(--w-soft);
}
.dim-presets { margin-top: 2px; }

.extra-label {
  margin: 16px 0 8px;
  font-family: var(--font-m);
  font-size: 11px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--w-faint);
}
.extra-label:first-child { margin-top: 0; }
.extra-label--first { margin-top: 0; }
.extra-opts { margin-top: 14px; }
.dim-help { margin-top: 12px; }
.coat-row--3 { grid-template-columns: repeat(3, 1fr); }

/* сегменты (металл) */
.seg { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.seg-btn {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 18px 20px;
  background: var(--card-d);
  border: 1px solid var(--line-d);
  border-radius: var(--r-sm);
  text-align: left;
  color: var(--white);
  transition: border-color 0.25s, background 0.25s;
}
.seg-btn:hover { border-color: rgba(255, 90, 31, 0.5); }
.seg-btn.active {
  border-color: var(--acc);
  background: linear-gradient(160deg, rgba(255, 90, 31, 0.12), var(--card-d) 60%);
}
.seg-title { font-weight: 700; font-size: 14.5px; }
.seg-note { font-size: 12.5px; color: var(--w-faint); }

/* покрытие / доставка */
.coat-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}
.coat-btn {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 15px 18px;
  background: var(--card-d);
  border: 1px solid var(--line-d);
  border-radius: var(--r-sm);
  text-align: left;
  color: var(--white);
  transition: border-color 0.25s, background 0.25s;
}
.coat-btn:hover { border-color: rgba(255, 90, 31, 0.5); }
.coat-btn.active {
  border-color: var(--acc);
  background: linear-gradient(160deg, rgba(255, 90, 31, 0.12), var(--card-d) 60%);
}
.coat-label { font-weight: 700; font-size: 14px; }
.coat-note { font-size: 12px; color: var(--w-faint); }

/* опции */
.opt-list { display: flex; flex-direction: column; gap: 10px; }
.opt {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 20px;
  background: var(--card-d);
  border: 1px solid var(--line-d);
  border-radius: var(--r-sm);
  cursor: pointer;
  transition: border-color 0.25s, background 0.25s;
}
.opt:hover { border-color: rgba(255, 90, 31, 0.5); }
.opt.active {
  border-color: var(--acc);
  background: linear-gradient(160deg, rgba(255, 90, 31, 0.1), var(--card-d) 60%);
}
.opt input { display: none; }
.opt-check {
  position: relative;
  width: 22px;
  height: 22px;
  flex-shrink: 0;
  border: 1.5px solid var(--line-d);
  border-radius: 6px;
  transition: all 0.25s;
}
.opt.active .opt-check {
  background: var(--acc);
  border-color: var(--acc);
}
.opt.active .opt-check::after {
  content: '';
  position: absolute;
  top: 4px;
  left: 7px;
  width: 5px;
  height: 9px;
  border: solid #fff;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}
.opt-body { flex: 1; display: flex; flex-direction: column; gap: 2px; }
.opt-title { font-weight: 700; font-size: 14.5px; }
.opt-note { font-size: 12.5px; color: var(--w-faint); }
.opt-price {
  font-family: var(--font-m);
  font-size: 12px;
  color: var(--w-soft);
  white-space: nowrap;
}
.opt.active .opt-price { color: var(--acc-hot); }

/* ============ панель итога (sticky до конца секции) ============ */
.clc-panel-wrap {
  position: sticky;
  top: 100px; /* фикс шапки (липнуть чуть позже) */
  align-self: start;
  z-index: 10;
}

.clc-panel {
  position: static;
  background:
    radial-gradient(ellipse at top right, rgba(255, 90, 31, 0.13), transparent 55%),
    var(--card-d);
  border: 1px solid rgba(255, 90, 31, 0.3);
  border-radius: var(--r);
  padding: 30px 28px;
}
.clc-panel--object {
  padding: 16px 16px 20px;
}
.clc-panel--object .panel-tag { margin-bottom: 10px; }
.clc-panel--object .panel-per { margin-bottom: 12px; }
.clc-panel--object .panel-time { margin-bottom: 12px; }
.clc-panel--object .pp-num { font-size: clamp(18px, 1.8vw, 22px); }

.panel-visual { margin-bottom: 16px; }
.panel-sketch {
  background: rgba(0, 0, 0, 0.28);
  border: 1px solid var(--line-d);
  border-radius: var(--r-sm);
  padding: 4px 2px 0;
  margin-bottom: 10px;
}
.panel-sketch--ghost {
  aspect-ratio: 400 / 218;
  min-height: 118px;
  pointer-events: none;
}

.sketch-fly {
  position: fixed;
  z-index: 45;
  margin: 0;
  padding: 4px 2px 0;
  overflow: hidden;
  pointer-events: none;
  background: rgba(0, 0, 0, 0.42);
  border: 1px solid rgba(255, 90, 31, 0.4);
  border-radius: var(--r-sm);
  backdrop-filter: blur(10px);
}
.sketch-fly :deep(.sketch) {
  display: block;
  width: 100%;
  height: 100%;
}
.sketch-fly--docked {
  z-index: 12;
  background: rgba(0, 0, 0, 0.28);
  border-color: var(--line-d);
  backdrop-filter: none;
}
.panel-stats {
  display: grid;
  grid-template-columns: 1fr 1fr 1.15fr;
  gap: 6px;
}
.panel-stats div {
  display: flex;
  flex-direction: column;
  gap: 1px;
  padding: 8px 8px 7px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.04);
  min-width: 0;
}
.panel-stats b {
  font-family: var(--font-d);
  font-size: 13px;
  font-weight: 700;
  color: var(--white);
  font-variant-numeric: tabular-nums;
  white-space: nowrap;
}
.panel-stats span {
  font-size: 10.5px;
  color: var(--w-faint);
  line-height: 1.3;
}

.panel-tag {
  font-family: var(--font-m);
  font-size: 11px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--acc);
  margin-bottom: 14px;
}

.panel-price {
  display: flex;
  align-items: baseline;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 6px;
}
.pp-num {
  font-family: var(--font-d);
  font-size: clamp(21px, 2vw, 25px);
  font-weight: 900;
  color: var(--white);
  white-space: nowrap;
  font-variant-numeric: tabular-nums;
}
.pp-dash { color: var(--w-faint); }
.pp-rub {
  font-family: var(--font-d);
  font-size: 19px;
  font-weight: 700;
  color: var(--acc-hot);
}

.panel-per {
  font-family: var(--font-m);
  font-size: 11.5px;
  color: var(--w-faint);
  margin-bottom: 20px;
}

.panel-time {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  border-radius: var(--r-sm);
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid var(--line-d);
  font-size: 13.5px;
  color: var(--w-soft);
  margin-bottom: 18px;
}
.panel-time svg { width: 18px; height: 18px; color: var(--acc-hot); flex-shrink: 0; }
.panel-time b { color: var(--white); }

.panel-toggle {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  padding: 12px 0;
  background: none;
  border: none;
  border-top: 1px dashed var(--line-d);
  color: var(--w-soft);
  font-size: 13.5px;
  font-weight: 600;
  transition: color 0.2s;
}
.panel-toggle:hover { color: var(--white); }
.pt-arrow { transition: transform 0.3s var(--ease); }
.pt-arrow.open { transform: rotate(180deg); }

.breakdown {
  display: grid;
  grid-template-rows: 0fr;
  transition: grid-template-rows 0.4s var(--ease);
}
.breakdown.open { grid-template-rows: 1fr; }
.breakdown-in { overflow: hidden; }
.breakdown.open .breakdown-in { padding-bottom: 14px; }

.bd-row {
  display: flex;
  justify-content: space-between;
  gap: 14px;
  padding: 6px 0;
  font-size: 13px;
  color: var(--w-soft);
}
.bd-row b { font-variant-numeric: tabular-nums; color: var(--white); font-weight: 600; white-space: nowrap; }
.bd-row--ok, .bd-row--ok b { color: var(--ok); }
.bd-row--vat {
  margin-top: 8px;
  padding-top: 10px;
  border-top: 1px dashed var(--line-d);
  color: var(--w-faint);
}
.bd-row--vat b { color: var(--w-soft); }

.panel-btn { margin-top: 8px; }
.panel-note {
  margin-top: 14px;
  font-size: 12px;
  line-height: 1.6;
  color: var(--w-faint);
}

/* мобильная плашка */
.clc-mobilebar { display: none; }

/* ============ форма ============ */
.clc-form-grid {
  display: grid;
  grid-template-columns: 1.1fr 0.9fr;
  gap: 56px;
  align-items: start;
}

.recap {
  margin-top: 30px;
  border: 1px solid var(--line-d);
  border-radius: var(--r);
  padding: 22px 26px;
  background: var(--card-d);
}
.recap-h {
  font-family: var(--font-m);
  font-size: 11px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--acc);
  margin-bottom: 12px;
}
.recap li {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  padding: 7px 0;
  border-bottom: 1px dashed var(--line-d);
  font-size: 13.5px;
  color: var(--white);
}
.recap li:last-child { border-bottom: none; }
.recap li span {
  font-family: var(--font-m);
  font-size: 11.5px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--w-faint);
}
.recap-total { font-weight: 700; color: var(--acc-hot) !important; }

.clc-form-card {
  background: var(--card-d);
  border: 1px solid var(--line-d);
  border-radius: var(--r);
  padding: 30px 28px;
}

/* ============ адаптив ============ */
@media (max-width: 1060px) {
  .clc-layout { grid-template-columns: 1fr 330px; gap: 28px; }
  .type-grid { grid-template-columns: repeat(2, 1fr); }
}

@media (max-width: 900px) {
  .clc-layout { grid-template-columns: 1fr; }
  .clc-panel-wrap { position: static; }
  .clc-step { scroll-margin-top: 126px; }
  .clc-form-grid { grid-template-columns: 1fr; gap: 36px; }
  .clc-modes { grid-template-columns: 1fr; }

  .clc-mobilebar {
    position: fixed;
    left: 12px;
    right: 12px;
    bottom: 12px;
    z-index: 60;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 14px;
    padding: 14px 20px;
    border-radius: var(--r-sm);
    background: rgba(11, 14, 17, 0.92);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 90, 31, 0.45);
    box-shadow: 0 12px 34px rgba(0, 0, 0, 0.45);
  }
  .mb-price {
    font-family: var(--font-d);
    font-size: 13.5px;
    font-weight: 700;
    color: var(--white);
    font-variant-numeric: tabular-nums;
  }
  .mb-cta {
    font-size: 13px;
    font-weight: 700;
    color: var(--acc-hot);
    white-space: nowrap;
  }
}

@media (max-width: 560px) {
  .type-grid { grid-template-columns: 1fr; }
  .seg { grid-template-columns: 1fr; }
  .coat-row { grid-template-columns: 1fr; }
  .coat-row--3 { grid-template-columns: 1fr; }
  .mass-box { padding: 20px 16px 18px; }
  .opt { flex-wrap: wrap; }
  .opt-price { width: 100%; padding-left: 38px; }
  .clc-mode { padding: 16px 16px; }
  .dim-box { padding: 16px 16px 14px; }
  .panel-stats { grid-template-columns: 1fr 1fr 1fr; }
}
</style>
