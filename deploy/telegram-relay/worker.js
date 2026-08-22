// Cloudflare Worker: прокладка до api.telegram.org.
// С российского сервера Telegram часто недоступен — этот воркер
// живёт у Cloudflare и просто проксирует запросы бота.
//
// 1) dash.cloudflare.com → Workers → Create → вставить этот файл
// 2) В backend/.env:
//    TELEGRAM_API_BASE=https://<имя>.<аккаунт>.workers.dev

export default {
  async fetch(request) {
    const src = new URL(request.url)
    const target = new URL("https://api.telegram.org" + src.pathname + src.search)
    const headers = new Headers(request.headers)
    headers.delete("host")
    const init = { method: request.method, headers }
    if (request.method !== "GET" && request.method !== "HEAD") {
      init.body = request.body
    }
    return fetch(target, init)
  },
}
