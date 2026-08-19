const SITE_URL = 'https://greydstroy.ru'

const DEFAULT_META = {
  title: 'Грэйдстрой — изготовление металлоконструкций на заказ | Резка, гибка, сварка',
  description:
    'Изготовление металлоконструкций на заказ: от одной детали до объекта под ключ. Лазерная и плазменная резка, гибка, сварка на собственном производстве. Расчёт за 1 рабочий день, отгрузка по всей России.',
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
  const url = SITE_URL + route.path

  document.title = title
  setTag('meta[name="description"]', { name: 'description', content: description })
  setTag('link[rel="canonical"]', { rel: 'canonical', href: url })
  setTag('meta[property="og:title"]', { property: 'og:title', content: title })
  setTag('meta[property="og:description"]', { property: 'og:description', content: description })
  setTag('meta[property="og:url"]', { property: 'og:url', content: url })

  const robots = route.meta?.noindex ? 'noindex, nofollow' : 'index, follow'
  setTag('meta[name="robots"]', { name: 'robots', content: robots })
}
