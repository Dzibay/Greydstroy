<script setup>
defineProps({
  variant: {
    type: String,
    default: 'light',
    validator: (v) => ['light', 'dark'].includes(v),
  },
  showText: { type: Boolean, default: true },
})
</script>

<template>
  <span class="brand" :class="`brand--${variant}`">
    <img
      class="brand-logo"
      src="/img/logo.png"
      alt="Грэйдстрой"
      width="44"
      height="52"
    />
    <span v-if="showText" class="brand-text">
      Грэйдстрой
      <small>металлоконструкции</small>
    </span>
  </span>
</template>

<style scoped>
.brand {
  display: inline-flex;
  align-items: center;
  gap: 12px;
}

.brand-logo {
  width: 44px;
  height: 52px;
  object-fit: contain;
  flex-shrink: 0;
}

.brand-text {
  font-family: var(--font-d);
  font-weight: 700;
  font-size: 16px;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  line-height: 1.1;
  display: flex;
  flex-direction: column;
}

.brand--light .brand-text { color: var(--white, #f2f4f6); }
.brand--dark .brand-text { color: var(--ink, #12161b); }

.brand-text small {
  font-family: var(--font-m);
  font-weight: 400;
  font-size: 9px;
  letter-spacing: 0.22em;
  text-transform: uppercase;
}

.brand--light .brand-text small { color: var(--w-faint, #67717d); }
.brand--dark .brand-text small { color: var(--ink-faint, #8b939d); }
</style>
