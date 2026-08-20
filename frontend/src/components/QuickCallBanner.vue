<template>
  <section id="quick-call" class="qcb-wrap" aria-label="Быстрая связь">
    <div class="container">
      <div class="qcb" v-reveal>
        <div class="qcb-left">
          <p class="qcb-kicker">⚡ Нет времени заполнять форму?</p>
          <p class="qcb-text">
            Позвоните — сориентируем по цене и срокам прямо во время разговора.
          </p>
        </div>

        <a href="tel:+79056646665" class="qcb-phone">+7 (905) 664-66-65</a>

        <ul class="qcb-meta">
          <li><span class="qcb-ico">◷</span> Пн–Пт: 08:00 – 17:00 (МСК)</li>
          <li><span class="qcb-ico">✓</span> Без автоответчиков и ботов</li>
        </ul>
      </div>
    </div>
  </section>
</template>

<style scoped>
.qcb-wrap {
  background: var(--bg1);
  padding: 34px 0;
  border-bottom: 1px solid var(--line-d);
}

.qcb {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 28px;
  flex-wrap: wrap;
  border: 1.5px solid color-mix(in srgb, var(--acc) 45%, transparent);
  background:
    repeating-linear-gradient(-45deg, transparent 0 18px, rgba(255, 90, 31, 0.04) 18px 36px),
    var(--card-d);
  border-radius: var(--r);
  padding: 26px 34px;
}

.qcb-kicker {
  font-family: var(--font-m);
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--acc-hot);
  margin-bottom: 8px;
}

.qcb-text {
  font-size: 14.5px;
  color: var(--w-soft);
  max-width: 340px;
  line-height: 1.55;
}

.qcb-phone {
  font-family: var(--font-m);
  font-size: clamp(22px, 2.6vw, 30px);
  font-weight: 600;
  color: var(--white);
  white-space: nowrap;
  transition: color 0.2s;
}
.qcb-phone:hover { color: var(--acc-hot); }

.qcb-meta {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.qcb-meta li {
  font-family: var(--font-m);
  font-size: 12px;
  color: var(--w-soft);
  letter-spacing: 0.04em;
  white-space: nowrap;
}

.qcb-ico {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  margin-right: 8px;
  border-radius: 5px;
  background: var(--acc-dim);
  color: var(--acc-hot);
  font-size: 11px;
}

@media (max-width: 900px) {
  .qcb {
    flex-direction: column;
    align-items: flex-start;
    gap: 18px;
    padding: 24px 24px;
  }
  .qcb-meta li { white-space: normal; }
}
</style>
