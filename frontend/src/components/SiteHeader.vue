<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import CompanyLogo from './ui/CompanyLogo.vue'

const scrolled = ref(false)
const progress = ref(0)
const menuOpen = ref(false)

const nav = [
  { to: { path: '/', hash: '#services' }, label: 'Услуги' },
  { to: { path: '/', hash: '#process' }, label: 'Процесс' },
  { to: { path: '/', hash: '#precision' }, label: 'Производство' },
  { to: '/projects', label: 'Объекты' },
  { to: { path: '/', hash: '#geo' }, label: 'Доставка' },
]

function onScroll() {
  scrolled.value = window.scrollY > 12
  const h = document.documentElement.scrollHeight - window.innerHeight
  progress.value = h > 0 ? (window.scrollY / h) * 100 : 0
}

onMounted(() => {
  window.addEventListener('scroll', onScroll, { passive: true })
  onScroll()
})
onUnmounted(() => window.removeEventListener('scroll', onScroll))
</script>

<template>
  <header class="hdr" :class="{ scrolled }">
    <div class="hdr-progress" :style="{ width: progress + '%' }"></div>
    <div class="container hdr-in">
      <RouterLink to="/" class="logo" @click="menuOpen = false">
        <CompanyLogo variant="light" />
      </RouterLink>

      <nav class="hdr-nav" :class="{ open: menuOpen }">
        <RouterLink
          v-for="item in nav"
          :key="item.label"
          :to="item.to"
          @click="menuOpen = false"
        >
          {{ item.label }}
        </RouterLink>
        <a href="tel:+79056646665" class="hdr-phone-m">+7 (905) 664-66-65</a>
      </nav>

      <div class="hdr-right">
        <a href="tel:+79056646665" class="hdr-phone">+7 (905) 664-66-65</a>
        <RouterLink to="/#cta" class="btn hdr-btn" @click="menuOpen = false">Рассчитать заказ</RouterLink>
        <button
          class="burger"
          :class="{ open: menuOpen }"
          @click="menuOpen = !menuOpen"
          aria-label="Меню"
        >
          <span></span><span></span><span></span>
        </button>
      </div>
    </div>
  </header>
</template>

<style scoped>
.hdr {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  background: transparent;
  transition: background 0.35s, box-shadow 0.35s;
}
.hdr.scrolled {
  background: rgba(11, 14, 17, 0.88);
  backdrop-filter: blur(14px);
  box-shadow: 0 1px 0 var(--line-d);
}
.hdr-progress {
  position: absolute;
  top: 0;
  left: 0;
  height: 2px;
  background: var(--acc);
  transition: width 0.1s linear;
}
.hdr-in {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  height: 76px;
}

.logo { display: flex; align-items: center; flex-shrink: 0; }

.hdr-nav { display: flex; gap: 28px; }
.hdr-nav a {
  font-size: 14px;
  font-weight: 600;
  color: var(--w-soft);
  transition: color 0.2s;
  position: relative;
}
.hdr-nav a:hover { color: var(--white); }
.hdr-nav a::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: -6px;
  width: 0;
  height: 2px;
  background: var(--acc);
  transition: width 0.25s var(--ease);
}
.hdr-nav a:hover::after { width: 100%; }
.hdr-phone-m { display: none; }

.hdr-right { display: flex; align-items: center; gap: 20px; }
.hdr-phone {
  font-family: var(--font-m);
  font-size: 14px;
  font-weight: 600;
  color: var(--white);
  white-space: nowrap;
}
.hdr-phone:hover { color: var(--acc-hot); }
.hdr-btn { padding: 12px 22px; font-size: 13.5px; }

.burger {
  display: none;
  flex-direction: column;
  gap: 5px;
  background: none;
  border: none;
  padding: 6px;
}
.burger span {
  width: 24px;
  height: 2.5px;
  background: var(--white);
  border-radius: 2px;
  transition: transform 0.3s, opacity 0.3s;
}
.burger.open span:nth-child(1) { transform: translateY(7.5px) rotate(45deg); }
.burger.open span:nth-child(2) { opacity: 0; }
.burger.open span:nth-child(3) { transform: translateY(-7.5px) rotate(-45deg); }

@media (max-width: 1060px) {
  .hdr-phone { display: none; }
}
@media (max-width: 880px) {
  .burger { display: flex; }
  .hdr-btn { display: none; }
  .hdr-nav {
    position: fixed;
    top: 76px;
    left: 0;
    right: 0;
    flex-direction: column;
    gap: 0;
    background: rgba(11, 14, 17, 0.97);
    backdrop-filter: blur(16px);
    border-bottom: 1px solid var(--line-d);
    padding: 8px 0 16px;
    transform: translateY(-12px);
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.3s, transform 0.3s;
  }
  .hdr-nav.open { opacity: 1; transform: none; pointer-events: auto; }
  .hdr-nav a { padding: 14px 28px; font-size: 16px; }
  .hdr-nav a::after { display: none; }
  .hdr-phone-m { display: block; color: var(--acc-hot); font-family: var(--font-m); }
}
</style>
