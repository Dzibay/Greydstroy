<script setup>
const placeholders = [1, 2, 3]
</script>

<template>
  <section id="cases" class="sec sec--light">
    <div class="container">
      <div class="sec-head" v-reveal>
        <p class="sec-tag"><span class="idx">/ 08</span> Кейсы</p>
        <h2 class="sec-title">Слова ничего не стоят. <em>Вот что мы делали</em></h2>
      </div>

      <div class="cases-grid">
        <article class="card case-card" v-reveal>
          <div class="photo-slot case-photo">
            <span>Фото объекта</span>
            <span class="ps-flag">Заполнить</span>
          </div>
          <div class="case-body">
            <p class="case-meta">Жилой комплекс · 3 недели · повторный заказ</p>
            <h3>Ограждения для жилого комплекса</h3>
            <p>
              340 метров, срок до сдачи объекта — 3 недели. Раскроили и сварили секции
              на своём производстве, отгружали партиями по мере готовности. Уложились
              в срок, заказчик разместил повторный заказ на входные группы.
            </p>
            <p class="case-note">⚠ иллюстративный пример — заменить на реальный кейс перед публикацией</p>
          </div>
        </article>

        <article
          v-for="n in placeholders"
          :key="n"
          class="card case-card case-card--empty"
          v-reveal="n * 90"
        >
          <div class="photo-slot case-photo">
            <span>Фото объекта</span>
            <span class="ps-flag">Заполнить</span>
          </div>
          <div class="case-body">
            <p class="case-meta">Отрасль · срок · результат</p>
            <h3>Название кейса</h3>
            <p>Задача клиента — что сделали — срок — результат. Место для реального проекта из вашего портфолио.</p>
          </div>
        </article>
      </div>
    </div>
  </section>
</template>

<style scoped>
.cases-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 22px;
}

.case-card {
  padding: 0;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.case-photo {
  border-radius: 0;
  border-left: none;
  border-right: none;
  border-top: none;
  min-height: 220px;
}

.case-body { padding: 28px 30px 30px; }

.case-meta {
  font-family: var(--font-m);
  font-size: 11px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--acc);
  margin-bottom: 12px;
}
.case-body h3 {
  font-family: var(--font-d);
  font-size: 17px;
  font-weight: 700;
  text-transform: uppercase;
  margin-bottom: 12px;
  line-height: 1.3;
}
.case-body p { font-size: 14.5px; color: var(--ink-soft); }

.case-note {
  margin-top: 16px;
  font-family: var(--font-m);
  font-size: 11px !important;
  color: #b5541f !important;
}

.case-card--empty { border-style: dashed; }
.case-card--empty h3 { color: var(--ink-faint); }
.case-card--empty .case-body p { color: var(--ink-faint); }
.case-card--empty .case-meta { color: color-mix(in srgb, var(--acc) 55%, transparent); }

@media (max-width: 760px) {
  .cases-grid { grid-template-columns: 1fr; }
}
</style>
