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
import FaqSection from '../components/FaqSection.vue'
import FinalCtaSection from '../components/FinalCtaSection.vue'
import ShopGallery from '../components/ShopGallery.vue'

const SITE = 'https://greydstroy.ru'

const props = defineProps({
  slug: { type: String, default: '' },
  childSlug: { type: String, default: '' },
  hub: { type: String, default: '' },
})

const isMkChild = computed(() => props.hub === 'metalwork')
const parent = computed(() => (props.slug ? getUslugaBySlug(props.slug) : null))
const child = computed(() => {
  if (isMkChild.value) return getMetalworkLanding(props.childSlug)
  if (props.childSlug) return getLaserLanding(props.childSlug)
  return null
})
const usluga = computed(() => child.value || parent.value)
const isLaserHub = computed(() => props.slug === 'lazernaya-rezka' && !props.childSlug)
const isLaserChild = computed(() => !!props.childSlug && !isMkChild.value)

const crumbs = computed(() => {
  const items = [{ name: 'Главная', to: '/' }]
  if (isMkChild.value) {
    items.push({ name: MK_PARENT_LABEL, to: MK_PARENT_PATH })
    items.push({ name: child.value.navLabel, to: '' })
    return items
  }
  items.push({ name: 'Услуги', to: '/uslugi' })
  if (isLaserChild.value) {
    items.push({ name: LASER_PARENT_LABEL, to: LASER_PARENT_PATH })
    items.push({ name: child.value.navLabel, to: '' })
  } else if (parent.value) {
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
  if (isMkChild.value) {
    return metalworkLandings.filter((p) => p.slug !== props.childSlug)
  }
  if (!isLaserChild.value && !isLaserHub.value) return []
  return laserLandings.filter((p) => p.slug !== props.childSlug)
})

const clusterParentTo = computed(() => (isMkChild.value ? MK_PARENT_PATH : LASER_PARENT_PATH))
const clusterParentLabel = computed(() =>
  isMkChild.value ? 'Все металлоконструкции →' : 'Вся лазерная резка →'
)
const clusterHeading = computed(() => {
  if (isMkChild.value) return 'Другие задачи по металлоконструкциям:'
  return isLaserHub.value ? 'По задачам лазерной резки:' : 'Другие задачи лазерной резки:'
})
const siblingPath = (slug) =>
  isMkChild.value ? metalworkLandingPath(slug) : laserLandingPath(slug)

const pageKey = computed(() => {
  if (isMkChild.value) return `mk-${props.childSlug}`
  if (props.childSlug) return `laser-${props.childSlug}`
  return props.slug
})

const tagIdx = computed(() => {
  if (isMkChild.value) return 'Металлоконструкции'
  if (isLaserChild.value) return 'Лазерная резка'
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
    <!-- ============ HERO ============ -->
    <section id="usluga-hero" class="sec sec--dark page-hero srv-hero">
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
          <RouterLink to="/kalkulyator" class="btn">Рассчитать стоимость</RouterLink>
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
              v-if="isLaserChild || isMkChild"
              :to="clusterParentTo"
              class="srv-other srv-other--acc"
            >
              {{ clusterParentLabel }}
            </RouterLink>
            <RouterLink
              v-for="s in siblings"
              :key="s.slug"
              :to="siblingPath(s.slug)"
              class="srv-other"
            >
              {{ s.navLabel }} →
            </RouterLink>
          </div>
        </div>

        <div class="srv-others" v-reveal="160">
          <p class="srv-others-h">{{ isMkChild ? 'Участки того же цеха:' : 'Другие участки производства:' }}</p>
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
              v-if="!isMkChild"
              to="/metallokonstruktsii"
              class="srv-other srv-other--acc"
            >
              Металлоконструкции под ключ →
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
@media (max-width: 900px) {
  .srv-stats { grid-template-columns: 1fr 1fr; gap: 24px; }
  .feat-grid,
  .detail-grid,
  .factor-grid { grid-template-columns: 1fr; }
  .price-row { grid-template-columns: 1fr; gap: 6px; }
}
</style>
