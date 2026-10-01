"""Super JinX bootstrap: zero-touch setup for PasarGuard on Railway. Idempotent: safe on every boot."""
import json, os, sys, time, urllib.error, urllib.parse, urllib.request

BASE = "http://127.0.0.1:8000"
DATA = "/var/lib/pasarguard"
DOMAIN = (os.getenv("PUBLIC_DOMAIN") or os.getenv("RAILWAY_PUBLIC_DOMAIN") or "").strip()
import subprocess
USER, PASS = "admin", "admin"          # fixed on purpose, re-applied on every boot
RESELLER_USER, RESELLER_PASS, RESELLER_GB = "reseller", "reseller", 50
CORE_NAME, NODE_NAME, GROUP_NAME = "JinX-Core", "JinX-Core", "jinx-all"
TITLE = os.getenv("CONFIG_TITLE", "جینکس")
GB = 1024 ** 3
DAY = 86400

# 5 VLESS + WS + TLS configs (Railway edge terminates TLS on 443), alpn http/1.1.
# Each one gets its own path, fingerprint and name so they don't look like copies.
# ?ed=2560 = WebSocket early data: the first packet rides on the handshake -> one round trip
# less on every new connection, which is exactly what the "ping" test in V2Box/v2rayNG measures.
INBOUNDS = [
    # tag              proto    port  net   server path                                   fp         name
    ("JX-VLESS-WS-1", "vless", 10001, "ws", "/ws/7a5a21d9-60f9-4542-943e-7838b90169e1",     "chrome",  "🚀 Turbo"),
    ("JX-VLESS-WS-2", "vless", 10002, "ws", "/stream/4868e537-9fd8-46e9-b63a-f36459d18a81", "firefox", "⚡ Flash"),
    ("JX-VLESS-WS-3", "vless", 10003, "ws", "/live/b1dfa4cc-0ed6-4956-b330-8ccb51dc0828",   "safari",  "🔥 Fire"),
    ("JX-VLESS-WS-4", "vless", 10004, "ws", "/gw/3d801b12-a333-452c-b9d5-90ece1a8d68c",    "edge",    "💎 Diamond"),
    ("JX-VLESS-WS-5", "vless", 10005, "ws", "/cdn/cc046fa3-78ec-4619-ac8f-9d6c7a5d0755",    "ios",     "🌙 Night"),
]
EARLY_DATA = "?ed=2560"
TEMPLATES = [  # name, GB, days
    ("10GB - 30 روز", 10, 30), ("30GB - 30 روز", 30, 30), ("50GB - 30 روز", 50, 30),
    ("100GB - 30 روز", 100, 30), ("200GB - 60 روز", 200, 60), ("نامحدود - 30 روز", 0, 30),
]
FIRST_USER = os.getenv("FIRST_USER", "jinx_user1")
FIRST_USER_GB = int(os.getenv("FIRST_USER_GB", "50"))
FIRST_USER_DAYS = int(os.getenv("FIRST_USER_DAYS", "30"))

TOKEN = None

def log(*a): print("[bootstrap]", *a, flush=True)

def req(method, path, body=None, form=False, ok=(200, 201, 204)):
    url = BASE + path
    headers = {"Accept": "application/json"}
    data = None
    if body is not None:
        if form:
            data = urllib.parse.urlencode(body).encode(); headers["Content-Type"] = "application/x-www-form-urlencoded"
        else:
            data = json.dumps(body).encode(); headers["Content-Type"] = "application/json"
    if TOKEN: headers["Authorization"] = f"Bearer {TOKEN}"
    r = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(r, timeout=30) as resp:
            raw = resp.read().decode()
            try: return resp.status, json.loads(raw) if raw.strip() else None
            except ValueError: return resp.status, raw
    except urllib.error.HTTPError as e:
        txt = e.read().decode(errors="ignore")
        try: return e.code, json.loads(txt)
        except Exception: return e.code, txt

def must(method, path, body=None):
    code, res = req(method, path, body)
    if code not in (200, 201, 204):
        raise RuntimeError(f"{method} {path} -> {code}: {res}")
    return res

def as_list(res, key):
    if isinstance(res, list): return res
    if isinstance(res, dict): return res.get(key) or []
    return []

def wait_panel():
    for _ in range(180):
        try:
            code, _ = req("GET", "/api/system")
            if code in (200, 401, 403): return
        except Exception: pass
        time.sleep(2)
    raise RuntimeError("panel did not come up")

TEMP_KEY_PY = """
import asyncio
from app.db.base import GetDB
from app.db.crud.temp_key import create_temp_key
async def main():
    async with GetDB() as db:
        k = await create_temp_key(db)
        print("KEY=" + k.key)
asyncio.run(main())
"""

def temp_key():
    out = subprocess.run([sys.executable, "-c", TEMP_KEY_PY], cwd="/code", capture_output=True, text=True, timeout=60)
    for line in out.stdout.splitlines():
        if line.startswith("KEY="): return line[4:].strip()
    raise RuntimeError(f"temp key failed: {out.stderr[-500:]}")

ADMIN_PW_PY = """
import asyncio, sys
from app.db.base import GetDB
from app.db.crud.admin import get_owner, get_admin
from app.models.admin import _hash_password_sync
async def main():
    mode, user, pw = sys.argv[1], sys.argv[2], sys.argv[3]
    async with GetDB() as db:
        if mode == "owner":
            o = await get_owner(db)
        else:
            o = await get_admin(db, user, load_users=False, load_usage_logs=False)
        if o is None:
            print("MISSING"); return
        o.username = user
        o.hashed_password = _hash_password_sync(pw)
        await db.commit()
        print("OK")
asyncio.run(main())
"""

def write_password(mode, user, pw):
    out = subprocess.run([sys.executable, "-c", ADMIN_PW_PY, mode, user, pw], cwd="/code",
                         capture_output=True, text=True, timeout=90)
    ok = out.stdout.strip().splitlines()[-1:] == ["OK"]
    if not ok: log(f"password write ({mode} {user}) failed:", (out.stdout + out.stderr)[-400:])
    return ok

def strong_tmp():
    import secrets
    return "Jx" + secrets.token_hex(8) + "Aa9!Zz7"

def ensure_owner():
    """Owner is ALWAYS admin/admin. The API refuses weak passwords, so the owner is created with a
    strong throwaway password and then admin/admin is written straight into the DB on every boot."""
    code, res = req("POST", "/api/setup/owner", {"key": temp_key(), "username": "jinxowner", "password": strong_tmp()})
    if code not in (200, 201, 409):
        log(f"owner create failed {code}: {res}")
    if write_password("owner", USER, PASS): log("owner ready:", USER)

def login():
    global TOKEN
    ensure_owner()
    for _ in range(30):
        code, res = req("POST", "/api/admin/token", {"username": USER, "password": PASS}, form=True)
        if code == 200: TOKEN = res["access_token"]; return
        time.sleep(3)
    raise RuntimeError(f"login failed: {code} {res}")

def inbound(tag, proto, port, net, path):
    stream = {"network": net, "security": "none"}
    if net == "ws": stream["wsSettings"] = {"path": path}
    elif net == "httpupgrade": stream["httpupgradeSettings"] = {"path": path}
    elif net == "xhttp": stream["xhttpSettings"] = {"path": path, "mode": "auto"}
    settings = {"clients": []}
    if proto == "vless": settings["decryption"] = "none"
    return {"tag": tag, "listen": "127.0.0.1", "port": port, "protocol": proto,
            "settings": settings, "streamSettings": stream,
            "sniffing": {"enabled": True, "destOverride": ["http", "tls", "quic"], "routeOnly": True}}

CORE_CONFIG = {
    "log": {"loglevel": "warning"},
    "dns": {"servers": ["https+local://1.1.1.1/dns-query", "8.8.8.8", "localhost"]},
    "inbounds": [inbound(*i[:5]) for i in INBOUNDS],
    "outbounds": [
        {"protocol": "freedom", "tag": "DIRECT", "settings": {"domainStrategy": "UseIPv4"}},
        {"protocol": "blackhole", "tag": "BLOCK"},
    ],
    "routing": {"domainStrategy": "IPIfNonMatch", "rules": [
        {"type": "field", "ip": ["geoip:private"], "outboundTag": "BLOCK"},
        {"type": "field", "protocol": ["bittorrent"], "outboundTag": "BLOCK"},
    ]},
    "policy": {"levels": {"0": {"handshake": 4, "connIdle": 300, "uplinkOnly": 1, "downlinkOnly": 1, "bufferSize": 512}}},
}

def ensure_core():
    cores = as_list(must("GET", "/api/cores"), "cores")
    for c in cores:
        if c.get("name") in (CORE_NAME, "jinx-core"):
            body = {"name": CORE_NAME, "config": CORE_CONFIG, "exclude_inbound_tags": [], "fallbacks_inbound_tags": []}
            code, res = req("PUT", f"/api/core/{c['id']}?restart_nodes=true", body)
            if code not in (200, 201):  # node may still be starting: save config without restart
                code, res = req("PUT", f"/api/core/{c['id']}?restart_nodes=false", body)
            log("core updated" if code in (200, 201) else f"core update failed {code}: {res}", c["id"])
            return c["id"]
    c = must("POST", "/api/core", {"name": CORE_NAME, "config": CORE_CONFIG,
                                    "exclude_inbound_tags": [], "fallbacks_inbound_tags": []})
    log("core created", c["id"]); return c["id"]

def ensure_node(core_id):
    api_key = open(f"{DATA}/node_api_key").read().strip()
    cert = open(f"{DATA}/node-certs/cert.pem").read().strip()
    body = {"name": NODE_NAME, "address": "127.0.0.1", "port": 62050, "usage_coefficient": 1,
            "connection_type": "grpc", "server_ca": cert, "keep_alive": 60,
            "core_config_id": core_id, "api_key": api_key}
    for n in as_list(must("GET", "/api/nodes"), "nodes"):
        if n.get("name") in (NODE_NAME, "jinx-local"):
            must("PUT", f"/api/node/{n['id']}", body); log("node updated"); return
    must("POST", "/api/node", body); log("node created")

def ensure_group():
    tags = [i[0] for i in INBOUNDS]
    for g in as_list(must("GET", "/api/groups"), "groups"):
        if g.get("name") == GROUP_NAME:
            must("PUT", f"/api/group/{g['id']}", {"name": GROUP_NAME, "inbound_tags": tags})
            return g["id"]
    g = must("POST", "/api/group", {"name": GROUP_NAME, "inbound_tags": tags})
    log("group created", g["id"]); return g["id"]

def ensure_hosts():
    if not DOMAIN:
        log("WARNING: no public domain yet (Settings > Networking > Generate Domain), hosts skipped"); return
    existing = as_list(must("GET", "/api/hosts"), "hosts")
    wanted = {i[0] for i in INBOUNDS}
    for h in existing:  # clean hosts left from older JinX versions
        if str(h.get("inbound_tag") or "").startswith("JX-") and h.get("inbound_tag") not in wanted:
            req("DELETE", f"/api/host/{h['id']}")
    for idx, (tag, proto, port, net, path, fp, name) in enumerate(INBOUNDS):
        body = {"remark": f"{name} | {TITLE}", "allowinsecure": False, "address": [DOMAIN], "inbound_tag": tag,
                "port": 443, "sni": [DOMAIN], "host": [DOMAIN], "path": path + EARLY_DATA, "security": "tls",
                "alpn": ["http/1.1"], "fingerprint": fp, "priority": idx + 1, "is_disabled": False}
        mine = [h for h in existing if h.get("inbound_tag") == tag]
        if mine:
            must("PUT", f"/api/host/{mine[0]['id']}", {**body, "id": mine[0]["id"]})
            for extra in mine[1:]:  # remove auto-created duplicates
                req("DELETE", f"/api/host/{extra['id']}")
        else:
            must("POST", "/api/host/", body)
    log("5 hosts ready on", DOMAIN)

def ensure_settings():
    if not DOMAIN: return
    code, s = req("GET", "/api/settings")
    if code != 200 or not isinstance(s, dict) or "subscription" not in s:
        log("settings endpoint not as expected, skipped"); return
    sub = s["subscription"]
    sub["url_prefix"] = f"https://{DOMAIN}"
    sub["profile_title"] = TITLE
    sub["update_interval"] = 12
    code, res = req("PUT", "/api/settings", {"subscription": sub})
    log("subscription settings", "ok" if code in (200, 201) else f"skipped ({code})")

RESELLER_ROLE = "نماینده"

def ensure_reseller_role(group_id):
    """Reseller role: manages only its own users, must use the ready-made templates."""
    own = {"scope": 1}
    role = {
        "name": RESELLER_ROLE,
        "permissions": {
            "users": {"create": own, "read": own, "read_simple": own, "update": own, "delete": own,
                      "reset_usage": own, "revoke_sub": own, "activate_next_plan": own},
            "templates": {"read": True, "read_simple": True},
            "groups": {"read_simple": True},
            "system": {"read": True},
            "settings": {"read_general": True},
        },
        "access": {"require_template": True, "allowed_group_ids": [group_id]},
        "disabled_when_limited": True,
    }
    for base in ("/api/admin-role",):
        code, res = req("GET", base + "s")
        if code != 200: continue
        roles = as_list(res, "roles")
        if any(r.get("name") == RESELLER_ROLE for r in roles):
            log("reseller role ready"); return
        code, res = req("POST", base, role)
        if code in (200, 201): log("reseller role created"); return
        log(f"reseller role failed {code}: {res}"); return
    log("reseller role endpoint not found, skipped")

def role_id_by_name(name):
    code, res = req("GET", "/api/admin-roles")
    for r in as_list(res, "roles") if code == 200 else []:
        if r.get("name") == name: return r["id"]
    return None

def ensure_demo_reseller():
    """A ready reseller account (like the reseller panels): 50 GB quota, own users only."""
    rid = role_id_by_name(RESELLER_ROLE)
    if not rid: log("demo reseller skipped (no role)"); return
    code, _ = req("POST", "/api/admin/token", {"username": RESELLER_USER, "password": RESELLER_PASS}, form=True)
    if code == 200: return
    code, res = req("POST", "/api/admin", {"username": RESELLER_USER, "password": strong_tmp(),
                                           "role_id": rid, "data_limit": RESELLER_GB * GB,
                                           "profile_title": TITLE})
    if code in (200, 201):
        write_password("user", RESELLER_USER, RESELLER_PASS); log("demo reseller ready:", RESELLER_USER)
    elif code != 409:
        log(f"demo reseller failed {code}: {res}")

def ensure_templates(group_id):
    have = {t.get("name") for t in as_list(must("GET", "/api/user_templates"), "templates")}
    for name, gb, days in TEMPLATES:
        if name in have: continue
        must("POST", "/api/user_template", {"name": name, "data_limit": gb * GB, "expire_duration": days * DAY,
                                            "group_ids": [group_id], "status": "active",
                                            "data_limit_reset_strategy": "no_reset"})
    log("user templates ready")

def ensure_first_user(group_id):
    code, _ = req("GET", f"/api/user/{FIRST_USER}")
    if code == 200: return
    u = must("POST", "/api/user", {"username": FIRST_USER, "group_ids": [group_id], "status": "active",
                                   "data_limit": FIRST_USER_GB * GB,
                                   "expire": int(time.time()) + FIRST_USER_DAYS * DAY,
                                   "data_limit_reset_strategy": "no_reset", "note": "auto-created"})
    log("first user:", FIRST_USER, "sub:", u.get("subscription_url"))

def attach_orphans(group_id):
    """Users created in the panel without a group get all 5 configs automatically."""
    code, res = req("GET", "/api/users?no_group=true&limit=200")
    if code == 401:
        login(); code, res = req("GET", "/api/users?no_group=true&limit=200")
    if code != 200: return
    for u in as_list(res, "users"):
        if u.get("group_ids"): continue
        c, r = req("PUT", f"/api/user/{u['username']}", {"group_ids": [group_id]})
        log(f"auto-attached 5 configs to {u['username']}" if c == 200 else f"attach {u['username']} failed {c}: {r}")

def watch(group_id):
    log("watcher on: new users get the 5 configs automatically")
    while True:
        try: attach_orphans(group_id)
        except Exception as e: log("watcher error:", e)
        time.sleep(15)

def step(name, fn, *a):
    try: return fn(*a)
    except Exception as e: log(f"{name} failed: {e}")

def main():
    wait_panel(); login()
    core_id = ensure_core()
    time.sleep(2)
    step("node", ensure_node, core_id)
    gid = None
    for _ in range(10):  # inbounds appear after the core is saved
        gid = step("group", ensure_group)
        if gid: break
        time.sleep(3)
    if not gid: raise RuntimeError("group could not be created")
    step("hosts", ensure_hosts)
    step("settings", ensure_settings)
    step("templates", ensure_templates, gid)
    step("reseller role", ensure_reseller_role, gid)
    step("demo reseller", ensure_demo_reseller)
    step("first user", ensure_first_user, gid)
    log("DONE ->", f"https://{DOMAIN}/dashboard/" if DOMAIN else "generate a Railway domain")
    watch(gid)

if __name__ == "__main__":
    try: main()
    except Exception as e: log("FATAL", e); sys.exit(1)
