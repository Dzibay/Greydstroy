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
import { company } from '../data/company'
import StatCounter from '../components/ui/StatCounter.vue'
import FaqSection from '../components/FaqSection.vue'
import FinalCtaSection from '../components/FinalCtaSection.vue'

const SITE = 'https://greydstroy.ru'
const page = getMetalworkLanding('proizvodstvo')
const siblings = metalworkLandings.filter((p) => p.slug !== 'proizvodstvo')
const seoParagraphs = Array.isArray(page.seoText) ? page.seoText : [page.seoText]

const stations = [
  {
    id: 'laser',
    n: '01',
    title: 'Лазер',
    spec: 'сталь 16 мм · нерж 12 · Al 8',
    text: 'Чистый контур, отверстия и пазы за один установ. Деталь с поста идёт в гибку или сразу в сборку.',
    to: '/uslugi/lazernaya-rezka',
    tone: 'laser',
  },
  {
    id: 'plasma',
    n: '02',
    title: 'Плазма',
    spec: 'до 25 мм · крупный раскрой',
    text: 'Толстый лист и фланцы: там, где лазеру уже невыгодно. Кромка под сварку без «доп. зачистки» в смете.',
    to: '/uslugi/plazmennaya-rezka',
    tone: 'plasma',
  },
  {
    id: 'gas',
    n: '03',
    title: 'Газ',
    spec: 'чёрная сталь до 70 мм',
    text: 'Плиты, закладные, основания. Пост берёт то, что лазер и плазма уже не берут.',
    to: '/uslugi/gazovaya-rezka',
    tone: 'gas',
  },
  {
    id: 'bend',
    n: '04',
    title: 'Гибка',
    spec: 'до 6 мм · длина до 3000 мм',
    text: 'ЧПУ-листогиб рядом с резкой: развёртку считаем сами, угол не «подгоняют на объекте».',
    to: '/uslugi/gibka-metalla',
    tone: 'bend',
  },
  {
    id: 'weld',
    n: '05',
    title: 'Сварка',
    spec: 'MIG · TIG · ручная (РДС)',
    text: 'Узлы и каркасы на стапеле. Швы проверяем до накладной, паспорт — на изделие.',
    to: '/uslugi/svarka',
    tone: 'weld',
  },
  {
    id: 'ship',
    n: '06',
    title: 'Отгрузка',
    spec: 'свой транспорт / ТК',
    text: 'С площадки, без чужого склада «перетарки». По области — свой транспорт, по России — терминал рядом.',
    to: '/dostavka',
    tone: 'ship',
  },
]

const materials = [
  { id: 'steel', label: 'Сталь', laserMax: 16, plasmaMax: 25, gasMax: 70 },
  { id: 'stainless', label: 'Нержавейка', laserMax: 12, plasmaMax: 25, gasMax: 0 },
  { id: 'aluminum', label: 'Алюминий', laserMax: 8, plasmaMax: 25, gasMax: 0 },
]
const SCALE_MAX = 70

const modes = [
  {
    id: 'series',
    title: 'Серийная партия',
    lead: 'Один макет — дальше поток. Раскрой плотнее, цена за штуку падает.',
    points: [
      'Закладные, кронштейны, однотипные узлы',
      'ЧПУ повторяет контур детали №1 на детали №100',
      'Отгрузка частями, если объекту так удобнее',
    ],
  },
  {
    id: 'unit',
    title: 'Единичный каркас',
    lead: 'КМД, резка и сварка в одном графике — не ждёте три смежника.',
    points: [
      'Фермы, рамы, каркас здания, нестандарт',
      'Контрольная сборка на стапеле до крана',
      'Срок фиксируем вместе с ценой, не «как пойдёт»',
    ],
  },
]

const flow = [
  { title: 'Раскрой', text: 'Лазер, плазма или газ — пост выбираем по толщине, не «всё в один станок».' },
  { title: 'Гибка', text: 'Если нужна. Развёртка с того же файла, что ушёл в рез.' },
  { title: 'Сборка', text: 'Укрупнение на стапеле: отверстия совпали, пока не на высоте.' },
  { title: 'Сварка', text: 'Узел или каркас. Контроль шва до паспорта.' },
  { title: 'Грунт', text: 'Если заказали покрытие. Не «потом у другого подрядчика».' },
  { title: 'Отгрузка', text: 'Маркировка, накладная, транспорт. С завода — сразу к вам.' },
]

const stationId = ref('laser')
const material = ref(materials[0])
const thickness = ref(8)
const modeId = ref('series')
const flowI = ref(0)

const station = computed(() => stations.find((s) => s.id === stationId.value) || stations[0])
const mode = computed(() => modes.find((m) => m.id === modeId.value) || modes[0])
const flowStep = computed(() => flow[flowI.value])

const verdict = computed(() => {
  const t = Number(thickness.value)
  const m = material.value
  if (t <= m.laserMax) {
    return {
      id: 'laser',
      title: 'Пост лазерной резки',
      spec: `${m.label.toLowerCase()} ${t} мм · до ${m.laserMax} мм на лазере`,
      note:
        t <= 6
          ? 'Чистая кромка, сразу в сборку. На этой толщине рядом стоит листогиб — согнём в той же партии.'
          : 'Контур и отверстия без окалины. Дальше — гибка или сварка на соседнем участке.',
    }
  }
  if (t <= m.plasmaMax) {
    return {
      id: 'plasma',
      title: 'Пост плазменной резки',
      spec: `${m.label.toLowerCase()} ${t} мм · лазер здесь уже невыгоден`,
      note: 'Крупный раскрой и толстый лист. Кромка под сварку — без отдельной зачистки в смете.',
    }
  }
  if (m.gasMax && t <= m.gasMax) {
    return {
      id: 'gas',
      title: 'Пост газовой резки',
      spec: `${m.label.toLowerCase()} ${t} мм · до ${m.gasMax} мм`,
      note: 'Плазма уже не берёт. Кислородный рез для плит и закладных под сварные конструкции.',
    }
  }
  return {
    id: 'custom',
    title: 'Нужен расчёт технолога',
    spec: m.gasMax ? `${m.label} свыше ${m.gasMax} мм` : `${m.label} свыше ${m.plasmaMax} мм`,
    note: 'Толщина вне типовых постов. Пришлите чертёж — скажем, берём ли и чем.',
  }
})

const pct = (v) => `${Math.min((v / SCALE_MAX) * 100, 100)}%`
const needlePos = computed(
  () => `calc(var(--lw) + (100% - var(--lw)) * ${Math.min(thickness.value / SCALE_MAX, 1)})`
)

function pickStation(id) {
  stationId.value = id
}

function applyVerdict() {
  if (verdict.value.id === 'custom') return
  stationId.value = verdict.value.id
  document.getElementById('floor')?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

let ldScript = null
watchEffect(() => {
  ldScript?.remove()
  const path = '/metallokonstruktsii/proizvodstvo'
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
    <section id="usluga-hero" class="sec sec--dark page-hero prz-hero">
      <div class="prz-ghost" aria-hidden="true">ЗАВОД</div>
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
          <a href="#floor" class="btn">Посмотреть участки цеха</a>
          <a href="#cta" class="btn btn--ghost">Прислать чертёж</a>
        </div>
        <div class="hero-stats" v-reveal="200">
          <div class="hero-stat">
            <b><StatCounter :value="3000" /> <small>м²</small></b>
            <span>свой цех</span>
          </div>
          <div class="hero-stat">
            <b>с 2013</b>
            <span>года в производстве</span>
          </div>
          <div class="hero-stat">
            <b><StatCounter :value="1500" suffix="+" /></b>
            <span>проектов</span>
          </div>
          <div class="hero-stat">
            <b>6</b>
            <span>участков на одной площадке</span>
          </div>
        </div>
      </div>
    </section>

    <!-- ============ ПЛАН ЦЕХА ============ -->
    <section id="floor" class="sec sec--deep">
      <div class="container">
        <div class="sec-head" v-reveal>
          <p class="sec-tag"><span class="idx">Цех</span> Свой завод</p>
          <h2 class="sec-title">Шесть участков, <em>не три подрядчика</em></h2>
          <p class="sec-sub">
            Производство металлоконструкций здесь — это станки и люди на Заревской объездной, 9В.
            Нажмите пост: что делает, до какой толщины, куда смотреть подробнее.
          </p>
        </div>

        <div class="floor" v-reveal="80">
          <button
            v-for="s in stations"
            :key="s.id"
            type="button"
            class="floor-cell"
            :class="['tone-' + s.tone, { active: stationId === s.id }]"
            :aria-pressed="stationId === s.id"
            @click="pickStation(s.id)"
          >
            <span class="floor-n">{{ s.n }}</span>
            <span class="floor-t">{{ s.title }}</span>
            <span class="floor-s">{{ s.spec }}</span>
          </button>
        </div>

        <div class="floor-panel" :class="'tone-' + station.tone" v-reveal="120">
          <div>
            <p class="floor-kicker">Участок {{ station.n }}</p>
            <h3>{{ station.title }}</h3>
            <p class="floor-spec">{{ station.spec }}</p>
            <p class="floor-text">{{ station.text }}</p>
            <RouterLink :to="station.to" class="floor-link">Подробнее об участке →</RouterLink>
          </div>
          <div class="floor-photo" v-if="station.id === 'bend'">
            <img src="/img/press-brake.png" alt="ЧПУ-листогиб на производстве Грэйдстрой" />
          </div>
          <div class="floor-photo" v-else-if="station.id === 'laser'">
            <img src="/img/hero-laser.png" alt="Лазерная резка металла в цехе" />
          </div>
        </div>
      </div>
    </section>

    <!-- ============ КАКОЙ ПОСТ ============ -->
    <section id="post" class="sec sec--dark">
      <div class="container">
        <div class="sec-head" v-reveal>
          <p class="sec-tag"><span class="idx">Посты</span> Подбор участка</p>
          <h2 class="sec-title">Какой пост возьмёт <em>вашу толщину</em></h2>
          <p class="sec-sub">
            Те же правила, по которым считает технолог: не гоним толстый лист на лазер
            и не обещаем газ по нержавейке.
          </p>
        </div>

        <div class="picker" v-reveal="80">
          <div class="picker-controls">
            <div>
              <p class="picker-label">Материал</p>
              <div class="mat-row">
                <button
                  v-for="m in materials"
                  :key="m.id"
                  type="button"
                  class="mat-btn"
                  :class="{ active: material.id === m.id }"
                  @click="material = m"
                >
                  {{ m.label }}
                </button>
              </div>
            </div>
            <div>
              <p class="picker-label">
                Толщина
                <span class="picker-value">{{ thickness }} мм</span>
              </p>
              <input
                v-model.number="thickness"
                type="range"
                min="1"
                :max="SCALE_MAX"
                step="1"
                class="thick-slider"
                aria-label="Толщина металла в миллиметрах"
              />
            </div>
          </div>

          <div class="scale" aria-hidden="true">
            <div class="scale-row">
              <span class="scale-name">Лазер</span>
              <div class="scale-track">
                <div
                  class="scale-bar scale-bar--laser"
                  :class="{ dim: verdict.id !== 'laser' }"
                  :style="{ width: pct(material.laserMax) }"
                />
              </div>
            </div>
            <div class="scale-row">
              <span class="scale-name">Плазма</span>
              <div class="scale-track">
                <div
                  class="scale-bar scale-bar--plasma"
                  :class="{ dim: verdict.id !== 'plasma' }"
                  :style="{ width: pct(material.plasmaMax) }"
                />
              </div>
            </div>
            <div class="scale-row" v-if="material.gasMax">
              <span class="scale-name">Газ</span>
              <div class="scale-track">
                <div
                  class="scale-bar scale-bar--gas"
                  :class="{ dim: verdict.id !== 'gas' }"
                  :style="{ width: pct(material.gasMax) }"
                />
              </div>
            </div>
            <div class="scale-needle" :style="{ left: needlePos }">
              <span class="needle-tip">{{ thickness }}</span>
            </div>
            <div class="scale-ticks">
              <span v-for="t in [0, 10, 20, 30, 40, 50, 60, 70]" :key="t">{{ t }}</span>
            </div>
          </div>

          <div class="verdict" :class="'verdict--' + verdict.id">
            <div class="verdict-head">
              <span class="verdict-dot" />
              <p class="verdict-tech">{{ verdict.title }}</p>
              <p class="verdict-spec">{{ verdict.spec }}</p>
            </div>
            <p class="verdict-note">{{ verdict.note }}</p>
            <div class="verdict-cta">
              <button v-if="verdict.id !== 'custom'" type="button" class="btn btn--ghost" @click="applyVerdict">
                Показать этот участок на плане
              </button>
              <RouterLink to="/kalkulyator" class="btn">Рассчитать деталь</RouterLink>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ============ СЕРИЯ / КАРКАС ============ -->
    <section id="mode" class="sec sec--light">
      <div class="container">
        <div class="sec-head" v-reveal>
          <p class="sec-tag"><span class="idx">Поток</span> Как завод берёт заказ</p>
          <h2 class="sec-title">Серия и каркас <em>на одних постах</em></h2>
        </div>

        <div class="mode-row" v-reveal="80">
          <button
            v-for="m in modes"
            :key="m.id"
            type="button"
            class="mode-btn"
            :class="{ active: modeId === m.id }"
            :aria-pressed="modeId === m.id"
            @click="modeId = m.id"
          >
            {{ m.title }}
          </button>
        </div>
        <div class="mode-panel" v-reveal="100">
          <p class="mode-lead">{{ mode.lead }}</p>
          <ul class="mode-points">
            <li v-for="p in mode.points" :key="p">{{ p }}</li>
          </ul>
          <RouterLink to="/metallokonstruktsii/izgotovlenie" class="mode-more">
            Собрать состав заказа на изготовление →
          </RouterLink>
        </div>

        <div class="sec-head flow-head" v-reveal>
          <p class="sec-tag"><span class="idx">Маршрут</span> Путь детали</p>
          <h2 class="sec-title">Как деталь идёт <em>по площадке</em></h2>
        </div>
        <div class="flow-nav" v-reveal="80">
          <button
            v-for="(f, i) in flow"
            :key="f.title"
            type="button"
            class="flow-tab"
            :class="{ active: flowI === i }"
            @click="flowI = i"
          >
            <span>{{ String(i + 1).padStart(2, '0') }}</span>
            {{ f.title }}
          </button>
        </div>
        <div class="flow-panel">
          <h3>{{ flowStep.title }}</h3>
          <p>{{ flowStep.text }}</p>
        </div>

        <div class="feat-grid">
          <article v-for="(f, i) in page.features" :key="f.title" class="card feat-card" v-reveal="i * 70">
            <span class="feat-num">{{ String(i + 1).padStart(2, '0') }}</span>
            <h3>{{ f.title }}</h3>
            <p>{{ f.text }}</p>
          </article>
        </div>

        <div class="visit" v-reveal>
          <div>
            <p class="visit-kicker">Можно приехать</p>
            <h2>Цех в Дзержинске, не «офис в переписке»</h2>
            <p>
              {{ company.postalAddress }}. {{ company.schedule }}.
              Имеет смысл захватить чертёж: часть вопросов закрывается у станка.
            </p>
            <div class="visit-actions">
              <a :href="company.yandexMaps.url" target="_blank" rel="noopener" class="btn">Открыть на карте</a>
              <RouterLink to="/kontakty" class="btn btn--ghost">Контакты и схема</RouterLink>
            </div>
          </div>
          <a :href="company.phoneHref" class="visit-phone" data-track="tel-proizvodstvo">{{ company.phone }}</a>
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
          <p class="srv-others-h">Другие задачи по металлоконструкциям:</p>
          <div class="srv-others-row">
            <RouterLink :to="MK_PARENT_PATH" class="srv-other srv-other--acc">Все металлоконструкции →</RouterLink>
            <RouterLink v-for="s in siblings" :key="s.slug" :to="metalworkLandingPath(s.slug)" class="srv-other">
              {{ s.navLabel }} →
            </RouterLink>
          </div>
        </div>
        <div class="srv-others">
          <p class="srv-others-h">Участки производства:</p>
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
      title-em="— производство металлоконструкций"
    />
    <FinalCtaSection />
  </main>
</template>

<style scoped>
.prz-hero { padding-bottom: 64px; overflow: hidden; }
#floor, #post, #mode { scroll-margin-top: 88px; }
.prz-ghost {
  position: absolute;
  top: 40px;
  right: -20px;
  font-family: var(--font-d);
  font-size: clamp(80px, 16vw, 220px);
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
.hero-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 18px;
  padding-top: 34px;
  border-top: 1px solid var(--line-d);
}
.hero-stat b {
  display: block;
  font-family: var(--font-d);
  font-size: clamp(18px, 2.2vw, 26px);
  font-weight: 900;
  color: var(--acc-hot);
  margin-bottom: 4px;
}
.hero-stat small { font-size: 0.55em; }
.hero-stat > span {
  font-family: var(--font-m);
  font-size: 11.5px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--w-faint);
}

.floor {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-bottom: 16px;
}
.floor-cell {
  text-align: left;
  padding: 20px 18px 18px;
  background: var(--card-d);
  border: 1px solid var(--line-d);
  border-left: 3px solid var(--acc);
  border-radius: var(--r-sm);
  color: var(--w-soft);
  transition: border-color 0.25s, color 0.25s, transform 0.25s var(--ease), background 0.25s;
}
.floor-cell.tone-plasma { border-left-color: #4f8dff; }
.floor-cell.tone-gas { border-left-color: #3dd68c; }
.floor-cell.tone-bend { border-left-color: #c9a227; }
.floor-cell.tone-weld { border-left-color: #e05c4a; }
.floor-cell.tone-ship { border-left-color: #8b939d; }
.floor-cell:hover { color: var(--white); transform: translateY(-2px); }
.floor-cell.active {
  color: var(--white);
  background: rgba(255, 90, 31, 0.08);
  border-color: var(--acc);
}
.floor-cell.tone-plasma.active { background: rgba(79, 141, 255, 0.08); border-color: #4f8dff; }
.floor-cell.tone-gas.active { background: rgba(61, 214, 140, 0.08); border-color: #3dd68c; }
.floor-cell.tone-bend.active { background: rgba(201, 162, 39, 0.1); border-color: #c9a227; }
.floor-cell.tone-weld.active { background: rgba(224, 92, 74, 0.1); border-color: #e05c4a; }
.floor-cell.tone-ship.active { background: rgba(255, 255, 255, 0.06); border-color: #8b939d; }
.floor-n {
  display: block;
  font-family: var(--font-m);
  font-size: 11px;
  color: var(--acc);
  margin-bottom: 6px;
}
.floor-t {
  display: block;
  font-family: var(--font-d);
  font-size: 16px;
  font-weight: 700;
  text-transform: uppercase;
  margin-bottom: 6px;
  color: var(--white);
}
.floor-s { font-size: 12.5px; }

.floor-panel {
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: 28px;
  align-items: center;
  padding: 28px 30px;
  border: 1px solid var(--line-d);
  border-radius: var(--r);
  background: var(--card-d);
  border-left: 3px solid var(--acc);
}
.floor-panel.tone-plasma { border-left-color: #4f8dff; }
.floor-panel.tone-gas { border-left-color: #3dd68c; }
.floor-panel.tone-bend { border-left-color: #c9a227; }
.floor-panel.tone-weld { border-left-color: #e05c4a; }
.floor-panel.tone-ship { border-left-color: #8b939d; }
.floor-kicker {
  font-family: var(--font-m);
  font-size: 11px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--acc);
  margin-bottom: 8px;
}
.floor-panel h3 {
  font-family: var(--font-d);
  font-size: 22px;
  text-transform: uppercase;
  margin-bottom: 6px;
}
.floor-spec { font-size: 13px; color: var(--w-faint); margin-bottom: 12px; }
.floor-text { font-size: 15px; color: var(--w-soft); max-width: 520px; margin-bottom: 16px; }
.floor-link { font-size: 14.5px; font-weight: 700; color: var(--acc); }
.floor-link:hover { color: var(--acc-hot); }
.floor-photo { border-radius: var(--r-sm); overflow: hidden; border: 1px solid var(--line-d); }
.floor-photo img { width: 100%; height: 180px; object-fit: cover; }
.floor-panel:not(:has(.floor-photo)) { grid-template-columns: 1fr; }

.picker {
  padding: 36px 32px 40px;
  border: 1px solid var(--line-d);
  border-radius: var(--r);
  background: var(--card-d);
}
.picker-controls {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 48px;
  align-items: end;
  margin-bottom: 36px;
}
.picker-label {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 16px;
  font-family: var(--font-m);
  font-size: 12px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--w-faint);
  margin-bottom: 14px;
}
.picker-value { font-size: 18px; letter-spacing: 0; color: var(--acc-hot); font-weight: 600; }
.mat-row { display: flex; gap: 8px; }
.mat-btn {
  padding: 11px 20px;
  background: transparent;
  border: 1px solid var(--line-d);
  border-radius: var(--r-sm);
  color: var(--w-soft);
  font-size: 14px;
  font-weight: 600;
  transition: all 0.25s;
}
.mat-btn:hover { border-color: rgba(255, 90, 31, 0.5); color: var(--white); }
.mat-btn.active { background: var(--acc); border-color: var(--acc); color: #fff; }
.thick-slider {
  width: 100%;
  height: 4px;
  appearance: none;
  -webkit-appearance: none;
  background: rgba(255, 255, 255, 0.12);
  border-radius: 2px;
  outline: none;
  cursor: pointer;
}
.thick-slider::-webkit-slider-thumb {
  appearance: none;
  -webkit-appearance: none;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: var(--acc);
  border: 3px solid var(--bg0);
  box-shadow: 0 0 0 1.5px var(--acc);
}

.scale {
  --lw: 92px;
  position: relative;
  padding-bottom: 26px;
  margin-bottom: 28px;
}
.scale-row {
  display: grid;
  grid-template-columns: 76px 1fr;
  align-items: center;
  gap: 16px;
  margin-bottom: 10px;
}
.scale-name {
  font-family: var(--font-m);
  font-size: 11.5px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--w-faint);
}
.scale-track {
  height: 14px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 4px;
  overflow: hidden;
}
.scale-bar { height: 100%; border-radius: 4px; transition: width 0.5s var(--ease), opacity 0.35s; }
.scale-bar--laser { background: linear-gradient(90deg, #ff7d3f, #ff5a1f); }
.scale-bar--plasma { background: linear-gradient(90deg, #4f8dff, #2f6bdb); }
.scale-bar--gas { background: linear-gradient(90deg, #3dd68c, #1fa968); }
.scale-bar.dim { opacity: 0.28; }
.scale-needle {
  position: absolute;
  top: -8px;
  bottom: 18px;
  width: 2px;
  background: var(--white);
  transition: left 0.15s linear;
  pointer-events: none;
}
.needle-tip {
  position: absolute;
  top: -22px;
  left: 50%;
  transform: translateX(-50%);
  font-family: var(--font-m);
  font-size: 11px;
  color: var(--white);
  background: rgba(255, 255, 255, 0.1);
  padding: 1px 7px;
  border-radius: 4px;
}
.scale-ticks {
  display: flex;
  justify-content: space-between;
  margin-left: var(--lw);
  margin-top: 4px;
  font-family: var(--font-m);
  font-size: 10.5px;
  color: var(--w-faint);
}

.verdict {
  border: 1px solid var(--line-d);
  border-left: 3px solid var(--acc);
  border-radius: var(--r-sm);
  padding: 24px 26px;
  background: rgba(255, 90, 31, 0.04);
}
.verdict--plasma { border-left-color: #4f8dff; background: rgba(79, 141, 255, 0.05); }
.verdict--gas { border-left-color: #3dd68c; background: rgba(61, 214, 140, 0.05); }
.verdict--custom { border-left-color: var(--w-faint); background: rgba(255, 255, 255, 0.03); }
.verdict-head { display: flex; align-items: baseline; gap: 14px; flex-wrap: wrap; margin-bottom: 10px; }
.verdict-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--acc);
  align-self: center;
  box-shadow: 0 0 14px rgba(255, 90, 31, 0.7);
}
.verdict--plasma .verdict-dot { background: #4f8dff; box-shadow: 0 0 14px rgba(79, 141, 255, 0.7); }
.verdict--gas .verdict-dot { background: #3dd68c; box-shadow: 0 0 14px rgba(61, 214, 140, 0.7); }
.verdict--custom .verdict-dot { background: var(--w-faint); box-shadow: none; }
.verdict-tech { font-family: var(--font-d); font-size: 18px; font-weight: 700; text-transform: uppercase; }
.verdict-spec {
  font-family: var(--font-m);
  font-size: 12px;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--w-faint);
}
.verdict-note { font-size: 14.5px; color: var(--w-soft); max-width: 640px; margin-bottom: 18px; }
.verdict-cta { display: flex; flex-wrap: wrap; gap: 10px; }

.mode-row { display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 16px; }
.mode-btn {
  padding: 14px 22px;
  background: var(--paper2);
  border: 1px solid var(--line-l);
  border-radius: var(--r-sm);
  font-weight: 700;
  color: var(--ink-soft);
}
.mode-btn.active { border-color: var(--acc); color: var(--ink); background: #fff; }
.mode-panel {
  padding: 28px 30px;
  border: 1px solid var(--line-l);
  border-radius: var(--r);
  background: var(--paper2);
  margin-bottom: 56px;
}
.mode-lead { font-size: 17px; font-weight: 600; margin-bottom: 16px; max-width: 640px; }
.mode-points { display: grid; gap: 8px; margin-bottom: 18px; }
.mode-points li {
  position: relative;
  padding-left: 22px;
  font-size: 14.5px;
  color: var(--ink-soft);
}
.mode-points li::before { content: '◆'; position: absolute; left: 0; top: 1px; font-size: 10px; color: var(--acc); }
.mode-more { font-size: 14.5px; font-weight: 700; color: var(--acc); }
.mode-more:hover { color: var(--acc-hot); }

.flow-head { margin-top: 8px; }
.flow-nav {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 8px;
  margin-bottom: 14px;
}
.flow-tab {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 6px;
  padding: 14px 12px;
  background: #fff;
  border: 1px solid var(--line-l);
  border-radius: var(--r-sm);
  font-size: 13px;
  font-weight: 700;
  color: var(--ink-soft);
  text-align: left;
}
.flow-tab span { font-family: var(--font-m); font-size: 11px; color: var(--acc); }
.flow-tab.active { border-color: var(--acc); color: var(--ink); }
.flow-panel {
  padding: 22px 26px;
  border: 1px solid var(--line-l);
  border-radius: var(--r);
  background: var(--paper2);
  margin-bottom: 48px;
}
.flow-panel h3 {
  font-family: var(--font-d);
  font-size: 16px;
  text-transform: uppercase;
  margin-bottom: 8px;
}
.flow-panel p { font-size: 15px; color: var(--ink-soft); max-width: 640px; }

.feat-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
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

.visit {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 28px;
  flex-wrap: wrap;
  padding: 32px 34px;
  margin-bottom: 40px;
  border-radius: var(--r);
  border: 1px solid rgba(255, 90, 31, 0.35);
  background:
    radial-gradient(ellipse at top left, rgba(255, 90, 31, 0.1), transparent 55%),
    var(--paper2);
}
.visit-kicker {
  font-family: var(--font-m);
  font-size: 11px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--acc);
  margin-bottom: 8px;
}
.visit h2 {
  font-family: var(--font-d);
  font-size: 20px;
  text-transform: uppercase;
  margin-bottom: 10px;
}
.visit p { font-size: 14.5px; color: var(--ink-soft); max-width: 560px; margin-bottom: 18px; }
.visit-actions { display: flex; flex-wrap: wrap; gap: 10px; }
.visit-phone {
  font-family: var(--font-m);
  font-size: clamp(16px, 2vw, 22px);
  font-weight: 700;
  color: var(--ink);
  white-space: nowrap;
}
.visit-phone:hover { color: var(--acc); }

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
  .floor, .flow-nav { grid-template-columns: 1fr 1fr; }
  .floor-panel { grid-template-columns: 1fr; }
  .picker-controls { grid-template-columns: 1fr; gap: 24px; }
}
@media (max-width: 900px) {
  .hero-stats, .feat-grid, .detail-grid { grid-template-columns: 1fr 1fr; }
  .prz-ghost { display: none; }
}
@media (max-width: 640px) {
  .floor, .flow-nav, .hero-stats, .feat-grid, .detail-grid { grid-template-columns: 1fr; }
  .flow-tab { flex-direction: row; align-items: center; gap: 10px; }
  .scale { --lw: 70px; }
  .scale-row { grid-template-columns: 60px 1fr; }
}
</style>
