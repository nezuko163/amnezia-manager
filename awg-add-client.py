#!/usr/bin/env python3
import os, subprocess, sys, re, time, base64, urllib.parse

DIR = "/etc/amnezia/amneziawg"
SERVER_IP = "194.154.30.212"
PORT = "51820"

def run(cmd):
    return subprocess.check_output(cmd, shell=True).decode().strip()

server_public = open(f"{DIR}/server_public.key").read().strip()

display_name = input("Введи название устройства: ").strip()
if not display_name:
    print("❌ Название не может быть пустым")
    sys.exit(1)

safe_name = re.sub(r'[^a-z0-9_-]', '', display_name.lower().replace(' ', '_'))
if not safe_name:
    safe_name = f"device_{int(time.time())}"

name = f"client_{safe_name}"

if os.path.exists(f"{DIR}/{name}_private.key"):
    print("❌ Клиент с таким именем уже существует")
    sys.exit(1)

# Первый свободный IP
ip = None
for i in range(2, 255):
    candidate = f"10.8.0.{i}"
    result = subprocess.run(
        f"grep -r 'AllowedIPs = {candidate}/32' {DIR}/",
        shell=True, capture_output=True
    )
    if result.returncode != 0:
        ip = candidate
        break

if not ip:
    print("❌ Нет свободных IP адресов")
    sys.exit(1)

# Генерация ключей
private_key = run("awg genkey")
public_key = run(f"echo '{private_key}' | awg pubkey")

with open(f"{DIR}/{name}_private.key", 'w') as f: f.write(private_key)
with open(f"{DIR}/{name}_public.key", 'w') as f: f.write(public_key)
with open(f"{DIR}/{name}_displayname.txt", 'w') as f: f.write(display_name)
os.chmod(f"{DIR}/{name}_private.key", 0o600)

client_conf = f"""[Interface]
PrivateKey = {private_key}
Address = {ip}/32
DNS = 1.1.1.1
Jc = 5
Jmin = 20
Jmax = 100
S1 = 30
S2 = 40
H1 = 1234567
H2 = 2345678
H3 = 3456789
H4 = 4567890

[Peer]
PublicKey = {server_public}
Endpoint = {SERVER_IP}:{PORT}
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25
"""

with open(f"{DIR}/{name}.conf", 'w') as f: f.write(client_conf)

peer_block = f"""
[Peer]
# {display_name}
PublicKey = {public_key}
AdvancedSecurity = on
AllowedIPs = {ip}/32
"""
with open(f"{DIR}/awg0.conf", 'a') as f: f.write(peer_block)

os.system(f"awg set awg0 peer {public_key} allowed-ips {ip}/32")

print(f"\n✅ Создан: {display_name} ({ip})")
conf_b64 = base64.b64encode(client_conf.encode()).decode()
encoded_name = urllib.parse.quote(display_name)
print(f"\nvpn://{conf_b64}?name={encoded_name}\n")