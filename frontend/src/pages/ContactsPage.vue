<script setup>
import { company } from '../data/company'

const cards = [
  {
    label: 'Телефон',
    value: company.phone,
    href: company.phoneHref,
    note: company.schedule,
    icon: 'phone',
  },
  {
    label: 'Электронная почта',
    value: company.email,
    href: `mailto:${company.email}`,
    note: 'Чертежи: PDF, DWG, DXF, STEP',
    icon: 'mail',
  },
  {
    label: 'Производство',
    value: 'г. Дзержинск, дорога Заревская объездная, д. 9В',
    note: 'Нижегородская область, 606000 · самовывоз по договорённости',
    icon: 'pin',
  },
]
</script>

<template>
  <main>
    <section class="sec sec--dark page-hero">
      <div class="container">
        <RouterLink to="/" class="page-back" v-reveal>← На главную</RouterLink>
        <div class="sec-head" v-reveal="60">
          <p class="sec-tag"><span class="idx">Связаться</span> Контакты</p>
          <h1 class="page-title">Контакты <em>ООО «Грэйдстрой»</em></h1>
          <p class="page-desc">
            Пришлите чертёж или просто опишите задачу — технолог посчитает
            и ответит в течение рабочего дня.
          </p>
        </div>

        <div class="con-grid">
          <component
            :is="c.href ? 'a' : 'div'"
            v-for="(c, i) in cards"
            :key="c.label"
            :href="c.href"
            class="card con-card"
            v-reveal="i * 90"
          >
            <span class="con-icon" aria-hidden="true">
              <svg v-if="c.icon === 'phone'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z" />
              </svg>
              <svg v-else-if="c.icon === 'mail'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <rect x="2" y="4" width="20" height="16" rx="2" /><path d="m22 7-10 6L2 7" />
              </svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z" /><circle cx="12" cy="10" r="3" />
              </svg>
            </span>
            <p class="con-label">{{ c.label }}</p>
            <p class="con-value">{{ c.value }}</p>
            <p class="con-note">{{ c.note }}</p>
          </component>
        </div>
      </div>
    </section>

    <section class="sec sec--light con-map-sec">
      <div class="container">
        <div class="con-map card" v-reveal>
          <iframe
            src="https://yandex.ru/map-widget/v1/?text=Дзержинск%2C%20Заревская%20объездная%2C%209В&z=15"
            title="Карта: производство ООО «Грэйдстрой» в Дзержинске"
            loading="lazy"
            allowfullscreen
          ></iframe>
        </div>

        <div class="con-cta" v-reveal="80">
          <div>
            <p class="con-cta-title">Нужен расчёт?</p>
            <p class="con-cta-text">
              Оставьте заявку — ответим с цифрами, а не с «нужно уточнить».
              Реквизиты для договора — на <RouterLink to="/rekvizity">отдельной странице</RouterLink>.
            </p>
          </div>
          <RouterLink to="/kalkulyator" class="btn">Рассчитать заказ</RouterLink>
        </div>
      </div>
    </section>
  </main>
</template>

<style scoped>
.con-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
}

.con-card { display: flex; flex-direction: column; }

.con-icon {
  width: 52px;
  height: 52px;
  display: grid;
  place-items: center;
  border-radius: 13px;
  background: var(--acc-dim);
  color: var(--acc-hot);
  margin-bottom: 20px;
  transition: background 0.3s, color 0.3s;
}
.con-icon svg { width: 26px; height: 26px; }
.con-card:hover .con-icon { background: var(--acc); color: #fff; }

.con-label {
  font-family: var(--font-m);
  font-size: 11px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--w-faint);
  margin-bottom: 10px;
}
.con-value {
  font-size: 17px;
  font-weight: 700;
  line-height: 1.45;
  color: var(--white);
  flex: 1;
}
a.con-card:hover .con-value { color: var(--acc-hot); }
.con-note {
  margin-top: 14px;
  padding-top: 12px;
  border-top: 1px dashed var(--line-d);
  font-size: 12.5px;
  color: var(--w-faint);
}

.con-map-sec { padding-top: 72px; }
.con-map { padding: 12px; overflow: hidden; }
.con-map:hover { transform: none; }
.con-map iframe {
  display: block;
  width: 100%;
  height: 420px;
  border: none;
  border-radius: calc(var(--r) - 6px);
}

.con-cta {
  margin-top: 28px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  flex-wrap: wrap;
  padding: 28px 32px;
  border-radius: var(--r);
  background: var(--paper2);
  border: 1px solid var(--line-l);
}
.con-cta-title {
  font-family: var(--font-d);
  font-size: 17px;
  font-weight: 700;
  text-transform: uppercase;
  margin-bottom: 6px;
}
.con-cta-text { font-size: 14.5px; color: var(--ink-soft); max-width: 560px; }
.con-cta-text a { color: var(--acc); text-decoration: underline; text-underline-offset: 2px; }
.con-cta-text a:hover { color: var(--acc-hot); }

@media (max-width: 900px) {
  .con-grid { grid-template-columns: 1fr; }
  .con-map iframe { height: 320px; }
}
</style>
