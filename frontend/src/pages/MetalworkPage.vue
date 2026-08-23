<script setup>
import ProcessSection from '../components/ProcessSection.vue'
import CompareSection from '../components/CompareSection.vue'
import CasesSection from '../components/CasesSection.vue'
import GeoSection from '../components/GeoSection.vue'
import FaqSection from '../components/FaqSection.vue'
import FinalCtaSection from '../components/FinalCtaSection.vue'
import ShopGallery from '../components/ShopGallery.vue'
import { metalworkLandings, metalworkLandingPath } from '../data/metallokonstruktsii'
import { homeGallery } from '../data/shopPhotos'

/* ---------- что изготавливаем (только уникальные блоки страницы) ---------- */
const products = [
  {
    title: 'Каркасы зданий',
    hint: 'Колонны, балки, связи, прогоны по чертежу КМ / КМД',
    price: 'от 57 000 ₽/т',
    icon: 'frame',
  },
  {
    title: 'Фермы',
    hint: 'Стропильные и подстропильные, пролёты до 36 м',
    price: 'от 65 000 ₽/т',
    icon: 'truss',
    to: '/metallokonstruktsii/fermy',
  },
  {
    title: 'Балки и колонны',
    hint: 'Сварные двутавры, обработка торцов, отверстия',
    price: 'от 52 000 ₽/т',
    icon: 'beam',
  },
  {
    title: 'Лестницы и площадки',
    hint: 'Марши, обслуживающие площадки, ограждения',
    price: 'от 75 000 ₽/т',
    icon: 'stairs',
    to: '/metallokonstruktsii/lestnitsy',
  },
  {
    title: 'Навесы и козырьки',
    hint: 'Для авто, входных групп, производственных зон',
    price: 'от 57 000 ₽/т',
    icon: 'canopy',
    to: '/metallokonstruktsii/navesy',
  },
  {
    title: 'Ангары и склады',
    hint: 'Быстровозводимые здания, с монтажом по области',
    price: 'от 57 000 ₽/т',
    icon: 'hangar',
    to: '/metallokonstruktsii/sklady-i-angary',
  },
  {
    title: 'Закладные детали',
    hint: 'Пластины, анкерные блоки, кронштейны — серийно',
    price: 'от 45 000 ₽/т',
    icon: 'plate',
    to: '/metallokonstruktsii/zakladnye',
  },
  {
    title: 'Нестандартные конструкции',
    hint: 'Ёмкости, бункеры, рамы, узлы по вашим чертежам',
    price: 'от 95 000 ₽/т',
    icon: 'tank',
  },
]
</script>

<template>
  <main>
    <!-- ============ HERO ============ -->
    <section id="mk-hero" class="sec sec--dark page-hero mk-hero">
      <div class="container">
        <nav class="crumbs" aria-label="Навигация" v-reveal>
          <RouterLink to="/">Главная</RouterLink>
          <span class="crumbs-sep" aria-hidden="true">/</span>
          <span aria-current="page">Металлоконструкции</span>
        </nav>
        <div class="sec-head" v-reveal="60">
          <p class="sec-tag"><span class="idx">Производство</span> Металлоконструкции</p>
          <h1 class="page-title">Металлоконструкции <em>на заказ</em></h1>
          <p class="page-desc">
            Свой цех 3000 м² в Дзержинске: резка, гибка, сварка и покрытие на одной
            площадке. От закладной детали до каркаса здания. Смета за 1 рабочий день,
            отгрузка по всей России.
          </p>
        </div>

        <div class="mk-hero-cta" v-reveal="140">
          <RouterLink to="/kalkulyator" class="btn">Рассчитать стоимость в калькуляторе</RouterLink>
          <a href="#cta" class="btn btn--ghost">Прислать чертёж на расчёт</a>
        </div>

        <nav class="mk-cluster" aria-label="Посадочные металлоконструкций" v-reveal="170">
          <RouterLink
            v-for="s in metalworkLandings"
            :key="s.slug"
            :to="metalworkLandingPath(s.slug)"
            class="mk-chip"
          >
            {{ s.navLabel }}
          </RouterLink>
        </nav>

        <div class="mk-stats" v-reveal="200">
          <div class="mk-stat"><b>3000 м²</b><span>своё производство</span></div>
          <div class="mk-stat"><b>1500+</b><span>выполненных проектов</span></div>
          <div class="mk-stat"><b>с 2013</b><span>года на рынке</span></div>
          <div class="mk-stat"><b>1 день</b><span>на расчёт сметы</span></div>
        </div>
      </div>
    </section>

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

.mk-hero-cta {
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
  margin-bottom: 20px;
}

.mk-cluster {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 48px;
}
.mk-chip {
  padding: 10px 16px;
  border: 1px solid var(--line-d);
  border-radius: 999px;
  font-size: 13.5px;
  font-weight: 600;
  color: var(--w-soft);
  transition: border-color 0.2s, color 0.2s;
}
.mk-chip:hover {
  border-color: var(--acc);
  color: var(--white);
}

.mk-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 18px;
  padding-top: 34px;
  border-top: 1px solid var(--line-d);
}
.mk-stat b {
  display: block;
  font-family: var(--font-d);
  font-size: clamp(20px, 2.4vw, 28px);
  font-weight: 900;
  color: var(--acc-hot);
  margin-bottom: 4px;
}
.mk-stat span {
  font-family: var(--font-m);
  font-size: 11.5px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--w-faint);
}

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
@media (max-width: 900px) {
  .mk-stats { grid-template-columns: 1fr 1fr; gap: 24px; }
}
@media (max-width: 560px) {
  .prod-grid { grid-template-columns: 1fr; }
}
</style>
