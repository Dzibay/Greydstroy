<script setup>
import { computed, ref, watch, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  type: { type: String, default: 'frame' },
  coating: { type: String, default: 'primer' },
  kmd: { type: Boolean, default: false },
  montage: { type: Boolean, default: false },
  compact: { type: Boolean, default: false },
})

const uid = `dp${Math.random().toString(36).slice(2, 8)}`
const animKey = ref(0)
const pulse = ref(false)
let pulseTimer = 0

watch(
  () => [props.type, props.coating, props.kmd, props.montage],
  () => {
    animKey.value += 1
    pulse.value = true
    clearTimeout(pulseTimer)
    pulseTimer = setTimeout(() => {
      pulse.value = false
    }, 520)
  },
)

const coat = computed(() => {
  if (props.coating === 'paint') {
    return {
      metal: '#ff7d3f',
      metalDeep: '#c44514',
      metalLite: '#ffb08a',
      edge: '#ff5a1f',
    }
  }
  if (props.coating === 'primer') {
    return {
      metal: '#8b5a3c',
      metalDeep: '#5c3a28',
      metalLite: '#b87a52',
      edge: '#a06840',
    }
  }
  return {
    metal: '#9aa3ad',
    metalDeep: '#5c6570',
    metalLite: '#c8d0d8',
    edge: '#7a8490',
  }
})

function raw(x, y, z) {
  return { x: (x - y) * 0.86602540378, y: (x + y) * 0.5 - z }
}

/** Fit world samples into viewBox with generous padding so nothing clips. */
function fitProject(samples, compact) {
  let minX = Infinity
  let maxX = -Infinity
  let minY = Infinity
  let maxY = -Infinity
  for (const [x, y, z] of samples) {
    const p = raw(x, y, z)
    if (p.x < minX) minX = p.x
    if (p.x > maxX) maxX = p.x
    if (p.y < minY) minY = p.y
    if (p.y > maxY) maxY = p.y
  }
  const bw = maxX - minX || 1
  const bh = maxY - minY || 1
  const vw = 400
  const vh = compact ? 210 : 248
  const padX = compact ? 72 : 88
  const padY = compact ? 52 : 64
  const s = Math.min((vw - padX) / bw, (vh - padY) / bh) * 0.92
  const ox = (vw - bw * s) / 2 - minX * s
  const oy = (vh - bh * s) / 2 - minY * s
  return (x, y, z) => {
    const p = raw(x, y, z)
    return { x: ox + p.x * s, y: oy + p.y * s }
  }
}

function pts(list) {
  return list.map((p) => `${p.x.toFixed(1)},${p.y.toFixed(1)}`).join(' ')
}

function isoBox(P, x0, y0, x1, y1, z0, z1) {
  return {
    top: pts([P(x0, y0, z1), P(x1, y0, z1), P(x1, y1, z1), P(x0, y1, z1)]),
    front: pts([P(x0, y0, z0), P(x1, y0, z0), P(x1, y0, z1), P(x0, y0, z1)]),
    side: pts([P(x1, y0, z0), P(x1, y1, z0), P(x1, y1, z1), P(x1, y0, z1)]),
    _d: x0 + x1 + y0 + y1,
  }
}

function pushBoxCorners(out, x0, y0, x1, y1, z0, z1) {
  out.push([x0, y0, z0], [x1, y0, z0], [x1, y1, z0], [x0, y1, z0])
  out.push([x0, y0, z1], [x1, y0, z1], [x1, y1, z1], [x0, y1, z1])
}

const geo = computed(() => {
  const t = props.type
  const samples = []
  let build = null

  if (t === 'plates') {
    const L = 10
    const W = 6.5
    const th = 0.55
    pushBoxCorners(samples, 0, 0, L, W, 0, th)
    samples.push([1.2, 1.2, th + 1.8], [L - 1.2, W - 1.2, th + 1.8])
    samples.push([-0.8, -0.8, 0], [L + 0.8, W + 0.8, 0])
    build = (P) => {
      const plate = isoBox(P, 0, 0, L, W, 0, th)
      const holes = [
        [1.2, 1.2],
        [L - 1.2, 1.2],
        [1.2, W - 1.2],
        [L - 1.2, W - 1.2],
        [L / 2, W / 2],
      ].map(([x, y]) => {
        const c = P(x, y, th + 0.02)
        return { cx: c.x, cy: c.y, r: 3.2 }
      })
      const anchors = [
        [1.2, 1.2],
        [L - 1.2, 1.2],
        [1.2, W - 1.2],
        [L - 1.2, W - 1.2],
      ].map(([x, y]) => {
        const a = P(x, y, th)
        const b = P(x, y, th + 1.8)
        return { x1: a.x, y1: a.y, x2: b.x, y2: b.y }
      })
      return {
        boxes: [plate],
        holes,
        anchors,
        ground: pts([P(-0.6, -0.6, 0), P(L + 0.6, -0.6, 0), P(L + 0.6, W + 0.6, 0), P(-0.6, W + 0.6, 0)]),
        dims: {
          L: { ...P(L / 2, -0.5, 0), text: 'L' },
          W: { ...P(L + 0.4, W / 2, 0), text: 'B' },
        },
      }
    }
  } else if (t === 'beams') {
    const L = 12
    const bf = 1.8
    const tw = 0.42
    const tf = 0.35
    const H = 3.2
    pushBoxCorners(samples, 0, 0, L, bf, 0, H)
    samples.push([-0.5, -0.6, 0], [L + 0.5, bf + 0.6, 0])
    build = (P) => {
      const bottom = isoBox(P, 0, 0, L, bf, 0, tf)
      const web = isoBox(P, 0, (bf - tw) / 2, L, (bf + tw) / 2, tf, H - tf)
      const top = isoBox(P, 0, 0, L, bf, H - tf, H)
      return {
        boxes: [bottom, web, top].sort((a, b) => b._d - a._d),
        ground: pts([P(-0.4, -0.5, 0), P(L + 0.4, -0.5, 0), P(L + 0.4, bf + 0.5, 0), P(-0.4, bf + 0.5, 0)]),
        dims: {
          L: { ...P(L / 2, -0.4, 0), text: 'L' },
          H: { ...P(-0.35, bf / 2, H / 2), text: 'H' },
        },
      }
    }
  } else if (t === 'truss') {
    const L = 14
    const W = 1.0
    const H = 3.0
    samples.push([0, 0, 0], [L, 0, 0], [0, W, 0], [L, W, 0], [L / 2, W / 2, H])
    samples.push([-0.6, -0.8, 0], [L + 0.6, W + 0.8, 0])
    build = (P) => {
      const chordBot = [
        { a: P(0, 0, 0.12), b: P(L, 0, 0.12) },
        { a: P(0, W, 0.12), b: P(L, W, 0.12) },
      ]
      const chordTop = [
        { a: P(0, 0, 0.12), b: P(L / 2, W / 2, H) },
        { a: P(L, 0, 0.12), b: P(L / 2, W / 2, H) },
        { a: P(0, W, 0.12), b: P(L / 2, W / 2, H) },
        { a: P(L, W, 0.12), b: P(L / 2, W / 2, H) },
      ]
      const n = 5
      const webs = []
      for (let i = 0; i <= n; i++) {
        const x = (i / n) * L
        const z = 0.12 + (H - 0.12) * (1 - Math.abs((i / n) * 2 - 1))
        webs.push({ a: P(x, 0, 0.12), b: P(x, 0, z) })
      }
      for (let i = 0; i < n; i++) {
        const x0 = (i / n) * L
        const x1 = ((i + 1) / n) * L
        const z1 = 0.12 + (H - 0.12) * (1 - Math.abs(((i + 1) / n) * 2 - 1))
        const z0 = 0.12 + (H - 0.12) * (1 - Math.abs((i / n) * 2 - 1))
        webs.push({ a: P(x0, 0, 0.12), b: P(x1, 0, z1) })
        webs.push({ a: P(x0, 0, z0), b: P(x1, 0, 0.12) })
      }
      return {
        lines: [...chordBot, ...chordTop, ...webs],
        peak: P(L / 2, W / 2, H),
        ground: pts([P(-0.5, -0.7, 0), P(L + 0.5, -0.7, 0), P(L + 0.5, W + 0.7, 0), P(-0.5, W + 0.7, 0)]),
        dims: {
          L: { ...P(L / 2, -0.55, 0), text: 'пролёт' },
          H: { ...P(L / 2 + 0.6, W / 2, H / 2), text: 'h' },
        },
      }
    }
  } else if (t === 'stairs') {
    const L = 7.5
    const W = 2.4
    const H = 4.2
    const n = 6
    const landW = 1.6
    const railH = 0.85
    samples.push([0, 0, 0], [L + landW, 0, H + railH], [L + landW, W * 1.25, H + railH], [0, W, 0])
    samples.push([-0.5, -0.5, 0], [L + landW + 0.4, W * 1.3, 0])
    build = (P) => {
      const treads = []
      const stringerA = []
      const stringerB = []
      for (let i = 0; i <= n; i++) {
        const u = i / n
        const x = u * L
        const z = u * H
        stringerA.push(P(x, 0, z))
        stringerB.push(P(x, W, z))
        treads.push({ a: P(x, 0, z), b: P(x, W, z) })
      }
      const land = [
        P(L, 0, H),
        P(L + landW, 0, H),
        P(L + landW, W * 1.25, H),
        P(L, W * 1.25, H),
      ]
      const rail = pts([
        P(0.15, 0, railH * 0.35),
        ...Array.from({ length: n + 1 }, (_, i) => {
          const u = i / n
          return P(u * L, 0, u * H + railH)
        }),
        P(L + landW, 0, H + railH),
        P(L + landW, W * 1.25, H + railH),
        P(L, W * 1.25, H + railH),
      ])
      const posts = [
        { a: P(0.15, 0, 0), b: P(0.15, 0, railH * 0.35) },
        { a: P(L, 0, H), b: P(L, 0, H + railH) },
        { a: P(L + landW, 0, H), b: P(L + landW, 0, H + railH) },
        { a: P(L + landW, W * 1.25, H), b: P(L + landW, W * 1.25, H + railH) },
      ]
      return {
        stairTreads: treads,
        stringerA: pts(stringerA),
        stringerB: pts(stringerB),
        land: pts(land),
        rail,
        posts,
        ground: pts([P(-0.4, -0.4, 0), P(L + landW + 0.3, -0.4, 0), P(L + landW + 0.3, W * 1.35, 0), P(-0.4, W * 1.35, 0)]),
        dims: {
          H: { ...P(-0.35, W / 2, H / 2), text: 'H' },
        },
      }
    }
  } else if (t === 'custom') {
    // Wireframe vessel — no solid faces that flood the panel
    const R = 2.6
    const H = 5.5
    const cx = 3.2
    const cy = 3.2
    const segs = 16
    for (let i = 0; i < segs; i++) {
      const a = (i / segs) * Math.PI * 2
      const x = cx + R * Math.cos(a)
      const y = cy + R * Math.sin(a)
      samples.push([x, y, 0], [x, y, H])
    }
    samples.push([cx, cy, H + 0.5], [cx - R - 0.6, cy - R - 0.6, -0.9], [cx + R + 0.6, cy + R + 0.6, 0])
    build = (P) => {
      const ring = (z) =>
        Array.from({ length: segs }, (_, i) => {
          const a = (i / segs) * Math.PI * 2 - Math.PI / 2
          return P(cx + R * Math.cos(a), cy + R * Math.sin(a), z)
        })
      const top = ring(H)
      const bot = ring(0)
      const mid = ring(H * 0.45)
      const verts = []
      for (let i = 0; i < segs; i += 2) {
        verts.push({ a: bot[i], b: top[i] })
      }
      const legs = [0, 4, 8, 12].map((i) => {
        const a = (i / segs) * Math.PI * 2 - Math.PI / 2
        const x = cx + (R - 0.15) * Math.cos(a)
        const y = cy + (R - 0.15) * Math.sin(a)
        return { a: P(x, y, 0), b: P(x, y, -0.85) }
      })
      const nozzle = {
        a: P(cx, cy, H),
        b: P(cx, cy, H + 0.45),
        cap: P(cx, cy, H + 0.45),
      }
      return {
        tankRings: [pts(bot.concat([bot[0]])), pts(mid.concat([mid[0]])), pts(top.concat([top[0]]))],
        tankVerts: verts,
        tankLegs: legs,
        tankNozzle: nozzle,
        ground: pts([
          P(cx - R - 0.5, cy - R - 0.5, 0),
          P(cx + R + 0.5, cy - R - 0.5, 0),
          P(cx + R + 0.5, cy + R + 0.5, 0),
          P(cx - R - 0.5, cy + R + 0.5, 0),
        ]),
        dims: {
          H: { ...P(cx - R - 0.55, cy, H / 2), text: 'Ø' },
        },
      }
    }
  } else {
    // frame / canopy — include roof peak in bounds
    const L = 10
    const W = 7
    const H = 4.6
    const rise = 0.95
    samples.push(
      [0, 0, 0],
      [L, 0, 0],
      [L, W, 0],
      [0, W, 0],
      [0, 0, H],
      [L, 0, H],
      [L, W, H],
      [0, W, H],
      [0, W / 2, H + rise],
      [L, W / 2, H + rise],
      [-0.7, -0.7, -0.5],
      [L + 0.7, W + 0.7, 0],
    )
    build = (P) => {
      const colXY = [
        [0.35, 0.35],
        [L - 0.35, 0.35],
        [0.35, W - 0.35],
        [L - 0.35, W - 0.35],
      ]
      const cols = colXY.map(([x, y]) => {
        const a = P(x, y, 0)
        const b = P(x, y, H)
        return { x1: a.x, y1: a.y, x2: b.x, y2: b.y, back: y > W * 0.5 }
      })
      const beams = [
        { a: P(0.35, 0.35, H), b: P(L - 0.35, 0.35, H) },
        { a: P(0.35, W - 0.35, H), b: P(L - 0.35, W - 0.35, H) },
        { a: P(0.35, 0.35, H), b: P(0.35, W - 0.35, H) },
        { a: P(L - 0.35, 0.35, H), b: P(L - 0.35, W - 0.35, H) },
      ]
      const roof = [
        pts([P(0, 0, H), P(L, 0, H), P(L, W / 2, H + rise), P(0, W / 2, H + rise)]),
        pts([P(0, W, H), P(L, W, H), P(L, W / 2, H + rise), P(0, W / 2, H + rise)]),
      ]
      const ridge = { a: P(0, W / 2, H + rise), b: P(L, W / 2, H + rise) }
      const pads = colXY.map(([x, y]) => isoBox(P, x - 0.55, y - 0.55, x + 0.55, y + 0.55, -0.45, 0))
      return {
        cols,
        beams,
        roof,
        ridge,
        boxes: pads,
        ground: pts([P(-0.35, -0.35, 0), P(L + 0.35, -0.35, 0), P(L + 0.35, W + 0.35, 0), P(-0.35, W + 0.35, 0)]),
        dims: {
          L: { ...P(L / 2, -0.35, 0), text: 'каркас' },
        },
      }
    }
  }

  const P = fitProject(samples, props.compact)
  const shape = build(P)

  let montage = null
  if (props.montage && shape.ground) {
    const base = shape.ground.split(' ').map((s) => {
      const [x, y] = s.split(',').map(Number)
      return { x, y }
    })
    if (base.length >= 4) {
      const cx = (base[0].x + base[2].x) / 2
      const cy = Math.min(...base.map((p) => p.y)) - 14
      montage = { x: cx, y: cy }
    }
  }

  return { ...shape, montage }
})

const typeLabel = computed(() => {
  const map = {
    plates: 'Закладная деталь',
    beams: 'Балка / колонна',
    frame: 'Каркас / навес',
    truss: 'Ферма',
    stairs: 'Лестничный марш',
    custom: 'Ёмкость / узел',
  }
  return map[props.type] || 'Конструкция'
})

const reduced = ref(false)
onMounted(() => {
  reduced.value = window.matchMedia('(prefers-reduced-motion: reduce)').matches
})
onUnmounted(() => {
  clearTimeout(pulseTimer)
})
</script>

<template>
  <div
    class="dp"
    :class="{
      'dp--compact': compact,
      'dp--kmd': kmd,
      'dp--pulse': pulse && !reduced,
    }"
  >
    <svg
      class="sketch"
      :class="{ 'sketch--compact': compact }"
      :viewBox="compact ? '0 0 400 210' : '0 0 400 248'"
      role="img"
      :aria-label="typeLabel"
    >
      <defs>
        <linearGradient :id="uid + '-gnd'" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stop-color="#ff5a1f" stop-opacity="0.16" />
          <stop offset="100%" stop-color="#ff5a1f" stop-opacity="0.03" />
        </linearGradient>
        <linearGradient :id="uid + '-metal'" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" :stop-color="coat.metalLite" />
          <stop offset="55%" :stop-color="coat.metal" />
          <stop offset="100%" :stop-color="coat.metalDeep" />
        </linearGradient>
        <linearGradient :id="uid + '-side'" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" :stop-color="coat.metal" stop-opacity="0.95" />
          <stop offset="100%" :stop-color="coat.metalDeep" />
        </linearGradient>
        <linearGradient :id="uid + '-top'" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0%" :stop-color="coat.metalLite" />
          <stop offset="100%" :stop-color="coat.metal" />
        </linearGradient>
        <pattern :id="uid + '-bp'" width="16" height="16" patternUnits="userSpaceOnUse">
          <path d="M16 0H0V16" fill="none" stroke="rgba(86,160,220,0.22)" stroke-width="0.6" />
        </pattern>
      </defs>

      <g v-if="kmd" class="bp-layer" :key="'bp' + animKey">
        <rect x="12" y="10" width="376" :height="compact ? 190 : 228" rx="6" class="bp-sheet" />
        <rect x="12" y="10" width="376" :height="compact ? 190 : 228" rx="6" :fill="`url(#${uid}-bp)`" />
        <text class="bp-stamp" x="28" y="28">КМД · деталировка</text>
        <text class="bp-stamp bp-stamp--r" x="372" :y="compact ? 188 : 226">1:50</text>
        <rect x="280" :y="compact ? 155 : 190" width="100" height="38" class="bp-title" />
        <text class="bp-tiny" x="288" :y="compact ? 168 : 203">Грэйдстрой</text>
        <text class="bp-tiny" x="288" :y="compact ? 180 : 215">лист 1</text>
      </g>

      <polygon
        v-if="geo.ground"
        :points="geo.ground"
        :fill="`url(#${uid}-gnd)`"
        stroke="rgba(255,90,31,0.3)"
        stroke-width="1"
        class="ground"
      />

      <g v-if="geo.boxes?.length" class="boxes">
        <g v-for="(box, i) in geo.boxes" :key="'bx' + i">
          <polygon :points="box.side" :fill="`url(#${uid}-side)`" :stroke="coat.edge" stroke-width="0.7" />
          <polygon :points="box.front" :fill="`url(#${uid}-metal)`" :stroke="coat.edge" stroke-width="0.7" />
          <polygon :points="box.top" :fill="`url(#${uid}-top)`" :stroke="coat.metalLite" stroke-width="0.85" />
        </g>
      </g>

      <!-- tank wireframe -->
      <g v-if="geo.tankRings" class="tank" fill="none" :stroke="coat.metalLite" stroke-linecap="round" stroke-linejoin="round">
        <polyline
          v-for="(r, i) in geo.tankRings"
          :key="'tr' + i"
          :points="r"
          :stroke-width="i === 2 ? 1.8 : 1.25"
          :opacity="i === 1 ? 0.45 : 0.9"
        />
        <line
          v-for="(v, i) in geo.tankVerts"
          :key="'tv' + i"
          :x1="v.a.x"
          :y1="v.a.y"
          :x2="v.b.x"
          :y2="v.b.y"
          stroke-width="1.2"
          opacity="0.8"
        />
        <line
          v-for="(leg, i) in geo.tankLegs"
          :key="'tl' + i"
          :x1="leg.a.x"
          :y1="leg.a.y"
          :x2="leg.b.x"
          :y2="leg.b.y"
          stroke-width="1.5"
        />
        <line
          v-if="geo.tankNozzle"
          :x1="geo.tankNozzle.a.x"
          :y1="geo.tankNozzle.a.y"
          :x2="geo.tankNozzle.b.x"
          :y2="geo.tankNozzle.b.y"
          stroke-width="1.6"
        />
        <circle
          v-if="geo.tankNozzle"
          :cx="geo.tankNozzle.cap.x"
          :cy="geo.tankNozzle.cap.y"
          r="3"
          :fill="coat.edge"
          stroke="none"
        />
      </g>

      <g v-if="geo.cols" class="frame">
        <g stroke="rgba(255,255,255,0.18)" stroke-width="1.15">
          <line
            v-for="(c, i) in geo.cols.filter((c) => c.back)"
            :key="'cb' + i"
            :x1="c.x1"
            :y1="c.y1"
            :x2="c.x2"
            :y2="c.y2"
          />
        </g>
        <g v-if="geo.roof" fill="rgba(255,90,31,0.08)" :stroke="coat.edge" stroke-width="1.45" stroke-linejoin="round">
          <polygon v-for="(p, i) in geo.roof" :key="'rf' + i" :points="p" />
        </g>
        <line
          v-if="geo.ridge"
          :x1="geo.ridge.a.x"
          :y1="geo.ridge.a.y"
          :x2="geo.ridge.b.x"
          :y2="geo.ridge.b.y"
          :stroke="coat.metalLite"
          stroke-width="1.65"
        />
        <g :stroke="coat.metalLite" stroke-width="1.75" stroke-linecap="round">
          <line
            v-for="(c, i) in geo.cols.filter((c) => !c.back)"
            :key="'cf' + i"
            :x1="c.x1"
            :y1="c.y1"
            :x2="c.x2"
            :y2="c.y2"
          />
          <line
            v-for="(b, i) in geo.beams || []"
            :key="'bm' + i"
            :x1="b.a.x"
            :y1="b.a.y"
            :x2="b.b.x"
            :y2="b.b.y"
          />
        </g>
      </g>

      <g v-if="geo.lines" class="truss" fill="none" :stroke="coat.metalLite" stroke-linecap="round" stroke-linejoin="round">
        <line
          v-for="(ln, i) in geo.lines"
          :key="'ln' + i"
          :x1="ln.a.x"
          :y1="ln.a.y"
          :x2="ln.b.x"
          :y2="ln.b.y"
          :stroke-width="i < 2 ? 2 : i < 6 ? 1.6 : 1.1"
          :opacity="i < 6 ? 1 : 0.72"
        />
        <circle
          v-if="geo.peak"
          :cx="geo.peak.x"
          :cy="geo.peak.y"
          r="3"
          :fill="coat.edge"
          stroke="none"
        />
      </g>

      <g v-if="geo.stairTreads" class="stairs" fill="none" :stroke="coat.metalLite" stroke-linecap="round" stroke-linejoin="round">
        <polygon
          :points="geo.land"
          fill="rgba(255,255,255,0.06)"
          :stroke="coat.edge"
          stroke-width="1.4"
        />
        <polyline :points="geo.stringerA" stroke-width="1.7" />
        <polyline :points="geo.stringerB" stroke-width="1.3" opacity="0.65" />
        <line
          v-for="(t, i) in geo.stairTreads"
          :key="'st' + i"
          :x1="t.a.x"
          :y1="t.a.y"
          :x2="t.b.x"
          :y2="t.b.y"
          stroke-width="1.2"
        />
        <line
          v-for="(p, i) in geo.posts"
          :key="'sp' + i"
          :x1="p.a.x"
          :y1="p.a.y"
          :x2="p.b.x"
          :y2="p.b.y"
          stroke-width="1.15"
        />
        <polyline :points="geo.rail" stroke-width="1.45" />
      </g>

      <g v-if="geo.holes">
        <circle
          v-for="(h, i) in geo.holes"
          :key="'h' + i"
          :cx="h.cx"
          :cy="h.cy"
          :r="h.r"
          fill="rgba(0,0,0,0.45)"
          :stroke="coat.edge"
          stroke-width="0.8"
        />
        <line
          v-for="(a, i) in geo.anchors || []"
          :key="'an' + i"
          :x1="a.x1"
          :y1="a.y1"
          :x2="a.x2"
          :y2="a.y2"
          :stroke="coat.metalLite"
          stroke-width="1.6"
          stroke-linecap="round"
        />
      </g>

      <g v-if="kmd && geo.dims" class="dims">
        <text
          v-for="(d, key) in geo.dims"
          :key="key"
          class="lbl"
          :x="d.x"
          :y="d.y + (key === 'L' ? 14 : 0)"
          :text-anchor="key === 'H' ? 'end' : 'middle'"
        >
          {{ d.text }}
        </text>
      </g>

      <g v-if="geo.montage" class="montage" :transform="`translate(${geo.montage.x}, ${geo.montage.y})`">
        <rect x="-28" y="-10" width="56" height="18" rx="4" fill="rgba(53,201,126,0.18)" stroke="#35c97e" stroke-width="1" />
        <text class="montage-lbl" text-anchor="middle" y="3">монтаж</text>
      </g>
    </svg>
  </div>
</template>

<style scoped>
.dp {
  position: relative;
  overflow: hidden;
  border-radius: inherit;
}
.sketch {
  display: block;
  width: 100%;
  height: auto;
  overflow: hidden;
}
.dp--pulse .sketch {
  animation: dp-in 0.4s cubic-bezier(0.22, 1, 0.36, 1);
}
@keyframes dp-in {
  0% {
    opacity: 0.4;
    transform: scale(0.96);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

.bp-sheet {
  fill: rgba(18, 42, 68, 0.55);
  stroke: rgba(86, 160, 220, 0.45);
  stroke-width: 1.2;
}
.bp-title {
  fill: rgba(12, 28, 48, 0.65);
  stroke: rgba(86, 160, 220, 0.5);
  stroke-width: 0.8;
}
.bp-stamp {
  font-family: var(--font-m);
  font-size: 10px;
  fill: rgba(120, 190, 255, 0.75);
  letter-spacing: 0.08em;
  text-transform: uppercase;
}
.bp-stamp--r {
  text-anchor: end;
}
.bp-tiny {
  font-family: var(--font-m);
  font-size: 9px;
  fill: rgba(140, 200, 255, 0.7);
}
.bp-layer {
  animation: bp-fade 0.4s ease;
}
@keyframes bp-fade {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.ground {
  transition: opacity 0.3s ease;
}
.dp--kmd .ground {
  opacity: 0.55;
}

.lbl {
  font-family: var(--font-m);
  font-size: 11px;
  fill: #7ec8ff;
  letter-spacing: 0.04em;
}

.montage-lbl {
  font-family: var(--font-m);
  font-size: 10px;
  fill: #35c97e;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}

.boxes polygon,
.frame line,
.truss line,
.tank polyline,
.tank line,
.stairs line,
.stairs polyline {
  transition:
    fill 0.35s ease,
    stroke 0.35s ease,
    opacity 0.3s ease;
}
</style>
