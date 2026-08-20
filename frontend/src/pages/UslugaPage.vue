<script setup>
import { computed, watchEffect, onUnmounted } from 'vue'
import { uslugi, getUslugaBySlug } from '../data/uslugi'
import FaqSection from '../components/FaqSection.vue'
import FinalCtaSection from '../components/FinalCtaSection.vue'

const props = defineProps({
  slug: { type: String, required: true },
})

const usluga = computed(() => getUslugaBySlug(props.slug))
const others = computed(() => uslugi.filter((u) => u.slug !== props.slug))

/* JSON-LD FAQPage: обновляется при переходе между страницами услуг */
let ldScript = null
watchEffect(() => {
  ldScript?.remove()
  if (!usluga.value) return
  ldScript = document.createElement('script')
  ldScript.type = 'application/ld+json'
  ldScript.textContent = JSON.stringify({
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: usluga.value.faq.map((f) => ({
      '@type': 'Question',
      name: f.q,
      acceptedAnswer: { '@type': 'Answer', text: f.a },
    })),
  })
  document.head.appendChild(ldScript)
})
onUnmounted(() => ldScript?.remove())
</script>

<template>
  <main v-if="usluga" :key="usluga.slug">
    <!-- ============ HERO ============ -->
    <section id="usluga-hero" class="sec sec--dark page-hero srv-hero">
      <div class="container">
        <RouterLink to="/uslugi" class="page-back" v-reveal>← Все услуги</RouterLink>
        <div class="sec-head" v-reveal="60">
          <p class="sec-tag"><span class="idx">Услуги</span> {{ usluga.label }}</p>
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

    <!-- ============ ПРИМЕНЕНИЕ + ДРУГИЕ УСЛУГИ ============ -->
    <section id="apps" class="sec sec--light">
      <div class="container">
        <div class="sec-head" v-reveal>
          <p class="sec-tag"><span class="idx">Применение</span> {{ usluga.appsTitle }}</p>
          <h2 class="sec-title">Под задачу, <em>а не «по прайсу»</em></h2>
        </div>

        <div class="apps-row" v-reveal="80">
          <span v-for="a in usluga.apps" :key="a" class="apps-chip">{{ a }}</span>
        </div>

        <p class="apps-text" v-reveal="120">{{ usluga.seoText }}</p>

        <div class="srv-others" v-reveal="160">
          <p class="srv-others-h">Другие участки производства:</p>
          <div class="srv-others-row">
            <RouterLink
              v-for="o in others"
              :key="o.slug"
              :to="`/uslugi/${o.slug}`"
              class="srv-other"
            >
              {{ o.label }} →
            </RouterLink>
            <RouterLink to="/metallokonstruktsii" class="srv-other srv-other--acc">
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
      :title-em="'— ' + usluga.label.toLowerCase()"
    />
    <FinalCtaSection />
  </main>
</template>

<style scoped>
/* ============ hero ============ */
.srv-hero { padding-bottom: 64px; }

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

.apps-text {
  max-width: 780px;
  font-size: 15px;
  line-height: 1.7;
  color: var(--ink-soft);
  margin-bottom: 40px;
}

.srv-others {
  padding: 26px 32px;
  border-radius: var(--r);
  background: var(--paper2);
  border: 1px solid var(--line-l);
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
@media (max-width: 900px) {
  .srv-stats { grid-template-columns: 1fr 1fr; gap: 24px; }
  .feat-grid { grid-template-columns: 1fr; }
}
</style>
