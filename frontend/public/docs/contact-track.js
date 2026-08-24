/** Клики по телефону и почте на статичных страницах /docs. */
(function () {
  var ENDPOINT = '/api/t'
  var VISITOR_KEY = 'gs_vid'
  var SESSION_KEY = 'gs_sid'

  function uid() {
    if (typeof crypto !== 'undefined' && crypto.randomUUID) return crypto.randomUUID()
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
      var r = (Math.random() * 16) | 0
      return (c === 'x' ? r : (r & 0x3) | 0x8).toString(16)
    })
  }

  function read(key, store) {
    try {
      return store.getItem(key) || ''
    } catch (e) {
      return ''
    }
  }

  function write(key, value, store) {
    try {
      store.setItem(key, value)
    } catch (e) { /* ignore */ }
  }

  function visitorId() {
    var id = read(VISITOR_KEY, localStorage)
    if (!id) {
      id = uid()
      write(VISITOR_KEY, id, localStorage)
    }
    return id
  }

  function sessionId() {
    var id = read(SESSION_KEY, sessionStorage)
    if (!id) {
      id = uid()
      write(SESSION_KEY, id, sessionStorage)
    }
    return id
  }

  function device() {
    var w = window.innerWidth
    if (w < 768) return 'mobile'
    if (w < 1024) return 'tablet'
    return 'desktop'
  }

  document.addEventListener('click', function (e) {
    var el = e.target && e.target.closest ? e.target.closest('a') : null
    if (!el) return
    var href = (el.getAttribute('href') || '').trim()
    var event = href.indexOf('tel:') === 0 ? 'tel' : href.indexOf('mailto:') === 0 ? 'mail' : ''
    if (!event) return
    var body = JSON.stringify({
      events: [{
        event: event,
        t: Date.now(),
        visitor_id: visitorId(),
        session_id: sessionId(),
        path: location.pathname,
        title: (document.title || '').slice(0, 160),
        label: (el.getAttribute('data-track') || '').slice(0, 120),
        href: href.slice(0, 400),
        props: event === 'mail' ? { provider: 'mailto' } : {},
        device: device(),
        viewport_w: window.innerWidth,
      }],
    })
    try {
      if (typeof navigator.sendBeacon === 'function') {
        navigator.sendBeacon(ENDPOINT, new Blob([body], { type: 'application/json' }))
        return
      }
    } catch (err) { /* fallthrough */ }
    fetch(ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: body,
      keepalive: true,
    }).catch(function () { /* ignore */ })
  }, true)
})()
