<script setup>
import { computed, ref, watchEffect, onUnmounted } from 'vue'
import {
  getMetalworkLanding,
  metalworkLandings,
  metalworkLandingPath,
  MK_PARENT_PATH,
  MK_PARENT_LABEL,
} from '../data/metallokonstruktsii'
import { uslugi } from '../data/uslugi'
import { otherCycleLinks, IZG_PATH } from '../data/services'
import DetailPreview from '../components/calc/DetailPreview.vue'
import FaqSection from '../components/FaqSection.vue'
import FinalCtaSection from '../components/FinalCtaSection.vue'
import ShopGallery from '../components/ShopGallery.vue'
import { izgotovlenieGallery } from '../data/shopPhotos'

const SITE = 'https://greydstroy.ru'
const page = getMetalworkLanding('izgotovlenie')

const siblings = metalworkLandings.filter((p) => p.slug !== 'izgotovlenie')
const cycleOthers = otherCycleLinks(IZG_PATH)
const seoParagraphs = Array.isArray(page.seoText) ? page.seoText : [page.seoText]

/* тарифы как в калькуляторе */
const METAL = 75000
const MONTAGE = 35000
const KMD_SHARE = 0.08
const LOW = 0.88
const HIGH = 1.12

const types = [
  {
    id: 'plates',
    preview: 'plates',
    label: 'Закладные',
    rate: 39000,
    hint: 'Пластины, анкеры, кронштейны — серией или по одной.',
    fit: 'От одной детали. Отверстия и фаски по КМД, не «досверлите на площадке».',
    to: '/metallokonstruktsii/zakladnye',
    toLabel: 'Закладные →',
  },
  {
    id: 'beams',
    preview: 'beams',
    label: 'Балки и колонны',
    rate: 45000,
    hint: 'Сварные двутавры, торцы, отверстия под узлы.',
    fit: 'Сечение и длина по вашему КМ. Торцы обрабатываем в цехе.',
  },
  {
    id: 'frame',
    preview: 'frame',
    label: 'Каркасы',
    rate: 49000,
    hint: 'Колонны, связи, прогоны — каркас здания или навес.',
    fit: 'Считаем по чертежу или габаритам. Навесы — отдельной посадочной.',
    to: '/metallokonstruktsii/navesy',
    toLabel: 'Навесы →',
  },
  {
    id: 'hangar',
    preview: 'frame',
    label: 'Ангары',
    rate: 49000,
    hint: 'Каркас склада или холодного ангара под ваш пролёт.',
    fit: 'Снег по району, шаг колонн под логистику. Сэндвич — в точном расчёте.',
    to: '/metallokonstruktsii/sklady-i-angary',
    toLabel: 'Склады и ангары →',
  },
  {
    id: 'truss',
    preview: 'truss',
    label: 'Фермы',
    rate: 55000,
    hint: 'Стропильные и подстропильные, пролёты до 36 м.',
    fit: 'Контрольная сборка на стапеле, если стыков много.',
    to: '/metallokonstruktsii/fermy',
    toLabel: 'Фермы →',
  },
  {
    id: 'stairs',
    preview: 'stairs',
    label: 'Лестницы',
    rate: 62000,
    hint: 'Марши, площадки обслуживания, ограждения.',
    fit: 'По КМ или по месту: снимем размеры и согласуем узел.',
    to: '/metallokonstruktsii/lestnitsy',
    toLabel: 'Лестницы →',
  },
  {
    id: 'custom',
    preview: 'custom',
    label: 'Нестандарт',
    rate: 79000,
    hint: 'Ёмкости, бункеры, рамы, узлы, которых нет в сортаменте.',
    fit: 'Сначала геометрия, потом тонна. Не копируем чужой прайс «за тонну всего».',
  },
]

const coatings = [
  { id: 'none', label: 'Без покрытия', rate: 0 },
  { id: 'primer', label: 'Грунт', rate: 6000 },
  { id: 'paint', label: 'Грунт + эмаль', rate: 12000 },
]

const starts = [
  {
    id: 'kmd',
    title: 'Есть КМ или КМД',
    tag: 'Быстрый путь',
    lead: 'Конструктив или деталировка: файл сразу идёт в расчёт — масса, работы, срок.',
    send: 'DWG, DXF или PDF. Чем полнее спецификация — тем уже вилка.',
    next: 'Смета в течение рабочего дня. КМД, если его нет, посчитаем отдельной строкой.',
  },
  {
    id: 'sketch',
    title: 'Есть эскиз или АР',
    tag: 'Нужна деталировка',
    lead: 'Снимем задачу и согласуем узлы до запуска в цех.',
    send: 'PDF, фото с размерами, архитектурный раздел (АР). Напишите, что нельзя менять.',
    next: 'Сначала конструктив и КМД — без сюрприза «чертёж в конце отдельно».',
  },
  {
    id: 'sample',
    title: 'Есть образец',
    tag: 'Снимем с натуры',
    lead: 'Привезите деталь или покажите на объекте — повторим геометрию.',
    send: 'Образец, фото с линейкой, примерный тираж.',
    next: 'Строим макет, согласуем и режем. Серия сидит размер в размер.',
  },
  {
    id: 'words',
    title: 'Пока только задача',
    tag: 'Начнём с разговора',
    lead: 'Опишите, что должно стоять и к какой дате.',
    send: 'Габариты, нагрузка если знаете, регион, нужен ли монтаж.',
    next: 'Дадим ориентир и список, чего не хватает для точной сметы. Ни к чему не обязывает.',
  },
]

const steps = [
  { n: '01', title: 'Исходники', text: 'Чертёж, эскиз или задача словами. Чем полнее — тем быстрее смета.' },
  { n: '02', title: 'Расчёт', text: 'Стоимость, срок и состав сметы — в течение рабочего дня.' },
  { n: '03', title: 'Договор', text: 'Фиксируем цену и срок. Аванс на металл — после согласования, не «сначала переведите».' },
  { n: '04', title: 'Цех', text: 'Резка, гибка, сборка, сварка на одной площадке. Геометрия проверяется до накладной.' },
  { n: '05', title: 'Отгрузка', text: 'Самовывоз, свой транспорт по области, ТК по России. По области можем смонтировать.' },
]

const typeId = ref('frame')
const tonnes = ref(2)
const metalOurs = ref(true)
const coatingId = ref('primer')
const needKmd = ref(false)
const needMontage = ref(false)
const startId = ref('kmd')
const stepI = ref(0)

const type = computed(() => types.find((t) => t.id === typeId.value) || types[0])
const coating = computed(() => coatings.find((c) => c.id === coatingId.value) || coatings[0])
const start = computed(() => starts.find((s) => s.id === startId.value) || starts[0])
const step = computed(() => steps[stepI.value])

const estimate = computed(() => {
  const t = Number(tonnes.value) || 0
  const works = type.value.rate * t
  const metal = metalOurs.value ? METAL * t : 0
  const coat = coating.value.rate * t
  const kmd = needKmd.value ? works * KMD_SHARE : 0
  const montage = needMontage.value ? MONTAGE * t : 0
  const mid = works + metal + coat + kmd + montage
  return {
    works,
    metal,
    coat,
    kmd,
    montage,
    mid,
    low: Math.round(mid * LOW),
    high: Math.round(mid * HIGH),
  }
})

const recap = computed(() => {
  const bits = ['работы цеха']
  bits.push(metalOurs.value ? 'наш металл' : 'ваш металл')
  if (coating.value.rate) bits.push(coating.value.label.toLowerCase())
  if (needKmd.value) bits.push('КМД')
  if (needMontage.value) bits.push('монтаж по области')
  return bits.join(' · ')
})

const money = (n) =>
  Math.round(n).toLocaleString('ru-RU') + ' ₽'

let ldScript = null
watchEffect(() => {
  ldScript?.remove()
  const path = '/metallokonstruktsii/izgotovlenie'
  ldScript = document.createElement('script')
  ldScript.type = 'application/ld+json'
  ldScript.textContent = JSON.stringify({
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'BreadcrumbList',
        itemListElement: [
          { '@type': 'ListItem', position: 1, name: 'Главная', item: SITE + '/' },
          { '@type': 'ListItem', position: 2, name: MK_PARENT_LABEL, item: SITE + MK_PARENT_PATH },
          { '@type': 'ListItem', position: 3, name: page.navLabel, item: SITE + path },
        ],
      },
      {
        '@type': 'Service',
        name: page.h1,
        description: page.metaDescription,
        url: SITE + path,
        provider: { '@id': `${SITE}/#organization` },
        areaServed: 'RU',
      },
      {
        '@type': 'FAQPage',
        mainEntity: page.faq.map((f) => ({
          '@type': 'Question',
          name: f.q,
          acceptedAnswer: { '@type': 'Answer', text: f.a },
        })),
      },
    ],
  })
  document.head.appendChild(ldScript)
})
onUnmounted(() => ldScript?.remove())
</script>

<template>
  <main>
    <section id="usluga-hero" class="sec sec--dark page-hero izg-hero">
      <div class="izg-ghost" aria-hidden="true">ИЗГОТОВЛЕНИЕ</div>
      <div class="container">
        <nav class="crumbs" aria-label="Навигация">
          <RouterLink to="/">Главная</RouterLink>
          <span class="crumbs-sep" aria-hidden="true">/</span>
          <RouterLink :to="MK_PARENT_PATH">{{ MK_PARENT_LABEL }}</RouterLink>
          <span class="crumbs-sep" aria-hidden="true">/</span>
          <span aria-current="page">{{ page.navLabel }}</span>
        </nav>
        <div class="sec-head" v-reveal="60">
          <p class="sec-tag"><span class="idx">Металлоконструкции</span> {{ page.label }}</p>
          <h1 class="page-title">{{ page.h1 }} <em>{{ page.h1em }}</em></h1>
          <p class="page-desc">{{ page.desc }}</p>
        </div>
        <div class="srv-hero-cta" v-reveal="140">
          <a href="#builder" class="btn">Собрать состав заказа</a>
          <a href="#cta" class="btn btn--ghost">Прислать чертёж</a>
        </div>
        <div class="srv-stats" v-reveal="200">
          <div v-for="st in page.stats" :key="st.b + st.s" class="srv-stat">
            <b>{{ st.b }}</b><span>{{ st.s }}</span>
          </div>
        </div>
      </div>
    </section>

    <!-- ============ С ЧЕГО НАЧАТЬ ============ -->
    <section id="start" class="sec sec--deep">
      <div class="container">
        <div class="sec-head" v-reveal>
          <p class="sec-tag"><span class="idx">Запуск</span> С чего начать</p>
          <h2 class="sec-title">Что у вас есть <em>на руках</em></h2>
          <p class="sec-sub">
            Изготовление металлоконструкций начинается не с прайса, а с исходников.
            Выберите, что уже есть — покажем следующий шаг.
          </p>
        </div>

        <div class="start-grid" v-reveal="80">
          <button
            v-for="s in starts"
            :key="s.id"
            type="button"
            class="start-btn"
            :class="{ active: startId === s.id }"
            :aria-pressed="startId === s.id"
            @click="startId = s.id"
          >
            <span class="start-tag">{{ s.tag }}</span>
            {{ s.title }}
          </button>
        </div>

        <div class="start-panel" v-reveal="120">
          <p class="start-lead">{{ start.lead }}</p>
          <div class="start-cols">
            <div>
              <p class="start-h">Что прислать</p>
              <p>{{ start.send }}</p>
            </div>
            <div>
              <p class="start-h">Что будет дальше</p>
              <p>{{ start.next }}</p>
            </div>
          </div>
          <div class="start-actions">
            <a href="#cta" class="btn">Прислать на расчёт</a>
            <RouterLink to="/kalkulyator" class="btn btn--ghost">Сначала ориентир в калькуляторе</RouterLink>
          </div>
        </div>
      </div>
    </section>

    <!-- ============ КОНСТРУКТОР СОСТАВА ============ -->
    <section id="builder" class="sec sec--dark izg-builder">
      <div class="container">
        <div class="sec-head" v-reveal>
          <p class="sec-tag"><span class="idx">Ориентир</span> Состав заказа</p>
          <h2 class="sec-title">Соберите изготовление <em>под свою задачу</em></h2>
          <p class="sec-sub">
            Тип, тоннаж и опции — живой ориентир, не оферта. Точная смета по чертежу
            приходит за рабочий день и этой суммы придерживаемся в договоре.
          </p>
        </div>

        <div class="builder" v-reveal="80">
          <div class="builder-main">
            <p class="picker-label">Что изготовить</p>
            <div class="type-row">
              <button
                v-for="t in types"
                :key="t.id"
                type="button"
                class="type-btn"
                :class="{ active: typeId === t.id }"
                :aria-pressed="typeId === t.id"
                @click="typeId = t.id"
              >
                {{ t.label }}
              </button>
            </div>
            <p class="type-hint">{{ type.hint }}</p>
            <p class="type-fit">{{ type.fit }}</p>
            <RouterLink v-if="type.to" :to="type.to" class="type-more">{{ type.toLabel }}</RouterLink>

            <label class="picker-label tonnes-label">
              Ориентир по массе
              <span class="picker-value">{{ tonnes }} т</span>
            </label>
            <input
              v-model.number="tonnes"
              type="range"
              min="0.2"
              max="15"
              step="0.1"
              class="ton-slider"
              aria-label="Масса заказа в тоннах"
            />

            <div class="opt-grid">
              <div class="opt-block">
                <p class="picker-label">Металл</p>
                <div class="seg">
                  <button type="button" :class="{ active: metalOurs }" @click="metalOurs = true">Наш</button>
                  <button type="button" :class="{ active: !metalOurs }" @click="metalOurs = false">Ваш</button>
                </div>
              </div>
              <div class="opt-block">
                <p class="picker-label">Покрытие</p>
                <div class="seg wrap">
                  <button
                    v-for="c in coatings"
                    :key="c.id"
                    type="button"
                    :class="{ active: coatingId === c.id }"
                    @click="coatingId = c.id"
                  >
                    {{ c.label }}
                  </button>
                </div>
              </div>
              <div class="opt-block">
                <p class="picker-label">Ещё в заказе</p>
                <div class="seg wrap">
                  <button type="button" :class="{ active: needKmd }" :aria-pressed="needKmd" @click="needKmd = !needKmd">КМД</button>
                  <button type="button" :class="{ active: needMontage }" :aria-pressed="needMontage" @click="needMontage = !needMontage">Монтаж</button>
                </div>
                <p v-if="needKmd" class="opt-note">Деталировка узлов, если готового КМД нет.</p>
                <p v-if="needMontage" class="opt-note">Монтаж своей бригадой — Нижегородская область.</p>
              </div>
            </div>
          </div>

          <aside class="builder-side">
            <DetailPreview
              :type="type.preview"
              :coating="coatingId"
              :kmd="needKmd"
              :montage="needMontage"
              compact
            />
            <div class="verdict">
              <p class="verdict-kicker">Ориентир по выбранному составу</p>
              <p class="verdict-sum">{{ money(estimate.low) }} – {{ money(estimate.high) }}</p>
              <p class="verdict-recap">{{ recap }}</p>
              <ul class="verdict-lines">
                <li><span>Работы</span><b>{{ money(estimate.works) }}</b></li>
                <li><span>{{ metalOurs ? 'Металл' : 'Металл ваш' }}</span><b>{{ metalOurs ? money(estimate.metal) : '—' }}</b></li>
                <li v-if="estimate.coat"><span>Покрытие</span><b>{{ money(estimate.coat) }}</b></li>
                <li v-if="estimate.kmd"><span>КМД (деталировка)</span><b>{{ money(estimate.kmd) }}</b></li>
                <li v-if="estimate.montage"><span>Монтаж</span><b>{{ money(estimate.montage) }}</b></li>
              </ul>
              <p class="verdict-note">Вилка ±12%. Без доставки и сэндвича. Не оферта.</p>
              <div class="verdict-cta">
                <RouterLink to="/kalkulyator" class="btn">Точнее в калькуляторе</RouterLink>
                <a href="#cta" class="btn btn--ghost">Чертёж на смету</a>
              </div>
            </div>
          </aside>
        </div>
      </div>
    </section>

    <ShopGallery
      :items="izgotovlenieGallery"
      tag="Цех"
      kicker="С площадки"
      title="Что уезжает"
      title-em="с Заревской"
    />

    <!-- ============ КАК ИДЁТ ЗАКАЗ ============ -->
    <section id="how" class="sec sec--light">
      <div class="container">
        <div class="sec-head" v-reveal>
          <p class="sec-tag"><span class="idx">Процесс</span> Как идёт заказ</p>
          <h2 class="sec-title">Пять шагов <em>без «пропадём после аванса»</em></h2>
        </div>

        <div class="how-nav" v-reveal="80">
          <button
            v-for="(s, i) in steps"
            :key="s.n"
            type="button"
            class="how-tab"
            :class="{ active: stepI === i }"
            :aria-pressed="stepI === i"
            @click="stepI = i"
          >
            <span>{{ s.n }}</span>
            {{ s.title }}
          </button>
        </div>
        <div class="how-panel" v-reveal="120">
          <p class="how-n">{{ step.n }}</p>
          <div>
            <h3>{{ step.title }}</h3>
            <p>{{ step.text }}</p>
          </div>
        </div>

        <div class="feat-grid izg-feat">
          <article v-for="(f, i) in page.features" :key="f.title" class="card feat-card" v-reveal="i * 70">
            <span class="feat-num">{{ String(i + 1).padStart(2, '0') }}</span>
            <h3>{{ f.title }}</h3>
            <p>{{ f.text }}</p>
          </article>
        </div>

        <div class="apps-copy">
          <p v-for="p in seoParagraphs" :key="p.slice(0, 40)" class="apps-text">{{ p }}</p>
        </div>
        <div class="detail-grid">
          <article v-for="d in page.details" :key="d.title" class="detail-card">
            <h2>{{ d.title }}</h2>
            <p>{{ d.text }}</p>
          </article>
        </div>

        <div class="srv-others srv-cluster">
          <p class="srv-others-h">Нужен монтаж, фундамент или здание целиком?</p>
          <div class="srv-others-row">
            <RouterLink
              v-for="s in cycleOthers"
              :key="s.to"
              :to="s.to"
              class="srv-other"
              :class="{ 'srv-other--acc': s.featured }"
            >
              {{ s.navLabel }} →
            </RouterLink>
          </div>
        </div>
        <div class="srv-others srv-cluster">
          <p class="srv-others-h">Другие задачи по металлоконструкциям:</p>
          <div class="srv-others-row">
            <RouterLink :to="MK_PARENT_PATH" class="srv-other srv-other--acc">Все металлоконструкции →</RouterLink>
            <RouterLink v-for="s in siblings" :key="s.slug" :to="metalworkLandingPath(s.slug)" class="srv-other">
              {{ s.navLabel }} →
            </RouterLink>
          </div>
        </div>
        <div class="srv-others">
          <p class="srv-others-h">Участки того же цеха:</p>
          <div class="srv-others-row">
            <RouterLink v-for="o in uslugi" :key="o.slug" :to="`/uslugi/${o.slug}`" class="srv-other">
              {{ o.label }} →
            </RouterLink>
          </div>
        </div>
      </div>
    </section>

    <FaqSection
      :items="page.faq"
      idx="Вопросы"
      title="Частые вопросы"
      title-em="— изготовление металлоконструкций"
    />
    <FinalCtaSection />
  </main>
</template>

<style scoped>
.izg-hero { padding-bottom: 64px; overflow: hidden; }
#start, #builder, #how { scroll-margin-top: 88px; }
.izg-ghost {
  position: absolute;
  top: 36px;
  right: -24px;
  font-family: var(--font-d);
  font-size: clamp(72px, 14vw, 200px);
  font-weight: 900;
  line-height: 1;
  color: transparent;
  -webkit-text-stroke: 1px rgba(255, 255, 255, 0.05);
  pointer-events: none;
  user-select: none;
}

.crumbs {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px 10px;
  margin-bottom: 36px;
  font-size: 13.5px;
  color: var(--w-faint);
}
.crumbs a { color: var(--w-soft); transition: color 0.2s; }
.crumbs a:hover { color: var(--acc-hot); }
.crumbs [aria-current="page"] { color: var(--white); }
.crumbs-sep { opacity: 0.55; }

.srv-hero-cta {
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
  margin-bottom: 48px;
}
.srv-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 18px;
  padding-top: 34px;
  border-top: 1px solid var(--line-d);
}
.srv-stat b {
  display: block;
  font-family: var(--font-d);
  font-size: clamp(18px, 2.2vw, 26px);
  font-weight: 900;
  color: var(--acc-hot);
  margin-bottom: 4px;
}
.srv-stat span {
  font-family: var(--font-m);
  font-size: 11.5px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--w-faint);
}

.start-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin-bottom: 18px;
}
.start-btn {
  text-align: left;
  padding: 20px 18px;
  background: var(--card-d);
  border: 1px solid var(--line-d);
  border-radius: var(--r-sm);
  color: var(--w-soft);
  font-weight: 700;
  font-size: 15px;
  transition: border-color 0.25s, color 0.25s, transform 0.25s var(--ease);
}
.start-btn:hover { border-color: rgba(255, 90, 31, 0.45); color: var(--white); transform: translateY(-2px); }
.start-btn.active {
  border-color: var(--acc);
  color: var(--white);
  background: rgba(255, 90, 31, 0.08);
}
.start-tag {
  display: block;
  font-family: var(--font-m);
  font-size: 11px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--acc);
  margin-bottom: 8px;
  font-weight: 600;
}
.start-panel {
  padding: 28px 30px;
  border: 1px solid var(--line-d);
  border-radius: var(--r);
  background: var(--card-d);
}
.start-lead {
  font-size: 17px;
  font-weight: 600;
  margin-bottom: 20px;
  max-width: 640px;
}
.start-cols {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 22px;
  margin-bottom: 24px;
}
.start-h {
  font-family: var(--font-m);
  font-size: 11px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--acc);
  margin-bottom: 8px;
}
.start-cols p + p, .start-cols div p { font-size: 14.5px; color: var(--w-soft); line-height: 1.65; }
.start-actions { display: flex; flex-wrap: wrap; gap: 12px; }

.builder {
  display: grid;
  grid-template-columns: 1.15fr 0.85fr;
  gap: 28px;
  align-items: start;
}
.builder-main {
  padding: 28px 28px 32px;
  border: 1px solid var(--line-d);
  border-radius: var(--r);
  background: var(--card-d);
}
.picker-label {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  font-family: var(--font-m);
  font-size: 12px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--w-faint);
  margin-bottom: 12px;
}
.picker-value { font-size: 18px; letter-spacing: 0; color: var(--acc-hot); font-weight: 600; }
.type-row { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 14px; }
.type-btn, .seg button {
  padding: 10px 14px;
  background: transparent;
  border: 1px solid var(--line-d);
  border-radius: var(--r-sm);
  color: var(--w-soft);
  font-size: 13.5px;
  font-weight: 600;
  transition: all 0.2s;
}
.type-btn:hover, .seg button:hover { border-color: rgba(255, 90, 31, 0.5); color: var(--white); }
.type-btn.active, .seg button.active {
  background: var(--acc);
  border-color: var(--acc);
  color: #fff;
}
.type-hint { font-size: 15px; font-weight: 600; margin-bottom: 6px; }
.type-fit { font-size: 14px; color: var(--w-soft); margin-bottom: 10px; max-width: 520px; }
.type-more { display: inline-block; font-size: 14px; font-weight: 700; color: var(--acc); margin-bottom: 22px; }
.type-more:hover { color: var(--acc-hot); }
.tonnes-label { margin-top: 8px; }
.ton-slider {
  width: 100%;
  height: 4px;
  appearance: none;
  -webkit-appearance: none;
  background: rgba(255, 255, 255, 0.12);
  border-radius: 2px;
  outline: none;
  cursor: pointer;
  margin-bottom: 28px;
}
.ton-slider::-webkit-slider-thumb {
  appearance: none;
  -webkit-appearance: none;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: var(--acc);
  border: 3px solid var(--bg0);
  box-shadow: 0 0 0 1.5px var(--acc);
}
.opt-grid { display: grid; gap: 20px; }
.seg { display: flex; flex-wrap: wrap; gap: 8px; }
.opt-note { margin-top: 8px; font-size: 12.5px; color: var(--w-faint); }

.builder-side { display: flex; flex-direction: column; gap: 16px; }
.builder-side :deep(.dp) {
  border-radius: var(--r);
  overflow: hidden;
  border: 1px solid var(--line-d);
}
.verdict {
  border: 1px solid var(--line-d);
  border-left: 3px solid var(--acc);
  border-radius: var(--r-sm);
  padding: 22px 22px 24px;
  background: rgba(255, 90, 31, 0.04);
}
.verdict-kicker {
  font-family: var(--font-m);
  font-size: 11px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--w-faint);
  margin-bottom: 8px;
}
.verdict-sum {
  font-family: var(--font-d);
  font-size: clamp(20px, 2.4vw, 28px);
  font-weight: 800;
  line-height: 1.2;
  margin-bottom: 8px;
}
.verdict-recap { font-size: 13.5px; color: var(--w-soft); margin-bottom: 16px; }
.verdict-lines { margin-bottom: 12px; }
.verdict-lines li {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  padding: 7px 0;
  border-top: 1px solid var(--line-d);
  font-size: 13.5px;
  color: var(--w-soft);
}
.verdict-lines b { color: var(--white); font-weight: 700; }
.verdict-note { font-size: 12.5px; color: var(--w-faint); margin-bottom: 16px; }
.verdict-cta { display: flex; flex-wrap: wrap; gap: 10px; }

.how-nav {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 8px;
  margin-bottom: 16px;
}
.how-tab {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 6px;
  padding: 16px 14px;
  background: var(--paper2);
  border: 1px solid var(--line-l);
  border-radius: var(--r-sm);
  color: var(--ink-soft);
  font-weight: 700;
  font-size: 13.5px;
  text-align: left;
  transition: border-color 0.2s, color 0.2s;
}
.how-tab span {
  font-family: var(--font-m);
  font-size: 11px;
  color: var(--acc);
}
.how-tab.active {
  border-color: var(--acc);
  color: var(--ink);
  background: #fff;
}
.how-panel {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 22px;
  align-items: start;
  padding: 26px 28px;
  border: 1px solid var(--line-l);
  border-radius: var(--r);
  background: var(--paper2);
  margin-bottom: 48px;
}
.how-n {
  font-family: var(--font-d);
  font-size: 32px;
  font-weight: 900;
  color: transparent;
  -webkit-text-stroke: 1.2px var(--acc);
  line-height: 1;
}
.how-panel h3 {
  font-family: var(--font-d);
  font-size: 18px;
  text-transform: uppercase;
  margin-bottom: 8px;
}
.how-panel p { font-size: 15px; color: var(--ink-soft); max-width: 640px; }

.feat-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-bottom: 40px;
}
.feat-card { padding: 28px; }
.feat-num {
  display: block;
  font-family: var(--font-d);
  font-size: 22px;
  font-weight: 900;
  color: transparent;
  -webkit-text-stroke: 1.2px rgba(18, 22, 27, 0.22);
  margin-bottom: 14px;
}
.feat-card:hover .feat-num { -webkit-text-stroke-color: var(--acc); }
.feat-card h3 {
  font-family: var(--font-d);
  font-size: 15px;
  font-weight: 700;
  text-transform: uppercase;
  margin-bottom: 10px;
}
.feat-card p { font-size: 14px; color: var(--ink-soft); }

.apps-copy { max-width: 780px; margin-bottom: 28px; }
.apps-text { font-size: 15px; line-height: 1.7; color: var(--ink-soft); margin-bottom: 16px; }
.detail-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 40px;
}
.detail-card {
  padding: 26px 28px;
  border: 1px solid var(--line-l);
  border-radius: var(--r);
  background: var(--paper2);
}
.detail-card h2 {
  font-family: var(--font-d);
  font-size: 16px;
  font-weight: 700;
  text-transform: uppercase;
  margin-bottom: 12px;
  line-height: 1.35;
}
.detail-card p { font-size: 14.5px; line-height: 1.7; color: var(--ink-soft); }

.srv-others {
  padding: 26px 32px;
  border-radius: var(--r);
  background: var(--paper2);
  border: 1px solid var(--line-l);
}
.srv-cluster { margin-bottom: 16px; }
.srv-others-h {
  font-family: var(--font-m);
  font-size: 11.5px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--acc);
  margin-bottom: 14px;
}
.srv-others-row { display: flex; gap: 12px 28px; flex-wrap: wrap; }
.srv-other { font-size: 15px; font-weight: 700; color: var(--ink); transition: color 0.2s; }
.srv-other:hover { color: var(--acc); }
.srv-other--acc { color: var(--acc); }

@media (max-width: 1000px) {
  .start-grid, .how-nav, .builder { grid-template-columns: 1fr 1fr; }
}
@media (max-width: 900px) {
  .srv-stats { grid-template-columns: 1fr 1fr; gap: 24px; }
  .feat-grid, .detail-grid, .start-cols { grid-template-columns: 1fr; }
  .izg-ghost { display: none; }
}
@media (max-width: 640px) {
  .start-grid, .how-nav, .builder { grid-template-columns: 1fr; }
  .how-tab { flex-direction: row; align-items: center; gap: 10px; }
}
</style>
