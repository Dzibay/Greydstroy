/** Живые кадры цеха и объектов. Чужие логотипы и бетон «не наш профиль» не включаем. */

export const shop = {
  hangarFrame: {
    src: '/img/shop/shop-02.jpg',
    alt: 'Каркас ангара из металлоконструкций: колонны и стропильные фермы',
  },
  hangarInside: {
    src: '/img/shop/shop-04.jpg',
    alt: 'Внутри каркаса склада: фермы покрытия и колонны',
  },
  warehouseWinter: {
    src: '/img/shop/shop-11.jpg',
    alt: 'Склад из сэндвич-панелей на металлическом каркасе зимой',
  },
  canopy: {
    src: '/img/shop/shop-28.jpg',
    alt: 'Монтаж навеса из металлоконструкций на объекте',
  },
  canopyWork: {
    src: '/img/shop/shop-29.jpg',
    alt: 'Навес из металлоконструкций в сборке: колонны, прогоны, профнастил',
  },
  platforms: {
    src: '/img/shop/shop-10.jpg',
    alt: 'Площадки обслуживания и лестница с ограждением на объекте',
  },
  stairs: {
    src: '/img/shop/shop-13.jpg',
    alt: 'Металлическая лестница и площадка в промышленном помещении',
  },
  columnsPainted: {
    src: '/img/shop/shop-31.jpg',
    alt: 'Колонны с опорными пластинами после грунта в цехе Грэйдстрой',
  },
  cncTable: {
    src: '/img/shop/shop-33.jpg',
    alt: 'ЧПУ-плазма режет отверстия в стальном листе',
  },
  cncConsole: {
    src: '/img/shop/shop-34.jpg',
    alt: 'Пульт станка плазменной резки в цехе Грэйдстрой',
  },
  cncHead: {
    src: '/img/shop/shop-37.jpg',
    alt: 'Резак плазмы над листом: отверстия под закладные и фланцы',
  },
  tankNode: {
    src: '/img/shop/shop-14.jpg',
    alt: 'Нестандартный металлический узел: ёмкость и обвязка',
  },
  montageCrew: {
    src: '/img/shop/shop-08.jpg',
    alt: 'Монтаж металлических узлов на объекте',
  },
}

export const homeGallery = [
  shop.hangarFrame,
  shop.cncHead,
  shop.columnsPainted,
  shop.canopy,
  shop.platforms,
  shop.hangarInside,
]

export const shopGallery = [
  shop.cncTable,
  shop.cncConsole,
  shop.cncHead,
  shop.columnsPainted,
]

export const montageGallery = [
  shop.hangarFrame,
  shop.canopy,
  shop.platforms,
  shop.montageCrew,
]

export const izgotovlenieGallery = [
  shop.columnsPainted,
  shop.cncTable,
  shop.hangarInside,
  shop.tankNode,
]
