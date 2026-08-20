<script setup>
const options = [
  {
    title: 'Самовывоз из Дзержинска',
    text: 'Заберёте готовый заказ с производства: г. Дзержинск, дорога Заревская объездная, д. 9В. Поможем с погрузкой.',
    spec: 'Бесплатно · в день готовности',
    icon: 'pickup',
  },
  {
    title: 'Наш транспорт по Нижегородской области',
    text: 'Доставим собственным транспортом до объекта или склада. Для металлоконструкций по договорённости — монтаж под ключ.',
    spec: 'Дзержинск · Нижний Новгород · область',
    icon: 'truck',
  },
  {
    title: 'Транспортные компании по всей России',
    text: 'Отгружаем через СДЭК и Деловые линии — терминал в двух шагах от производства, поэтому отправка не добавляет дней к сроку.',
    spec: 'СДЭК · Деловые линии',
    icon: 'box',
  },
  {
    title: 'Крупные и ответственные отправки',
    text: 'Негабарит и крупные партии — отдельным транспортом. Страхование груза обсуждается индивидуально при заказе.',
    spec: 'Негабарит · страхование груза',
    icon: 'shield',
  },
]

const steps = [
  { title: 'Согласуем способ на этапе расчёта', text: 'Стоимость и срок доставки фиксируем в счёте вместе со стоимостью работ — без сюрпризов при отгрузке.' },
  { title: 'Упакуем под перевозку', text: 'Детали пакуем так, чтобы кромки и покрытие доехали целыми: обрешётка или паллет — по характеру груза.' },
  { title: 'Передадим трек и документы', text: 'После отгрузки пришлём накладную и номер для отслеживания, оригиналы документов — с грузом или почтой.' },
]
</script>

<template>
  <main>
    <section id="delivery" class="sec sec--dark page-hero">
      <div class="container">
        <RouterLink to="/" class="page-back" v-reveal>← На главную</RouterLink>
        <div class="sec-head" v-reveal="60">
          <p class="sec-tag"><span class="idx">Логистика</span> Доставка</p>
          <h1 class="page-title">Доставка металлоконструкций <em>по всей России</em></h1>
          <p class="page-desc">
            От Нижнего Новгорода до любой точки России — вопрос не «довезёте ли»,
            а «как быстро». Способ и стоимость доставки фиксируем ещё на этапе расчёта заказа.
          </p>
        </div>

        <div class="del-grid">
          <article v-for="(o, i) in options" :key="o.title" class="card del-card" v-reveal="i * 90">
            <span class="del-icon" aria-hidden="true">
              <svg v-if="o.icon === 'pickup'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M3 21V8l9-5 9 5v13" /><path d="M3 21h18" /><path d="M9 21v-8h6v8" />
              </svg>
              <svg v-else-if="o.icon === 'truck'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M1 5h14v12H1z" /><path d="M15 9h4l4 4v4h-8" /><circle cx="6" cy="19" r="2" /><circle cx="18" cy="19" r="2" />
              </svg>
              <svg v-else-if="o.icon === 'box'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="m21 8-9-5-9 5v8l9 5 9-5z" /><path d="m3 8 9 5 9-5" /><path d="M12 13v9" />
              </svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 22s8-3.5 8-10V5l-8-3-8 3v7c0 6.5 8 10 8 10z" /><path d="m9 12 2 2 4-4" />
              </svg>
            </span>
            <h2>{{ o.title }}</h2>
            <p>{{ o.text }}</p>
            <p class="del-spec">{{ o.spec }}</p>
          </article>
        </div>
      </div>
    </section>

    <section id="delivery-how" class="sec sec--light">
      <div class="container">
        <div class="sec-head" v-reveal>
          <p class="sec-tag"><span class="idx">Порядок</span> Как это устроено</p>
          <h2 class="sec-title">Доставка — часть заказа, <em>а не отдельная забота</em></h2>
        </div>

        <ol class="del-steps">
          <li v-for="(s, i) in steps" :key="s.title" class="card del-step" v-reveal="i * 100">
            <span class="del-step-num">{{ String(i + 1).padStart(2, '0') }}</span>
            <h3>{{ s.title }}</h3>
            <p>{{ s.text }}</p>
          </li>
        </ol>

        <div class="del-cta" v-reveal="120">
          <p>Скажите, куда везти — посчитаем доставку вместе со стоимостью работ.</p>
          <RouterLink to="/kalkulyator" class="btn">Рассчитать заказ</RouterLink>
        </div>
      </div>
    </section>
  </main>
</template>

<style scoped>
.del-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 18px;
}

.del-card { display: flex; flex-direction: column; }

.del-icon {
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
.del-icon svg { width: 26px; height: 26px; }
.del-card:hover .del-icon { background: var(--acc); color: #fff; }

.del-card h2 {
  font-family: var(--font-d);
  font-size: 16px;
  font-weight: 700;
  text-transform: uppercase;
  line-height: 1.3;
  margin-bottom: 12px;
}
.del-card > p {
  font-size: 14.5px;
  color: var(--w-soft);
  flex: 1;
}
.del-spec {
  margin-top: 18px;
  padding-top: 14px;
  border-top: 1px dashed var(--line-d);
  font-family: var(--font-m);
  font-size: 11.5px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--acc-hot) !important;
  flex: 0 !important;
}

.del-steps {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
}

.del-step-num {
  display: block;
  font-family: var(--font-d);
  font-size: 26px;
  font-weight: 900;
  color: transparent;
  -webkit-text-stroke: 1.2px rgba(18, 22, 27, 0.25);
  margin-bottom: 16px;
}
.del-step:hover .del-step-num { -webkit-text-stroke-color: var(--acc); }

.del-step h3 {
  font-family: var(--font-d);
  font-size: 14.5px;
  font-weight: 700;
  text-transform: uppercase;
  line-height: 1.3;
  margin-bottom: 10px;
}
.del-step p { font-size: 14px; color: var(--ink-soft); }

.del-cta {
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
.del-cta p { font-size: 16px; font-weight: 600; color: var(--ink); max-width: 560px; }

@media (max-width: 900px) {
  .del-grid { grid-template-columns: 1fr; }
  .del-steps { grid-template-columns: 1fr; }
}
</style>
