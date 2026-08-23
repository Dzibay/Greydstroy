const SITE_URL = 'https://greydstroy.ru'
const DEFAULT_IMAGE = `${SITE_URL}/img/hero-laser.png`

const DEFAULT_META = {
  title: 'Грэйдстрой — изготовление металлоконструкций на заказ | Резка, гибка, сварка',
  description:
    'Изготовление металлоконструкций на заказ: от одной детали до объекта под ключ. Лазерная, плазменная и газовая резка, гибка, сварка на собственном производстве. Расчёт за 1 рабочий день, отгрузка по всей России.',
}

function setTag(selector, attrs) {
  let el = document.head.querySelector(selector)
  if (!el) {
    el = document.createElement(attrs.rel ? 'link' : 'meta')
    document.head.appendChild(el)
  }
  Object.entries(attrs).forEach(([name, value]) => el.setAttribute(name, value))
}

export function applyPageMeta(route) {
  const title = route.meta?.title || DEFAULT_META.title
  const description = route.meta?.description || DEFAULT_META.description
  const noindex = !!route.meta?.noindex
  const url = noindex ? `${SITE_URL}/` : SITE_URL + route.path
  const image = route.meta?.image || DEFAULT_IMAGE

  document.title = title
  setTag('meta[name="description"]', { name: 'description', content: description })
  setTag('link[rel="canonical"]', { rel: 'canonical', href: url })

  setTag('meta[property="og:title"]', { property: 'og:title', content: title })
  setTag('meta[property="og:description"]', { property: 'og:description', content: description })
  setTag('meta[property="og:url"]', { property: 'og:url', content: url })
  setTag('meta[property="og:image"]', { property: 'og:image', content: image })

  setTag('meta[name="twitter:title"]', { name: 'twitter:title', content: title })
  setTag('meta[name="twitter:description"]', { name: 'twitter:description', content: description })
  setTag('meta[name="twitter:image"]', { name: 'twitter:image', content: image })

  const robots = noindex ? 'noindex, nofollow' : 'index, follow'
  setTag('meta[name="robots"]', { name: 'robots', content: robots })
}
