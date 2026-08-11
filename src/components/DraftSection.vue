<template>
  <section class="sec sec--light sec--light2">
    <div class="container">
      <div class="sec-head" v-reveal>
        <p class="sec-tag"><span class="idx">/ 11</span> Нет чертежа?</p>
        <h2 class="sec-title">Чертежа нет? Это <em>начало работы</em>, а не проблема</h2>
      </div>

      <div class="draft-grid">
        <article class="card draft-card" v-reveal>
          <p class="draft-kicker">Вариант 1</p>
          <h3>Есть КМ или АР</h3>
          <p>Сразу делаем КМД и запускаем в производство — сроки минимальны.</p>
        </article>
        <article class="card draft-card" v-reveal="100">
          <p class="draft-kicker">Вариант 2</p>
          <h3>Проекта нет</h3>
          <p>
            Разработаем его с нуля. Честно: это добавит времени. Но переделка потом
            всегда обходится дороже и дольше, чем нормальный чертёж сейчас.
          </p>
        </article>
      </div>

      <div class="magnet" v-reveal="150">
        <div class="magnet-text">
          <p class="magnet-kicker">Бесплатный чек-лист</p>
          <h3>Хотите сократить время на расчёт?</h3>
          <p>
            Откройте чек-лист — что подготовить, чтобы мы посчитали
            стоимость и сроки за 1 день.
          </p>
        </div>
        <div class="magnet-cta">
          <a href="/docs/chek-list.html" target="_blank" rel="noopener" class="btn">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M14 3h7v7" /><path d="M10 14 21 3" /><path d="M21 10v11H3V3h11" />
            </svg>
            Открыть чек-лист
          </a>
          <p class="btn-note">2 страницы · откроется в новой вкладке</p>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.draft-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 22px;
  margin-bottom: 26px;
}

.draft-card { padding: 32px; }
.draft-kicker {
  font-family: var(--font-m);
  font-size: 11px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--acc);
  margin-bottom: 14px;
}
.draft-card h3 {
  font-family: var(--font-d);
  font-size: 18px;
  font-weight: 700;
  text-transform: uppercase;
  margin-bottom: 12px;
}
.draft-card p { font-size: 15px; color: var(--ink-soft); }

.magnet {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 40px;
  background: var(--bg0);
  color: var(--white);
  border-radius: var(--r);
  padding: 40px 44px;
  position: relative;
  overflow: hidden;
}
.magnet::before {
  content: '';
  position: absolute;
  right: -60px;
  top: -60px;
  width: 240px;
  height: 240px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255, 90, 31, 0.28), transparent 70%);
}

.magnet-kicker {
  font-family: var(--font-m);
  font-size: 11px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--acc-hot);
  margin-bottom: 12px;
}
.magnet-text h3 {
  font-family: var(--font-d);
  font-size: clamp(18px, 2.2vw, 24px);
  font-weight: 700;
  text-transform: uppercase;
  margin-bottom: 10px;
}
.magnet-text p { color: var(--w-soft); font-size: 15px; max-width: 480px; }

.magnet-cta { flex-shrink: 0; position: relative; }
.magnet-cta .btn svg { width: 18px; height: 18px; }
.magnet-cta .btn { text-decoration: none; }
.magnet-cta .btn-note { text-align: center; }

@media (max-width: 820px) {
  .draft-grid { grid-template-columns: 1fr; }
  .magnet { flex-direction: column; align-items: flex-start; padding: 32px 26px; }
}
</style>
