<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  value: { type: Number, required: true },
  prefix: { type: String, default: '' },
  suffix: { type: String, default: '' },
  duration: { type: Number, default: 1700 },
})

const el = ref(null)
const shown = ref(0)
let io = null

onMounted(() => {
  io = new IntersectionObserver(
    ([entry]) => {
      if (!entry.isIntersecting) return
      io.disconnect()
      const start = performance.now()
      const tick = (now) => {
        const p = Math.min(1, (now - start) / props.duration)
        shown.value = Math.round(props.value * (1 - Math.pow(1 - p, 3)))
        if (p < 1) requestAnimationFrame(tick)
      }
      requestAnimationFrame(tick)
    },
    { threshold: 0.4 }
  )
  io.observe(el.value)
})

onUnmounted(() => io?.disconnect())

const fmt = (n) => n.toLocaleString('ru-RU')
</script>

<template>
  <span ref="el">{{ prefix }}{{ fmt(shown) }}{{ suffix }}</span>
</template>
