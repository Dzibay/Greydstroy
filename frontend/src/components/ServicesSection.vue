<script setup>
const services = [
  {
    title: 'Лазерная резка',
    text: 'Сложный контур сегодня, деталь для сборки — без доработки напильником',
    spec: 'до 20 мм · чистая кромка',
    icon: 'laser',
  },
  {
    title: 'Плазменная резка',
    text: 'Толстый металл, большие объёмы, кромка без «доп. зачистки», о которой вы не договаривались',
    spec: 'до 50 мм · чёрный металл',
    icon: 'plasma',
  },
  {
    title: 'Гибка на листогибе',
    text: 'Деталь №50 гнётся под тем же углом, что и деталь №1',
    spec: 'ЧПУ · до 6 мм · до 3000 мм',
    icon: 'bend',
  },
  {
    title: 'Сварка и металлоконструкции',
    text: 'От одного шва до объекта под ключ, в Нижегородской области — с монтажом',
    spec: 'MIG/MAG · TIG · РДС',
    icon: 'weld',
  },
]
</script>

<template>
  <section id="services" class="sec sec--dark">
    <div class="container">
      <div class="sec-head" v-reveal>
        <p class="sec-tag"><span class="idx">/ 03</span> Что мы делаем</p>
        <h2 class="sec-title">Один подрядчик <em>вместо трёх</em></h2>
        <p class="sec-sub">
          Пока деталь пересылают между цехом резки, гибочным участком и сварочным постом —
          время теряется на каждой пересылке. У нас всё происходит на одной площадке:
          один договор, один контакт, одна ответственность за результат.
        </p>
      </div>

      <div class="srv-grid">
        <article v-for="(s, i) in services" :key="s.title" class="card srv-card" v-reveal="i * 90">
          <div class="srv-top">
            <span class="srv-icon" aria-hidden="true">
              <svg v-if="s.icon === 'laser'" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 3h8l-2 6h-4l-2-6z" /><path d="M14 9v4h4V9" /><path d="M16 13v6" />
                <path d="m16 19-6 8m6-8 6 8m-6-8v9" stroke-dasharray="2.5 3" />
              </svg>
              <svg v-else-if="s.icon === 'plasma'" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M11 3h10l-3 7h-4l-3-7z" /><path d="M16 10v5" />
                <path d="M16 15c-2 3-5 4-5 8m5-8c2 3 5 4 5 8m-5-8v10" stroke-dasharray="3 2.5" />
                <path d="M6 29h20" />
              </svg>
              <svg v-else-if="s.icon === 'bend'" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M4 24 16 12l12 12" /><path d="M16 12V4" /><path d="M9 4h14" />
                <circle cx="16" cy="24" r="2.6" />
              </svg>
              <svg v-else viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M5 20 14 11l7 7-9 9z" /><path d="m14 11 5-5 3-1 4 4-1 3-4 4" />
                <path d="m22 18 5 5" stroke-dasharray="2.5 3" /><circle cx="9" cy="24" r="1" fill="currentColor" />
              </svg>
            </span>
            <span class="srv-num">{{ String(i + 1).padStart(2, '0') }}</span>
          </div>
          <h3>{{ s.title }}</h3>
          <p>{{ s.text }}</p>
          <p class="srv-spec">{{ s.spec }}</p>
        </article>
      </div>
    </div>
  </section>
</template>

<style scoped>
.srv-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 18px;
}

.srv-card {
  display: flex;
  flex-direction: column;
  min-height: 300px;
  position: relative;
  overflow: hidden;
}
.srv-card::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: 0;
  width: 100%;
  height: 3px;
  background: var(--acc);
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.4s var(--ease);
}
.srv-card:hover::after { transform: scaleX(1); }

.srv-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 26px;
}
.srv-icon {
  width: 58px;
  height: 58px;
  display: grid;
  place-items: center;
  border-radius: 14px;
  background: var(--acc-dim);
  color: var(--acc-hot);
  transition: background 0.3s, color 0.3s;
}
.srv-icon svg { width: 30px; height: 30px; }
.srv-card:hover .srv-icon { background: var(--acc); color: #fff; }

.srv-num {
  font-family: var(--font-d);
  font-size: 26px;
  font-weight: 900;
  color: transparent;
  -webkit-text-stroke: 1.2px rgba(255, 255, 255, 0.16);
}
.srv-card:hover .srv-num { -webkit-text-stroke-color: var(--acc); }

.srv-card h3 {
  font-family: var(--font-d);
  font-size: 16.5px;
  font-weight: 700;
  text-transform: uppercase;
  line-height: 1.25;
  margin-bottom: 12px;
}
.srv-card p {
  font-size: 14px;
  color: var(--w-soft);
  flex: 1;
}
.srv-spec {
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

@media (max-width: 1060px) {
  .srv-grid { grid-template-columns: 1fr 1fr; }
}
@media (max-width: 560px) {
  .srv-grid { grid-template-columns: 1fr; }
  .srv-card { min-height: 0; }
}
</style>
