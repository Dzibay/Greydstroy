<script setup>
const placeholders = [1, 2, 3]
</script>

<template>
  <section class="sec sec--light">
    <div class="container">
      <div class="sec-head" v-reveal>
        <p class="sec-tag"><span class="idx">/ 13</span> Отзывы</p>
        <h2 class="sec-title">Что говорят те, кто уже заказывал — <em>не мы, а они</em></h2>
      </div>

      <div class="rev-grid">
        <article v-for="n in placeholders" :key="n" class="card rev-card" v-reveal="n * 90">
          <span class="rev-quote" aria-hidden="true">
            <svg viewBox="0 0 32 32" fill="currentColor">
              <path d="M13 8v8h-5c0 3.3 2.2 5.4 5 6v3c-5.2-.7-9-4.6-9-10V8h9zm14 0v8h-5c0 3.3 2.2 5.4 5 6v3c-5.2-.7-9-4.6-9-10V8h9z" />
            </svg>
          </span>
          <p class="rev-text">Здесь будет отзыв вашего клиента — с реальными деталями заказа и результатом.</p>
          <div class="rev-author">
            <span class="rev-avatar" aria-hidden="true"></span>
            <div>
              <p class="rev-name">Имя, должность</p>
              <p class="rev-company">Компания</p>
            </div>
          </div>
          <span class="rev-flag">Заполнить реальным отзывом</span>
        </article>
      </div>

      <p class="rev-note" v-reveal>
        Без подписи (компания + контактное лицо) в B2B отзыв почти не работает
        на доверие — поэтому публикуем только отзывы с реальными подписями.
      </p>
    </div>
  </section>
</template>

<style scoped>
.rev-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.rev-card {
  border-style: dashed;
  display: flex;
  flex-direction: column;
  position: relative;
  padding: 30px 28px;
}

.rev-quote {
  color: var(--acc);
  opacity: 0.75;
  margin-bottom: 18px;
}
.rev-quote svg { width: 34px; height: 34px; }

.rev-text {
  font-size: 15px;
  font-style: italic;
  color: var(--ink-faint);
  flex: 1;
  margin-bottom: 24px;
}

.rev-author { display: flex; align-items: center; gap: 14px; }
.rev-avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: repeating-linear-gradient(-45deg, var(--paper2) 0 6px, #dfdbd2 6px 12px);
  border: 1.5px dashed var(--ink-faint);
  flex-shrink: 0;
}
.rev-name { font-weight: 700; font-size: 14px; color: var(--ink-soft); }
.rev-company { font-family: var(--font-m); font-size: 11.5px; color: var(--ink-faint); }

.rev-flag {
  position: absolute;
  top: 18px;
  right: 18px;
  font-family: var(--font-m);
  font-size: 9.5px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--acc);
  border: 1px solid color-mix(in srgb, var(--acc) 45%, transparent);
  border-radius: 4px;
  padding: 3px 8px;
}

.rev-note {
  margin-top: 28px;
  font-family: var(--font-m);
  font-size: 12px;
  color: var(--ink-faint);
  max-width: 640px;
  line-height: 1.7;
}

@media (max-width: 880px) {
  .rev-grid { grid-template-columns: 1fr; }
}
</style>
