<script setup>
import { computed } from 'vue'

const props = defineProps({
  items: { type: Array, required: true },
  tag: { type: String, default: 'Фото' },
  kicker: { type: String, default: 'С площадки' },
  title: { type: String, default: 'Цех и объекты' },
  titleEm: { type: String, default: 'без стока' },
  lead: { type: String, default: '' },
})

const tiles = computed(() => {
  const list = props.items.slice(0, 6)
  return list.length === 5 ? list.slice(0, 4) : list
})
</script>

<template>
  <section v-if="tiles.length" class="sec shop-gal">
    <div class="container">
      <div class="sec-head" v-reveal>
        <p class="sec-tag"><span class="idx">{{ tag }}</span> {{ kicker }}</p>
        <h2 class="sec-title">{{ title }} <em>{{ titleEm }}</em></h2>
        <p v-if="lead" class="sec-sub">{{ lead }}</p>
      </div>
      <div class="gal" :class="'n-' + tiles.length" v-reveal="80">
        <figure v-for="p in tiles" :key="p.src">
          <img :src="p.src" :alt="p.alt" loading="lazy" />
        </figure>
      </div>
    </div>
  </section>
</template>

<style scoped>
.shop-gal {
  background: var(--deep, #11161b);
}
.gal {
  display: grid;
  gap: 12px;
  align-items: stretch;
}
.gal.n-1 { grid-template-columns: 1fr; }
.gal.n-2,
.gal.n-4 { grid-template-columns: 1fr 1fr; }
.gal.n-3,
.gal.n-6 { grid-template-columns: 1fr 1fr 1fr; }
.gal figure {
  margin: 0;
  min-width: 0;
  aspect-ratio: 4 / 3;
  overflow: hidden;
  border-radius: var(--r);
  border: 1px solid var(--line-d);
  background: #0b0e11;
}
.gal.n-1 figure { aspect-ratio: 16 / 9; }
.gal img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
}
@media (max-width: 880px) {
  .gal.n-6 {
    grid-template-columns: 1fr 1fr;
  }
}
@media (max-width: 560px) {
  .gal.n-3 {
    grid-template-columns: 1fr;
  }
}
</style>
