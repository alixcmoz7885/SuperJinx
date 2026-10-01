# Changelog

## v5.0.0
- 🌌 New subscription page, rebuilt from scratch: live usage ring, days left, Persian expiry date, warnings, one-tap import for V2Box / v2rayNG / Hiddify / Streisand / Happ / NekoBox
- 🔳 QR codes are generated inside the page (no external service), sharp and downloadable as PNG
- ⚡ WebSocket early data (`ed=2560`) on all 5 configs: one round trip less per connection, lower ping
- 🎭 Each config has its own path, TLS fingerprint and name
- 🧲 Users created in the panel without a group get the 5 configs automatically
- 🩺 Docker health check for nginx and panel

## v4.0.0
- 👑 Fixed owner login `admin / admin`, re-applied on every boot
- 🤝 Reseller role and a ready reseller account with 50 GB quota
- 🔌 Port fixed to 8080

## v3.0.0
- 5 × VLESS + WS + TLS configs with `alpn=http/1.1` and `fp=chrome`
- Ready-made sales templates

## v2.0.0
- Owner account created in the database (env admins are blocked in production)

## v1.0.0
- First release: PasarGuard + Xray + nginx in one Railway service
