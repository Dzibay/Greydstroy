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
import { otherCycleLinks, MONTAZH_PATH } from '../data/services'
import DetailPreview from '../components/calc/DetailPreview.vue'
import FaqSection from '../components/FaqSection.vue'
import FinalCtaSection from '../components/FinalCtaSection.vue'
import ShopGallery from '../components/ShopGallery.vue'
import { montageGallery } from '../data/shopPhotos'

const SITE = 'https://greydstroy.ru'
const page = getMetalworkLanding('montazh')
const siblings = metalworkLandings.filter((p) => p.slug !== 'montazh')
const cycleOthers = otherCycleLinks(MONTAZH_PATH)
const seoParagraphs = Array.isArray(page.seoText) ? page.seoText : [page.seoText]

const RATE = 35000
const LOW = 0.88
const HIGH = 1.12

const geos = [
  {
    id: 'oblast',
    title: 'Нижегородская область',
    tag: 'Своя бригада',
    lead: 'Выезжаем сами: каркас, навес, площадки, ангар. Кто варил в цехе — тот и ставит.',
  },
  {
    id: 'russia',
    title: 'Другой регион',
    tag: 'Отгрузка + схема',
    lead: 'Конструкцию отгружаем с маркировкой и КМД. Командировку считаем отдельно — в публичный прайс «по всей России» не пишем.',
  },
]

const cities = [
  'Дзержинск',
  'Нижний Новгород',
  'Кстово',
  'Бор',
  'Балахна',
  'Богородск',
  'Павлово',
  'Городец',
  'Арзамас',
  'Выкса',
]

const checks = [
  { id: 'found', title: 'Фундамент уже стоит', text: 'Колоннам есть куда сесть: бетон залит, точки совпадают с чертежом.' },
  { id: 'crane', title: 'Кран сможет встать', text: 'Дорога, ворота и грунт выдерживают кран — не через живую стройку.' },
  { id: 'stack', title: 'Куда сложить конструкции', text: 'Есть место для готовых секций, пока их поднимают на каркас.' },
  { id: 'weld', title: 'Можно варить на объекте', text: 'Есть электричество, укрытие от дождя и допуск на сварочные работы.' },
  { id: 'plan', title: 'Площадка свободна по графику', text: 'Бригада не стоит сутки, пока льют бетон или не уберут леса.' },
]

const kinds = [
  {
    id: 'frame',
    preview: 'frame',
    label: 'Каркас здания',
    hint: 'Колонны, связи, прогоны, фермы — в маркировке цеха.',
  },
  {
    id: 'canopy',
    preview: 'frame',
    label: 'Навес',
    hint: 'Стоянка, рампа, входная группа. Снег уже заложен в сечении.',
    to: '/metallokonstruktsii/navesy',
    toLabel: 'Навесы →',
  },
  {
    id: 'hangar',
    preview: 'frame',
    label: 'Ангар / склад',
    hint: 'Каркас быстровозводимого здания, монтаж по области.',
    to: '/metallokonstruktsii/sklady-i-angary',
    toLabel: 'Склады и ангары →',
  },
  {
    id: 'stairs',
    preview: 'stairs',
    label: 'Площадки и лестницы',
    hint: 'Обслуживание оборудования, марши, ограждения.',
  },
]

const steps = [
  { n: '01', title: 'Площадка', text: 'Фото стаканов под колонны, генплан, подъезд крана. Если основания не готовы — честно скажем «ещё рано».' },
  { n: '02', title: 'Цех', text: 'Режем и варим у себя. Укрупнение на стапеле, чтобы на высоте осталось меньше швов.' },
  { n: '03', title: 'Выезд', text: 'Бригада с маркировкой, которая уже видела эти узлы. Не «первый раз видим ваш каркас».' },
  { n: '04', title: 'Постановка', text: 'Подъём, оси, монтажные швы ручной сваркой (РДС). Геометрия — по чертежу, не «на глаз от угла здания».' },
  { n: '05', title: 'Сдача', text: 'Исполнительная, паспорт. Если шов наш и он не сел — переварим, без переписки на две недели.' },
]

const geoId = ref('oblast')
const done = ref(['found'])
const kindId = ref('frame')
const tonnes = ref(3)
const craneOurs = ref(false)
const tight = ref(false)
const stepI = ref(0)

const geo = computed(() => geos.find((g) => g.id === geoId.value))
const kind = computed(() => kinds.find((k) => k.id === kindId.value) || kinds[0])
const step = computed(() => steps[stepI.value])
const inOblast = computed(() => geoId.value === 'oblast')

const checkCount = computed(() => done.value.length)
const siteStatus = computed(() => {
  const n = checkCount.value
  if (n >= 5) {
    return {
      tag: 'Можно ставить дату',
      text: 'Площадка выглядит рабочей. В смете останутся тоннаж, кран и стеснённость — не «сначала приедем и удивимся».',
    }
  }
  if (n >= 3) {
    return {
      tag: 'Выходим после уточнения',
      text: 'База есть, но дыры лучше закрыть до выезда. Пришлите фото — скажем, чего не хватает.',
    }
  }
  return {
    tag: 'Сначала площадка',
    text: 'Бригада на неготовой площадке стоит дороже, чем доделать фундамент. Дособерём чек-лист, потом дату.',
  }
})

const estimate = computed(() => {
  const t = Number(tonnes.value) || 0
  const mid = RATE * t
  return { mid, low: Math.round(mid * LOW), high: Math.round(mid * HIGH) }
})

const recap = computed(() => {
  const bits = ['монтаж с окраской']
  bits.push(craneOurs.value ? 'кран нашим подрядом' : 'кран заказчика')
  if (tight.value) bits.push('стеснённая площадка')
  return bits.join(' · ')
})

const money = (n) => Math.round(n).toLocaleString('ru-RU') + ' ₽'

const siteLayers = computed(() => ({
  found: done.value.includes('found'),
  crane: done.value.includes('crane'),
  stack: done.value.includes('stack'),
  weld: done.value.includes('weld'),
  plan: done.value.includes('plan'),
}))

function toggleCheck(id) {
  if (done.value.includes(id)) {
    done.value = done.value.filter((x) => x !== id)
  } else {
    done.value = [...done.value, id]
  }
}

let ldScript = null
watchEffect(() => {
  ldScript?.remove()
  const path = '/metallokonstruktsii/montazh'
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
    <section id="usluga-hero" class="sec sec--dark page-hero mnt-hero">
      <div class="mnt-ghost" aria-hidden="true">МОНТАЖ</div>
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
          <a href="#geo" class="btn">Где объект</a>
          <a href="#cta" class="btn btn--ghost">Прислать чертёж и фото площадки</a>
        </div>
        <div class="srv-stats" v-reveal="200">
          <div v-for="st in page.stats" :key="st.b + st.s" class="srv-stat">
            <b>{{ st.b }}</b><span>{{ st.s }}</span>
          </div>
        </div>
      </div>
    </section>

    <!-- ============ ГДЕ ОБЪЕКТ ============ -->
    <section id="geo" class="sec sec--deep">
      <div class="container">
        <div class="sec-head" v-reveal>
          <p class="sec-tag"><span class="idx">География</span> Честно про выезд</p>
          <h2 class="sec-title">Где стоит <em>ваш объект</em></h2>
          <p class="sec-sub">
            Монтаж металлоконструкций своей бригадой — Нижегородская область.
            Дальше не обещаем «под ключ по России» мелким шрифтом.
          </p>
        </div>

        <div class="geo-grid" v-reveal="80">
          <button
            v-for="g in geos"
            :key="g.id"
            type="button"
            class="geo-btn"
            :class="{ active: geoId === g.id }"
            :aria-pressed="geoId === g.id"
            @click="geoId = g.id"
          >
            <span class="geo-tag">{{ g.tag }}</span>
            {{ g.title }}
          </button>
        </div>
        <div class="geo-panel">
          <p class="geo-lead">{{ geo.lead }}</p>
          <div v-if="inOblast" class="city-row">
            <span v-for="c in cities" :key="c" class="city-chip">{{ c }}</span>
            <span class="city-chip city-chip--more">и районные объекты</span>
          </div>
          <div v-else class="geo-actions">
            <RouterLink to="/dostavka" class="btn">Как отгружаем по России</RouterLink>
            <RouterLink to="/metallokonstruktsii/izgotovlenie" class="btn btn--ghost">Сначала изготовление</RouterLink>
          </div>
        </div>
      </div>
    </section>

    <!-- ============ ПЛОЩАДКА + СМЕТА ============ -->
    <section id="site" class="sec sec--dark">
      <div class="container">
        <div class="sec-head" v-reveal>
          <p class="sec-tag"><span class="idx">Площадка</span> До выезда</p>
          <h2 class="sec-title">Готова ли площадка <em>принять бригаду</em></h2>
          <p class="sec-sub">
            Отметьте, что уже есть. Это не формальность: простой на объекте
            обычно дороже, чем доделать фундамент.
          </p>
        </div>

        <div class="site-grid" v-reveal="80">
          <div>
            <div class="check-list">
              <button
                v-for="c in checks"
                :key="c.id"
                type="button"
                class="check-btn"
                :class="{ on: done.includes(c.id) }"
                :aria-pressed="done.includes(c.id)"
                @click="toggleCheck(c.id)"
              >
                <span class="check-box" aria-hidden="true" />
                <span>
                  <b>{{ c.title }}</b>
                  <i>{{ c.text }}</i>
                </span>
              </button>
            </div>
            <div class="site-status" :class="'st-' + checkCount">
              <p class="site-tag">{{ siteStatus.tag }}</p>
              <p>{{ siteStatus.text }}</p>
              <p class="site-count">{{ checkCount }} из {{ checks.length }}</p>
            </div>
          </div>

          <aside v-if="inOblast" class="est">
            <p class="picker-label">Что ставим</p>
            <div class="kind-row">
              <button
                v-for="k in kinds"
                :key="k.id"
                type="button"
                class="kind-btn"
                :class="{ active: kindId === k.id }"
                :aria-pressed="kindId === k.id"
                @click="kindId = k.id"
              >
                {{ k.label }}
              </button>
            </div>
            <p class="kind-hint">{{ kind.hint }}</p>
            <RouterLink v-if="kind.to" :to="kind.to" class="kind-more">{{ kind.toLabel }}</RouterLink>

            <DetailPreview :type="kind.preview" coating="paint" compact :site="siteLayers" />

            <label class="picker-label tonnes-label">
              Ориентир по массе
              <span class="picker-value">{{ tonnes }} т</span>
            </label>
            <input
              v-model.number="tonnes"
              type="range"
              min="0.5"
              max="20"
              step="0.5"
              class="ton-slider"
              aria-label="Масса конструкций в тоннах"
            />

            <div class="seg wrap">
              <button type="button" :class="{ active: !craneOurs }" :aria-pressed="!craneOurs" @click="craneOurs = false">Кран ваш</button>
              <button type="button" :class="{ active: craneOurs }" :aria-pressed="craneOurs" @click="craneOurs = true">Кран наш подряд</button>
              <button type="button" :class="{ active: tight }" :aria-pressed="tight" @click="tight = !tight">Стеснённо</button>
            </div>

            <div class="verdict">
              <p class="verdict-kicker">Монтаж с окраской, ориентир</p>
              <p class="verdict-sum">{{ money(estimate.low) }} – {{ money(estimate.high) }}</p>
              <p class="verdict-recap">{{ recap }}</p>
              <p class="verdict-note">
                База {{ money(RATE) }}/т. Кран, высота и ночные работы в вилку не зашиты —
                всплывут отдельной строкой, не внутри «от 35 000».
              </p>
              <div class="verdict-cta">
                <RouterLink to="/kalkulyator" class="btn">В калькуляторе с изготовлением</RouterLink>
                <a href="#cta" class="btn btn--ghost">Смета по проекту</a>
              </div>
            </div>
          </aside>

          <aside v-else class="est est--alt">
            <p class="verdict-kicker">Не область</p>
            <h3>Свой монтаж сюда не обещаем по прайсу</h3>
            <p>
              Отгрузим каркас с маркировкой и схемой. Местная бригада ставит по нашей КМД.
              Если тоннаж большой и выезд всё же нужен — это отдельный расчёт проживания и логистики, не строка «монтаж 35 000 ₽/т».
            </p>
            <div class="verdict-cta">
              <RouterLink to="/dostavka" class="btn">Доставка</RouterLink>
              <a href="#cta" class="btn btn--ghost">Описать объект</a>
            </div>
          </aside>
        </div>
      </div>
    </section>

    <ShopGallery
      :items="montageGallery"
      tag="Объект"
      kicker="Монтаж"
      title="Как ставим"
      title-em="на площадке"
    />

    <!-- ============ КАК ИДЁТ + СБОРКА ============ -->
    <section id="how" class="sec sec--light">
      <div class="container">
        <div class="sec-head" v-reveal>
          <p class="sec-tag"><span class="idx">Порядок</span> Как ставим</p>
          <h2 class="sec-title">Пять шагов <em>от стаканов до сдачи</em></h2>
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
        <div class="how-panel">
          <p class="how-n">{{ step.n }}</p>
          <div>
            <h3>{{ step.title }}</h3>
            <p>{{ step.text }}</p>
          </div>
        </div>

        <div class="split">
          <article class="split-card">
            <p class="split-kicker">Не путать</p>
            <h2>Монтаж — на объекте</h2>
            <p>
              Установка на фундаменты, оси, кран, монтажные швы. Это эта страница.
              Своя бригада по Нижегородской области.
            </p>
          </article>
          <article class="split-card split-card--acc">
            <p class="split-kicker">Рядом в цехе</p>
            <h2>Сборка — на стапеле</h2>
            <p>
              Укрупнение узлов до отгрузки: меньше сварки на высоте, отверстия ловятся на полу.
            </p>
            <RouterLink to="/metallokonstruktsii/sborka">Цеховая сборка →</RouterLink>
          </article>
        </div>

        <div class="feat-grid">
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
          <p class="srv-others-h">Нужно изготовление, фундамент или здание целиком?</p>
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
      title-em="— монтаж металлоконструкций"
    />
    <FinalCtaSection />
  </main>
</template>

<style scoped>
.mnt-hero { padding-bottom: 64px; overflow: hidden; }
#geo, #site, #how { scroll-margin-top: 88px; }
.mnt-ghost {
  position: absolute;
  top: 36px;
  right: -12px;
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

.srv-hero-cta { display: flex; gap: 14px; flex-wrap: wrap; margin-bottom: 48px; }
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

.geo-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 16px; }
.geo-btn {
  text-align: left;
  padding: 22px 22px;
  background: var(--card-d);
  border: 1px solid var(--line-d);
  border-radius: var(--r-sm);
  color: var(--w-soft);
  font-size: 18px;
  font-weight: 800;
  font-family: var(--font-d);
  text-transform: uppercase;
  cursor: pointer;
  transition: border-color 0.25s, color 0.25s, transform 0.25s var(--ease);
}
.geo-btn:hover { color: var(--white); transform: translateY(-2px); }
.geo-btn.active { border-color: var(--acc); color: var(--white); background: rgba(255, 90, 31, 0.08); }
.geo-tag {
  display: block;
  font-family: var(--font-m);
  font-size: 11px;
  letter-spacing: 0.12em;
  color: var(--acc);
  margin-bottom: 8px;
  font-weight: 600;
  text-transform: uppercase;
}
.geo-panel {
  padding: 26px 28px;
  border: 1px solid var(--line-d);
  border-radius: var(--r);
  background: var(--card-d);
}
.geo-lead { font-size: 16.5px; font-weight: 600; max-width: 720px; margin-bottom: 18px; }
.city-row { display: flex; flex-wrap: wrap; gap: 8px; }
.city-chip {
  padding: 8px 12px;
  border: 1px solid var(--line-d);
  border-radius: 999px;
  font-size: 13px;
  color: var(--w-soft);
}
.city-chip--more { border-color: rgba(255, 90, 31, 0.4); color: var(--acc-hot); }
.geo-actions { display: flex; flex-wrap: wrap; gap: 10px; }

.site-grid { display: grid; grid-template-columns: 1.05fr 0.95fr; gap: 24px; align-items: start; }
.check-list { display: grid; gap: 8px; margin-bottom: 14px; }
.check-btn {
  display: grid;
  grid-template-columns: 22px 1fr;
  gap: 14px;
  text-align: left;
  padding: 14px 16px;
  background: var(--card-d);
  border: 1px solid var(--line-d);
  border-radius: var(--r-sm);
  color: var(--w-soft);
  cursor: pointer;
  transition: border-color 0.2s, background 0.2s;
}
.check-btn.on { border-color: var(--acc); background: rgba(255, 90, 31, 0.07); color: var(--white); }
.check-box {
  width: 18px;
  height: 18px;
  margin-top: 2px;
  border: 1.5px solid var(--w-faint);
  border-radius: 4px;
}
.check-btn.on .check-box {
  background: var(--acc);
  border-color: var(--acc);
  box-shadow: inset 0 0 0 2px var(--bg1);
}
.check-btn b { display: block; font-size: 14.5px; margin-bottom: 2px; }
.check-btn i { font-style: normal; font-size: 12.5px; color: var(--w-faint); }
.site-status {
  padding: 18px 20px;
  border-radius: var(--r-sm);
  border: 1px solid var(--line-d);
  border-left: 3px solid var(--w-faint);
}
.site-status.st-3, .site-status.st-4 { border-left-color: #c9a227; }
.site-status.st-5 { border-left-color: #3dd68c; }
.site-tag {
  font-family: var(--font-d);
  font-size: 15px;
  text-transform: uppercase;
  margin-bottom: 6px;
}
.site-status p { font-size: 14px; color: var(--w-soft); }
.site-count {
  margin-top: 10px;
  font-family: var(--font-m);
  font-size: 12px;
  color: var(--acc);
}

.est {
  padding: 24px 22px 26px;
  border: 1px solid var(--line-d);
  border-radius: var(--r);
  background: var(--card-d);
}
.est--alt h3 {
  font-family: var(--font-d);
  font-size: 18px;
  text-transform: uppercase;
  margin: 8px 0 12px;
}
.est--alt p { font-size: 14.5px; color: var(--w-soft); margin-bottom: 18px; line-height: 1.65; }
.picker-label {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  font-family: var(--font-m);
  font-size: 12px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--w-faint);
  margin-bottom: 10px;
}
.picker-value { font-size: 18px; letter-spacing: 0; color: var(--acc-hot); font-weight: 600; }
.kind-row { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 10px; }
.kind-btn, .seg button {
  padding: 9px 12px;
  background: transparent;
  border: 1px solid var(--line-d);
  border-radius: var(--r-sm);
  color: var(--w-soft);
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
}
.kind-btn.active, .seg button.active { background: var(--acc); border-color: var(--acc); color: #fff; }
.kind-hint { font-size: 13.5px; color: var(--w-soft); margin-bottom: 8px; }
.kind-more { display: inline-block; font-size: 14px; font-weight: 700; color: var(--acc); margin-bottom: 14px; }
.est :deep(.dp) { border-radius: var(--r-sm); overflow: hidden; margin-bottom: 8px; border: 1px solid var(--line-d); }
.tonnes-label { margin-top: 8px; }
.ton-slider {
  width: 100%;
  height: 4px;
  appearance: none;
  -webkit-appearance: none;
  background: rgba(255, 255, 255, 0.12);
  border-radius: 2px;
  margin-bottom: 16px;
  cursor: pointer;
}
.ton-slider::-webkit-slider-thumb {
  appearance: none;
  -webkit-appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: var(--acc);
  border: 3px solid var(--bg0);
}
.seg { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 16px; }

.verdict {
  border: 1px solid var(--line-d);
  border-left: 3px solid var(--acc);
  border-radius: var(--r-sm);
  padding: 18px 18px 20px;
  background: rgba(255, 90, 31, 0.04);
}
.verdict-kicker {
  font-family: var(--font-m);
  font-size: 11px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--w-faint);
  margin-bottom: 6px;
}
.verdict-sum {
  font-family: var(--font-d);
  font-size: clamp(18px, 2vw, 24px);
  font-weight: 800;
  margin-bottom: 6px;
}
.verdict-recap { font-size: 13px; color: var(--w-soft); margin-bottom: 10px; }
.verdict-note { font-size: 12.5px; color: var(--w-faint); margin-bottom: 14px; line-height: 1.55; }
.verdict-cta { display: flex; flex-wrap: wrap; gap: 10px; }

.how-nav {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 8px;
  margin-bottom: 14px;
}
.how-tab {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 6px;
  padding: 14px 12px;
  background: #fff;
  border: 1px solid var(--line-l);
  border-radius: var(--r-sm);
  font-size: 13.5px;
  font-weight: 700;
  color: var(--ink-soft);
  text-align: left;
  cursor: pointer;
}
.how-tab span { font-family: var(--font-m); font-size: 11px; color: var(--acc); }
.how-tab.active { border-color: var(--acc); color: var(--ink); }
.how-panel {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 20px;
  padding: 24px 26px;
  border: 1px solid var(--line-l);
  border-radius: var(--r);
  background: var(--paper2);
  margin-bottom: 36px;
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

.split {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 40px;
}
.split-card {
  padding: 26px 28px;
  border: 1px solid var(--line-l);
  border-radius: var(--r);
  background: #fff;
}
.split-card--acc { border-color: rgba(255, 90, 31, 0.35); }
.split-kicker {
  font-family: var(--font-m);
  font-size: 11px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--acc);
  margin-bottom: 8px;
}
.split-card h2 {
  font-family: var(--font-d);
  font-size: 18px;
  text-transform: uppercase;
  margin-bottom: 10px;
}
.split-card p { font-size: 14.5px; color: var(--ink-soft); margin-bottom: 12px; }
.split-card a { font-weight: 700; color: var(--acc); }

.feat-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 40px; }
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
.detail-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 40px; }
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
.srv-other { font-size: 15px; font-weight: 700; color: var(--ink); }
.srv-other:hover { color: var(--acc); }
.srv-other--acc { color: var(--acc); }

@media (max-width: 1000px) {
  .site-grid, .geo-grid, .split, .how-nav { grid-template-columns: 1fr; }
}
@media (max-width: 900px) {
  .srv-stats, .feat-grid, .detail-grid { grid-template-columns: 1fr 1fr; }
  .mnt-ghost { display: none; }
}
@media (max-width: 640px) {
  .srv-stats, .feat-grid, .detail-grid { grid-template-columns: 1fr; }
  .how-tab { flex-direction: row; align-items: center; gap: 10px; }
}
</style>
