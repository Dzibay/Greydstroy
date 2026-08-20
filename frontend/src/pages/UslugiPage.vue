<script setup>
import { ref, computed } from 'vue'

/* ---------- интерактивный подбор технологии ---------- */
const materials = [
  { id: 'steel', label: 'Сталь', laserMax: 16, plasmaMax: 25, gasMax: 70 },
  { id: 'stainless', label: 'Нержавейка', laserMax: 12, plasmaMax: 25, gasMax: 0 },
  { id: 'aluminum', label: 'Алюминий', laserMax: 8, plasmaMax: 25, gasMax: 0 },
]
const SCALE_MAX = 70

const material = ref(materials[0])
const thickness = ref(6)

const verdict = computed(() => {
  const t = Number(thickness.value)
  const m = material.value
  if (t <= m.laserMax) {
    return {
      tech: 'Лазерная резка',
      tag: 'laser',
      spec: `${m.label.toLowerCase()} до ${m.laserMax} мм · чистая кромка · ЧПУ`,
      note:
        t <= 6
          ? 'Кромка без зачистки, деталь идёт сразу в сборку. Бонус: на этой толщине доступна гибка на листогибе — согнём в той же партии.'
          : 'Чистый рез без окалины. Деталь встаёт в узел без доработки напильником.',
    }
  }
  if (t <= m.plasmaMax) {
    return {
      tech: 'Плазменная резка',
      tag: 'plasma',
      spec: `${m.label.toLowerCase()} до ${m.plasmaMax} мм · большие форматы`,
      note: 'На этой толщине лазеру работать уже невыгодно, а плазме — самое то. Кромка без «доп. зачистки», о которой вы не договаривались.',
    }
  }
  if (m.gasMax && t <= m.gasMax) {
    return {
      tech: 'Газовая резка',
      tag: 'gas',
      spec: `${m.label.toLowerCase()} до ${m.gasMax} мм · сверхтолстый лист`,
      note: 'Плазма здесь уже не берёт. Кислородная резка — рабочий способ для толстой чёрной стали под сварку.',
    }
  }
  return {
    tech: 'Нужен расчёт технолога',
    tag: 'custom',
    spec: m.gasMax
      ? `${m.label.toLowerCase()} свыше ${m.gasMax} мм`
      : `${m.label.toLowerCase()} свыше ${m.plasmaMax} мм`,
    note: 'Толщина за пределами типовых режимов. Пришлите чертёж — технолог подберёт способ и посчитает стоимость в течение рабочего дня.',
  }
})

const pct = (v) => `${Math.min((v / SCALE_MAX) * 100, 100)}%`
const needlePos = computed(
  () => `calc(var(--lw) + (100% - var(--lw)) * ${Math.min(thickness.value / SCALE_MAX, 1)})`
)

/* ---------- услуги (аккордеон) ---------- */
const services = [
  {
    title: 'Лазерная резка металла',
    slug: 'lazernaya-rezka',
    chips: ['до 16 мм', 'ЧПУ', 'DXF / DWG'],
    lead: 'Сложный контур сегодня — деталь для сборки без доработки напильником.',
    points: [
      'Чистая кромка без окалины — деталь идёт сразу в сборку или на покраску',
      'Точность реза, одинаковая у детали №1 и детали №100 из партии',
      'Отверстия, пазы, гравировка маркировки — за один установ',
      'Работаем по вашим DXF / DWG или отрисуем макет по эскизу',
    ],
    fit: 'Детали под сборку · серийные партии · сложный контур',
    icon: 'laser',
  },
  {
    title: 'Плазменная резка металла',
    slug: 'plazmennaya-rezka',
    chips: ['до 25 мм', 'чёрный металл', 'большие форматы'],
    lead: 'Толстый лист и большие объёмы — там, где лазеру работать уже невыгодно.',
    points: [
      'Раскрой листа до 25 мм — фланцы, косынки, закладные, основания',
      'Экономичнее лазера на толщинах от 16 мм — не переплачиваете за технологию',
      'Кромка под сварку без дополнительной механической обработки',
      'Крупногабаритный раскрой для металлоконструкций',
    ],
    fit: 'Толстый лист · фланцы и закладные · крупный раскрой',
    icon: 'plasma',
  },
  {
    title: 'Газовая резка металла',
    slug: 'gazovaya-rezka',
    chips: ['до 70 мм', 'чёрная сталь', 'сверхтолстый лист'],
    lead: 'Сверхтолстая сталь — там, где лазер и плазма уже не берут.',
    points: [
      'Раскрой чёрной стали до 70 мм — плиты, закладные, основания',
      'Рабочий способ на толщинах свыше 25 мм — без переплаты за чужую технологию',
      'Кромка под сварку металлоконструкций',
      'Крупногабаритный раскрой тяжёлых элементов',
    ],
    fit: 'Плиты и основания · толстые фланцы · закладные',
    icon: 'gas',
  },
  {
    title: 'Гибка на листогибе с ЧПУ',
    slug: 'gibka-metalla',
    chips: ['до 6 мм', 'до 3000 мм', 'повторяемость'],
    lead: 'Деталь №50 гнётся под тем же углом, что и деталь №1.',
    points: [
      'ЧПУ-контроль угла — без «подгонки по месту» на объекте',
      'Длина гиба до 3000 мм — короба, кожухи, лотки, профили',
      'Гибка сразу после резки: одна площадка, одна партия, один срок',
      'Сложные многогибочные детали по чертежу или образцу',
    ],
    fit: 'Короба и кожухи · лотки · панели · нестандартный профиль',
    icon: 'bend',
  },
  {
    title: 'Сварка металлоконструкций',
    slug: 'svarka',
    chips: ['MIG/MAG', 'TIG', 'РДС'],
    lead: 'От одного шва до объекта под ключ — в Нижегородской области с монтажом.',
    points: [
      'Сварка узлов и металлоконструкций по КМ / КМД',
      'Паспорт на каждое изделие — швы проверяются перед отгрузкой',
      'Сборка конструкции целиком: резка, гибка и сварка на одной площадке',
      'Монтаж на объекте по Нижегородской области — по договорённости',
    ],
    fit: 'Каркасы и фермы · ёмкости · нестандартные узлы · под ключ',
    icon: 'weld',
  },
]

const openService = ref(0)
const toggleService = (i) => {
  openService.value = openService.value === i ? -1 : i
}

/* ---------- FAQ ---------- */
const faq = [
  {
    q: 'Какую толщину металла вы режете?',
    a: 'Лазером — сталь до 16 мм, нержавейку до 12 мм, алюминий до 8 мм. Плазмой — до 25 мм. Газовой резкой — чёрную сталь до 70 мм. Если толщина больше — пришлите чертёж, технолог предложит способ.',
  },
  {
    q: 'Лазер, плазма или газ — что выбрать?',
    a: 'До 16 мм по стали выгоднее лазер: чище кромка, точнее контур. От 16 до 25 мм — плазма: тот же результат для сварных конструкций, но дешевле. Свыше 25 мм по чёрной стали — газовая резка до 70 мм. Если сомневаетесь — посчитаем варианты, сравните цифры.',
  },
  {
    q: 'В каком виде прислать чертёж?',
    a: 'Идеально — DXF или DWG. Подойдут PDF, фото эскиза от руки с размерами или просто образец детали. Макет для резки подготовим сами.',
  },
  {
    q: 'Возьмёте заказ на одну деталь?',
    a: 'Да. Работаем от одной детали до серийной партии — цена за штуку при серии будет ниже за счёт раскроя.',
  },
  {
    q: 'Сколько стоит резка металла?',
    a: 'Зависит от толщины, длины реза и материала — универсального прайса честнее не обещать. Пришлите чертёж — расчёт стоимости и сроков будет у вас в течение рабочего дня.',
  },
]

const openFaq = ref(-1)
const toggleFaq = (i) => {
  openFaq.value = openFaq.value === i ? -1 : i
}
</script>

<template>
  <main>
    <!-- ============ HERO ============ -->
    <section id="uslugi-hero" class="sec sec--dark page-hero usl-hero">
      <div class="usl-hero-ghost" aria-hidden="true">УСЛУГИ</div>
      <div class="container">
        <RouterLink to="/" class="page-back" v-reveal>← На главную</RouterLink>
        <div class="sec-head" v-reveal="60">
          <p class="sec-tag"><span class="idx">Производство</span> Услуги</p>
          <h1 class="page-title">Резка, гибка и сварка металла — <em>на одной площадке</em></h1>
          <p class="page-desc">
            Услуги металлообработки для
            <RouterLink to="/metallokonstruktsii" class="page-desc-link">изготовления металлоконструкций</RouterLink>:
            лазерная, плазменная и газовая резка, гибка на ЧПУ-листогибе, сварка. Один договор, один
            контакт, одна ответственность — от чертежа до отгрузки по всей России.
          </p>
        </div>

        <div class="usl-anchor-row" v-reveal="140">
          <RouterLink
            v-for="(s, i) in services"
            :key="s.title"
            :to="`/uslugi/${s.slug}`"
            class="usl-anchor"
          >
            <span class="ua-num">{{ String(i + 1).padStart(2, '0') }}</span>
            {{ s.title.replace(' металла', '').replace(' металлоконструкций', '') }}
          </RouterLink>
        </div>
      </div>
    </section>

    <!-- ============ ПОДБОР ТЕХНОЛОГИИ ============ -->
    <section id="tech-picker" class="sec sec--deep usl-picker-sec">
      <div class="container">
        <div class="sec-head" v-reveal>
          <p class="sec-tag">Подбор технологии</p>
          <h2 class="sec-title">Какой рез нужен <em>вашей детали</em></h2>
          <p class="sec-sub">
            Выберите материал и толщину — покажем, какая технология подойдёт
            и почему. Это те же правила, по которым считает наш технолог.
          </p>
        </div>

        <div class="picker card" v-reveal="100">
          <div class="picker-controls">
            <div class="picker-block">
              <p class="picker-label">Материал</p>
              <div class="mat-row">
                <button
                  v-for="m in materials"
                  :key="m.id"
                  class="mat-btn"
                  :class="{ active: material.id === m.id }"
                  @click="material = m"
                >
                  {{ m.label }}
                </button>
              </div>
            </div>

            <div class="picker-block">
              <p class="picker-label">
                Толщина
                <span class="picker-value">{{ thickness }} мм</span>
              </p>
              <input
                v-model.number="thickness"
                type="range"
                min="1"
                :max="SCALE_MAX"
                step="1"
                class="thick-slider"
                aria-label="Толщина металла в миллиметрах"
              />
            </div>
          </div>

          <!-- шкала диапазонов -->
          <div class="scale" aria-hidden="true">
            <div class="scale-row">
              <span class="scale-name">Лазер</span>
              <div class="scale-track">
                <div
                  class="scale-bar scale-bar--laser"
                  :class="{ dim: verdict.tag !== 'laser' }"
                  :style="{ width: pct(material.laserMax) }"
                ></div>
              </div>
            </div>
            <div class="scale-row">
              <span class="scale-name">Плазма</span>
              <div class="scale-track">
                <div
                  class="scale-bar scale-bar--plasma"
                  :class="{ dim: verdict.tag !== 'plasma' }"
                  :style="{ width: pct(material.plasmaMax) }"
                ></div>
              </div>
            </div>
            <div class="scale-row" v-if="material.gasMax">
              <span class="scale-name">Газ</span>
              <div class="scale-track">
                <div
                  class="scale-bar scale-bar--gas"
                  :class="{ dim: verdict.tag !== 'gas' }"
                  :style="{ width: pct(material.gasMax) }"
                ></div>
              </div>
            </div>
            <div class="scale-needle" :style="{ left: needlePos }">
              <span class="needle-tip">{{ thickness }}</span>
            </div>
            <div class="scale-ticks">
              <span v-for="t in [0, 10, 20, 30, 40, 50, 60, 70]" :key="t">{{ t }}</span>
            </div>
          </div>

          <!-- вердикт -->
          <div class="verdict" :class="'verdict--' + verdict.tag">
            <div class="verdict-head">
              <span class="verdict-dot"></span>
              <p class="verdict-tech">{{ verdict.tech }}</p>
              <p class="verdict-spec">{{ verdict.spec }}</p>
            </div>
            <p class="verdict-note">{{ verdict.note }}</p>
            <RouterLink to="/kalkulyator" class="btn verdict-btn">Рассчитать мою деталь</RouterLink>
          </div>
        </div>
      </div>
    </section>

    <!-- ============ УСЛУГИ (АККОРДЕОН) ============ -->
    <section id="uslugi-list" class="sec sec--light">
      <div class="container">
        <div class="sec-head" v-reveal>
          <p class="sec-tag"><span class="idx">Подробно</span> Пять участков</p>
          <h2 class="sec-title">Один подрядчик <em>вместо трёх</em></h2>
          <p class="sec-sub">
            Пока деталь пересылают между цехом резки, гибочным участком и сварочным постом —
            время теряется на каждой пересылке. У нас всё происходит на одной площадке.
          </p>
        </div>

        <div class="acc">
          <article
            v-for="(s, i) in services"
            :key="s.title"
            class="acc-item"
            :class="{ open: openService === i }"
            v-reveal="i * 70"
          >
            <button class="acc-head" @click="toggleService(i)" :aria-expanded="openService === i">
              <span class="acc-num">{{ String(i + 1).padStart(2, '0') }}</span>
              <span class="acc-title">{{ s.title }}</span>
              <span class="acc-chips">
                <span v-for="c in s.chips" :key="c" class="chip">{{ c }}</span>
              </span>
              <span class="acc-x" aria-hidden="true"></span>
            </button>

            <div class="acc-body">
              <div class="acc-body-in">
                <p class="acc-lead">{{ s.lead }}</p>
                <ul class="acc-points">
                  <li v-for="p in s.points" :key="p">{{ p }}</li>
                </ul>
                <div class="acc-foot">
                  <p class="acc-fit"><span>Подходит для:</span> {{ s.fit }}</p>
                  <div class="acc-actions">
                    <RouterLink :to="`/uslugi/${s.slug}`" class="acc-more">Подробнее об услуге →</RouterLink>
                    <RouterLink to="/kalkulyator" class="btn btn--ghost acc-btn">Рассчитать</RouterLink>
                  </div>
                </div>
              </div>
            </div>
          </article>
        </div>
      </div>
    </section>

    <!-- ============ FAQ ============ -->
    <section id="uslugi-faq" class="sec sec--dark">
      <div class="container">
        <div class="sec-head" v-reveal>
          <p class="sec-tag"><span class="idx">Вопросы</span> FAQ</p>
          <h2 class="sec-title">Что спрашивают <em>перед заказом</em></h2>
        </div>

        <div class="faq">
          <div
            v-for="(f, i) in faq"
            :key="f.q"
            class="faq-item"
            :class="{ open: openFaq === i }"
            v-reveal="i * 60"
          >
            <button class="faq-q" @click="toggleFaq(i)" :aria-expanded="openFaq === i">
              {{ f.q }}
              <span class="acc-x" aria-hidden="true"></span>
            </button>
            <div class="faq-a">
              <p>{{ f.a }}</p>
            </div>
          </div>
        </div>

        <div class="usl-cta" v-reveal="120">
          <div>
            <p class="usl-cta-title">Не нашли свой случай?</p>
            <p class="usl-cta-text">
              Пришлите чертёж или опишите задачу словами — технолог посчитает
              и ответит в течение рабочего дня.
            </p>
          </div>
          <RouterLink to="/kalkulyator" class="btn">Рассчитать стоимость и сроки</RouterLink>
        </div>
      </div>
    </section>
  </main>
</template>

<style scoped>
/* ============ hero ============ */
.usl-hero { padding-bottom: 72px; }

.page-desc-link {
  color: var(--acc-hot);
  text-decoration: underline;
  text-underline-offset: 3px;
}
.page-desc-link:hover { color: var(--acc); }

.usl-hero-ghost {
  position: absolute;
  top: 40px;
  right: -30px;
  font-family: var(--font-d);
  font-size: clamp(120px, 18vw, 260px);
  font-weight: 900;
  line-height: 1;
  color: transparent;
  -webkit-text-stroke: 1px rgba(255, 255, 255, 0.05);
  pointer-events: none;
  user-select: none;
}

.usl-anchor-row {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}
.usl-anchor {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 12px 20px;
  border: 1px solid var(--line-d);
  border-radius: var(--r-sm);
  font-size: 14px;
  font-weight: 600;
  color: var(--w-soft);
  transition: border-color 0.25s, color 0.25s, transform 0.25s var(--ease);
}
.usl-anchor:hover {
  border-color: var(--acc);
  color: var(--white);
  transform: translateY(-2px);
}
.ua-num {
  font-family: var(--font-m);
  font-size: 11px;
  color: var(--acc);
}

/* ============ подбор технологии ============ */
.usl-picker-sec { padding-top: 96px; }

.picker {
  padding: 38px 36px 42px;
  cursor: default;
}
.picker:hover { transform: none; }

.picker-controls {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 48px;
  align-items: end;
  margin-bottom: 40px;
}

.picker-label {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 16px;
  font-family: var(--font-m);
  font-size: 12px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--w-faint);
  margin-bottom: 14px;
}
.picker-value {
  font-size: 18px;
  font-weight: 600;
  letter-spacing: 0;
  color: var(--acc-hot);
}

.mat-row { display: flex; gap: 8px; }
.mat-btn {
  padding: 11px 20px;
  background: transparent;
  border: 1px solid var(--line-d);
  border-radius: var(--r-sm);
  color: var(--w-soft);
  font-size: 14px;
  font-weight: 600;
  transition: all 0.25s;
}
.mat-btn:hover { border-color: rgba(255, 90, 31, 0.5); color: var(--white); }
.mat-btn.active {
  background: var(--acc);
  border-color: var(--acc);
  color: #fff;
}

.thick-slider {
  width: 100%;
  height: 4px;
  appearance: none;
  -webkit-appearance: none;
  background: rgba(255, 255, 255, 0.12);
  border-radius: 2px;
  outline: none;
  cursor: pointer;
}
.thick-slider::-webkit-slider-thumb {
  appearance: none;
  -webkit-appearance: none;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: var(--acc);
  border: 3px solid var(--bg0);
  box-shadow: 0 0 0 1.5px var(--acc), 0 0 22px rgba(255, 90, 31, 0.55);
  transition: transform 0.2s;
}
.thick-slider::-webkit-slider-thumb:hover { transform: scale(1.15); }
.thick-slider::-moz-range-thumb {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: var(--acc);
  border: 3px solid var(--bg0);
  box-shadow: 0 0 0 1.5px var(--acc), 0 0 22px rgba(255, 90, 31, 0.55);
}

/* шкала */
.scale {
  --lw: 92px; /* ширина колонки подписей + gap */
  position: relative;
  padding-bottom: 26px;
  margin-bottom: 34px;
}
.scale-row {
  display: grid;
  grid-template-columns: 76px 1fr;
  align-items: center;
  gap: 16px;
  margin-bottom: 10px;
}
.scale-name {
  font-family: var(--font-m);
  font-size: 11.5px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--w-faint);
}
.scale-track {
  height: 14px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 4px;
  overflow: hidden;
}
.scale-bar {
  height: 100%;
  border-radius: 4px;
  transition: width 0.5s var(--ease), opacity 0.35s;
}
.scale-bar--laser { background: linear-gradient(90deg, #ff7d3f, #ff5a1f); }
.scale-bar--plasma { background: linear-gradient(90deg, #4f8dff, #2f6bdb); }
.scale-bar--gas { background: linear-gradient(90deg, #3dd68c, #1fa968); }
.scale-bar.dim { opacity: 0.28; }

.scale-needle {
  position: absolute;
  top: -8px;
  bottom: 18px;
  width: 2px;
  background: var(--white);
  transition: left 0.15s linear;
  pointer-events: none;
}
.needle-tip {
  position: absolute;
  top: -22px;
  left: 50%;
  transform: translateX(-50%);
  font-family: var(--font-m);
  font-size: 11px;
  color: var(--white);
  background: rgba(255, 255, 255, 0.1);
  padding: 1px 7px;
  border-radius: 4px;
  white-space: nowrap;
}
.scale-ticks {
  display: flex;
  justify-content: space-between;
  margin-left: var(--lw);
  margin-top: 4px;
  font-family: var(--font-m);
  font-size: 10.5px;
  color: var(--w-faint);
}

/* вердикт */
.verdict {
  border: 1px solid var(--line-d);
  border-left: 3px solid var(--acc);
  border-radius: var(--r-sm);
  padding: 26px 28px;
  background: rgba(255, 90, 31, 0.04);
  transition: border-color 0.35s, background 0.35s;
}
.verdict--plasma {
  border-left-color: #4f8dff;
  background: rgba(79, 141, 255, 0.05);
}
.verdict--gas {
  border-left-color: #3dd68c;
  background: rgba(61, 214, 140, 0.05);
}
.verdict--custom {
  border-left-color: var(--w-faint);
  background: rgba(255, 255, 255, 0.03);
}

.verdict-head {
  display: flex;
  align-items: baseline;
  gap: 14px;
  flex-wrap: wrap;
  margin-bottom: 10px;
}
.verdict-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--acc);
  align-self: center;
  box-shadow: 0 0 14px rgba(255, 90, 31, 0.7);
  animation: pulse 2s infinite;
}
.verdict--plasma .verdict-dot { background: #4f8dff; box-shadow: 0 0 14px rgba(79, 141, 255, 0.7); }
.verdict--gas .verdict-dot { background: #3dd68c; box-shadow: 0 0 14px rgba(61, 214, 140, 0.7); }
.verdict--custom .verdict-dot { background: var(--w-faint); box-shadow: none; animation: none; }

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.25); }
}

.verdict-tech {
  font-family: var(--font-d);
  font-size: 19px;
  font-weight: 700;
  text-transform: uppercase;
}
.verdict-spec {
  font-family: var(--font-m);
  font-size: 12px;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--w-faint);
}
.verdict-note {
  font-size: 14.5px;
  color: var(--w-soft);
  max-width: 640px;
  margin-bottom: 20px;
}

/* ============ аккордеон услуг ============ */
.acc { border-top: 1px solid var(--line-l); }

.acc-item { border-bottom: 1px solid var(--line-l); }

.acc-head {
  display: grid;
  grid-template-columns: 56px 1fr auto 40px;
  align-items: center;
  gap: 20px;
  width: 100%;
  padding: 26px 8px;
  background: none;
  border: none;
  text-align: left;
  color: var(--ink);
  transition: padding 0.3s var(--ease);
}
.acc-item:hover .acc-head { padding-left: 16px; }

.acc-num {
  font-family: var(--font-d);
  font-size: 20px;
  font-weight: 900;
  color: transparent;
  -webkit-text-stroke: 1.2px rgba(18, 22, 27, 0.3);
  transition: -webkit-text-stroke-color 0.3s;
}
.acc-item.open .acc-num,
.acc-item:hover .acc-num { -webkit-text-stroke-color: var(--acc); }

.acc-title {
  font-family: var(--font-d);
  font-size: clamp(15px, 2vw, 20px);
  font-weight: 700;
  text-transform: uppercase;
  line-height: 1.25;
}

.acc-chips { display: flex; gap: 8px; flex-wrap: wrap; }
.chip {
  font-family: var(--font-m);
  font-size: 11px;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--ink-soft);
  border: 1px solid var(--line-l);
  border-radius: 4px;
  padding: 4px 10px;
  white-space: nowrap;
}
.acc-item.open .chip { border-color: rgba(255, 90, 31, 0.45); color: var(--acc); }

.acc-x {
  position: relative;
  width: 26px;
  height: 26px;
  flex-shrink: 0;
  justify-self: end;
}
.acc-x::before,
.acc-x::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 16px;
  height: 2px;
  background: currentColor;
  transform: translate(-50%, -50%);
  transition: transform 0.35s var(--ease);
}
.acc-x::after { transform: translate(-50%, -50%) rotate(90deg); }
.acc-item.open .acc-x::after,
.faq-item.open .acc-x::after { transform: translate(-50%, -50%) rotate(0deg); }

.acc-body {
  display: grid;
  grid-template-rows: 0fr;
  transition: grid-template-rows 0.5s var(--ease);
}
.acc-item.open .acc-body { grid-template-rows: 1fr; }
.acc-body-in {
  overflow: hidden;
  padding-left: 76px;
  padding-right: 8px;
}
.acc-item.open .acc-body-in { padding-bottom: 34px; }

.acc-lead {
  font-size: 16.5px;
  font-weight: 600;
  color: var(--ink);
  margin-bottom: 18px;
  max-width: 620px;
}

.acc-points {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px 32px;
  max-width: 860px;
  margin-bottom: 22px;
}
.acc-points li {
  position: relative;
  padding-left: 22px;
  font-size: 14.5px;
  color: var(--ink-soft);
}
.acc-points li::before {
  content: '◆';
  position: absolute;
  left: 0;
  top: 1px;
  font-size: 10px;
  color: var(--acc);
}

.acc-foot {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  flex-wrap: wrap;
}
.acc-fit {
  font-family: var(--font-m);
  font-size: 12px;
  letter-spacing: 0.05em;
  color: var(--ink-faint);
}
.acc-fit span { color: var(--acc); text-transform: uppercase; }
.acc-actions {
  display: flex;
  align-items: center;
  gap: 22px;
  flex-wrap: wrap;
}
.acc-more {
  font-size: 14.5px;
  font-weight: 700;
  color: var(--acc);
  transition: color 0.2s;
}
.acc-more:hover { color: var(--acc-hot); }
.acc-btn { padding: 13px 26px; }

/* ============ FAQ ============ */
.faq {
  max-width: 860px;
  border-top: 1px solid var(--line-d);
  margin-bottom: 64px;
}
.faq-item { border-bottom: 1px solid var(--line-d); }

.faq-q {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  width: 100%;
  padding: 22px 4px;
  background: none;
  border: none;
  text-align: left;
  color: var(--white);
  font-size: 16px;
  font-weight: 600;
  transition: color 0.25s;
}
.faq-q:hover { color: var(--acc-hot); }

.faq-a {
  display: grid;
  grid-template-rows: 0fr;
  transition: grid-template-rows 0.45s var(--ease);
}
.faq-item.open .faq-a { grid-template-rows: 1fr; }
.faq-a p {
  overflow: hidden;
  font-size: 14.5px;
  color: var(--w-soft);
  max-width: 720px;
}
.faq-item.open .faq-a p { padding-bottom: 24px; }

/* ============ CTA ============ */
.usl-cta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 28px;
  flex-wrap: wrap;
  padding: 36px 40px;
  border-radius: var(--r);
  border: 1px solid rgba(255, 90, 31, 0.35);
  background:
    radial-gradient(ellipse at top left, rgba(255, 90, 31, 0.14), transparent 55%),
    var(--card-d);
}
.usl-cta-title {
  font-family: var(--font-d);
  font-size: 20px;
  font-weight: 700;
  text-transform: uppercase;
  margin-bottom: 8px;
}
.usl-cta-text { font-size: 14.5px; color: var(--w-soft); max-width: 520px; }

/* ============ адаптив ============ */
@media (max-width: 900px) {
  .picker-controls { grid-template-columns: 1fr; gap: 28px; }
  .acc-head { grid-template-columns: 40px 1fr 32px; }
  .acc-chips { display: none; }
  .acc-x { grid-column: 3; }
  .acc-body-in { padding-left: 60px; }
  .acc-points { grid-template-columns: 1fr; }
}

@media (max-width: 640px) {
  .picker { padding: 26px 20px 30px; }
  .scale { --lw: 70px; }
  .scale-row { grid-template-columns: 60px 1fr; gap: 10px; }
  .acc-body-in { padding-left: 0; }
  .usl-cta { padding: 28px 22px; }
  .usl-hero-ghost { display: none; }
}
</style>
