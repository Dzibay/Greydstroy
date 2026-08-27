<template>
  <section id="team" class="sec sec--dark sec--deep">
    <div class="container">
      <div class="team-grid">
        <figure class="team-media" v-reveal>
          <img src="/img/team-shop.jpg" alt="Сварщик за работой в цеху Грэйдстрой" loading="lazy" />
          <figcaption>
            <span class="cap-line"></span>
            Наш цех · рабочая смена
          </figcaption>
        </figure>

        <div>
          <div class="sec-head team-head" v-reveal="80">
            <p class="sec-tag"><span class="idx">/ 12</span> Команда</p>
            <h2 class="sec-title">
              Расскажем не о том, какие мы классные, а о том, <em>где облажались</em>
            </h2>
          </div>
          <div class="team-text" v-reveal="160">
            <p>
              Был заказ, где мы неправильно посчитали загрузку станков — и подвели по срокам.
              Было ТЗ, где допуск клиента не совпал с реальностью оборудования — узнали
              об этом уже после начала резки, а не до.
            </p>
            <p>
              Каждый такой случай — не «ну бывает», а пункт в регламенте, который теперь
              работает на вас: сроки считаем с запасом, а ТЗ сверяем с технологом
              до начала работы, а не после.
            </p>
            <p class="team-strong">
              Кто-то называет это опытом. Мы называем это набитыми шишками,
              которые вам проходить не придётся.
            </p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.team-grid {
  display: grid;
  grid-template-columns: 0.95fr 1.05fr;
  gap: 64px;
  align-items: center;
}

.team-media { position: relative; }
.team-media img {
  border-radius: var(--r);
  width: 100%;
  aspect-ratio: 4 / 3.3;
  object-fit: cover;
}
.team-media::before {
  content: '';
  position: absolute;
  top: -22px;
  left: -22px;
  right: 22px;
  bottom: 22px;
  border: 1.5px solid var(--acc);
  border-radius: var(--r);
  opacity: 0.5;
}
.team-media figcaption {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 18px;
  font-family: var(--font-m);
  font-size: 11.5px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--w-faint);
}
.cap-line { width: 30px; height: 2px; background: var(--acc); flex-shrink: 0; }

.team-head { margin-bottom: 26px; }

.team-text p {
  font-size: 15.5px;
  color: var(--w-soft);
  margin-bottom: 18px;
  max-width: 560px;
}
.team-strong {
  font-weight: 800;
  color: var(--white) !important;
  border-left: 3px solid var(--acc);
  padding-left: 20px;
}

@media (max-width: 920px) {
  .team-grid { grid-template-columns: 1fr; gap: 48px; }
  .team-media { order: 2; }
  .team-media::before { top: 14px; left: 14px; right: -14px; bottom: -14px; }
}
</style>
