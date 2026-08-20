<script setup>
import { ref, computed, watch } from 'vue'
import LeadForm from '../components/ui/LeadForm.vue'

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

/* ---------- состояние ---------- */
const type = ref(TYPES[2])
const mass = ref(3)
const ownMetal = ref(false) // false = наш металл, true = давальческий
const coating = ref(COATINGS[1])
const needKmd = ref(false)
const needMontage = ref(false)
const urgent = ref(false)
const delivery = ref(DELIVERY[0])

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

/* ---------- скидка за объём ---------- */
const discountShare = computed(() => {
  let share = 0
  for (const t of DISCOUNT_TIERS) if (mass.value >= t.min) share = t.share
  return share
})

const nextTier = computed(() => {
  const t = DISCOUNT_TIERS.find((t) => mass.value < t.min)
  if (!t) return null
  return { need: roundMass(t.min - mass.value), pct: t.share * 100 }
})

/* ---------- смета ---------- */
const fmt = (n) => Math.round(n).toLocaleString('ru-RU')
const roundK = (n) => Math.round(n / 1000) * 1000

const calc = computed(() => {
  const m = mass.value
  const work = type.value.rate * m
  const kmd = needKmd.value ? work * RATES.kmdShare : 0
  const urgentFee = urgent.value ? (work + kmd) * RATES.urgentShare : 0
  const material = ownMetal.value ? 0 : RATES.metalPerTonne * m
  const coat = coating.value.rate * m
  const montage = needMontage.value ? RATES.montagePerTonne * m : 0
  const discount = (work + kmd) * discountShare.value
  const deliveryCost = delivery.value.cost

  const total = work + kmd + urgentFee + material + coat + montage - discount + deliveryCost
  const vat = total * RATES.vatShare
  return {
    work,
    kmd,
    urgentFee,
    material,
    coat,
    montage,
    discount,
    deliveryCost,
    total,
    vat,
    low: roundK(total * RATES.rangeLow),
    high: roundK(total * RATES.rangeHigh),
    vatLow: roundK(total * RATES.rangeLow * RATES.vatShare),
    vatHigh: roundK(total * RATES.rangeHigh * RATES.vatShare),
    perTonne: total / m,
  }
})

/* ---------- срок изготовления ---------- */
const leadTime = computed(() => {
  const m = mass.value
  if (urgent.value) {
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
    'Конфигурация из калькулятора:',
    `• Тип: ${type.value.label}`,
    `• Масса: ${mass.value} т`,
    `• Металл: ${ownMetal.value ? 'давальческий (заказчика)' : 'наш, входит в смету'}`,
    `• Покрытие: ${coating.value.label}`,
  ]
  const opts = []
  if (needKmd.value) opts.push('разработка КМД')
  if (needMontage.value) opts.push('монтаж')
  if (urgent.value) opts.push('срочно')
  if (opts.length) lines.push(`• Опции: ${opts.join(', ')}`)
  lines.push(`• Доставка: ${delivery.value.label}`)
  lines.push(`• Ориентир калькулятора: ${fmt(calc.value.low)} – ${fmt(calc.value.high)} ₽`)
  lines.push(`• В т.ч. НДС 20%: ${fmt(calc.value.vatLow)} – ${fmt(calc.value.vatHigh)} ₽`)
  return lines.join('\n')
})

const breakdownOpen = ref(false)

/* без отдельной навигации шагов — правый блок всегда в поле зрения */
</script>

<template>
  <main>
    <!-- ============ HERO ============ -->
    <section class="sec sec--dark page-hero clc-hero">
      <div class="container">
        <RouterLink to="/" class="page-back" v-reveal>← На главную</RouterLink>
        <div class="sec-head" v-reveal="60">
          <p class="sec-tag"><span class="idx">Онлайн</span> Калькулятор</p>
          <h1 class="page-title">Калькулятор стоимости <em>металлоконструкций</em></h1>
          <p class="page-desc">
            Соберите конфигурацию — получите ориентир цены и срока без звонков
            и «оставьте номер, мы перезвоним». Точный расчёт по чертежу
            технолог сделает бесплатно за 1 рабочий день.
          </p>
        </div>

        <div class="clc-hero-cta" v-reveal="140">
          <a href="#calculator" class="btn">Рассчитать стоимость</a>
        </div>
      </div>
    </section>

    <!-- ============ КАЛЬКУЛЯТОР ============ -->
    <section id="calculator" class="sec sec--deep clc-sec">
      <div class="container">
        <div class="clc-layout">
          <!-- ЛЕВАЯ КОЛОНКА: ШАГИ -->
          <div class="clc-steps">
            <!-- ШАГ 1: тип -->
            <div id="step-type" class="clc-step" v-reveal>
              <p class="clc-step-tag"><span>01</span> Что изготовить</p>
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
              <p class="clc-step-tag"><span>02</span> Масса конструкции</p>
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
                  Нет чертежа — <a href="#calc-form">пришлите эскиз</a>, посчитаем сами.
                </p>
              </div>
            </div>

            <!-- ШАГ 3: металл -->
            <div id="step-metal" class="clc-step" v-reveal="60">
              <p class="clc-step-tag"><span>03</span> Чей металл</p>
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
              <p class="clc-step-tag"><span>04</span> Покрытие</p>
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
              <p class="clc-step-tag"><span>05</span> Дополнительно</p>
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
              <p class="clc-step-tag"><span>06</span> Доставка</p>
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
          </div>

          <!-- ПРАВАЯ КОЛОНКА: ИТОГ -->
          <aside class="clc-panel-wrap">
            <div class="clc-panel" v-reveal="120">
              <p class="panel-tag">Ориентир стоимости</p>

              <p class="panel-price">
                <span class="pp-num">{{ fmt(shownLow) }}</span>
                <span class="pp-dash">—</span>
                <span class="pp-num">{{ fmt(shownHigh) }}</span>
                <span class="pp-rub">₽</span>
              </p>
              <p class="panel-per">≈ {{ fmt(calc.perTonne) }} ₽/т · с учётом всех выбранных опций</p>

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
                  <p class="bd-row"><span>Работы ({{ type.label.toLowerCase() }})</span><b>{{ fmt(calc.work) }} ₽</b></p>
                  <p v-if="calc.material" class="bd-row"><span>Металл</span><b>{{ fmt(calc.material) }} ₽</b></p>
                  <p v-if="calc.coat" class="bd-row"><span>{{ coating.label }}</span><b>{{ fmt(calc.coat) }} ₽</b></p>
                  <p v-if="calc.kmd" class="bd-row"><span>КМД</span><b>{{ fmt(calc.kmd) }} ₽</b></p>
                  <p v-if="calc.montage" class="bd-row"><span>Монтаж с окраской</span><b>{{ fmt(calc.montage) }} ₽</b></p>
                  <p v-if="calc.urgentFee" class="bd-row"><span>Срочность</span><b>{{ fmt(calc.urgentFee) }} ₽</b></p>
                  <p v-if="calc.discount" class="bd-row bd-row--ok"><span>Скидка за объём −{{ discountShare * 100 }}%</span><b>−{{ fmt(calc.discount) }} ₽</b></p>
                  <p class="bd-row"><span>Доставка</span><b>{{ delivery.external ? 'по тарифу ТК' : calc.deliveryCost ? fmt(calc.deliveryCost) + ' ₽' : 'бесплатно' }}</b></p>
                  <p class="bd-row bd-row--vat"><span>В том числе НДС 20%</span><b>{{ fmt(calc.vat) }} ₽</b></p>
                </div>
              </div>

              <a href="#calc-form" class="btn btn--block panel-btn">Получить точный расчёт</a>
              <p class="panel-note">
                Это ориентир, а не оферта: точная цена зависит от чертежа и текущей цены металла.
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
            <ul>
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

/* ============ layout ============ */
.clc-sec { padding-top: 72px; overflow: visible; }

.clc-layout {
  display: grid;
  grid-template-columns: 1fr 380px;
  gap: 40px;
  align-items: start;
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
  .mass-box { padding: 20px 16px 18px; }
  .opt { flex-wrap: wrap; }
  .opt-price { width: 100%; padding-left: 38px; }
}
</style>
