<script setup>
import { computed } from 'vue'

const props = defineProps({
  length: { type: Number, required: true },
  width: { type: Number, required: true },
  height: { type: Number, required: true },
  roof: { type: String, default: 'gable' },
  crane: { type: String, default: 'none' },
  colStep: { type: Number, default: 6 },
  mezzanine: { type: Boolean, default: false },
  stairs: { type: Boolean, default: false },
  foundation: { type: String, default: 'pads' },
  compact: { type: Boolean, default: false },
})

function raw(x, y, z) {
  return { x: (x - y) * 0.86602540378, y: (x + y) * 0.5 - z }
}

function fitProject(L, W, H, rise, compact, foundation) {
  const depth = foundation === 'piles' ? H * 0.48 : H * 0.16
  const samples = [
    raw(0, 0, 0),
    raw(L, 0, 0),
    raw(L, W, 0),
    raw(0, W, 0),
    raw(0, 0, H),
    raw(L, 0, H),
    raw(L, W, H),
    raw(0, W, H),
    raw(0, W / 2, H + rise),
    raw(L, W / 2, H + rise),
    raw(0, 0, H + rise),
    raw(L, 0, H + rise),
    raw(0, W, H + rise),
    raw(L, W, H + rise),
    raw(-1, -1, -depth),
    raw(L + 1, W + 1, -depth),
  ]
  let minX = Infinity
  let maxX = -Infinity
  let minY = Infinity
  let maxY = -Infinity
  for (const p of samples) {
    if (p.x < minX) minX = p.x
    if (p.x > maxX) maxX = p.x
    if (p.y < minY) minY = p.y
    if (p.y > maxY) maxY = p.y
  }
  const bw = maxX - minX || 1
  const bh = maxY - minY || 1
  const vw = 400
  const vh = compact ? 210 : 248
  const padX = compact ? 36 : 52
  const padY = compact ? 28 : 40
  const s = Math.min((vw - padX) / bw, (vh - padY) / bh)
  const ox = (vw - bw * s) / 2 - minX * s
  const oy = (vh - bh * s) / 2 - minY * s + (compact ? 4 : 6)
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
  }
}

function isoHex(P, cx, cy, r, z0, z1) {
  const v = []
  for (let i = 0; i < 6; i++) {
    const a = Math.PI / 6 + i * (Math.PI / 3)
    v.push({ x: cx + r * Math.cos(a), y: cy + r * Math.sin(a) })
  }
  const faces = []
  for (let i = 0; i < 6; i++) {
    const a = v[i]
    const b = v[(i + 1) % 6]
    faces.push({
      poly: pts([P(a.x, a.y, z0), P(b.x, b.y, z0), P(b.x, b.y, z1), P(a.x, a.y, z1)]),
      _d: a.x + b.x + a.y + b.y,
    })
  }
  faces.sort((a, b) => b._d - a._d)
  return {
    faces: faces.slice(-3),
    top: pts(v.map((p) => P(p.x, p.y, z1))),
    _d: cx + cy,
  }
}

const geo = computed(() => {
  const L = props.length
  const W = props.width
  const H = props.height
  const rise =
    props.roof === 'arch'
      ? Math.min(W * 0.22, H * 0.45)
      : Math.min(W * 0.16, H * 0.32)
  const P = fitProject(L, W, H, rise, props.compact, props.foundation)

  const ground = [P(0, 0, 0), P(L, 0, 0), P(L, W, 0), P(0, W, 0)]

  const nCols = Math.min(12, Math.max(2, Math.round(L / Math.max(props.colStep, 4)) + 1))
  const xs = Array.from({ length: nCols }, (_, i) => (i / (nCols - 1)) * L)
  const yRows = W > 28 ? [0, W / 2, W] : [0, W]

  const cols = []
  for (const x of xs) {
    for (const y of yRows) {
      const a = P(x, y, 0)
      const b = P(x, y, H)
      const back = y > W * 0.4
      cols.push({ x1: a.x, y1: a.y, x2: b.x, y2: b.y, back })
    }
  }

  const eaves = [
    { a: P(0, 0, H), b: P(L, 0, H) },
    { a: P(0, W, H), b: P(L, W, H) },
    { a: P(0, 0, H), b: P(0, W, H) },
    { a: P(L, 0, H), b: P(L, W, H) },
  ]

  const portals = xs.map((x) => ({
    a: P(x, 0, H),
    b: P(x, W, H),
  }))

  let roof = []
  let ridge = null
  if (props.roof === 'gable') {
    const r0 = P(0, W / 2, H + rise)
    const r1 = P(L, W / 2, H + rise)
    ridge = { a: r0, b: r1 }
    roof = [
      [P(0, 0, H), P(L, 0, H), r1, r0],
      [P(0, W, H), P(L, W, H), r1, r0],
    ]
  } else if (props.roof === 'single') {
    roof = [[P(0, 0, H + rise), P(L, 0, H + rise), P(L, W, H), P(0, W, H)]]
  } else {
    const steps = 10
    const arc = (x) =>
      Array.from({ length: steps + 1 }, (_, i) => {
        const t = i / steps
        return P(x, t * W, H + rise * Math.sin(Math.PI * t))
      })
    roof = [arc(0), arc(L)]
  }

  let crane = null
  if (props.crane && props.crane !== 'none') {
    const z = H * 0.72
    const c0 = P(L * 0.12, 0, z)
    const c1 = P(L * 0.12, W, z)
    const hookTop = P(L * 0.12, W * 0.45, z)
    const hookBot = P(L * 0.12, W * 0.45, z - H * 0.22)
    crane = { c0, c1, hookTop, hookBot }
  }

  let mezz = null
  if (props.mezzanine) {
    const z = H * 0.48
    mezz = [P(0, 0, z), P(L * 0.55, 0, z), P(L * 0.55, W, z), P(0, W, z)]
  }

  let stairs = null
  if (props.stairs) {
    const zTop = props.mezzanine ? H * 0.48 : H * 0.42
    const x0 = L * 0.04
    const x1 = L * 0.26
    const y0 = 0
    const y1 = Math.min(W * 0.16, W * 0.5)
    const n = 7
    const treads = []
    const stringerA = []
    const stringerB = []
    for (let i = 0; i <= n; i++) {
      const t = i / n
      const x = x0 + t * (x1 - x0)
      const z = t * zTop
      stringerA.push(P(x, y0, z))
      stringerB.push(P(x, y1, z))
      treads.push({ a: P(x, y0, z), b: P(x, y1, z) })
    }
    const landW = Math.min(L * 0.12, (x1 - x0) * 0.7)
    const landD = y1 * 1.45
    const land = [P(x1, y0, zTop), P(x1 + landW, y0, zTop), P(x1 + landW, landD, zTop), P(x1, landD, zTop)]
    const railH = H * 0.1
    const rail = [
      P(x0, y0, railH * 0.3),
      ...Array.from({ length: n + 1 }, (_, i) => {
        const t = i / n
        return P(x0 + t * (x1 - x0), y0, t * zTop + railH)
      }),
      P(x1 + landW, y0, zTop + railH),
      P(x1 + landW, landD, zTop + railH),
      P(x1, landD, zTop + railH),
    ]
    const posts = [
      { a: P(x0, y0, 0), b: P(x0, y0, railH * 0.3) },
      { a: P(x1, y0, zTop), b: P(x1, y0, zTop + railH) },
      { a: P(x1 + landW, y0, zTop), b: P(x1 + landW, y0, zTop + railH) },
      { a: P(x1 + landW, landD, zTop), b: P(x1 + landW, landD, zTop + railH) },
      { a: P(x1, landD, zTop), b: P(x1, landD, zTop + railH) },
    ]
    stairs = {
      stringerA: pts(stringerA),
      stringerB: pts(stringerB),
      treads,
      land: pts(land),
      rail: pts(rail),
      posts,
    }
  }

  const foundBoxes = []
  const foundPiles = []
  const fz = Math.min(H * 0.13, Math.max(L, W) * 0.03, 1.35)
  const kind = props.foundation || 'pads'
  const addBox = (x0, y0, x1, y1, z0, z1) => {
    foundBoxes.push({
      ...isoBox(P, x0, y0, x1, y1, z0, z1),
      _d: x0 + x1 + y0 + y1,
    })
  }

  if (kind === 'pads') {
    const s = Math.min(2.8, Math.max(1.45, Math.min(L, W) * 0.065))
    const cup = s * 0.52
    for (const x of xs) {
      for (const y of yRows) {
        addBox(x - s / 2, y - s / 2, x + s / 2, y + s / 2, -fz, -fz * 0.22)
        addBox(x - cup / 2, y - cup / 2, x + cup / 2, y + cup / 2, -fz * 0.22, 0)
      }
    }
  } else if (kind === 'strip') {
    const t = Math.min(2.1, Math.max(0.95, Math.min(L, W) * 0.05))
    addBox(-t, W - t, L + t, W + t, -fz, 0)
    addBox(L - t, t, L + t, W - t, -fz, 0)
    addBox(-t, t, t, W - t, -fz, 0)
    addBox(-t, -t, L + t, t, -fz, 0)
  } else if (kind === 'piles') {
    const r = Math.min(0.52, Math.max(0.34, Math.min(L, W) * 0.018))
    const pz = -Math.min(H * 0.4, Math.max(L, W) * 0.08, 2.6)
    const pxs = []
    for (let i = 0; i < xs.length; i++) {
      pxs.push(xs[i])
      if (i < xs.length - 1) pxs.push((xs[i] + xs[i + 1]) / 2)
    }
    const pys = yRows.length > 2 ? yRows : [0, W / 2, W]
    for (const x of pxs) {
      for (const y of pys) {
        foundPiles.push(isoHex(P, x, y, r, pz, 0))
      }
    }
    foundPiles.sort((a, b) => b._d - a._d)
    const bw = Math.min(0.7, Math.max(0.38, Math.min(L, W) * 0.02))
    const rz0 = -fz * 0.12
    const rz1 = fz * 0.08
    for (const y of pys) {
      addBox(-bw, y - bw, L + bw, y + bw, rz0, rz1)
    }
    for (const x of pxs) {
      addBox(x - bw, bw, x + bw, W - bw, rz0, rz1)
    }
  } else if (kind === 'slab') {
    const m = Math.min(1.4, Math.max(0.55, Math.min(L, W) * 0.035))
    addBox(-m, -m, L + m, W + m, -fz * 0.72, 0)
  }
  foundBoxes.sort((a, b) => b._d - a._d)

  const midL = P(L / 2, 0, 0)
  const midW = P(L, W / 2, 0)
  const midH = P(0, 0, H / 2)

  return {
    ground: pts(ground),
    cols,
    eaves,
    portals,
    roof: roof.map((poly) => pts(poly)),
    ridge,
    crane,
    mezz: mezz ? pts(mezz) : null,
    stairs,
    foundBoxes,
    foundPiles,
    labels: {
      L: { ...midL, text: `${fmtM(L)} м` },
      W: { ...midW, text: `${fmtM(W)} м` },
      H: { ...midH, text: `${fmtM(H)} м` },
    },
  }
})

function fmtM(n) {
  return Number.isInteger(n) ? String(n) : n.toFixed(1).replace('.', ',')
}
</script>

<template>
  <svg
    class="sketch"
    :class="{ 'sketch--compact': compact }"
    :viewBox="compact ? '0 0 400 210' : '0 0 400 248'"
    role="img"
    aria-label="Схема каркаса здания"
  >
    <defs>
      <linearGradient id="gnd" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="#ff5a1f" stop-opacity="0.16" />
        <stop offset="100%" stop-color="#ff5a1f" stop-opacity="0.03" />
      </linearGradient>
    </defs>

    <polygon
      v-if="foundation !== 'slab'"
      :points="geo.ground"
      fill="url(#gnd)"
      stroke="rgba(255,90,31,0.35)"
      stroke-width="1.2"
    />

    <g v-if="geo.foundPiles.length" class="found-piles">
      <g v-for="(pile, i) in geo.foundPiles" :key="'pl' + i">
        <polygon
          v-for="(f, j) in pile.faces"
          :key="j"
          :points="f.poly"
          :class="j % 2 ? 'fn-pile-a' : 'fn-pile-b'"
        />
        <polygon :points="pile.top" class="fn-pile-top" />
      </g>
    </g>

    <g v-if="geo.foundBoxes.length" class="found">
      <g v-for="(box, i) in geo.foundBoxes" :key="'fn' + i">
        <polygon :points="box.side" class="fn-side" />
        <polygon :points="box.front" class="fn-front" />
        <polygon :points="box.top" class="fn-top" />
      </g>
    </g>

    <polygon
      v-if="geo.mezz"
      :points="geo.mezz"
      fill="rgba(255,255,255,0.06)"
      stroke="rgba(255,255,255,0.22)"
      stroke-width="1"
      stroke-dasharray="4 3"
    />

    <g stroke="rgba(255,255,255,0.18)" stroke-width="1.15">
      <line
        v-for="(c, i) in geo.cols.filter((c) => c.back)"
        :key="'b' + i"
        :x1="c.x1"
        :y1="c.y1"
        :x2="c.x2"
        :y2="c.y2"
      />
      <line
        v-for="(e, i) in geo.eaves.slice(1)"
        :key="'e' + i"
        :x1="e.a.x"
        :y1="e.a.y"
        :x2="e.b.x"
        :y2="e.b.y"
      />
    </g>

    <g v-if="roof === 'arch'" fill="none" stroke="#ff7d3f" stroke-width="1.6" stroke-linejoin="round">
      <polyline v-for="(p, i) in geo.roof" :key="'a' + i" :points="p" />
    </g>
    <g v-else fill="rgba(255,90,31,0.08)" stroke="#ff7d3f" stroke-width="1.55" stroke-linejoin="round">
      <polygon v-for="(p, i) in geo.roof" :key="'r' + i" :points="p" />
    </g>
    <line
      v-if="geo.ridge"
      :x1="geo.ridge.a.x"
      :y1="geo.ridge.a.y"
      :x2="geo.ridge.b.x"
      :y2="geo.ridge.b.y"
      stroke="#ff5a1f"
      stroke-width="1.8"
    />

    <g v-if="geo.crane" stroke="#35c97e" stroke-width="1.6" fill="none">
      <line :x1="geo.crane.c0.x" :y1="geo.crane.c0.y" :x2="geo.crane.c1.x" :y2="geo.crane.c1.y" />
      <line
        :x1="geo.crane.hookTop.x"
        :y1="geo.crane.hookTop.y"
        :x2="geo.crane.hookBot.x"
        :y2="geo.crane.hookBot.y"
        stroke-dasharray="3 2"
      />
      <circle :cx="geo.crane.hookBot.x" :cy="geo.crane.hookBot.y" r="3.2" fill="#35c97e" stroke="none" />
    </g>

    <g stroke="#f2f4f6" stroke-width="1.7" stroke-linecap="round">
      <line
        v-for="(c, i) in geo.cols.filter((c) => !c.back)"
        :key="'f' + i"
        :x1="c.x1"
        :y1="c.y1"
        :x2="c.x2"
        :y2="c.y2"
      />
      <line
        :x1="geo.eaves[0].a.x"
        :y1="geo.eaves[0].a.y"
        :x2="geo.eaves[0].b.x"
        :y2="geo.eaves[0].b.y"
      />
    </g>

    <g stroke="rgba(255,125,63,0.45)" stroke-width="1">
      <line
        v-for="(p, i) in geo.portals"
        :key="'p' + i"
        :x1="p.a.x"
        :y1="p.a.y"
        :x2="p.b.x"
        :y2="p.b.y"
      />
    </g>

    <g v-if="geo.stairs" fill="none" stroke="#86b6ff" stroke-linejoin="round" stroke-linecap="round">
      <polygon
        :points="geo.stairs.land"
        fill="rgba(134,182,255,0.16)"
        stroke="#86b6ff"
        stroke-width="1.45"
      />
      <polyline :points="geo.stairs.stringerA" stroke-width="1.7" />
      <polyline :points="geo.stairs.stringerB" stroke-width="1.35" opacity="0.7" />
      <line
        v-for="(t, i) in geo.stairs.treads"
        :key="'st' + i"
        :x1="t.a.x"
        :y1="t.a.y"
        :x2="t.b.x"
        :y2="t.b.y"
        stroke-width="1.25"
      />
      <line
        v-for="(p, i) in geo.stairs.posts"
        :key="'sp' + i"
        :x1="p.a.x"
        :y1="p.a.y"
        :x2="p.b.x"
        :y2="p.b.y"
        stroke-width="1.2"
      />
      <polyline :points="geo.stairs.rail" stroke-width="1.45" />
    </g>

    <text class="lbl lbl-l" :x="geo.labels.L.x" :y="geo.labels.L.y + 16" text-anchor="middle">
      {{ geo.labels.L.text }}
    </text>
    <text class="lbl lbl-w" :x="geo.labels.W.x + 14" :y="geo.labels.W.y + 4">
      {{ geo.labels.W.text }}
    </text>
    <text class="lbl lbl-h" :x="geo.labels.H.x - 10" :y="geo.labels.H.y" text-anchor="end">
      {{ geo.labels.H.text }}
    </text>
  </svg>
</template>

<style scoped>
.sketch {
  display: block;
  width: 100%;
  height: auto;
  overflow: visible;
}
.lbl {
  font-family: var(--font-m);
  font-size: 11px;
  fill: var(--acc-hot);
  letter-spacing: 0.02em;
}
.sketch--compact .lbl { font-size: 12.5px; }
.lbl-w { fill: var(--w-soft); }
.lbl-h { fill: var(--w-soft); }
.fn-side { fill: rgba(138, 124, 104, 0.72); stroke: #8a7d6c; stroke-width: 0.7; }
.fn-front { fill: rgba(168, 154, 132, 0.78); stroke: #8a7d6c; stroke-width: 0.7; }
.fn-top { fill: rgba(210, 198, 176, 0.82); stroke: #b0a390; stroke-width: 0.8; }
.fn-pile-a { fill: rgba(92, 86, 78, 0.88); stroke: #6e675e; stroke-width: 0.45; }
.fn-pile-b { fill: rgba(122, 112, 98, 0.9); stroke: #6e675e; stroke-width: 0.45; }
.fn-pile-top { fill: rgba(186, 176, 158, 0.92); stroke: #8a8174; stroke-width: 0.55; }
</style>
