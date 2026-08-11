<script setup>
const rows = [
  {
    label: 'Точность',
    others: 'высокая, но под их стандарты — не под ваш проект без пересогласования',
    good: 'под допуск вашего проекта, партия проверяется',
  },
  {
    label: 'Оборудование',
    others: 'современный парк, но очередь на производство — 2–4 недели',
    good: 'лазер, плазма, листогиб и сварка на одной площадке',
  },
  {
    label: 'Документы',
    others: 'полный пакет, но согласование и выдача — через юротдел, не за день',
    good: 'паспорт (сертификат качества) на каждое изделие',
  },
  {
    label: 'Договорённости',
    others: 'жёсткий договор, штрафы за мелкие партии и изменения ТЗ',
    good: 'договор, аванс идёт в производство после согласования цены и сроков',
  },
  {
    label: 'Если брак',
    others: 'рассмотрение по регламенту, пересмотр — 14+ дней',
    good: 'переделываем за свой счёт — это в договоре',
  },
  {
    label: 'Объёмы',
    others: 'минимальная партия от N штук, единичные заказы не берут',
    good: 'от единичной детали до серийной партии, с частичной отгрузкой',
  },
]
</script>

<template>
  <section class="sec sec--dark sec--deep">
    <div class="container">
      <div class="sec-head" v-reveal>
        <p class="sec-tag"><span class="idx">/ 05</span> Почему мы</p>
        <h2 class="sec-title">Производство — это не <em>«гараж с генератором»</em></h2>
        <p class="sec-sub">
          Вы уже сталкивались с исполнителями, у которых «есть станок».
          Разница не в станке. Разница в том, что происходит, когда что-то пошло не так.
        </p>
      </div>

      <div class="cmp" v-reveal>
        <div class="cmp-row cmp-head">
          <div class="cmp-cell cmp-label">Критерий</div>
          <div class="cmp-cell cmp-oth-h">Другие производители</div>
          <div class="cmp-cell cmp-good-h">Грэйдстрой</div>
        </div>
        <div v-for="(row, i) in rows" :key="row.label" class="cmp-row" v-reveal="i * 60">
          <div class="cmp-cell cmp-label">{{ row.label }}</div>
          <div class="cmp-cell cmp-oth">
            <span class="mark mark-e" aria-hidden="true">~</span>
            {{ row.others }}
          </div>
          <div class="cmp-cell cmp-good">
            <span class="mark mark-v" aria-hidden="true">✓</span>
            {{ row.good }}
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.cmp {
  border: 1px solid var(--line-d);
  border-radius: var(--r);
  overflow: hidden;
}

.cmp-row {
  display: grid;
  grid-template-columns: 0.75fr 1.15fr 1.15fr;
}
.cmp-row + .cmp-row { border-top: 1px solid var(--line-d); }

.cmp-cell {
  padding: 22px 22px;
  font-size: 14px;
  display: flex;
  align-items: flex-start;
  gap: 12px;
}
.cmp-cell + .cmp-cell { border-left: 1px solid var(--line-d); }

.cmp-head { background: var(--bg2); }
.cmp-head .cmp-cell {
  font-family: var(--font-m);
  font-size: 11px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  padding: 17px 22px;
}
.cmp-oth-h { color: var(--w-soft); font-weight: 600; }
.cmp-good-h { color: var(--acc-hot); font-weight: 600; }

.cmp-label {
  font-family: var(--font-d);
  font-size: 12.5px;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--w-soft);
}

.cmp-oth {
  color: var(--w-soft);
  background: rgba(255, 255, 255, 0.03);
}
.cmp-good {
  color: var(--white);
  font-weight: 600;
  background: rgba(255, 90, 31, 0.055);
}

.mark {
  flex-shrink: 0;
  width: 21px;
  height: 21px;
  display: grid;
  place-items: center;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 800;
  margin-top: 1px;
}
.mark-e { background: rgba(255, 255, 255, 0.1); color: var(--w-soft); }
.mark-v { background: rgba(255, 90, 31, 0.2); color: var(--acc-hot); }

@media (max-width: 820px) {
  .cmp { border: none; display: flex; flex-direction: column; gap: 14px; }
  .cmp-head { display: none; }
  .cmp-row {
    grid-template-columns: 1fr;
    border: 1px solid var(--line-d) !important;
    border-radius: var(--r);
    overflow: hidden;
  }
  .cmp-cell + .cmp-cell { border-left: none; border-top: 1px solid var(--line-d); }
  .cmp-label { background: var(--bg2); padding: 14px 20px; }
  .cmp-cell { padding: 16px 20px; font-size: 14px; }
  .cmp-oth::before,
  .cmp-good::before {
    display: block;
    font-family: var(--font-m);
    font-size: 10px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 8px;
    opacity: 0.7;
  }
  .cmp-oth::before { content: 'Другие производители'; }
  .cmp-good::before { content: 'Грэйдстрой'; color: var(--acc-hot); }
}
</style>
