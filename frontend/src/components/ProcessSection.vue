<script setup>
const steps = [
  {
    title: 'Заявка',
    text: 'Звонок, смс или форма на сайте. Просто скажите, что у вас есть — готовый чертёж или задача, которую пока нужно решить.',
  },
  {
    title: 'Если чертежа нет',
    text: 'Разработаем КМ с нуля или сделаем КМД на основе вашего КМ — без поиска отдельного проектировщика.',
  },
  {
    title: 'Расчёт',
    text: 'Присылаем стоимость, срок и допуски по вашему заказу — обычно в течение рабочего дня, а не «на следующей неделе».',
  },
  {
    title: 'Согласование и договор',
    text: 'Фиксируем объём, срок и цену. После этого — аванс на материал и запуск в производство.',
  },
  {
    title: 'Производство',
    text: 'Мы не начинаем резать металл, пока не пришёл аванс. Это не «мы вам не доверяем» — это гарантия, что ни объём, ни цена не «поплывут» на середине заказа. Работает в обе стороны.',
  },
  {
    title: 'Готовность',
    text: 'Уведомляем о завершении. При больших объёмах можем отгружать частями по мере готовности — под ваш график на объекте.',
  },
  {
    title: 'Отгрузка',
    text: 'Самовывоз, доставка своим транспортом по Нижегородской области, СДЭК или Деловые линии — по всей России.',
  },
  {
    title: 'Гарантия',
    text: 'Если в деталях наш брак — переделаем бесплатно. Без споров и лишней переписки.',
  },
]
</script>

<template>
  <section id="process" class="sec sec--light sec--light2">
    <div class="container">
      <div class="sec-head" v-reveal>
        <p class="sec-tag"><span class="idx">/ 04</span> Как мы работаем</p>
        <h2 class="sec-title">Как проходит заказ — <em>от заявки до отгрузки</em></h2>
        <p class="sec-sub">
          Главный страх в B2B — «возьмут аванс и пропадут». Поэтому процесс у нас
          прозрачный: вы всегда знаете, на каком шаге ваш заказ и что происходит дальше.
        </p>
      </div>

      <div class="proc-grid">
        <article v-for="(step, i) in steps" :key="step.title" class="proc-step" v-reveal="(i % 4) * 90">
          <div class="ps-head">
            <span class="ps-num">{{ String(i + 1).padStart(2, '0') }}</span>
            <span class="ps-line" aria-hidden="true"></span>
          </div>
          <h3>{{ step.title }}</h3>
          <p>{{ step.text }}</p>
        </article>
      </div>
    </div>
  </section>
</template>

<style scoped>
.proc-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 44px 28px;
}

.proc-step { position: relative; }

.ps-head {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 18px;
}
.ps-num {
  font-family: var(--font-d);
  font-size: 38px;
  font-weight: 900;
  line-height: 1;
  color: transparent;
  -webkit-text-stroke: 1.6px var(--acc);
  flex-shrink: 0;
  transition: color 0.3s;
}
.proc-step:hover .ps-num { color: var(--acc); }
.ps-line {
  flex: 1;
  height: 1.5px;
  background: repeating-linear-gradient(90deg, var(--line-l) 0 8px, transparent 8px 15px);
}

.proc-step h3 {
  font-family: var(--font-d);
  font-size: 15px;
  font-weight: 700;
  text-transform: uppercase;
  margin-bottom: 10px;
}
.proc-step p {
  font-size: 14px;
  line-height: 1.6;
  color: var(--ink-soft);
}

@media (max-width: 1000px) {
  .proc-grid { grid-template-columns: 1fr 1fr; }
}
@media (max-width: 560px) {
  .proc-grid { grid-template-columns: 1fr; gap: 32px; }
}
</style>
