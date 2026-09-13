<script setup>
import { computed, watchEffect, onUnmounted } from 'vue'
import { uslugi, getUslugaBySlug } from '../data/uslugi'
import {
  laserLandings,
  getLaserLanding,
  laserLandingPath,
  LASER_PARENT_PATH,
  LASER_PARENT_LABEL,
} from '../data/lazernayaRezka'
import {
  metalworkLandings,
  getMetalworkLanding,
  metalworkLandingPath,
  MK_PARENT_PATH,
  MK_PARENT_LABEL,
} from '../data/metallokonstruktsii'
import {
  mainServices,
  getWorkLanding,
  workLandingPath,
  otherCycleLinks,
  WORKS_PARENT_PATH,
  WORKS_PARENT_LABEL,
  IZG_PATH,
} from '../data/services'
import FaqSection from '../components/FaqSection.vue'
import FinalCtaSection from '../components/FinalCtaSection.vue'
import ShopGallery from '../components/ShopGallery.vue'
import LeadForm from '../components/ui/LeadForm.vue'
import QuickCallBanner from '../components/QuickCallBanner.vue'
import { company } from '../data/company'

const SITE = 'https://greydstroy.ru'

const props = defineProps({
  slug: { type: String, default: '' },
  childSlug: { type: String, default: '' },
  hub: { type: String, default: '' },
})

const isMkChild = computed(() => props.hub === 'metalwork')
const isWork = computed(() => props.hub === 'works')
const parent = computed(() => (props.slug ? getUslugaBySlug(props.slug) : null))
const child = computed(() => {
  if (isMkChild.value) return getMetalworkLanding(props.childSlug)
  if (isWork.value) return getWorkLanding(props.childSlug)
  if (props.childSlug) return getLaserLanding(props.childSlug)
  return null
})
const usluga = computed(() => child.value || parent.value)
const isLaserHub = computed(() => props.slug === 'lazernaya-rezka' && !props.childSlug)
const isLaserChild = computed(() => !!props.childSlug && !isMkChild.value && !isWork.value)

const crumbs = computed(() => {
  const items = [{ name: 'Главная', to: '/' }]
  if (isMkChild.value) {
    items.push({ name: MK_PARENT_LABEL, to: MK_PARENT_PATH })
    items.push({ name: child.value.navLabel, to: '' })
    return items
  }
  items.push({ name: WORKS_PARENT_LABEL, to: WORKS_PARENT_PATH })
  if (isWork.value) {
    items.push({ name: child.value.navLabel, to: '' })
  } else if (isLaserChild.value) {
    items.push({ name: 'Изготовление', to: IZG_PATH })
    items.push({ name: LASER_PARENT_LABEL, to: LASER_PARENT_PATH })
    items.push({ name: child.value.navLabel, to: '' })
  } else if (parent.value) {
    items.push({ name: 'Изготовление', to: IZG_PATH })
    items.push({ name: parent.value.label, to: '' })
  }
  return items
})

const seoParagraphs = computed(() => {
  const t = usluga.value?.seoText
  if (!t) return []
  return Array.isArray(t) ? t : [t]
})

const others = computed(() => {
  const skip = isLaserChild.value ? 'lazernaya-rezka' : props.slug
  return uslugi.filter((u) => u.slug !== skip)
})

const siblings = computed(() => {
  if (isWork.value) {
    const current = workLandingPath(props.childSlug)
    return mainServices
      .filter((s) => s.to !== current)
      .map((s) => ({ to: s.to, navLabel: s.navLabel }))
  }
  if (isMkChild.value) {
    return metalworkLandings
      .filter((p) => p.slug !== props.childSlug)
      .map((p) => ({ to: metalworkLandingPath(p.slug), navLabel: p.navLabel }))
  }
  if (!isLaserChild.value && !isLaserHub.value) return []
  return laserLandings
    .filter((p) => p.slug !== props.childSlug)
    .map((p) => ({ to: laserLandingPath(p.slug), navLabel: p.navLabel }))
})

const clusterParentTo = computed(() => {
  if (isWork.value) return WORKS_PARENT_PATH
  return isMkChild.value ? MK_PARENT_PATH : LASER_PARENT_PATH
})
const clusterParentLabel = computed(() => {
  if (isWork.value) return 'Все услуги →'
  return isMkChild.value ? 'Все металлоконструкции →' : 'Вся лазерная резка →'
})
const clusterHeading = computed(() => {
  if (isWork.value) return 'Другие услуги полного цикла:'
  if (isMkChild.value) return 'Другие задачи по металлоконструкциям:'
  return isLaserHub.value ? 'По задачам лазерной резки:' : 'Другие задачи лазерной резки:'
})

const pageKey = computed(() => {
  if (isWork.value) return `work-${props.childSlug}`
  if (isMkChild.value) return `mk-${props.childSlug}`
  if (props.childSlug) return `laser-${props.childSlug}`
  return props.slug
})

const isTech = computed(() => !!parent.value && !isWork.value && !isMkChild.value)

const cycleOthers = computed(() => {
  const current = isWork.value
    ? workLandingPath(props.childSlug)
    : isMkChild.value
      ? metalworkLandingPath(props.childSlug)
      : IZG_PATH
  return otherCycleLinks(current)
})

const tagIdx = computed(() => {
  if (isMkChild.value) return 'Металлоконструкции'
  if (isLaserChild.value) return 'Лазерная резка'
  if (isTech.value) return 'Технологии производства'
  return 'Услуги'
})

const faqTitleEm = computed(() => {
  const label = usluga.value?.label?.toLowerCase() || ''
  return '— ' + label
})

/* JSON-LD: FAQ + хлебные крошки + Service */
let ldScript = null
watchEffect(() => {
  ldScript?.remove()
  if (!usluga.value) return

  const path = isMkChild.value
    ? metalworkLandingPath(props.childSlug)
    : isWork.value
      ? workLandingPath(props.childSlug)
      : isLaserChild.value
        ? laserLandingPath(props.childSlug)
        : `/uslugi/${props.slug}`

  const graph = [
    {
      '@type': 'BreadcrumbList',
      itemListElement: crumbs.value.map((c, i) => ({
        '@type': 'ListItem',
        position: i + 1,
        name: c.name,
        item: c.to ? SITE + c.to : SITE + path,
      })),
    },
    {
      '@type': 'Service',
      name: usluga.value.h1,
      description: usluga.value.metaDescription || usluga.value.desc,
      url: SITE + path,
      provider: { '@id': `${SITE}/#organization` },
      areaServed: 'RU',
    },
    {
      '@type': 'FAQPage',
      mainEntity: usluga.value.faq.map((f) => ({
        '@type': 'Question',
        name: f.q,
        acceptedAnswer: { '@type': 'Answer', text: f.a },
      })),
    },
  ]

  ldScript = document.createElement('script')
  ldScript.type = 'application/ld+json'
  ldScript.textContent = JSON.stringify({ '@context': 'https://schema.org', '@graph': graph })
  document.head.appendChild(ldScript)
})
onUnmounted(() => ldScript?.remove())
</script>

<template>
  <main v-if="usluga" :key="pageKey">
    <!-- ============ HERO (лазер — как на главной) ============ -->
    <template v-if="isLaserHub">
      <section id="usluga-hero" class="sec sec--dark page-hero srv-hero srv-hero--split">
        <div class="container">
          <nav class="crumbs" aria-label="Навигация">
            <template v-for="(c, i) in crumbs" :key="c.name">
              <RouterLink v-if="c.to" :to="c.to">{{ c.name }}</RouterLink>
              <span v-else aria-current="page">{{ c.name }}</span>
              <span v-if="i < crumbs.length - 1" class="crumbs-sep" aria-hidden="true">/</span>
            </template>
          </nav>

          <div class="hero-in">
            <div class="hero-left">
              <p class="hero-kicker" v-reveal>
                <span class="dot"></span>
                Звоните прямо сейчас, чтобы получить расчёт цены
              </p>

              <h1 class="hero-title" v-reveal="80">
                {{ usluga.h1 }} <em>{{ usluga.h1em }}</em>
              </h1>

              <p class="hero-sub" v-reveal="160">{{ usluga.desc }}</p>

              <ul class="hero-trust" v-reveal="240">
                <li v-for="st in usluga.stats" :key="st.b + st.s">{{ st.b }} {{ st.s }}</li>
              </ul>

              <div class="hero-cta" v-reveal="320">
                <RouterLink to="/kalkulyator" class="btn" data-track="calc-usluga">Калькулятор цены</RouterLink>
                <p class="btn-note">Ориентир цены и срока — сразу.<br />Точный расчёт по чертежу.</p>
              </div>
            </div>

            <div class="hero-form" v-reveal="300">
              <div class="hero-form-filter" role="note">
                <p class="hff-lead">Только для коммерческих заказов</p>
                <p class="hff-warn">
                  Штучные не берём, работаем с сериями: свяжитесь с нами,
                  чтобы узнать стоимость и сроки
                </p>
              </div>
              <LeadForm button-text="Рассчитать стоимость" />
            </div>

            <div class="hero-qcb" v-reveal="360">
              <QuickCallBanner embedded />
            </div>
          </div>
        </div>
      </section>

      <div class="qcb-standalone">
        <QuickCallBanner />
      </div>
    </template>

    <!-- ============ HERO (остальные услуги) ============ -->
    <section v-else id="usluga-hero" class="sec sec--dark page-hero srv-hero">
      <div class="container">
        <nav class="crumbs" aria-label="Навигация">
          <template v-for="(c, i) in crumbs" :key="c.name">
            <RouterLink v-if="c.to" :to="c.to">{{ c.name }}</RouterLink>
            <span v-else aria-current="page">{{ c.name }}</span>
            <span v-if="i < crumbs.length - 1" class="crumbs-sep" aria-hidden="true">/</span>
          </template>
        </nav>
        <div class="sec-head" v-reveal="60">
          <p class="sec-tag">
            <span class="idx">{{ tagIdx }}</span>
            {{ usluga.label }}
          </p>
          <h1 class="page-title">{{ usluga.h1 }} <em>{{ usluga.h1em }}</em></h1>
          <p class="page-desc">{{ usluga.desc }}</p>
        </div>

        <div class="srv-hero-cta" v-reveal="140">
          <RouterLink to="/kalkulyator" class="btn" data-track="calc-usluga">Рассчитать стоимость</RouterLink>
          <a href="#cta" class="btn btn--ghost">Прислать чертёж</a>
        </div>

        <div class="srv-stats" v-reveal="200">
          <div v-for="st in usluga.stats" :key="st.b + st.s" class="srv-stat">
            <b>{{ st.b }}</b><span>{{ st.s }}</span>
          </div>
        </div>
      </div>
    </section>

    <!-- ============ ЧТО ВЫ ПОЛУЧАЕТЕ ============ -->
    <section id="features" class="sec sec--deep">
      <div class="container">
        <div class="sec-head" v-reveal>
          <p class="sec-tag"><span class="idx">Суть</span> Что вы получаете</p>
          <h2 class="sec-title">Что вы получите <em>на выходе</em></h2>
        </div>

        <div v-if="isLaserHub" class="feat-cta" v-reveal="40">
          <a
            :href="company.phoneHref"
            class="btn"
            data-track="tel-laser-engineer"
          >Позвонить инженеру</a>
          <p class="feat-cta-note">Сориентируем по срокам и цене прямо во время разговора</p>
        </div>

        <div class="feat-grid">
          <article v-for="(f, i) in usluga.features" :key="f.title" class="card feat-card" v-reveal="i * 80">
            <span class="feat-num">{{ String(i + 1).padStart(2, '0') }}</span>
            <h3>{{ f.title }}</h3>
            <p>{{ f.text }}</p>
          </article>
        </div>
      </div>
    </section>

    <ShopGallery
      v-if="usluga.photos?.length"
      :items="usluga.photos"
      tag="Объект"
      kicker="С площадки"
      title="Как это выглядит"
      title-em="в металле"
    />

    <!-- ============ ОТ ЧЕГО ЗАВИСИТ ЦЕНА ============ -->
    <section v-if="usluga.factors" id="factors" class="sec sec--dark">
      <div class="container">
        <div class="sec-head" v-reveal>
          <p class="sec-tag"><span class="idx">Стоимость</span> Из чего складывается цена</p>
          <h2 class="sec-title">От чего зависит <em>{{ usluga.factorsEm || 'цена' }}</em></h2>
        </div>
        <div class="factor-grid">
          <article v-for="(f, i) in usluga.factors" :key="f.title" class="factor-card" v-reveal="i * 70">
            <span class="feat-num">{{ String(i + 1).padStart(2, '0') }}</span>
            <h3>{{ f.title }}</h3>
            <p>{{ f.text }}</p>
          </article>
        </div>
      </div>
    </section>

    <!-- ============ ПРИМЕНЕНИЕ + ДРУГИЕ УСЛУГИ ============ -->
    <section id="apps" class="sec sec--light">
      <div class="container">
        <div class="sec-head" v-reveal>
          <p class="sec-tag"><span class="idx">Применение</span> {{ usluga.appsTitle }}</p>
          <h2 class="sec-title">
            <template v-if="usluga.appsH2">
              {{ usluga.appsH2 }} <em v-if="usluga.appsH2em">{{ usluga.appsH2em }}</em>
            </template>
            <template v-else>
              Под задачу, <em>а не «по прайсу»</em>
            </template>
          </h2>
        </div>

        <div class="apps-row" v-reveal="80">
          <span v-for="a in usluga.apps" :key="a" class="apps-chip">{{ a }}</span>
        </div>

        <div class="apps-copy">
          <p v-for="p in seoParagraphs" :key="p.slice(0, 48)" class="apps-text">{{ p }}</p>
        </div>

        <div v-if="usluga.details" class="detail-grid">
          <article v-for="d in usluga.details" :key="d.title" class="detail-card">
            <h2>{{ d.title }}</h2>
            <p>{{ d.text }}</p>
          </article>
        </div>

        <div v-if="usluga.priceRows" class="price-wrap" v-reveal="80">
          <p class="price-note">Ориентир за работы без металла. С металлом, покрытием и монтажом считает калькулятор и смета по чертежу.</p>
          <div class="price-table">
            <div v-for="row in usluga.priceRows" :key="row.name" class="price-row">
              <div>
                <b>{{ row.name }}</b>
                <span>{{ row.note }}</span>
              </div>
              <p>{{ row.price }}</p>
            </div>
          </div>
        </div>

        <div v-if="siblings.length" class="srv-others srv-cluster" v-reveal="140">
          <p class="srv-others-h">{{ clusterHeading }}</p>
          <div class="srv-others-row">
            <RouterLink
              v-if="isLaserChild || isMkChild || isWork"
              :to="clusterParentTo"
              class="srv-other srv-other--acc"
            >
              {{ clusterParentLabel }}
            </RouterLink>
            <RouterLink
              v-for="s in siblings"
              :key="s.to"
              :to="s.to"
              class="srv-other"
            >
              {{ s.navLabel }} →
            </RouterLink>
          </div>
        </div>

        <div v-if="isTech" class="srv-others srv-cycle" v-reveal="150">
          <p class="srv-others-h">Нужны готовые конструкции, а не только резка?</p>
          <p class="srv-cycle-text">
            Этот участок — часть нашего цеха. Изготовим каркас целиком, привезём
            и смонтируем на объекте или построим здание под ключ.
          </p>
          <div class="srv-others-row">
            <RouterLink :to="IZG_PATH" class="srv-other srv-other--acc">Изготовление металлоконструкций →</RouterLink>
            <RouterLink
              v-for="s in cycleOthers"
              :key="s.to"
              :to="s.to"
              class="srv-other"
            >
              {{ s.navLabel }} →
            </RouterLink>
          </div>
        </div>

        <div class="srv-others" v-reveal="160">
          <p class="srv-others-h">{{ isMkChild ? 'Участки того же цеха:' : isWork ? 'Технологии производства на заводе:' : 'Другие участки производства:' }}</p>
          <div class="srv-others-row">
            <RouterLink
              v-for="o in others"
              :key="o.slug"
              :to="`/uslugi/${o.slug}`"
              class="srv-other"
            >
              {{ o.label }} →
            </RouterLink>
            <RouterLink
              v-if="isWork"
              to="/metallokonstruktsii"
              class="srv-other srv-other--acc"
            >
              Каталог металлоконструкций →
            </RouterLink>
          </div>
        </div>
      </div>
    </section>

    <FaqSection
      :items="usluga.faq"
      idx="Вопросы"
      title="Частые вопросы"
      :title-em="faqTitleEm"
    />
    <FinalCtaSection />
  </main>
</template>

<style scoped>
/* ============ hero ============ */
.srv-hero { padding-bottom: 64px; }

.crumbs {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px 10px;
  margin-bottom: 36px;
  font-size: 13.5px;
  color: var(--w-faint);
}
.crumbs a {
  color: var(--w-soft);
  transition: color 0.2s;
}
.crumbs a:hover { color: var(--acc-hot); }
.crumbs [aria-current="page"] { color: var(--white); }
.crumbs-sep { color: var(--w-faint); opacity: 0.55; }

/* ---- laser hub: same structure as home HeroSection ---- */
.srv-hero--split { padding-bottom: 90px; }

.hero-in {
  display: grid;
  grid-template-columns: 1.35fr 0.75fr;
  gap: 64px;
  align-items: center;
}

.hero-kicker {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-family: var(--font-m);
  font-size: 12px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--w-soft);
  border: 1px solid var(--line-d);
  padding: 8px 16px;
  border-radius: 40px;
  margin-bottom: 30px;
  background: rgba(11, 14, 17, 0.5);
  max-width: 100%;
  line-height: 1.4;
}
.hero-kicker .dot {
  width: 7px;
  height: 7px;
  flex-shrink: 0;
  border-radius: 50%;
  background: var(--acc);
  box-shadow: 0 0 12px var(--acc);
  animation: srv-pulse 2s infinite;
}
@keyframes srv-pulse {
  50% { opacity: 0.4; }
}

.hero-title {
  font-family: var(--font-d);
  font-size: clamp(24px, 4.6vw, 38px);
  font-weight: 900;
  line-height: 1.08;
  text-transform: uppercase;
  letter-spacing: -0.015em;
  margin-bottom: 28px;
}
.hero-title em {
  font-style: normal;
  color: var(--acc);
  text-shadow: 0 0 44px rgba(255, 90, 31, 0.45);
}

.hero-sub {
  font-size: clamp(15px, 1.5vw, 18px);
  color: var(--w-soft);
  max-width: 560px;
  margin-bottom: 30px;
}

.hero-trust {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 38px;
}
.hero-trust li {
  font-family: var(--font-m);
  font-size: 12px;
  color: var(--white);
  border: 1px solid var(--line-d);
  background: rgba(255, 255, 255, 0.05);
  padding: 8px 15px;
  border-radius: 6px;
  backdrop-filter: blur(6px);
}
.hero-trust li::before {
  content: '▸ ';
  color: var(--acc);
}

.hero-cta {
  display: flex;
  align-items: center;
  gap: 24px;
  flex-wrap: wrap;
}
.hero-cta .btn-note { margin-top: 0; }

.hero-form {
  background: rgba(17, 21, 26, 0.86);
  backdrop-filter: blur(18px);
  border: 1px solid var(--line-d);
  border-top: 3px solid var(--acc);
  border-radius: var(--r);
  padding: 30px 28px;
  box-shadow: 0 40px 80px rgba(0, 0, 0, 0.5);
}

.hero-form-filter {
  margin-bottom: 20px;
  padding-bottom: 18px;
  border-bottom: 1px solid var(--line-d);
}
.hff-lead {
  font-family: var(--font-d);
  font-size: 15px;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--white);
  margin-bottom: 8px;
}
.hff-warn {
  font-size: 12.5px;
  line-height: 1.5;
  color: var(--w-soft);
}

.hero-qcb {
  display: none;
  grid-column: 1 / -1;
}

@media (min-width: 1100px) and (min-height: 820px) {
  .hero-qcb { display: block; }
  .srv-hero--split { padding-bottom: 110px; }
  .qcb-standalone { display: none; }
}

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

/* ============ features ============ */
.feat-cta {
  display: flex;
  align-items: center;
  gap: 20px;
  flex-wrap: wrap;
  margin-bottom: 28px;
}
.feat-cta-note {
  font-size: 14px;
  color: var(--w-soft);
  max-width: 320px;
}

.feat-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}
.feat-card { padding: 28px; }
.feat-num {
  display: block;
  font-family: var(--font-d);
  font-size: 22px;
  font-weight: 900;
  color: transparent;
  -webkit-text-stroke: 1.2px rgba(255, 255, 255, 0.22);
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
.feat-card p { font-size: 14px; color: var(--w-soft); }

/* ============ цена ============ */
.factor-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}
.factor-card {
  padding: 26px 24px;
  border: 1px solid var(--line-d);
  border-radius: var(--r);
  background: var(--card-d);
}
.factor-card h3 {
  font-family: var(--font-d);
  font-size: 15px;
  font-weight: 700;
  text-transform: uppercase;
  margin-bottom: 10px;
}
.factor-card p { font-size: 14px; color: var(--w-soft); line-height: 1.65; }
.factor-card .feat-num { -webkit-text-stroke-color: rgba(255, 255, 255, 0.22); }
.factor-card:hover .feat-num { -webkit-text-stroke-color: var(--acc); }

.price-wrap { margin-bottom: 40px; }
.price-note {
  font-size: 14px;
  color: var(--ink-soft);
  margin-bottom: 16px;
  max-width: 720px;
}
.price-table {
  border: 1px solid var(--line-l);
  border-radius: var(--r);
  overflow: hidden;
  background: var(--paper2);
}
.price-row {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 16px;
  align-items: center;
  padding: 16px 22px;
  border-bottom: 1px solid var(--line-l);
}
.price-row:last-child { border-bottom: none; }
.price-row b {
  display: block;
  font-size: 14.5px;
  margin-bottom: 2px;
}
.price-row span {
  font-size: 13px;
  color: var(--ink-faint);
}
.price-row p {
  font-family: var(--font-m);
  font-size: 14px;
  font-weight: 700;
  color: var(--acc);
  white-space: nowrap;
}

/* ============ применение ============ */
.apps-row {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-bottom: 26px;
}
.apps-chip {
  padding: 10px 20px;
  border: 1px solid var(--line-l);
  border-radius: 999px;
  font-size: 14px;
  font-weight: 600;
  color: var(--ink-soft);
  background: var(--paper2);
}

.apps-copy { max-width: 780px; margin-bottom: 28px; }
.apps-text {
  font-size: 15px;
  line-height: 1.7;
  color: var(--ink-soft);
  margin-bottom: 16px;
}
.apps-text:last-child { margin-bottom: 0; }

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
.detail-card p {
  font-size: 14.5px;
  line-height: 1.7;
  color: var(--ink-soft);
}

.srv-others {
  padding: 26px 32px;
  border-radius: var(--r);
  background: var(--paper2);
  border: 1px solid var(--line-l);
}
.srv-cluster { margin-bottom: 16px; }
.srv-cycle { margin-bottom: 16px; }
.srv-cycle-text {
  font-size: 14.5px;
  color: var(--ink-soft);
  max-width: 640px;
  margin-bottom: 16px;
}
.srv-others-h {
  font-family: var(--font-m);
  font-size: 11.5px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--acc);
  margin-bottom: 14px;
}
.srv-others-row {
  display: flex;
  gap: 12px 28px;
  flex-wrap: wrap;
}
.srv-other {
  font-size: 15px;
  font-weight: 700;
  color: var(--ink);
  transition: color 0.2s;
}
.srv-other:hover { color: var(--acc); }
.srv-other--acc { color: var(--acc); }
.srv-other--acc:hover { color: var(--acc-hot); }

/* ============ адаптив ============ */
@media (max-width: 980px) {
  .hero-in { grid-template-columns: 1fr; gap: 44px; }
  .hero-form { max-width: 460px; }
}
@media (max-width: 900px) {
  .srv-stats { grid-template-columns: 1fr 1fr; gap: 24px; }
  .feat-grid,
  .detail-grid,
  .factor-grid { grid-template-columns: 1fr; }
  .price-row { grid-template-columns: 1fr; gap: 6px; }
}
</style>
