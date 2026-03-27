#!/usr/bin/env python3
import os, subprocess, sys, glob

DIR = "/etc/amnezia/amneziawg"

clients = []
for f in glob.glob(f"{DIR}/client_*_displayname.txt"):
    safe = os.path.basename(f).replace("_displayname.txt", "")
    display = open(f).read().strip()
    pub_file = f"{DIR}/{safe}_public.key"
    conf_file = f"{DIR}/{safe}.conf"
    if not os.path.exists(pub_file):
        continue
    pub = open(pub_file).read().strip()
    ip = ""
    if os.path.exists(conf_file):
        for line in open(conf_file):
            if "Address" in line:
                ip = line.split("=")[1].strip().split("/")[0]
    clients.append((display, ip, safe, pub))

if not clients:
    print("❌ Нет клиентов")
    sys.exit(1)

lines = [f"{d} | {ip} | {s}" for d, ip, s, p in clients]
result = subprocess.run(
    ["fzf", "--height=15", "--border", "--no-info",
     "--delimiter=|", "--with-nth=1,2",
     "--pointer=➤", "--header=Выбери клиента для удаления"],
    input="\n".join(lines), capture_output=True, text=True
)

chosen = result.stdout.strip()
if not chosen:
    sys.exit(0)

safe = chosen.split("|")[2].strip()
display = chosen.split("|")[0].strip()
pub = open(f"{DIR}/{safe}_public.key").read().strip()

confirm = input(f"Удалить '{display}'? (y/N): ").strip().lower()
if confirm != 'y':
    print("Отменено")
    sys.exit(0)

os.system(f"awg set awg0 peer {pub} remove")
print("✅ Peer удалён из интерфейса")

with open(f"{DIR}/awg0.conf", 'r') as f:
    content = f.read()

blocks = content.split('\n\n')
filtered = [b for b in blocks if not ('[Peer]' in b and pub in b)]

with open(f"{DIR}/awg0.conf", 'w') as f:
    f.write('\n\n'.join(filtered))
print("✅ Peer удалён из awg0.conf")

for ext in ['_private.key', '_public.key', '_displayname.txt', '.conf']:
    path = f"{DIR}/{safe}{ext}"
    if os.path.exists(path):
        os.remove(path)

print(f"✅ Удалён: {display}")