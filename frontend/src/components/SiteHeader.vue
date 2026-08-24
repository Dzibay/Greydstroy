<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import CompanyLogo from './ui/CompanyLogo.vue'
import { mainServices } from '../data/services'
import { company } from '../data/company'

const scrolled = ref(false)
const progress = ref(0)
const menuOpen = ref(false)
const dropLocked = ref(false)

function closeMenus() {
  menuOpen.value = false
  dropLocked.value = true
  const el = document.activeElement
  if (el instanceof HTMLElement) el.blur()
}

function unlockDrop() {
  dropLocked.value = false
}

const nav = [
  {
    to: '/uslugi',
    label: 'Услуги',
    children: mainServices.map((s) => ({ to: s.to, label: s.navLabel })),
  },
  { to: '/metallokonstruktsii', label: 'Металлоконструкции' },
  { to: '/projects', label: 'Объекты' },
  { to: '/dostavka', label: 'Доставка' },
  { to: '/kontakty', label: 'Контакты' },
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
        <template v-for="item in nav" :key="item.label">
          <div
            v-if="item.children"
            class="hdr-item"
            :class="{ 'drop-locked': dropLocked }"
            @mouseenter="unlockDrop"
            @mouseleave="unlockDrop"
          >
            <RouterLink :to="item.to" class="hdr-item-link" @click="closeMenus">
              {{ item.label }}
              <svg class="hdr-caret" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <path d="m2.5 4.5 3.5 3.5 3.5-3.5" />
              </svg>
            </RouterLink>
            <div class="hdr-drop">
              <div class="hdr-drop-in">
                <RouterLink
                  v-for="c in item.children"
                  :key="c.to"
                  :to="c.to"
                  class="hdr-drop-link"
                  @click="closeMenus"
                >
                  {{ c.label }}
                </RouterLink>
                <RouterLink :to="item.to" class="hdr-drop-link hdr-drop-link--all" @click="closeMenus">
                  Все услуги →
                </RouterLink>
              </div>
            </div>
          </div>
          <RouterLink v-else :to="item.to" @click="menuOpen = false">
            {{ item.label }}
          </RouterLink>
        </template>
        <a :href="company.phoneHref" class="hdr-phone-m" data-track="tel-header">{{ company.phone }}</a>
        <RouterLink to="/kalkulyator" class="btn hdr-calc-m" data-track="calc-header" @click="menuOpen = false">
          Рассчитать заказ
        </RouterLink>
      </nav>

      <div class="hdr-right">
        <a :href="company.phoneHref" class="hdr-phone" data-track="tel-header">{{ company.phone }}</a>
        <RouterLink to="/kalkulyator" class="btn hdr-btn" data-track="calc-header" @click="menuOpen = false">Рассчитать заказ</RouterLink>
        <button
          class="burger"
          :class="{ open: menuOpen }"
          @click="menuOpen = !menuOpen; dropLocked = false"
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
.hdr-phone-m,
.hdr-calc-m { display: none; }

/* ---------- выпадающее меню услуг ---------- */
.hdr-item { position: relative; display: flex; }
.hdr-item-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}
.hdr-caret {
  width: 11px;
  height: 11px;
  margin-top: 1px;
  transition: transform 0.25s var(--ease);
}
.hdr-item:hover .hdr-caret,
.hdr-item:focus-within .hdr-caret { transform: rotate(180deg); }

.hdr-drop {
  position: absolute;
  top: 100%;
  left: -18px;
  padding-top: 16px;
  opacity: 0;
  transform: translateY(-8px);
  pointer-events: none;
  transition: opacity 0.25s, transform 0.25s var(--ease);
  z-index: 20;
}
.hdr-item:hover .hdr-drop,
.hdr-item:focus-within .hdr-drop {
  opacity: 1;
  transform: none;
  pointer-events: auto;
}
.hdr-item.drop-locked .hdr-drop,
.hdr-item.drop-locked:hover .hdr-drop,
.hdr-item.drop-locked:focus-within .hdr-drop {
  opacity: 0;
  transform: translateY(-8px);
  pointer-events: none;
}
.hdr-drop-in {
  min-width: 300px;
  padding: 8px 0;
  background: rgba(11, 14, 17, 0.97);
  backdrop-filter: blur(16px);
  border: 1px solid var(--line-d);
  border-radius: 10px;
  box-shadow: 0 24px 48px rgba(0, 0, 0, 0.45);
}
.hdr-nav .hdr-drop-link {
  display: block;
  padding: 11px 20px;
  font-size: 14px;
  font-weight: 600;
  color: var(--w-soft);
  white-space: nowrap;
  transition: color 0.2s, background 0.2s;
}
.hdr-nav .hdr-drop-link::after { display: none; }
.hdr-nav .hdr-drop-link:hover {
  color: var(--white);
  background: rgba(255, 90, 31, 0.09);
}
.hdr-nav .hdr-drop-link--all {
  color: var(--acc-hot);
  border-top: 1px solid var(--line-d);
  margin-top: 6px;
  padding-top: 13px;
}
.hdr-nav .hdr-drop-link--all:hover { color: var(--acc); }

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
  .hdr-nav { max-height: calc(100vh - 76px); overflow-y: auto; }
  .hdr-nav a { padding: 14px 28px; font-size: 16px; }
  .hdr-nav a::after { display: none; }
  .hdr-item { flex-direction: column; }
  .hdr-caret { display: none; }
  .hdr-drop {
    position: static;
    padding-top: 0;
    opacity: 1;
    transform: none;
    pointer-events: auto;
  }
  .hdr-item.drop-locked .hdr-drop,
  .hdr-item.drop-locked:hover .hdr-drop,
  .hdr-item.drop-locked:focus-within .hdr-drop {
    opacity: 1;
    transform: none;
    pointer-events: auto;
  }
  .hdr-drop-in {
    min-width: 0;
    padding: 0 0 6px;
    background: transparent;
    backdrop-filter: none;
    border: none;
    border-radius: 0;
    box-shadow: none;
  }
  .hdr-nav .hdr-drop-link {
    padding: 10px 28px 10px 44px;
    font-size: 14.5px;
    white-space: normal;
  }
  .hdr-nav .hdr-drop-link--all { margin-top: 4px; padding-top: 12px; }
  .hdr-phone-m { display: block; color: var(--acc-hot); font-family: var(--font-m); }
  .hdr-nav a.hdr-calc-m {
    display: inline-flex;
    align-self: flex-start;
    width: auto;
    margin: 12px 28px 10px;
    padding: 13px 22px;
    font-size: 13.5px;
    font-weight: 800;
    color: #fff;
    background: var(--acc);
  }
  .hdr-nav a.hdr-calc-m:hover {
    color: #fff;
    background: var(--acc-hot);
  }
}
</style>
