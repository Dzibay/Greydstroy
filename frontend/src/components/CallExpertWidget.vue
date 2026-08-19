<script setup>
import { ref } from 'vue'

const open = ref(false)
</script>

<template>
  <div class="cew">
    <transition name="cew-pop">
      <div v-if="open" class="cew-card" role="dialog" aria-label="Связь с инженером">
        <button class="cew-close" aria-label="Закрыть" @click="open = false">✕</button>

        <p class="cew-tag">⚡ Прямая линия производства</p>
        <p class="cew-title">Звоните прямо сейчас</p>
        <p class="cew-text">
          Проконсультируем по материалам, срокам и стоимости —
          расчёт по вашему чертежу за 1 рабочий день.
        </p>

        <a href="tel:+79056646665" class="cew-phone">+7 (905) 664-66-65</a>

        <ul class="cew-list">
          <li><span>◆</span> Пн–Пт: 08:00 – 17:00 (МСК)</li>
          <li><span>◆</span> Отвечает инженер, а не колл-центр</li>
        </ul>

        <a href="/kalkulyator" class="btn btn--block cew-btn" @click="open = false">Рассчитать заказ</a>
      </div>
    </transition>

    <button class="cew-fab" :class="{ open }" @click="open = !open">
      <span class="cew-fab-icon" aria-hidden="true">
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path
            d="M6.6 10.8c1.5 2.9 3.7 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.6 21 3 13.4 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.2.2 2.4.6 3.6.1.3 0 .7-.2 1l-2.3 2.2Z"
            fill="currentColor"
          />
        </svg>
      </span>
      <span class="cew-fab-label">Прямая связь с инженером</span>
    </button>
  </div>
</template>

<style scoped>
.cew {
  position: fixed;
  left: 22px;
  bottom: 22px;
  z-index: 90;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 14px;
}

/* ---- кнопка ---- */
.cew-fab {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  background: var(--acc);
  color: #fff;
  border: none;
  padding: 13px 20px;
  font-family: var(--font-m);
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  clip-path: polygon(0 0, calc(100% - 12px) 0, 100% 12px, 100% 100%, 12px 100%, 0 calc(100% - 12px));
  box-shadow: 0 12px 34px rgba(255, 90, 31, 0.4);
  transition: background 0.25s, transform 0.25s var(--ease);
  animation: cew-glow 2.6s infinite;
}
.cew-fab:hover {
  background: var(--acc-hot);
  transform: translateY(-2px);
}
.cew-fab.open { animation: none; }

@keyframes cew-glow {
  0%, 100% { box-shadow: 0 12px 34px rgba(255, 90, 31, 0.4); }
  50% { box-shadow: 0 12px 44px rgba(255, 90, 31, 0.75); }
}

.cew-fab-icon {
  width: 17px;
  height: 17px;
  flex-shrink: 0;
}
.cew-fab-icon svg { width: 100%; height: 100%; }

/* ---- карточка ---- */
.cew-card {
  position: relative;
  width: 320px;
  max-width: calc(100vw - 44px);
  background: rgba(17, 21, 26, 0.97);
  backdrop-filter: blur(18px);
  border: 1px solid var(--line-d);
  border-top: 3px solid var(--acc);
  border-radius: var(--r);
  padding: 26px 24px 22px;
  box-shadow: 0 30px 70px rgba(0, 0, 0, 0.55);
}

.cew-close {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: none;
  border: none;
  color: var(--w-faint);
  font-size: 14px;
  transition: color 0.2s;
}
.cew-close:hover { color: var(--white); }

.cew-tag {
  display: inline-block;
  font-family: var(--font-m);
  font-size: 10px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--acc-hot);
  border: 1px solid color-mix(in srgb, var(--acc) 50%, transparent);
  background: var(--acc-dim);
  padding: 5px 12px;
  border-radius: 999px;
  margin-bottom: 14px;
}

.cew-title {
  font-family: var(--font-d);
  font-size: 18px;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--white);
  margin-bottom: 10px;
}

.cew-text {
  font-size: 13.5px;
  color: var(--w-soft);
  line-height: 1.6;
  margin-bottom: 18px;
}

.cew-phone {
  display: block;
  text-align: center;
  font-family: var(--font-m);
  font-size: 21px;
  font-weight: 600;
  color: var(--white);
  border: 1.5px solid var(--line-d);
  background: rgba(255, 255, 255, 0.04);
  border-radius: var(--r-sm);
  padding: 14px 10px;
  margin-bottom: 16px;
  transition: border-color 0.2s, color 0.2s;
}
.cew-phone:hover {
  color: var(--acc-hot);
  border-color: color-mix(in srgb, var(--acc) 60%, transparent);
}

.cew-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 18px;
}
.cew-list li {
  font-family: var(--font-m);
  font-size: 11.5px;
  color: var(--w-soft);
  letter-spacing: 0.04em;
}
.cew-list li span {
  color: var(--acc);
  font-size: 9px;
  margin-right: 8px;
}

.cew-btn { font-size: 13.5px; padding: 13px 20px; }

/* ---- анимация ---- */
.cew-pop-enter-active,
.cew-pop-leave-active {
  transition: opacity 0.3s var(--ease), transform 0.3s var(--ease);
}
.cew-pop-enter-from,
.cew-pop-leave-to {
  opacity: 0;
  transform: translateY(14px) scale(0.97);
}

@media (max-width: 560px) {
  .cew { left: 14px; bottom: 14px; }
  .cew-fab-label { display: none; }
  .cew-fab { padding: 14px; }
  .cew-fab-icon { width: 20px; height: 20px; }
}
</style>
