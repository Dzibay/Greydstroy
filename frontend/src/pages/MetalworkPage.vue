<script setup>
import ProcessSection from '../components/ProcessSection.vue'
import CompareSection from '../components/CompareSection.vue'
import CasesSection from '../components/CasesSection.vue'
import GeoSection from '../components/GeoSection.vue'
import FaqSection from '../components/FaqSection.vue'
import FinalCtaSection from '../components/FinalCtaSection.vue'
import ShopGallery from '../components/ShopGallery.vue'
import LeadForm from '../components/ui/LeadForm.vue'
import QuickCallBanner from '../components/QuickCallBanner.vue'
import { metalworkLandings, metalworkLandingPath } from '../data/metallokonstruktsii'
import { uslugi } from '../data/uslugi'
import { mainServices } from '../data/services'
import { homeGallery } from '../data/shopPhotos'
import { company } from '../data/company'

const stats = [
  { b: '3000 м²', s: 'своё производство' },
  { b: '1500+', s: 'проектов' },
  { b: 'с 2013', s: 'года на рынке' },
  { b: '1 день', s: 'на расчёт сметы' },
]

/* ---------- что изготавливаем (только уникальные блоки страницы) ---------- */
const products = [
  {
    title: 'Каркасы зданий',
    hint: 'Колонны, балки, связи, прогоны по чертежу КМ / КМД',
    price: 'от 49 000 ₽/т',
    icon: 'frame',
  },
  {
    title: 'Фермы',
    hint: 'Стропильные и подстропильные, пролёты до 36 м',
    price: 'от 55 000 ₽/т',
    icon: 'truss',
    to: '/metallokonstruktsii/fermy',
  },
  {
    title: 'Балки и колонны',
    hint: 'Сварные двутавры, обработка торцов, отверстия',
    price: 'от 45 000 ₽/т',
    icon: 'beam',
  },
  {
    title: 'Лестницы и площадки',
    hint: 'Марши, обслуживающие площадки, ограждения',
    price: 'от 62 000 ₽/т',
    icon: 'stairs',
    to: '/metallokonstruktsii/lestnitsy',
  },
  {
    title: 'Навесы и козырьки',
    hint: 'Для авто, входных групп, производственных зон',
    price: 'от 49 000 ₽/т',
    icon: 'canopy',
    to: '/metallokonstruktsii/navesy',
  },
  {
    title: 'Ангары и склады',
    hint: 'Быстровозводимые здания, с монтажом по области',
    price: 'от 49 000 ₽/т',
    icon: 'hangar',
    to: '/metallokonstruktsii/sklady-i-angary',
  },
  {
    title: 'Закладные детали',
    hint: 'Пластины, анкерные блоки, кронштейны — серийно',
    price: 'от 39 000 ₽/т',
    icon: 'plate',
    to: '/metallokonstruktsii/zakladnye',
  },
  {
    title: 'Нестандартные конструкции',
    hint: 'Ёмкости, бункеры, рамы, узлы по вашим чертежам',
    price: 'от 79 000 ₽/т',
    icon: 'tank',
  },
]
</script>

<template>
  <main>
    <!-- ============ HERO ============ -->
    <section id="mk-hero" class="sec sec--dark page-hero mk-hero mk-hero--split">
      <div class="container">
        <nav class="crumbs" aria-label="Навигация" v-reveal>
          <RouterLink to="/">Главная</RouterLink>
          <span class="crumbs-sep" aria-hidden="true">/</span>
          <span aria-current="page">Металлоконструкции</span>
        </nav>

        <div class="hero-in">
          <div class="hero-left">
            <p class="hero-kicker" v-reveal>
              <span class="dot"></span>
              Звоните прямо сейчас, чтобы получить расчёт цены
            </p>

            <h1 class="hero-title" v-reveal="80">
              Металлоконструкции <em>на заказ</em>
            </h1>

            <p class="hero-sub" v-reveal="160">
              Свой цех в Дзержинске: от закладной до каркаса здания.
              Смета за день, отгрузка по России.
            </p>

            <ul class="hero-trust" v-reveal="240">
              <li v-for="st in stats" :key="st.b + st.s">{{ st.b }} {{ st.s }}</li>
            </ul>

            <div class="hero-cta" v-reveal="320">
              <RouterLink to="/kalkulyator" class="btn" data-track="calc-mk">Калькулятор цены</RouterLink>
              <p class="btn-note">Ориентир цены и срока — сразу.<br />Точный расчёт по чертежу.</p>
            </div>

            <nav class="mk-cluster" aria-label="Посадочные металлоконструкций" v-reveal="360">
              <RouterLink
                v-for="s in metalworkLandings"
                :key="s.slug"
                :to="metalworkLandingPath(s.slug)"
                class="mk-chip"
              >
                {{ s.navLabel }}
              </RouterLink>
            </nav>
          </div>

          <div class="hero-form" v-reveal="300">
            <div class="hero-form-filter" role="note">
              <p class="hff-lead">Заказы от 50&nbsp;м²</p>
              <p class="hff-warn">
                Если меньший объём —
                закройте страницу, мы его не возьмём. Работаем с коммерческими объектами.
              </p>
            </div>
            <LeadForm button-text="Рассчитать стоимость" />
          </div>

          <div class="hero-qcb" v-reveal="380">
            <QuickCallBanner embedded />
          </div>
        </div>
      </div>
    </section>

    <div class="qcb-standalone">
      <QuickCallBanner />
    </div>

    <!-- ============ ЧТО ИЗГОТАВЛИВАЕМ ============ -->
    <section id="products" class="sec sec--deep">
      <div class="container">
        <div class="sec-head" v-reveal>
          <p class="sec-tag"><span class="idx">Каталог</span> Что изготавливаем</p>
          <h2 class="sec-title">От закладной до каркаса <em>целого здания</em></h2>
          <p class="sec-sub">
            Цены указаны за работы без металла — ориентир, который уточняется по чертежу.
            С металлом и покрытием посчитает калькулятор.
          </p>
        </div>

        <div class="feat-cta" v-reveal="40">
          <a
            :href="company.phoneHref"
            class="btn"
            data-track="tel-mk-engineer"
          >Позвонить инженеру</a>
          <p class="feat-cta-note">Сориентируем по срокам и цене прямо во время разговора</p>
        </div>

        <div class="prod-grid">
          <component
            :is="p.to ? 'RouterLink' : 'article'"
            v-for="(p, i) in products"
            :key="p.title"
            class="card prod-card"
            :to="p.to"
            v-reveal="i * 60"
          >
            <span class="prod-icon" aria-hidden="true">
              <svg v-if="p.icon === 'frame'" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M4 26V12l12-7 12 7v14" /><path d="M4 26h24" /><path d="M10 26V15m6 11V12m6 14V15" />
              </svg>
              <svg v-else-if="p.icon === 'truss'" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M3 22h26M5 22l5-9h12l5 9" /><path d="M10 13l4 9m8-9-4 9m-4-9v9" />
              </svg>
              <svg v-else-if="p.icon === 'beam'" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M7 6h18M7 26h18M12 6v20M20 6v20" />
              </svg>
              <svg v-else-if="p.icon === 'stairs'" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M5 27h6v-6h6v-6h6V9h6" />
              </svg>
              <svg v-else-if="p.icon === 'canopy'" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M4 12c4-5 20-5 24 0" /><path d="M6 12v14m20-14v14" /><path d="M6 20h20" />
              </svg>
              <svg v-else-if="p.icon === 'hangar'" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M3 26V14C3 8 9 5 16 5s13 3 13 9v12" /><path d="M3 26h26" /><path d="M12 26v-8h8v8" />
              </svg>
              <svg v-else-if="p.icon === 'plate'" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <rect x="5" y="9" width="22" height="14" rx="1.5" /><circle cx="10" cy="14" r="1.6" /><circle cx="22" cy="14" r="1.6" /><circle cx="10" cy="19" r="1.6" /><circle cx="22" cy="19" r="1.6" />
              </svg>
              <svg v-else viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M8 10a8 4 0 0 1 16 0v12a8 4 0 0 1-16 0z" /><ellipse cx="16" cy="10" rx="8" ry="4" />
              </svg>
            </span>
            <h3>{{ p.title }}</h3>
            <p>{{ p.hint }}</p>
            <p class="prod-price">{{ p.price }} <small>работы</small></p>
          </component>
        </div>

        <div class="mk-works" v-reveal="120">
          <p class="mk-works-h">Изготовление — не единственная услуга:</p>
          <div class="mk-works-row">
            <RouterLink
              v-for="s in mainServices"
              :key="s.id"
              :to="s.to"
              class="mk-work"
              :class="{ 'mk-work--acc': s.featured }"
            >
              {{ s.navLabel }} →
            </RouterLink>
          </div>
        </div>

        <div class="mk-works mk-tech" v-reveal="160">
          <p class="mk-works-h">Технологии производства:</p>
          <div class="mk-works-row">
            <RouterLink
              v-for="u in uslugi"
              :key="u.slug"
              :to="`/uslugi/${u.slug}`"
              class="mk-work"
            >
              {{ u.label }} →
            </RouterLink>
          </div>
        </div>
      </div>
    </section>

    <ShopGallery
      :items="homeGallery"
      tag="Площадка"
      kicker="Цех и объекты"
      title="Как выглядит"
      title-em="работа, не рендер"
      lead="Каркасы, фермы, раскрой и навесы — кадры с наших объектов и из цеха в Дзержинске."
    />

    <ProcessSection />
    <CompareSection />
    <CasesSection />
    <GeoSection />
    <FaqSection />
    <FinalCtaSection />
  </main>
</template>

<style scoped>
/* ============ hero ============ */
.mk-hero { padding-bottom: 64px; }
.mk-hero--split { padding-bottom: 90px; }

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

.hero-in {
  display: grid;
  grid-template-columns: 1.35fr 0.75fr;
  gap: 64px;
  align-items: center;
  min-width: 0;
  width: 100%;
}
.hero-left,
.hero-form {
  min-width: 0;
  max-width: 100%;
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
  animation: mk-pulse 2s infinite;
}
@keyframes mk-pulse {
  50% { opacity: 0.4; }
}

.hero-title {
  font-family: var(--font-d);
  font-size: clamp(22px, 7vw, 38px);
  font-weight: 900;
  line-height: 1.12;
  text-transform: uppercase;
  letter-spacing: -0.015em;
  margin-bottom: 28px;
  overflow-wrap: anywhere;
  word-break: break-word;
  max-width: 100%;
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
  margin-bottom: 28px;
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
  .mk-hero--split { padding-bottom: 110px; }
  .qcb-standalone { display: none; }
}

.mk-cluster {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  max-width: 100%;
}
.mk-chip {
  padding: 10px 16px;
  border: 1px solid var(--line-d);
  border-radius: 999px;
  font-size: 13.5px;
  font-weight: 600;
  color: var(--w-soft);
  transition: border-color 0.2s, color 0.2s;
  max-width: 100%;
}
.mk-chip:hover {
  border-color: var(--acc);
  color: var(--white);
}

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

.mk-works {
  margin-top: 28px;
  padding: 26px 32px;
  border-radius: var(--r);
  border: 1px solid var(--line-d);
  background: var(--card-d);
}
.mk-works-h {
  font-family: var(--font-m);
  font-size: 11.5px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--acc);
  margin-bottom: 14px;
}
.mk-works-row {
  display: flex;
  gap: 12px 28px;
  flex-wrap: wrap;
}
.mk-work {
  font-size: 15px;
  font-weight: 700;
  color: var(--white);
  transition: color 0.2s;
}
.mk-work:hover { color: var(--acc-hot); }
.mk-work--acc { color: var(--acc); }
.mk-work--acc:hover { color: var(--acc-hot); }
.mk-tech { margin-top: 16px; }

/* ============ каталог ============ */
.prod-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}
.prod-card { display: flex; flex-direction: column; padding: 26px 24px; color: inherit; text-decoration: none; }
.prod-icon {
  width: 48px;
  height: 48px;
  display: grid;
  place-items: center;
  border-radius: 12px;
  background: var(--acc-dim);
  color: var(--acc-hot);
  margin-bottom: 18px;
  transition: background 0.3s, color 0.3s;
}
.prod-icon svg { width: 25px; height: 25px; }
.prod-card:hover .prod-icon { background: var(--acc); color: #fff; }

.prod-card h3 {
  font-family: var(--font-d);
  font-size: 14px;
  font-weight: 700;
  text-transform: uppercase;
  line-height: 1.3;
  margin-bottom: 10px;
}
.prod-card > p { font-size: 13px; color: var(--w-soft); flex: 1; }
.prod-price {
  margin-top: 16px;
  padding-top: 12px;
  border-top: 1px dashed var(--line-d);
  font-family: var(--font-m);
  font-size: 13px;
  color: var(--acc-hot);
}
.prod-price small {
  font-size: 10.5px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--w-faint);
}

/* ============ адаптив ============ */
@media (max-width: 1060px) {
  .prod-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 980px) {
  .hero-in { grid-template-columns: 1fr; gap: 44px; }
  .hero-form { max-width: 100%; }
  .hero-title { font-size: clamp(20px, 8.2vw, 30px); }
}
@media (max-width: 560px) {
  .prod-grid { grid-template-columns: 1fr; }
}
</style>
